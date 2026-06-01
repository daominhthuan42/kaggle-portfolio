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
    RANDOM_STATE = 42
    TRAIN_PATH = (ROOT_DIR / "dataset" / "train.csv").as_posix()
    TEST_PATH = (ROOT_DIR / "dataset" / "test.csv").as_posix()
    DATASET_NAME = "HR Attrition"
    TARGET_FEATURE = "Attrition"
    EMPLOYEE_ID = "Employee_ID"
    DEFAULT_ENCODING = ["utf-8", "latin1", "cp1252", "ISO-8859-1"]
    SPLIT = {
        "method": "stratified_shuffle",
        "n_splits": 1,
        "test_size": 0.2
    }
    COLORS = {
    "primary": "#667eea",
    "secondary": "#764ba2",
    "accent": "#f093fb",
    "highlight": "#4facfe",
    "dark": "#2d3561",
    "light": "#e0c3fc"
    }
