# utils.py
import os
import re
import numpy as np
import logging
import pandas as pd
from typing import Optional, Iterable, List
from urllib.parse import urlparse

class Utils:
    """
    Collection of reusable utility functions for data preprocessing
    and dataset management.

    This class groups together helper methods commonly used in data
    analysis pipelines, including column cleaning, memory optimization,
    categorical conversion, dataset memory reporting, Google Drive URL
    normalization, and safe CSV loading.

    These utilities are designed to simplify data ingestion and
    preprocessing workflows while keeping code reusable and consistent
    across projects.

    Notes
    -----
    All methods are implemented as static methods so they can be called
    without creating a class instance.

    Example
    -------
    df = Utils.clean_columns(df)  
    df = Utils.reduce_mem_usage(df.columns, df)  
    memory = Utils.memory_report(df)
    """

    @staticmethod
    def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize column names in a DataFrame.

        This function removes leading/trailing spaces, special characters,
        and replaces whitespace with underscores.

        Parameters
        ----------
        df : pandas.DataFrame
            Input DataFrame whose columns need to be standardized.

        Returns
        -------
        pandas.DataFrame
            DataFrame with cleaned column names.
        """
        df.columns = (
            df.columns
            .str.strip()
            .str.replace(r"[^\w\s]", "", regex=True)  # remove special characters
            .str.replace(r"\s+", "_", regex=True)     # replace spaces with underscore
        )
        return df

    @staticmethod
    def reduce_mem_usage(cols: List[str], df: pd.DataFrame) -> pd.DataFrame:
        """
        Reduce memory usage by downcasting numeric columns.

        This function attempts to convert numeric columns to smaller
        integer or float types where possible.

        Parameters
        ----------
        cols : list of str
            List of columns to optimize.

        df : pandas.DataFrame
            Input DataFrame.

        Returns
        -------
        pandas.DataFrame
            DataFrame with optimized column data types.
        """

        for col in cols:
            col_type = df[col].dtype

            if pd.api.types.is_numeric_dtype(col_type):
                c_min = df[col].min()
                c_max = df[col].max()

                # Downcast integer columns
                if pd.api.types.is_integer_dtype(col_type):
                    if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                        df[col] = df[col].astype(np.int8)
                    elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                        df[col] = df[col].astype(np.int16)
                    elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                        df[col] = df[col].astype(np.int32)
                    else:
                        pass
                # Downcast float columns
                else:
                    if c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                        df[col] = df[col].astype(np.float32)
                    else:
                        pass

            else:
                # Convert non-numeric columns to categorical
                df[col] = df[col].astype("category")

        return df

    @staticmethod
    def convert_cat(features: List[str], df: pd.DataFrame) -> pd.DataFrame:
        """
        Convert specified columns to categorical type.

        Parameters
        ----------
        features : list of str
            Columns to convert.

        df : pandas.DataFrame
            Input DataFrame.

        Returns
        -------
        pandas.DataFrame
            DataFrame with updated categorical columns.
        """

        for feature in features:
            if feature in df.columns:
                df[feature] = df[feature].astype("category")

        return df

    @staticmethod
    def memory_report(df: pd.DataFrame) -> float:
        """
        Calculate total DataFrame memory usage.

        Parameters
        ----------
        df : pandas.DataFrame
            Input DataFrame.

        Returns
        -------
        float
            Total memory usage in MB.
        """
        return round(df.memory_usage(deep=True).sum() / 1024**2, 2)

    @staticmethod
    def _convert_gdrive_url(url: str) -> str:
        """
        Convert a Google Drive sharing link into a direct download URL.

        Parameters
        ----------
        url : str
            Google Drive sharing URL.

        Returns
        -------
        str
            Direct download URL usable by pandas or requests.

        Raises
        ------
        ValueError
            If the URL format is invalid.
        """

        patterns = [
            r"/d/([a-zA-Z0-9_-]+)",
            r"id=([a-zA-Z0-9_-]+)"
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                file_id = match.group(1)
                return f"https://drive.google.com/uc?id={file_id}"

        raise ValueError("Invalid Google Drive URL")

    @staticmethod
    def read_csv_safe(
        path: str,
        logger: logging.Logger,
        encodings: Iterable[str],
        sep: str | None = None
    ) -> Optional[pd.DataFrame]:
        """
        Safely read a CSV file from a local path or URL.

        This function attempts to read the CSV using multiple encodings
        until one succeeds. It supports both local files and HTTP/HTTPS
        URLs and logs progress and errors.

        Parameters
        ----------
        path : str
            Local file path or HTTP/HTTPS URL.

        logger : logging.Logger
            Logger used for reporting progress and errors.

        encodings : Iterable[str]
            Encodings to try when reading the file.

        sep : str or None, optional
            Column delimiter.

        Returns
        -------
        pandas.DataFrame or None
            Loaded DataFrame if successful, otherwise None.
        """

        def _is_url(p: str) -> bool:
            """Check whether a path is an HTTP/HTTPS URL."""
            return urlparse(p).scheme in ("http", "https")

        # Convert Google Drive sharing links automatically
        if "drive.google.com" in path:
            path = Utils._convert_gdrive_url(path)

        # Validate local file existence
        if not _is_url(path) and not os.path.exists(path):
            logger.error(f"File not found: {path}")
            return None

        # Attempt reading file with different encodings
        for enc in encodings:
            try:
                if sep is None:
                    df = pd.read_csv(path, encoding=enc)
                else:
                    df = pd.read_csv(path, encoding=enc, sep=sep)
                logger.info(f"Loaded file with encoding: {enc} | Shape: {df.shape}")
                return df

            except UnicodeDecodeError:
                logger.warning(f"Failed with encoding: {enc}")
                continue

            except pd.errors.EmptyDataError:
                logger.error("CSV file is empty.")
                continue

            except pd.errors.ParserError:
                logger.error("CSV parsing error. Please check file format.")
                continue

            except Exception as e:
                logger.error(f"Unexpected error while reading CSV: {e}")
                continue

        logger.error("Unable to read file with all provided encodings.")
        return None
