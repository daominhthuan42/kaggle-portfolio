import pandas as pd
import logging
from utils.validation_utils import DataValidator

def build_dim_products(
    products: pd.DataFrame,
    reviews: pd.DataFrame,
    returns: pd.DataFrame,
    logger: logging.Logger,
) -> pd.DataFrame:
    """
    Build the enriched product dimension table.

    The function enriches the product dataset with profitability,
    review, and return metrics.

    Parameters
    ----------
    products : pandas.DataFrame
        Product master data.

    reviews : pandas.DataFrame
        Product review data used to calculate average rating
        and review count.

    returns : pandas.DataFrame
        Product return data used to calculate return quantity
        and total refund amount.

    logger : logging.Logger
        Logger used for reporting transformation progress.

    Returns
    -------
    pandas.DataFrame
        Enriched product dimension table.
    """
    logger.info("Building dim_products")

    # Create a copy to preserve the original product dataset
    dim_products = products.copy()

    # Calculate product profitability metrics
    dim_products["gross_margin_pct"] = (
        (dim_products["price"] - dim_products["cogs"]) / dim_products["price"] * 100
    ).round(2)

    dim_products["profit_per_unit"] = (
        dim_products["price"] - dim_products["cogs"]
    ).round(2)

    # Aggregate product review metrics
    avg_rating = reviews.groupby("product_id")["rating"].agg(["mean", "count"]).reset_index()

    avg_rating.columns = ["product_id", "avg_rating", "review_count"]

    # Aggregate product return metrics
    ret_stats = (
        returns.groupby("product_id")
        .agg(
            total_returns=("return_id", "count"),
            total_return_qty=("return_quantity", "sum"),
            total_refund=("refund_amount", "sum"),
        )
        .reset_index()
    )

    # Enrich product dimension with review metrics
    dim_products = dim_products.merge(avg_rating, on="product_id", how="left")

    # Enrich product dimension with return metrics
    dim_products = dim_products.merge(ret_stats, on="product_id", how="left")

    # Checking NULL for dim_products
    logger.info(f"Checking missing values for dim_products...")
    DataValidator.checkNULL(df=dim_products, logger=logger)
    logger.info("Completed checking for NULL values across datasets.")

    # Fill missing values
    dim_products[["review_count", "total_returns", "total_return_qty"]] = (
        dim_products[["review_count", "total_returns", "total_return_qty"]]
        .fillna(0)
        .astype(int)
    )

    dim_products["total_refund"] = dim_products["total_refund"].fillna(0)

    logger.info(
        f"dim_products built successfully: "
        f"{dim_products.shape[0]} rows x {dim_products.shape[1]} cols"
    )

    return dim_products
