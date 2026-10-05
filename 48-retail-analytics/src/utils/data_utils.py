from typing import Iterable, Optional
from urllib.parse import urlparse
import pandas as pd
import numpy as np
import os
from pathlib import Path
import logging
import re

# Project Paths
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

INPUT_DIR = ROOT_DIR / "datasets"
OUTPUT_DIR = ROOT_DIR / "power_bi_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

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

def load(name_data: str, logger: logging.Logger, input_data: str,
         encodings: Iterable[str], sep: str | None = None, 
         parse_dates: list[str] | None = None) -> Optional[pd.DataFrame]:
    """
    Load a CSV file from a local path or URL.

    This function supports local files, HTTP/HTTPS URLs, and Google Drive
    sharing links. It attempts to read the CSV using multiple encodings
    until one succeeds and logs progress and errors.

    Parameters
    ----------
    name_data : str
        Name or path of the input CSV file.

    logger : logging.Logger
        Logger used for reporting progress and errors.

    input_data : str
        Base directory or path containing the input file.

    encodings : Iterable[str]
        Encodings to try when reading the file.

    sep : str or None, optional
        Column delimiter. If None, the default pandas delimiter is used.

    parse_dates : list of str or None, optional
        List of column names to parse as datetime during CSV loading.
        If None, no columns are explicitly parsed as datetime.

    Returns
    -------
    pandas.DataFrame or None
        Loaded DataFrame if successful, otherwise None.
    """
    
    path = os.path.join(input_data, name_data)
    
    def _is_url(p: str) -> bool:
        """Check whether a path is an HTTP/HTTPS URL."""
        return urlparse(p).scheme in ("http", "https")

    # Convert Google Drive sharing links automatically
    if "drive.google.com" in path:
        path = _convert_gdrive_url(path)

    # Validate local file existence
    if not _is_url(path) and not os.path.exists(path):
        logger.error(f"File not found: {path}")
        return None

    # Attempt reading file with different encodings
    for enc in encodings:
        try:
            df = pd.read_csv(path, encoding=enc, sep=sep, parse_dates=parse_dates)
            logger.info(f"Loaded file {name_data} with encoding: {enc} | Shape: {df.shape}")
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

    logger.error(f"Unable to read file {name_data} with all provided encodings.")
    return None

def save_df(df: pd.DataFrame, name_data: str, logger: logging.Logger, output_data: str = OUTPUT_DIR) -> None:
    """
    Save a DataFrame to a CSV file.

    The function creates the output directory if it does not exist,
    saves the DataFrame without the index, and logs the number of
    rows and the output file size.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame to be saved.

    name_data : str
        Name of the output CSV file.

    logger : logging.Logger
        Logger used for reporting progress and errors.

    output_data : str, optional
        Directory where the output file will be saved.
        Defaults to OUTPUT_DIR.

    Returns
    -------
    None
        This function does not return a value.
    """
    try:
        os.makedirs(output_data, exist_ok=True)
        path = os.path.join(output_data, name_data)
        df.to_csv(path, index=False)
        size_mb = os.path.getsize(path) / 1024 / 1024
        logger.info(f"Saved {name_data}: {df.shape[0]:,} rows ({size_mb:.1f} MB)")
    except OSError as e:
        logger.error(f"Failed to save file {name_data}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error while saving {name_data}: {e}")
 