import os
import logging
from typing import List
from pathlib import Path
from io_config import IOConfig
from pyspark.sql import SparkSession

class BronzeIngestion:
        @staticmethod
        def upload_file_to_bronze(spark: SparkSession, logger: logging, list_entity: List, path_data: str | None = None, 
                                  path_cp: str | None = None, name_catalog: str | None = None, file_format: str = "csv", 
                                  header: bool = True) -> None:
            """
            Ingest CSV files into Bronze Delta tables using
            Spark Structured Streaming with incremental processing.

            The schema is inferred once using batch read and reused
            for streaming ingestion to ensure consistency.

            The job runs in micro-batch mode using `trigger(once=True)`
            and stores checkpoints for fault tolerance.

            Parameters
            ----------
            spark : SparkSession
                Active Spark session.

            logger : logging.Logger
                Logger instance.

            list_entity : List[str]
                List of entities to ingest.

            path_data : str
                Root path of source data.

            path_cp : str
                Root path for checkpoints.

            name_catalog : str, optional
                Target catalog name.

            file_format : str, default "csv"
                Input format (only CSV supported).

            header : bool, default True
                Whether CSV contains headers.

            Returns
            -------
            None

            Notes
            -----
            - This method uses Delta Lake as the Bronze storage format.
            - Checkpoints ensure exactly-once processing semantics.
            - `trigger(once=True)` makes this suitable for scheduled jobs
            (e.g., Airflow, Databricks Jobs).
            """

            if file_format.lower() != "csv":
                logger.warning(f"Unsupported file format: {file_format}")
                return

            if name_catalog is None:
                name_catalog = "urban_mobility_data_platform"

            for entity in list_entity:
                logger.info(f"Starting Bronze ingestion for entity: {entity.title()}")
                path_data_entity = Path(os.path.join(path_data, entity)).as_posix()
                path_cp_entity = Path(os.path.join(path_cp, entity)).as_posix()
                try:
                    # Structured Streaming with CSV does NOT support schema inference.
                    # Therefore, we perform a one-time batch read to infer the schema.
                    # This schema will be reused for the streaming read.
                    logger.info(f"Uploading file: {path_data_entity}")
                    bronze_df_batch = (
                            spark.read
                            .option("header", header)
                            .option("inferSchema", True)
                            .csv(path_data_entity)
                    )

                    # Skip ingestion if directory is empty
                    if bronze_df_batch.limit(1).count() == 0:
                        logger.warning(f"{entity.title()}: Source directory is empty. Skipping ingestion.")
                        continue

                    # Extract inferred schema from batch DataFrame
                    schema_entity = bronze_df_batch.schema
                    logger.info(f"{entity.title()}: Schema inferred successfully")

                    # Spark continuously monitors the directory for new files.
                    # When new files arrive, they are processed as micro-batches.
                    # The schema is explicitly provided to ensure consistency.
                    bronze_df_batch = (
                        spark.readStream.format("csv")
                        .option("header", header)
                        .schema(schema_entity)
                        .load(path_data_entity)
                    )

                    # Streaming Write to Bronze Delta Table
                    # format("delta"):
                    #   - Delta Lake is the recommended storage format for Bronze layer
                    #
                    # outputMode("append"):
                    #   - Only new records are appended to the table
                    #
                    # checkpointLocation:
                    #   - Stores streaming state and progress
                    #   - Ensures fault tolerance and prevents duplicate ingestion
                    #
                    # trigger(once=True):
                    #   - Executes the streaming query once and then stops
                    #   - Behaves like a batch job with streaming guarantees
                    #   - Ideal for incremental Bronze ingestion
                    #
                    # toTable():
                    #   - Writes directly to a managed Delta table
                    query = (
                        bronze_df_batch.writeStream
                        .format("delta")
                        .outputMode("append")
                        .option("checkpointLocation", path_cp_entity)
                        .trigger(once=True)
                        .toTable(f"{name_catalog}.bronze.{entity}")
                    )

                    # Wait until the streaming query finishes
                    query.awaitTermination()

                    logger.info(f"Completed Bronze ingestion for entity: {entity.title()}")
                    spark.read.table(f"{IOConfig.BRONZE_COMMON}.{entity}").show(n=10, truncate=False)
                    logger.info("-" * 80)
                except Exception as e:
                    logger.exception(f"Bronze ingestion FAILED for entity: {entity.title()} | Error: {str(e)}")
