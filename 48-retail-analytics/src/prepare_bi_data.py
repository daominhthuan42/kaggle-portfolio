from utils.data_utils import *
from utils.config_loader import load_config
from utils.logger import LoggerConfig
from utils.transformations import (build_dim_products)

# Initialize the project logger.
logger = LoggerConfig.setup_logger()

# Load the global project configuration from the YAML file.
config = load_config(logger=logger)

# Step 1: Load the Raw Dataset
logger.info("*" * 80)
logger.info("Step 1: Load the Raw Dataset")
logger.info("*" * 80)

#orders
df_orders = load(name_data=config["dataset"]["name_data"]["orders"], parse_dates=["order_date"],
                 logger=logger, input_data=INPUT_DIR, sep=",", encodings=config["default_encoding"])
logger.info("\n" + df_orders.head().to_string())

# order_items
df_order_items = load(name_data=config["dataset"]["name_data"]["order_items"],
                      logger=logger, input_data=INPUT_DIR, sep=",", encodings=config["default_encoding"])
# Fix mixed data types in promo_id_2 (string values and NaN)
df_order_items["promo_id_2"] = df_order_items["promo_id_2"].astype("string")
logger.info("\n" + df_order_items.head().to_string())

# payments
df_payments = load(name_data=config["dataset"]["name_data"]["payments"],
                   logger=logger, input_data=INPUT_DIR, sep=",", encodings=config["default_encoding"])
logger.info("\n" + df_payments.head().to_string())

# products
df_products = load(name_data=config["dataset"]["name_data"]["products"],
                   logger=logger, input_data=INPUT_DIR, sep=",", encodings=config["default_encoding"])
logger.info("\n" + df_products.head().to_string())

# customers
df_customers = load(name_data=config["dataset"]["name_data"]["customers"], parse_dates=["signup_date"],
                 logger=logger, input_data=INPUT_DIR, sep=",", encodings=config["default_encoding"])
logger.info("\n" + df_customers.head().to_string())

# geography
df_geography = load(name_data=config["dataset"]["name_data"]["geography"],
                 logger=logger, input_data=INPUT_DIR, sep=",", encodings=config["default_encoding"])
logger.info("\n" + df_geography.head().to_string())

# promotions
df_promotions = load(name_data=config["dataset"]["name_data"]["promotions"], parse_dates=["start_date", "end_date"],
                 logger=logger, input_data=INPUT_DIR, sep=",", encodings=config["default_encoding"])
logger.info("\n" + df_promotions.head().to_string())

# shipments
df_shipments = load(name_data=config["dataset"]["name_data"]["shipments"], parse_dates=["ship_date", "delivery_date"],
                 logger=logger, input_data=INPUT_DIR, sep=",", encodings=config["default_encoding"])
logger.info("\n" + df_shipments.head().to_string())

# returns
df_returns = load(name_data=config["dataset"]["name_data"]["returns"], parse_dates=["return_date"],
                 logger=logger, input_data=INPUT_DIR, sep=",", encodings=config["default_encoding"])
logger.info("\n" + df_returns.head().to_string())

# reviews
df_reviews = load(name_data=config["dataset"]["name_data"]["reviews"], parse_dates=["review_date"],
                 logger=logger, input_data=INPUT_DIR, sep=",", encodings=config["default_encoding"])
logger.info("\n" + df_reviews.head().to_string())

# inventory
df_inventory = load(name_data=config["dataset"]["name_data"]["inventory"], parse_dates=["snapshot_date"],
                 logger=logger, input_data=INPUT_DIR, sep=",", encodings=config["default_encoding"])
logger.info("\n" + df_inventory.head().to_string())

# web_traffic
df_web_traffic = load(name_data=config["dataset"]["name_data"]["web_traffic"], parse_dates=["date"],
                 logger=logger, input_data=INPUT_DIR, sep=",", encodings=config["default_encoding"])
logger.info("\n" + df_web_traffic.head().to_string())

# web_traffic
df_sales = load(name_data=config["dataset"]["name_data"]["sales"], parse_dates=["Date"],
                 logger=logger, input_data=INPUT_DIR, sep=",", encodings=config["default_encoding"])
logger.info("\n" + df_sales.head().to_string())

# Step 2: dim_products
logger.info("*" * 80)
logger.info("Step 2: dim_products (enriched)")
logger.info("*" * 80)
# Add profitability, review, and return metrics to the product dimension
df_products = build_dim_products(products=df_products, reviews=df_reviews, 
                                 returns=df_returns, logger=logger)
# Preview the enriched product dimension
logger.info("\n" + df_products.head().to_string())
save_df(df=df_products, name_data=config["dataset"]["name_data_output"]["dim_products"],
        logger=logger)
