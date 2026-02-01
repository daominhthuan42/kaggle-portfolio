# utils.py
import logging
from typing import List
from pyspark.sql import DataFrame
from pyspark.sql.window import Window
from pyspark.sql.functions import *
from delta.tables import DeltaTable
import traceback

class transformation:

    @staticmethod
    def dedup(df: DataFrame, dedup_cols: List, cdc: str) -> DataFrame:
        """
        Remove duplicate records and keep only the latest record per key.

        This function generates a deduplication key by concatenating
        the specified columns, then uses a window function to rank
        records within each key group based on the CDC column.
        Only the first (latest) record is retained.

        Args:
            df (DataFrame): Input Spark DataFrame.
            dedup_cols (List): List of column names used to identify duplicates.
            cdc (str): Column name used for ordering records
                    (e.g. last_updated_timestamp).

        Returns:
            DataFrame: Deduplicated DataFrame containing only the latest records.
        """

        df = df.withColumn("dedupKey", concat(*dedup_cols))
        df = df.withColumn("dedupCounts", row_number() \
                                .over(Window.partitionBy("dedupKey") \
                                .orderBy(col(cdc).desc()))
                          )
        df = df.filter(df.dedupCounts == 1)
        df = df.drop("dedupKey", "dedupCounts")

        return df

    @staticmethod
    def process_timestamp(df: DataFrame) -> None:
        """
        Add processing timestamp to track when the record is transformed.

        This column is used for auditing, debugging, and data lineage
        to identify when the data was processed in the pipeline.
        """

        return (df.withColumn("process_timestamp", current_timestamp()))

    @staticmethod
    def upsert(df: DataFrame, key_cols: List, table: str, cdc: str, name_catalog: str, 
               name_schema: str, logger: logging) -> None:
        """
        Perform a CDC-based UPSERT (MERGE) operation into a Delta Lake table.

        This function merges records from a source Spark DataFrame into a
        target Delta table using the specified key columns. Existing records
        are updated only when the source CDC column value is newer than or
        equal to the target. New records are inserted when no match is found.

        The merge logic follows these rules:

        - MATCHED rows:
          Update all columns if src.<cdc> >= trg.<cdc>

        - NOT MATCHED rows:
          Insert all columns

        All operations are logged using the provided logger. Any exception
        occurring during execution is logged with full stack trace and
        re-raised to the caller.

        Parameters
        ----------
        df : pyspark.sql.DataFrame
            Source DataFrame containing new or updated records.

        key_cols : List[str]
            List of column names used as merge keys. These columns must
            uniquely identify records in the target table.

        table : str
            Target Delta table name (without catalog and schema).

        cdc : str
            Name of the CDC (Change Data Capture) column used to determine
            record freshness (e.g., updated_at, last_modified_ts).

        name_catalog : str
            Catalog name containing the target Delta table.

        name_schema : str
            Schema (database) name containing the target Delta table.

        logger : logging.Logger
            Configured logger instance used for logging execution status
            and error details.

        Returns
        -------
        None
            This function does not return a value. It raises an exception
            if the merge operation fails.

        Raises
        ------
        Exception
            Propagates any exception raised during Delta merge execution
            after logging the error details.

        Examples
        --------
        >>> upsert(
        ...     df=source_df,
        ...     key_cols=["id", "email"],
        ...     table="customer",
        ...     cdc="updated_at",
        ...     name_catalog="main",
        ...     name_schema="silver",
        ...     logger=logger
        ... )
        """

        try:
            # Build merge condition using key columns
            # Example: src.id = trg.id AND src.email = trg.email
            merge_condition = " AND ".join(
                [f"src.{i} = trg.{i}" for i in key_cols]
            )
            target_table = f"{name_catalog}.{name_schema}.{table}"
            logger.info(f"Starting MERGE into {target_table}")

            # Load target Delta table
            dlt_obj = DeltaTable.forName(df.sparkSession, target_table)

            # Merge source DataFrame into target table
            # - Update all columns when matched
            # - Insert all columns when not matched
            dlt_obj.alias("trg").merge(df.alias("src"), merge_condition) \
                                .whenMatchedUpdateAll(condition = f"src.{cdc} >= trg.{cdc}") \
                                .whenNotMatchedInsertAll() \
                                .execute()
            logger.info(f"MERGE completed successfully: {target_table}")
        except Exception as e:
            logger.exception(f"MERGE FAILED on {table}: {str(e)}")
            raise
