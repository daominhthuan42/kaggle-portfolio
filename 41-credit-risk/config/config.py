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

class CFG:
    RANDOM_STATE = 42

    DATA_PATH = "Credit_Risk_Dataset_Onyx_Data_September_25 - Credit Risk Data.csv"

    DATASET_NAME = "Credit Risk Dataset"

    TARGET_FEATURE = "loan_status"

    DEFAULT_ENCODING = ["utf-8", "latin1", "cp1252", "ISO-8859-1"]

    SPLIT = {
        "method": "stratified_shuffle",
        "n_splits": 1,
        "test_size": 0.2
    }
