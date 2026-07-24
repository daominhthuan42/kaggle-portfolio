# =========================================================
# Global configuration for the Machine Learning project
# ---------------------------------------------------------
# This file stores all high-level configuration used across
# the project such as reproducibility, data source settings,
# and default model parameters.
#
# The configuration is intended to be loaded by the
# config_loader module and used across training, tuning,
# and inference pipelines.
# =========================================================
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

class CFG:
    """ Experiment Configuration """

    # Random seed used for reproducibility
    RANDOM_STATE = 42

    # Dataset location
    DATA_PATH = (ROOT_DIR / "dataset" / "bank_churn_dataset.csv").as_posix()

    # Dataset display name
    DATASET_NAME = "Bank Churn Dataset"

    # Target variable
    TARGET_FEATURE = "exit"

    # Supported file encodings when loading CSV files
    DEFAULT_ENCODING = ["utf-8", "latin1", "cp1252", "ISO-8859-1"]

    # Train/Test Split Configuration
    SPLIT = {
        "method": "stratified_shuffle",
        "n_splits": 1,
        "test_size": 0.2
    }

    CV = {
        "n_splits": 5
    }

    # Default color palette used throughout EDA and reports.
    COLORS = ["#667eea", "#764ba2", "#a855f7", "#f093fb", "#fbc2eb"]

    # Identifier columns that do not provide predictive
    # information for machine learning models.
    COLUMNS_DROP = ["id", "full_name", "address"]

    # Mapbox Configuration
    # ------------------------------------------------------
    # Personal access token for Plotly ScatterMapbox.
    #
    # Required for rendering interactive geographic maps.
    # Token can be generated from:
    # https://account.mapbox.com/access-tokens/
    MAPBOX_TOKEN = "Your Token"

    # Geographic Coordinates
    # ------------------------------------------------------
    # Approximate latitude and longitude of each province.
    #
    # Used for:
    # - ScatterMapbox visualization
    # - Geographic customer analysis
    # - Regional segmentation
    #
    # "Tỉnh khác" (Other Provinces) is represented by the
    # geographic center of Da Nang City.
    PROVINCE_COORDINATES = {
        "TP. Hồ Chí Minh": {
            "lat": 10.8231,
            "lon": 106.6297
        },
        "Hà Nội": {
            "lat": 21.0285,
            "lon": 105.8542
        },
        "Bình Dương": {
            "lat": 11.3254,
            "lon": 106.4770
        },
        "Đồng Nai": {
            "lat": 10.9453,
            "lon": 106.8240
        },
        "Long An": {
            "lat": 10.6956,
            "lon": 106.2431
        },
        "Tiền Giang": {
            "lat": 10.4493,
            "lon": 106.3421
        },
        "Bà Rịa - Vũng Tàu": {
            "lat": 10.5417,
            "lon": 107.2429
        },
        "Cần Thơ": {
            "lat": 10.0452,
            "lon": 105.7469
        },
        "Tỉnh Khác": {
            "lat": 16.0471,
            "lon": 108.2068
        }
    }

