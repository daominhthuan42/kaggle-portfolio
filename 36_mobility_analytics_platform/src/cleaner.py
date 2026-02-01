from pyspark.sql import DataFrame
from pyspark.sql.functions import *
from typing import List

class Cleaner:
    """
    Utility class for cleaning and standardizing text data
    in the Silver layer of the data pipeline.

    This class provides reusable methods to:
    - Normalize whitespace
    - Convert text to lowercase
    - Remove special characters

    It is typically used after Bronze ingestion
    and before deduplication and merging.
    """

    def clean_space(self, df: DataFrame, cols: List):
        """
        Clean extra whitespace in specified string columns.

        This function:
        - Removes leading and trailing spaces
        - Replaces multiple spaces with a single space

        Args:
            df (DataFrame): Input Spark DataFrame.
            cols (List): List of column names to clean.

        Returns:
            DataFrame: DataFrame with cleaned string columns.
        """

        for c in cols:
            df = df.withColumn(c, trim(regexp_replace(col(c), r"\s+", " ")))

        return df
    
    def clean_lowercase(self, df: DataFrame, cols: List):
        """
        Convert text in specified columns to lowercase.

        This function:
        - Standardizes text format
        - Helps improve matching, joining, and searching

        Args:
            df (DataFrame): Input Spark DataFrame.
            cols (List): List of column names to convert.

        Returns:
            DataFrame: DataFrame with lowercase text columns.
        """

        for c in cols:
            df = df.withColumn(c, lower(col(c)))

        return df

    def clean_special_char(self, df: DataFrame, cols: List):
        """
        Remove special characters from specified columns.

        This function:
        - Keeps only letters, numbers, and spaces
        - Removes punctuation and symbols

        Args:
            df (DataFrame): Input Spark DataFrame.
            cols (List): List of column names to clean.

        Returns:
            DataFrame: DataFrame with cleaned text columns.
        """

        for c in cols:
            df = df.withColumn(c, regexp_replace(col(c), r"[^a-zA-Z0-9\s]", ""))

        return df
