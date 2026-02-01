# silver_transformation.py
import logging
from io_config import IOConfig
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from utils.utils import transformation

class GoldTransformation:
    """
    Handle Gold layer transformations for Mobility Analytics Platform.

    This class is responsible for transforming curated Silver data
    into analytics-ready Gold dimension and fact tables.
    """ 

    @staticmethod
    def transformation_customer(spark: SparkSession, logger: logging,
                                name_catalog: str, name_schema: str) -> None:
        """
        Transform Silver customer data into Gold dimension table.

        This method performs:
        - Column selection and standardization
        - Metadata enrichment (ETL timestamp)
        - Incremental upsert based on CDC column
        - Persistence into Gold layer

        Parameters
        ----------
        spark : SparkSession
            Active Spark session.

        logger : logging.Logger
            Application logger for tracking execution.

        name_catalog : str
            Name of the catalog to drop.

        name_schema : str
            Target schema name (e.g., bronze)
        """

        logger.info("*" * 80)
        logger.info("Starting Gold transformation for customers...")
        df_gold_customer = spark.read.table(IOConfig.SILVER_CUSTOMER)

        record_count = df_gold_customer.count()
        logger.info(f"Loaded {record_count} records from Silver customers")

        if record_count == 0:
            logger.warning("No data found in Silver customers. Skipping transformation.")
            return

        # ===============================
        # Feature Select
        # ===============================
        df_gold_customer = df_gold_customer.select(
            "customer_id",
            "full_name",
            "email",
            "city",
            "signup_date",
            "last_updated_timestamp"
        ).withColumn("ingested_at", current_timestamp())

        logger.info("Feature select completed")

        # Initialize transformation utility class for customer
        customer_util = transformation()

        # Persist transformed data to Gold layer
        if not spark.catalog.tableExists(IOConfig.GOLD_CUSTOMER):
            logger.info("Gold customers table not found. Creating new table...")
            df_gold_customer.write.format("delta") \
                                    .mode("append") \
                                    .saveAsTable(IOConfig.GOLD_CUSTOMER)
            logger.info("Gold customers table created successfully")
        else:
            logger.info("Gold customers table exists. Performing upsert...")
            customer_util.upsert(df=df_gold_customer, key_cols=["customer_id"],
                                 table = "dim_customers", cdc="last_updated_timestamp",
                                 name_catalog=name_catalog, name_schema=name_schema, logger=logger)
            logger.info("Upsert completed successfully")

        # Only showing top 10 rows
        logger.debug("Showing top 10 records from Gold customers")
        spark.read.table(IOConfig.GOLD_CUSTOMER).show(n=10, truncate=False)
        logger.info("Gold transformation for customers completed.")
        logger.info("*" * 80)

    @staticmethod
    def transformation_drivers(spark: SparkSession, logger: logging,
                               name_catalog: str, name_schema: str) -> None:
        """
        Transform Silver drivers data into Gold dimension table.

        This method performs:
        - Column selection and standardization
        - Metadata enrichment (ETL timestamp)
        - Incremental upsert based on CDC column
        - Persistence into Gold layer

        Parameters
        ----------
        spark : SparkSession
            Active Spark session.

        logger : logging.Logger
            Application logger for tracking execution.

        name_catalog : str
            Name of the catalog to drop.

        name_schema : str
            Target schema name (e.g., bronze)
        """

        logger.info("Starting Gold transformation for drivers...")
        df_gold_driver = spark.read.table(IOConfig.SILVER_DRIVERS)
        record_count = df_gold_driver.count()
        logger.info(f"Loaded {record_count} records from Silver drivers")

        if record_count == 0:
            logger.warning("No data found in Silver drivers. Skipping transformation.")
            return

        # ===============================
        # Feature Select
        # ===============================
        df_gold_driver = df_gold_driver.select(
            "driver_id",
            "vehicle_id",
            "full_name",
            "driver_rating",
            "city",
            "last_updated_timestamp"
        ).withColumn("ingested_at", current_timestamp())

        logger.info("Feature select completed")

        # Initialize transformation utility class for customer
        driver_util = transformation()

        # Persist transformed data to Gold layer
        if not spark.catalog.tableExists(IOConfig.GOLD_DRIVERS):
            logger.info("Gold drivers table not found. Creating new table...")
            df_gold_driver.write.format("delta") \
                                    .mode("append") \
                                    .saveAsTable(IOConfig.GOLD_DRIVERS)
            logger.info("Gold drivers table created successfully")
        else:
            logger.info("Gold drivers table exists. Performing upsert...")
            driver_util.upsert(df=df_gold_driver, key_cols=["driver_id"],
                               table = "dim_drivers", cdc="last_updated_timestamp",
                               name_catalog=name_catalog, name_schema=name_schema, logger=logger)
            logger.info("Upsert completed successfully")

        # Only showing top 10 rows
        logger.debug("Showing top 10 records from Gold drivers")
        spark.read.table(IOConfig.GOLD_DRIVERS).show(n=10, truncate=False)
        logger.info("Gold transformation for drivers completed.")
        logger.info("*" * 80)

    @staticmethod
    def transformation_locations(spark: SparkSession, logger: logging,
                                 name_catalog: str, name_schema: str) -> None:
        """
        Transform Silver locations data into Gold dimension table.

        This method performs:
        - Column selection and standardization
        - Metadata enrichment (ETL timestamp)
        - Incremental upsert based on CDC column
        - Persistence into Gold layer

        Parameters
        ----------
        spark : SparkSession
            Active Spark session.

        logger : logging.Logger
            Application logger for tracking execution.

        name_catalog : str
            Name of the catalog to drop.

        name_schema : str
            Target schema name (e.g., bronze)
        """

        logger.info("Starting Gold transformation for locations...")
        df_gold_locations = spark.read.table(IOConfig.SILVER_LOCATIONS)

        record_count = df_gold_locations.count()
        logger.info(f"Loaded {record_count} records from Silver locations")

        if record_count == 0:
            logger.warning("No data found in Silver locations. Skipping transformation.")
            return

        # ===============================
        # Feature Select
        # ===============================
        df_gold_locations = df_gold_locations.select(
            "location_id",
            "city",
            "state",
            "country",
            "latitude",
            "longitude",
            "last_updated_timestamp"
        ).withColumn("ingested_at", current_timestamp())

        logger.info("Feature select completed")

        # Initialize transformation utility class for customer
        location_util = transformation()

        # Persist transformed data to Gold layer
        if not spark.catalog.tableExists(IOConfig.GOLD_LOCATIONS):
            logger.info("Gold locations table not found. Creating new table...")
            df_gold_locations.write.format("delta") \
                                    .mode("append") \
                                    .saveAsTable(IOConfig.GOLD_LOCATIONS)
            logger.info("Gold locations table created successfully")
        else:
            logger.info("Gold locations table exists. Performing upsert...")
            location_util.upsert(df=df_gold_locations, key_cols=["location_id"],
                                 table = "dim_locations", cdc="last_updated_timestamp",
                                 name_catalog=name_catalog, name_schema=name_schema, logger=logger)
            logger.info("Upsert completed successfully")

        # Only showing top 10 rows
        logger.debug("Showing top 10 records from Gold locations")
        spark.read.table(IOConfig.GOLD_LOCATIONS).show(n=10, truncate=False)
        logger.info("Gold transformation for locations completed.")
        logger.info("*" * 80)

    @staticmethod
    def transformation_payments(spark: SparkSession, logger: logging,
                                name_catalog: str, name_schema: str) -> None:
        """
        Transform Silver payments data into Gold dimension table.

        This method performs:
        - Column selection and standardization
        - Metadata enrichment (ETL timestamp)
        - Incremental upsert based on CDC column
        - Persistence into Gold layer

        Parameters
        ----------
        spark : SparkSession
            Active Spark session.

        logger : logging.Logger
            Application logger for tracking execution.

        name_catalog : str
            Name of the catalog to drop.

        name_schema : str
            Target schema name (e.g., bronze)
        """

        logger.info("Starting Gold transformation for payments...")
        df_gold_payment = spark.read.table(IOConfig.SILVER_PAYMENTS)

        record_count = df_gold_payment.count()
        logger.info(f"Loaded {record_count} records from Silver payments")

        if record_count == 0:
            logger.warning("No data found in Silver payments. Skipping transformation.")
            return

        # ===============================
        # Feature Select
        # ===============================
        df_gold_payment = df_gold_payment.select(
            "payment_id",
            "trip_id",
            "customer_id",
            "payment_channel",
            "amount",
            "transaction_time",
            "last_updated_timestamp"
        ).withColumn("ingested_at", current_timestamp())

        logger.info("Feature select completed")

        # Initialize transformation utility class for payment
        paymemt_utils = transformation()

        # Persist transformed data to Gold layer
        if not spark.catalog.tableExists(IOConfig.GOLD_PAYMENTS):
            logger.info("Gold payments table not found. Creating new table...")
            df_gold_payment.write.format("delta") \
                                    .mode("append") \
                                    .saveAsTable(IOConfig.GOLD_PAYMENTS)
            logger.info("Gold payments table created successfully")
        else:
            logger.info("Gold payments table exists. Performing upsert...")
            paymemt_utils.upsert(df=df_gold_payment, key_cols=["payment_id"],
                                 table = "dim_payments", cdc="last_updated_timestamp",
                                 name_catalog=name_catalog, name_schema=name_schema, logger=logger)
            logger.info("Upsert completed successfully")

        # Only showing top 10 rows
        logger.debug("Showing top 10 records from Gold payments")
        spark.read.table(IOConfig.GOLD_PAYMENTS).show(n=10, truncate=False)
        logger.info("Gold transformation for payments completed.")
        logger.info("*" * 80)

    @staticmethod
    def transformation_trips(spark: SparkSession, logger: logging,
                             name_catalog: str, name_schema: str) -> None:
        """
        Transform Silver trips data into Gold fact table.

        This method performs:
        - Column selection and standardization
        - Metadata enrichment (ETL timestamp)
        - Incremental upsert based on CDC column
        - Persistence into Gold layer

        Parameters
        ----------
        spark : SparkSession
            Active Spark session.

        logger : logging.Logger
            Application logger for tracking execution.

        name_catalog : str
            Name of the catalog to drop.

        name_schema : str
            Target schema name (e.g., bronze)
        """

        logger.info("Starting Gold transformation for trips...")
        df_gold_trips = spark.read.table(IOConfig.SILVER_TRIPS)

        record_count = df_gold_trips.count()
        logger.info(f"Loaded {record_count} records from Silver trips")

        if record_count == 0:
            logger.warning("No data found in Silver trips. Skipping transformation.")
            return

        # ===============================
        # Feature Select
        # ===============================
        df_gold_trips = df_gold_trips.select(
            "trip_id",
            "driver_id",
            "customer_id",
            "vehicle_id",
            "trip_start_time",
            "trip_end_time",
            "start_location",
            "end_location",
            "distance_km",
            "fare_amount",
            "payment_method",
            "trip_status",
            "last_updated_timestamp"
        ).withColumn("ingested_at", current_timestamp())

        logger.info("Feature select completed")

        # Initialize transformation utility class for payment
        trip_utils = transformation()

        # Persist transformed data to Gold layer
        if not spark.catalog.tableExists(IOConfig.GOLD_TRIPS):
            logger.info("Gold trips table not found. Creating new table...")
            df_gold_trips.write.format("delta") \
                                    .mode("append") \
                                    .saveAsTable(IOConfig.GOLD_TRIPS)
            logger.info("Gold trips table created successfully")
        else:
            logger.info("Gold trips table exists. Performing upsert...")
            trip_utils.upsert(df=df_gold_trips, key_cols=["trip_id"],
                              table = "fact_trips", cdc="last_updated_timestamp",
                              name_catalog=name_catalog, name_schema=name_schema, logger=logger)
            logger.info("Upsert completed successfully")

        # Only showing top 10 rows
        logger.debug("Showing top 10 records from Gold trips")
        spark.read.table(IOConfig.GOLD_TRIPS).show(n=10, truncate=False)
        logger.info("Gold transformation for trips completed.")
        logger.info("*" * 80)

    @staticmethod
    def transformation_vehicles(spark: SparkSession, logger: logging,
                                name_catalog: str, name_schema: str) -> None:
        """
        Transform Silver trips data into Gold dimension table.

        This method performs:
        - Column selection and standardization
        - Metadata enrichment (ETL timestamp)
        - Incremental upsert based on CDC column
        - Persistence into Gold layer

        Parameters
        ----------
        spark : SparkSession
            Active Spark session.

        logger : logging.Logger
            Application logger for tracking execution.

        name_catalog : str
            Name of the catalog to drop.

        name_schema : str
            Target schema name (e.g., bronze)
        """

        logger.info("Starting Silver transformation for vehicles...")
        df_gold_vehicles = spark.read.table(IOConfig.SILVER_VEHICLES)

        record_count = df_gold_vehicles.count()
        logger.info(f"Loaded {record_count} records from Silver vehicles")

        if record_count == 0:
            logger.warning("No data found in Silver vehicles. Skipping transformation.")
            return

        # ===============================
        # Feature Select
        # ===============================
        df_gold_vehicles = df_gold_vehicles.select(
            "vehicle_id",
            "model",
            "make",
            "year",
            "vehicle_type",
            "last_updated_timestamp"
        ).withColumn("ingested_at", current_timestamp())

        logger.info("Feature select completed")

        # Initialize transformation utility class for payment
        vehicles_utils = transformation()

        # Persist transformed data to Gold layer
        if not spark.catalog.tableExists(IOConfig.GOLD_VEHICLES):
            logger.info("Gold vehicles table not found. Creating new table...")
            df_gold_vehicles.write.format("delta") \
                                    .mode("append") \
                                    .saveAsTable(IOConfig.GOLD_VEHICLES)
            logger.info("Gold vehicles table created successfully")
        else:
            logger.info("Gold vehicles table exists. Performing upsert...")
            vehicles_utils.upsert(df=df_gold_vehicles, key_cols=["vehicle_id"],
                                  table = "dim_vehicles", cdc="last_updated_timestamp",
                                  name_catalog=name_catalog, name_schema=name_schema, logger=logger)
            logger.info("Upsert completed successfully")

        # Only showing top 10 rows
        logger.debug("Showing top 10 records from Gold vehicles")
        spark.read.table(IOConfig.GOLD_VEHICLES).show(n=10, truncate=False)
        logger.info("Gold transformation for vehicles completed.")
        logger.info("*" * 80)
