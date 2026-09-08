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
# Visualization
import matplotlib.pyplot as plt
import seaborn as sns 

ROOT_DIR = Path(__file__).resolve().parent.parent

class CFG:
    """ Experiment Configuration """

    # Random seed used for reproducibility
    RANDOM_STATE = 42

    # Dataset location
    DATA_PATH_TRAIN = (ROOT_DIR / "dataset" / "train.csv").as_posix()
    DATA_PATH_TEST = (ROOT_DIR / "dataset" / "test.csv").as_posix()
    DATA_PATH_ORIGINAL = (ROOT_DIR / "dataset" / "EV_Adoption_and_Range_Anxiety_Dataset.csv").as_posix()

    # Dataset display name
    DATASET_NAME = "EV Adoption Prediction Dataset"

    # Target variable
    TARGET_FEATURE = "Will_Buy_EV"

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
    COLUMNS_TRAIN_TEST = ["id"]
    COLUMNS_ORIGINAL = ["Buyer_ID"]

    @staticmethod
    def setup_plot_style():
        """
        Configure a global dark theme for all Matplotlib and Seaborn visualizations.

        Returns
        -------
        None
        """

        plt.style.use("dark_background")

        sns.set_theme(
            style="ticks",
            rc={
                "axes.facecolor": "#181818",
                "figure.facecolor": "#181818",
                "savefig.facecolor": "#181818",
                "axes.edgecolor": "#777777",
                "axes.labelcolor": "white",
                "xtick.color": "white",
                "ytick.color": "white",
                "text.color": "white",
                "grid.color": "#555555",
                "legend.facecolor": "#252525",
                "legend.edgecolor": "#666666",
            },
        )

        plt.rcParams.update({
            # Figure
            "figure.figsize": (12, 6),
            "figure.dpi": 120,
            "savefig.dpi": 150,

            # Font
            "font.size": 11,
            "axes.titlesize": 13,
            "axes.titleweight": "bold",
            "axes.labelsize": 11,
            "figure.titlesize": 20,

            # Grid
            "axes.grid": True,
            "grid.linestyle": "--",
            "grid.alpha": 0.18,

            # Legend
            "legend.frameon": True,
            "legend.fontsize": 9,

            # Lines
            "lines.linewidth": 2,

            # Boxplot
            "boxplot.flierprops.markersize": 2
        })
