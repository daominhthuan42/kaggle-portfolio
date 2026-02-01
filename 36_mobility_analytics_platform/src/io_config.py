# io_config.py
import os
from pathlib import Path

PROJECT_ROOT = os.getcwd()
PROJECT_NAME = "36_mobility_analytics_platform"

class IOConfig:
    # Raw Data Paths
    DATASET_DIR        = Path(os.path.join(PROJECT_ROOT, PROJECT_NAME, "fixtures")).as_posix()
    LOG_DIR            = Path(os.path.join(PROJECT_ROOT, PROJECT_NAME, "logs")).as_posix()
    COMMON             = "/Volumes/urban_mobility_data_platform/source/source_data/"
    BRONZE_COMMON      = "urban_mobility_data_platform.bronze"
    BRONZE_CUSTOMERS   = "urban_mobility_data_platform.bronze.customers"
    BRONZE_TRIPS       = "urban_mobility_data_platform.bronze.trips"
    BRONZE_DRIVERS     = "urban_mobility_data_platform.bronze.drivers"
    BRONZE_PAYMENTS    = "urban_mobility_data_platform.bronze.payments"
    BRONZE_VEHICLES    = "urban_mobility_data_platform.bronze.vehicles"
    BRONZE_LOCATIONS   = "urban_mobility_data_platform.bronze.locations"
    SILVER_CUSTOMER    = "urban_mobility_data_platform.silver.customers"
    SILVER_TRIPS       = "urban_mobility_data_platform.silver.trips"
    SILVER_DRIVERS     = "urban_mobility_data_platform.silver.drivers"
    SILVER_PAYMENTS    = "urban_mobility_data_platform.silver.payments"
    SILVER_VEHICLES    = "urban_mobility_data_platform.silver.vehicles"
    SILVER_LOCATIONS   = "urban_mobility_data_platform.silver.locations"
    GOLD_CUSTOMER      = "urban_mobility_data_platform.gold.dim_customers"
    GOLD_TRIPS         = "urban_mobility_data_platform.gold.fact_trips"
    GOLD_DRIVERS       = "urban_mobility_data_platform.gold.dim_drivers"
    GOLD_PAYMENTS      = "urban_mobility_data_platform.gold.dim_payments"
    GOLD_VEHICLES      = "urban_mobility_data_platform.gold.dim_vehicles"
    GOLD_LOCATIONS     = "urban_mobility_data_platform.gold.dim_locations"
    CP_PATH            = "/Volumes/urban_mobility_data_platform/bronze/checkpoints/"
