# spark_config.py
import os
import logging
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, count
from delta import configure_spark_with_delta_pip

# Try importing Databricks Connect
# If not installed, fallback to local Spark
try:
    from databricks.connect import DatabricksSession
    DATABRICKS_AVAILABLE = True
except ImportError:
    DATABRICKS_AVAILABLE = False

class SparkConfig:
    """
    Utility class for creating and managing SparkSession.

    This class centralizes Spark configuration and initialization
    logic across different execution environments.

    Supported Environments
    ----------------------
    - Databricks Connect (remote cluster)
    - Local Spark with Delta Lake support

    Main Responsibilities
    ---------------------
    - Configure Spark parameters
    - Initialize SparkSession
    - Enable Delta Lake integration
    - Provide profiling utilities
    - Manage Spark lifecycle
    """

    # Core Config
    MASTER   = os.getenv("SPARK_MASTER", "local[*]")

    # Spark Config
    SPARK_CONF = {
        # Performance tuning
        "spark.sql.shuffle.partitions": "200",
        # Enable Delta SQL extensions
        "spark.sql.extensions": "io.delta.sql.DeltaSparkSessionExtension",
        # Use Delta catalog for table management
        "spark.sql.catalog.spark_catalog": "org.apache.spark.sql.delta.catalog.DeltaCatalog"
    }

    @staticmethod
    def create_spark(app_name: str = "MobilityAnalytics", 
                  logger: logging.Logger | None = None) -> SparkSession:
        """
        Create and return SparkSession.

        Parameters
        ----------
        app_name : str
            Spark application name.

        logger : logging.Logger, optional
            External logger instance.
            If provided, all logs will be sent to this logger.

        Returns
        -------
        SparkSession
        """

        # Databricks Connect
        if DATABRICKS_AVAILABLE:
            try:
                spark = DatabricksSession.builder.getOrCreate()
                logger.info("Connected to Databricks.")
                return spark
            except Exception as e:
                logger.error("Failed to connect to Databricks.")
                logger.debug(e)

        # Fallback to Local Spark with Delta Lake
        try:
            builder = (
                SparkSession.builder
                .appName(app_name)
                .master(SparkConfig.MASTER)
            )

            for k, v in SparkConfig.SPARK_CONF.items():
                builder = builder.config(k, v)

            spark = configure_spark_with_delta_pip(builder).getOrCreate()
            logger.info("Running in local Spark mode with Delta Lake.")

            return spark
        except Exception as e:
            logger.error("Failed to initialize Spark session.", exc_info=e)
            raise RuntimeError(f"Spark initialization failed: {e}")

    @staticmethod
    def stop_spark(spark: SparkSession,
                   logger: logging.Logger | None = None) -> None:
        """
        Stop Spark session safely.
        """

        if spark is not None:
            spark.stop()
            logger.info("Spark session stopped.")

    @staticmethod
    def spark_info(df: DataFrame, logger: logging.Logger | None = None, run_count: bool = True):
        """
        Log basic profiling information for a Spark DataFrame.

        This method provides lightweight data diagnostics
        for validation and quality assessment.

        Reported Information
        --------------------
        - Total row count (optional)
        - Total column count
        - DataFrame schema
        - Non-null count per column

        Parameters
        ----------
        df : pyspark.sql.DataFrame
            Input Spark DataFrame to be analyzed.

        logger : logging.Logger
            Logger instance for writing profiling output.

        run_count : bool, optional
            Whether to compute total row count.

            Note: This operation triggers a full scan
            and may be expensive on large datasets.

            Default is True.

        Returns
        -------
        None
        """

        # Log total number of rows (optional due to performance cost)
        if run_count:
            logger.info(f"Rows    : {df.count()}")

        # Log total number of columns
        logger.info(f"Columns : {len(df.columns)}")

        # Print DataFrame schema
        df.printSchema()

        # Show non-null count for each column
        df.select([
            count(col(c)).alias(c) for c in df.columns
        ]).show(vertical=True)
