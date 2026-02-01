# silver_transformation.py
import logging
from cleaner import Cleaner
from io_config import IOConfig
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from utils.utils import transformation

class SilverTransformation:
    """
    Handle Silver layer transformations for Mobility Analytics Platform.

    This class is responsible for cleansing, standardizing, and enriching
    Bronze-layer data before persisting it to the Silver layer.
    """

    @staticmethod
    def transformation_customer(spark: SparkSession, logger: logging, 
                                name_catalog: str, name_schema: str) -> None:
        """
        Transform Bronze customer data into Silver format.

        This method performs the following transformations:
        - Extract email domain
        - Standardize phone numbers
        - Create full name
        - Remove duplicate records using CDC logic
        - Add processing timestamp
        - Clean extra whitespace
        - Persist transformed data to Silver layer

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
        logger.info("Starting Silver transformation for customers...")
        df_silver_customer = spark.read.table(IOConfig.BRONZE_CUSTOMERS)

        record_count = df_silver_customer.count()
        logger.info(f"Loaded {record_count} records from Bronze customers")

        if record_count == 0:
            logger.warning("No data found in Bronze customers. Skipping transformation.")
            return

        # ===============================
        # Feature engineering
        # ===============================
        # Extract email domain (e.g., john@gmail.com → gmail.com)
        df_silver_customer = df_silver_customer.withColumn("domain", split(col("email"), "@")[1])

        # Standardize phone numbers
        # - regexp_replace: replace text using regular expression
        # - r"[^0-9]": match all characters that are NOT digits (0–9)
        # - "" : replace them with empty string (remove them)
        # Example:
        # "+84-912 345 678" -> "84912345678"
        df_silver_customer = df_silver_customer.withColumn("phone_number", regexp_replace(col("phone_number"), r"[^0-9]", ""))

        # Create full name and drop original name columns
        df_silver_customer = df_silver_customer.withColumn("full_name", concat_ws(" ", col("first_name"), col("last_name"))) \
                                               .drop("first_name", "last_name")

        logger.info("Feature engineering completed")

        # Initialize transformation utility class for customer
        customer_util = transformation()

        # Remove duplicate customer records based on "customer_id" and "last_updated_timestamp"
        # - dedup_cols = ["customer_id"] → Use customer_id as unique identifier
        # - cdc = "last_updated_timestamp" → Use latest update time to keep newest record
        # - For each customer_id, only the most recently updated row is kept
        df_silver_customer = customer_util.dedup(df=df_silver_customer, dedup_cols=["customer_id"], cdc="last_updated_timestamp") \
                                          .sort(col("customer_id"))
        logger.info("Deduplication completed")

        # Add processing timestamp to track 
        df_silver_customer = customer_util.process_timestamp(df_silver_customer)
        logger.info("Processing timestamp added")

        # Clean extra whitespace in specified string columns.
        df_silver_customer = Cleaner().clean_space(df=df_silver_customer, 
                                                   cols=["email", "city", "phone_number", "domain", "full_name"])
        logger.info("Whitespace cleaning completed")

        # Persist transformed data to Silver layer
        if not spark.catalog.tableExists(IOConfig.SILVER_CUSTOMER):
            logger.info("Silver customers table not found. Creating new table...")
            df_silver_customer.write.format("delta") \
                                    .mode("append") \
                                    .saveAsTable(IOConfig.SILVER_CUSTOMER)
            logger.info("Silver customers table created successfully")
        else:
            logger.info("Silver customers table exists. Performing upsert...")
            customer_util.upsert(df=df_silver_customer, key_cols=["customer_id"],
                                 table="customers", cdc="last_updated_timestamp",
                                 name_catalog=name_catalog, name_schema=name_schema, logger=logger)
            logger.info("Upsert completed successfully")

        # Only showing top 10 rows
        logger.debug("Showing top 10 records from Silver customers")
        spark.read.table(IOConfig.SILVER_CUSTOMER).show(n=10, truncate=False)
        logger.info("Silver transformation for customers completed.")
        logger.info("*" * 80)

    @staticmethod
    def transformation_drivers(spark: SparkSession, logger: logging,
                               name_catalog: str, name_schema: str) -> None:
        """
        Transform Bronze drivers data into Silver format.

        This method performs the following transformations:
         - Standardize phone numbers
        - Create full name
        - Remove duplicate records using CDC logic
        - Add processing timestamp
        - Clean extra whitespace
        - Persist transformed data to Silver layer

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

        logger.info("Starting Silver transformation for drivers...")
        df_silver_driver = spark.read.table(IOConfig.BRONZE_DRIVERS)
        record_count = df_silver_driver.count()
        logger.info(f"Loaded {record_count} records from Bronze drivers")

        if record_count == 0:
            logger.warning("No data found in Bronze drivers. Skipping transformation.")
            return

        # ===============================
        # Feature engineering
        # ===============================
        # Standardize phone numbers
        df_silver_driver = df_silver_driver.withColumn("phone_number", regexp_replace(col("phone_number"), r"[^0-9]", ""))

        # Create full name by concatenating first and last name
        df_silver_driver = df_silver_driver.withColumn("full_name", concat_ws(" ", col("first_name"), col("last_name")))
        # Remove original name columns after creating full_name to avoid redundancy
        df_silver_driver = df_silver_driver.drop("first_name", "last_name")

        logger.info("Feature engineering completed")

        # Initialize transformation utility class for customer
        driver_util = transformation()

        # Remove duplicate customer records based on "driver_id" and "last_updated_timestamp"
        df_silver_driver = driver_util.dedup(df=df_silver_driver, dedup_cols=["driver_id"], cdc="last_updated_timestamp") \
                                        .sort(col("driver_id"))
        logger.info("Deduplication completed")

        # Add processing timestamp to track 
        df_silver_driver = driver_util.process_timestamp(df_silver_driver)
        logger.info("Processing timestamp added")

        # Clean extra whitespace in specified string columns.
        df_silver_driver = Cleaner().clean_space(df=df_silver_driver, cols=["full_name", "city", "phone_number"])
        logger.info("Whitespace cleaning completed")

        # Persist transformed data to Silver layer
        if not spark.catalog.tableExists(IOConfig.SILVER_DRIVERS):
            logger.info("Silver drivers table not found. Creating new table...")
            df_silver_driver.write.format("delta") \
                                    .mode("append") \
                                    .saveAsTable(IOConfig.SILVER_DRIVERS)
            logger.info("Silver drivers table created successfully")
        else:
            logger.info("Silver drivers table exists. Performing upsert...")
            driver_util.upsert(df=df_silver_driver, key_cols=["driver_id"],
                               table = "drivers", cdc="last_updated_timestamp",
                               name_catalog=name_catalog, name_schema=name_schema, logger=logger)
            logger.info("Upsert completed successfully")

        # Only showing top 10 rows
        logger.debug("Showing top 10 records from Silver drivers")
        spark.read.table(IOConfig.SILVER_DRIVERS).show(n=10, truncate=False)
        logger.info("Silver transformation for drivers completed.")
        logger.info("*" * 80)

    @staticmethod
    def transformation_locations(spark: SparkSession, logger: logging,
                                 name_catalog: str, name_schema: str) -> None:
        """
        Transform Bronze locations data into Silver format.

        This method performs the following transformations:
        - Remove duplicate records using CDC logic
        - Add processing timestamp
        - Clean extra whitespace
        - Persist transformed data to Silver layer

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

        logger.info("Starting Silver transformation for locations...")
        df_silver_locations = spark.read.table(IOConfig.BRONZE_LOCATIONS)

        record_count = df_silver_locations.count()
        logger.info(f"Loaded {record_count} records from Bronze locations")

        if record_count == 0:
            logger.warning("No data found in Bronze locations. Skipping transformation.")
            return

        # Initialize transformation utility class for customer
        location_util = transformation()

        # Remove duplicate customer records based on "location_id" and "last_updated_timestamp"
        df_silver_locations = location_util.dedup(df=df_silver_locations, dedup_cols=["location_id"], cdc="last_updated_timestamp") \
                                        .sort(col("location_id"))
        logger.info("Deduplication completed")

        # Add processing timestamp to track 
        df_silver_locations = location_util.process_timestamp(df=df_silver_locations)
        logger.info("Processing timestamp added")

        # Clean extra whitespace in specified string columns.
        df_silver_locations = Cleaner().clean_space(df=df_silver_locations, cols=["city", "state", "country"])
        logger.info("Whitespace cleaning completed")

        # Persist transformed data to Silver layer
        if not spark.catalog.tableExists(IOConfig.SILVER_LOCATIONS):
            logger.info("Silver locations table not found. Creating new table...")
            df_silver_locations.write.format("delta") \
                                    .mode("append") \
                                    .saveAsTable(IOConfig.SILVER_LOCATIONS)
            logger.info("Silver locations table created successfully")
        else:
            logger.info("Silver locations table exists. Performing upsert...")
            location_util.upsert(df=df_silver_locations, key_cols=["location_id"],
                                 table = "locations", cdc="last_updated_timestamp",
                                 name_catalog=name_catalog, name_schema=name_schema, logger=logger)
            logger.info("Upsert completed successfully")

        # Only showing top 10 rows
        logger.debug("Showing top 10 records from Silver locations")
        spark.read.table(IOConfig.SILVER_LOCATIONS).show(n=10, truncate=False)
        logger.info("Silver transformation for locations completed.")
        logger.info("*" * 80)

    @staticmethod
    def transformation_payments(spark: SparkSession, logger: logging,
                                name_catalog: str, name_schema: str) -> None:
        """
        Transform Bronze payments data into Silver format.

        This method performs the following transformations:
        - Create a new column "payment_channel" to classify payment type based on method and status
        - Remove duplicate records using CDC logic
        - Add processing timestamp
        - Clean extra whitespace
        - Persist transformed data to Silver layer

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

        logger.info("Starting Silver transformation for payments...")
        df_silver_payment = spark.read.table(IOConfig.BRONZE_PAYMENTS)

        record_count = df_silver_payment.count()
        logger.info(f"Loaded {record_count} records from Bronze payments")

        if record_count == 0:
            logger.warning("No data found in Bronze payments. Skipping transformation.")
            return

        # ===============================
        # Feature engineering
        # ===============================
        # Create a new column "payment_channel" to classify payment type based on method and status
        df_silver_payment = df_silver_payment.withColumn("payment_channel", 
                                                        when((col("payment_method").isin("Card", "Wallet")) & (col("payment_status") == "Success"), "online-success") \
                                                        .when((col("payment_method").isin("Card", "Wallet")) & (col("payment_status") == "Failed"), "online-failed") \
                                                        .when((col("payment_method").isin("Card", "Wallet")) & (col("payment_status") == "Pending"), "online-pending") \
                                                        .otherwise("offline")
                                                    )
        logger.info("Feature engineering completed")

        # Initialize transformation utility class for payment
        paymemt_utils = transformation()

        # Remove duplicate customer records based on "payment_id" and "last_updated_timestamp"
        df_silver_payment = paymemt_utils.dedup(df=df_silver_payment, dedup_cols=["payment_id"], cdc="last_updated_timestamp") \
                                        .sort(col("payment_id"))
        logger.info("Deduplication completed")

        # Add processing timestamp to track 
        df_silver_payment = paymemt_utils.process_timestamp(df=df_silver_payment)
        logger.info("Processing timestamp added")

        # Clean extra whitespace in specified string columns.
        df_silver_payment = Cleaner().clean_space(df=df_silver_payment, cols=["payment_method", "payment_status", "payment_channel"])
        logger.info("Whitespace cleaning completed")

        # Persist transformed data to Silver layer
        if not spark.catalog.tableExists(IOConfig.SILVER_PAYMENTS):
            logger.info("Silver payments table not found. Creating new table...")
            df_silver_payment.write.format("delta") \
                                    .mode("append") \
                                    .saveAsTable(IOConfig.SILVER_PAYMENTS)
            logger.info("Silver payments table created successfully")
        else:
            logger.info("Silver payments table exists. Performing upsert...")
            paymemt_utils.upsert(df=df_silver_payment, key_cols=["payment_id"],
                                 table = "payments", cdc="last_updated_timestamp",
                                 name_catalog=name_catalog, name_schema=name_schema, logger=logger)
            logger.info("Upsert completed successfully")

        # Only showing top 10 rows
        logger.debug("Showing top 10 records from Silver payments")
        spark.read.table(IOConfig.SILVER_PAYMENTS).show(n=10, truncate=False)
        logger.info("Silver transformation for payments completed.")
        logger.info("*" * 80)

    @staticmethod
    def transformation_trips(spark: SparkSession, logger: logging,
                             name_catalog: str, name_schema: str) -> None:
        """
        Transform Bronze trips data into Silver format.

        This method performs the following transformations:
        - Remove duplicate records using CDC logic
        - Add processing timestamp
        - Clean extra whitespace
        - Persist transformed data to Silver layer

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

        logger.info("Starting Silver transformation for trips...")
        df_silver_trips = spark.read.table(IOConfig.BRONZE_TRIPS)

        record_count = df_silver_trips.count()
        logger.info(f"Loaded {record_count} records from Bronze trips")

        if record_count == 0:
            logger.warning("No data found in Bronze trips. Skipping transformation.")
            return

        # Initialize transformation utility class for payment
        trip_utils = transformation()

        # Remove duplicate customer records based on "trip_id" and "last_updated_timestamp"
        df_silver_trips = trip_utils.dedup(df=df_silver_trips, dedup_cols=["trip_id"], cdc="last_updated_timestamp") \
                                        .sort(col("trip_id"))
        logger.info("Deduplication completed")

        # Add processing timestamp to track 
        df_silver_trips = trip_utils.process_timestamp(df=df_silver_trips)
        logger.info("Processing timestamp added")

        # Clean extra whitespace in specified string columns.
        df_silver_trips = Cleaner().clean_space(df=df_silver_trips,
                                                cols=["start_location", "end_location", "payment_method", "trip_status"])
        logger.info("Whitespace cleaning completed")

        # Persist transformed data to Silver layer
        if not spark.catalog.tableExists(IOConfig.SILVER_TRIPS):
            logger.info("Silver trips table not found. Creating new table...")
            df_silver_trips.write.format("delta") \
                                    .mode("append") \
                                    .saveAsTable(IOConfig.SILVER_TRIPS)
            logger.info("Silver trips table created successfully")
        else:
            logger.info("Silver trips table exists. Performing upsert...")
            trip_utils.upsert(df=df_silver_trips, key_cols=["trip_id"],
                                 table = "trips", cdc="last_updated_timestamp",
                                 name_catalog=name_catalog, name_schema=name_schema, logger=logger)
            logger.info("Upsert completed successfully")

        # Only showing top 10 rows
        logger.debug("Showing top 10 records from Silver trips")
        spark.read.table(IOConfig.SILVER_TRIPS).show(n=10, truncate=False)
        logger.info("Silver transformation for trips completed.")
        logger.info("*" * 80)

    @staticmethod
    def transformation_vehicles(spark: SparkSession, logger: logging,
                                name_catalog: str, name_schema: str) -> None:
        """
        Transform Bronze vehicles data into Silver format.

        This method performs the following transformations:
        - Remove duplicate records using CDC logic
        - Add processing timestamp
        - Clean extra whitespace
        - Persist transformed data to Silver layer

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
        df_silver_vehicles = spark.read.table(IOConfig.BRONZE_VEHICLES)

        record_count = df_silver_vehicles.count()
        logger.info(f"Loaded {record_count} records from Bronze vehicles")

        if record_count == 0:
            logger.warning("No data found in Bronze vehicles. Skipping transformation.")
            return

        # Initialize transformation utility class for payment
        vehicles_utils = transformation()

        # Remove duplicate customer records based on "vehicle_id" and "last_updated_timestamp"
        df_silver_vehicles = vehicles_utils.dedup(df=df_silver_vehicles, dedup_cols=["vehicle_id"], cdc="last_updated_timestamp") \
                                           .sort(col("vehicle_id"))
        logger.info("Deduplication completed")

        # Add processing timestamp to track 
        df_silver_vehicles = vehicles_utils.process_timestamp(df=df_silver_vehicles)
        logger.info("Processing timestamp added")

        # Clean extra whitespace in specified string columns.
        df_silver_vehicles = Cleaner().clean_space(df=df_silver_vehicles,
                                                   cols=["license_plate", "model", "make", "vehicle_type"])
        logger.info("Whitespace cleaning completed")

        # Persist transformed data to Silver layer
        if not spark.catalog.tableExists(IOConfig.SILVER_VEHICLES):
            logger.info("Silver vehicles table not found. Creating new table...")
            df_silver_vehicles.write.format("delta") \
                                    .mode("append") \
                                    .saveAsTable(IOConfig.SILVER_VEHICLES)
            logger.info("Silver vehicles table created successfully")
        else:
            logger.info("Silver vehicles table exists. Performing upsert...")
            vehicles_utils.upsert(df=df_silver_vehicles, key_cols=["vehicle_id"],
                                  table = "vehicles", cdc="last_updated_timestamp",
                                  name_catalog=name_catalog, name_schema=name_schema, logger=logger)
            logger.info("Upsert completed successfully")

        # Only showing top 10 rows
        logger.debug("Showing top 10 records from Silver vehicles")
        spark.read.table(IOConfig.SILVER_VEHICLES).show(n=10, truncate=False)
        logger.info("Silver transformation for vehicles completed.")
        logger.info("*" * 80)
