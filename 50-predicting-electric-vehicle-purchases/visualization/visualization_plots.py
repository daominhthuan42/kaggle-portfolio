import logging
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from utils.colors_utils import ColorUtils
from typing import List
from scipy.stats import pearsonr, pointbiserialr
# Visualization libraries
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import init_notebook_mode
init_notebook_mode(connected=True)

def plot_numerical_features_v2(df: pd.DataFrame,
                               numerical_features: List[str]) -> None:
    """ Plot distribution of numerical features using Histogram and Boxplot. """

    plt.style.use("default")
    fig, ax = plt.subplots(len(numerical_features), 2, figsize=(14, len(numerical_features)*4.2), facecolor="white")
    ax = np.atleast_2d(ax)
    for i, feature in enumerate(numerical_features):
        sns.histplot(data=df, x=feature, bins=25, kde=True, color="#3B82F6", 
                     edgecolor="white", linewidth=0.6, alpha=0.85, ax=ax[i,0])
        median = df[feature].median()
        ax[i,0].axvline(median, color="#DC2626", linestyle="--", linewidth=2)
        ax[i,0].text(0.98, 0.92, f"Median: {median:,.2f}", transform=ax[i,0].transAxes, ha="right", fontsize=9,
                    bbox=dict(
                        boxstyle="round",
                        fc="white",
                        ec="#DC2626",
                        alpha=.9
                    )
                )

        ax[i,0].set_title(feature.replace("_"," ").title(), fontsize=12, fontweight="bold", pad=15)
        # ax[i,0].grid(axis="y", linestyle="--", alpha=.25)
        ax[i,0].set_facecolor("#FCFCFC")
        ax[i,0].set_xlabel("")
        ax[i,0].set_ylabel("")
        sns.despine(ax=ax[i,0])

        # ================= Boxplot =================
        sns.boxplot(data=df,  x=feature,  orient="h",  color="#22C55E", width=.45, linewidth=1, fliersize=2, ax=ax[i,1])
        ax[i,1].set_title("Distribution Summary", fontsize=12, fontweight="bold", pad=15)
        # ax[i,1].grid(axis="x", linestyle="--", alpha=.25)
        ax[i,1].set_facecolor("#FCFCFC")
        ax[i,1].set_xlabel("")
        ax[i,1].set_ylabel("")
        sns.despine(ax=ax[i,1])

    plt.tight_layout()
    plt.show()

def plot_numerical_features_v3(
    df_train: pd.DataFrame, df_test: pd.DataFrame, df_original: pd.DataFrame, num_features: List[str]
) -> None:
    """
    Plot numerical feature distributions.

    Left:
        - Histogram (Train vs Test)
        - Median line for each dataset

    Right:
        - Horizontal boxplot comparison
    """
    
    # Generate color palette for 3 datasets
    colors = ColorUtils.color(n_colors=3)
    train_color, test_color, original_color = colors
    n_features = len(num_features)

    # Create subplot grid: each feature has 1 row, 2 columns (hist + boxplot)
    fig, axes = plt.subplots(nrows=n_features, ncols=2, figsize=(13, 4 * n_features), 
                             facecolor="#181818", gridspec_kw={"width_ratios": [1.15, 1]})
    axes = np.array(axes).reshape(n_features, 2)

    fig.suptitle("Numerical Feature Distributions", fontsize=18, fontweight="bold", y=0.995)
    
    # Plot Each Feature    
    for i, feature in enumerate(num_features):
        train_data = df_train[feature].dropna()
        original_data = df_original[feature].dropna()
        test_data = df_test[feature].dropna()

        train_median = train_data.median()
        original_median = original_data.median()
        test_median = test_data.median()

        # kdeplot
        sns.kdeplot(train_data, color=train_color, label="Train", ax=axes[i, 0], fill=True)
        sns.kdeplot(original_data, color=original_color, label="Original", ax=axes[i, 0], fill=True)
        sns.kdeplot(test_data,  color=test_color, label="Test",  ax=axes[i, 0], fill=True)

        # Median Lines
        axes[i, 0].axvline(train_median, color=train_color, linestyle="--", linewidth=2.5, label=f"Train Median ({train_median:.2f})")
        axes[i, 0].axvline(original_median, color=original_color, linestyle="--", linewidth=2.5, label=f"Original Median ({original_median:.2f})")
        axes[i, 0].axvline(test_median, color=test_color, linestyle="--", linewidth=2.5, label=f"Test Median ({test_median:.2f})")
        axes[i, 0].set_title(f"Distribution of {feature}", fontsize=12, fontweight="bold", pad=15)
        axes[i, 0].set_xlabel("")
        axes[i, 0].set_ylabel("Density")
        axes[i, 0].legend(fontsize=9)
        axes[i, 0].grid(False)
        sns.despine(ax=axes[i, 0])

        # Legend
        legend = axes[i, 0].legend(
            [
                f"Train Median ({train_median:.2f})",
                f"Original Median ({original_median:.2f})",
                f"Test Median ({test_median:.2f})",
            ],
            loc="best",
            fontsize=8,
            frameon=True,
            facecolor="#252525",
            edgecolor="#555555",
        )

        for text in legend.get_texts():
            text.set_color("white")

        # Prepare Data for Boxplot
        df_plot = pd.concat([
                pd.DataFrame({"Dataset": "Train", feature: train_data}),
                pd.DataFrame({"Dataset": "Original", feature: original_data}),
                pd.DataFrame({"Dataset": "Test", feature: test_data}),
            ],
            ignore_index=True
        )

        # Boxplot
        sns.boxplot(data=df_plot, x=feature, y="Dataset", orient="h", palette=colors, width=0.55, fliersize=2, ax=axes[i, 1])
        axes[i, 1].set_title(f"Boxplot of {feature}", fontsize=12, fontweight="bold", pad=15)
        axes[i, 1].set_xlabel("")
        axes[i, 1].set_ylabel("")
        # axes[i, 1].grid(axis="x", linestyle="--", alpha=0.25)
        axes[i, 1].grid(False)
        sns.despine(ax=axes[i, 1])

    plt.tight_layout()
    plt.show()

def plot_numerical_features(df_train: pd.DataFrame, df_test: pd.DataFrame, 
                            num_features: List[str], n_colors: int) -> None:
    """
    Plot histogram and boxplot for each numerical feature.

    - Histogram shows distribution and skewness.
    - Boxplot highlights median and potential outliers.
    """

    # Generate color palette for 3 datasets
    colors = ColorUtils.color(n_colors=n_colors)
    n = len(num_features)

    # Create subplot grid: each feature has 1 row, 2 columns (hist + boxplot)
    fig, ax = plt.subplots(n, 2, figsize=(12, n * 4))
    ax = np.array(ax).reshape(n, 2)

    for i, feature in enumerate(num_features):
        # Histogram + KDE Plot
        sns.kdeplot(data=df_train[feature], color=colors[0], ax=ax[i, 0], label="Train data", fill=True)
        sns.kdeplot(data=df_test[feature], color=colors[1], ax=ax[i, 0], label="Test data", fill=True)

        # Format histogram
        ax[i, 0].set_title(f"Histogram of {feature}", pad=15, weight="bold", fontsize=12)
        ax[i, 0].legend()
        ax[i, 0].set_xlabel("")
        ax[i, 0].set_ylabel("")
        sns.despine(left=False, bottom=False, ax=ax[i, 0])

        df_plot = pd.concat([
            pd.DataFrame({"Dataset": "Train data", feature: df_train[feature]}),
            pd.DataFrame({"Dataset": "Test data", feature: df_test[feature]})
        ]).reset_index(drop=True)

        # Prepare Data for Boxplot
        sns.boxplot(data=df_plot, x=feature, y="Dataset", palette=colors, orient="h", ax=ax[i, 1])
        ax[i, 1].set_title(f"Horizontal Box plot of {feature}", pad=15, weight="bold", fontsize=12)
        ax[i, 1].set_xlabel("")
        ax[i, 1].set_ylabel("")
        sns.despine(left=False, bottom=False, ax=ax[i, 1])

    # Adjust layout to prevent overlap
    plt.tight_layout()
    plt.show()

def _compute_corr_pval(df):
    """
    Compute correlation and p-value matrices for numeric features.

    This function calculates pairwise relationships between numeric columns:
    - Uses Pearson correlation for continuous-continuous pairs
    - Uses point-biserial correlation when one variable is binary (0/1)

    It also computes corresponding p-values to assess statistical significance.
    """

    # Select only numeric columns
    cols = df.select_dtypes(include=np.number).columns
    cols = [col for col in cols if df[col].dtype != "category"]

    # Initialize empty matrices
    corr_matrix = pd.DataFrame(index=cols, columns=cols, dtype=float)
    pval_matrix = pd.DataFrame(index=cols, columns=cols, dtype=float)

    # Iterate over all feature pairs
    for i in cols:
        for j in cols:
            x = df[i]
            y = df[j]

            # Remove NaN values pairwise to ensure valid computation
            valid = x.notna() & y.notna()
            x = x[valid]
            y = y[valid]

            # Check if variables are binary (0/1)
            is_i_binary = set(x.unique()).issubset({0, 1})
            is_j_binary = set(y.unique()).issubset({0, 1})

            try:
                if i == j:
                    # Diagonal: perfect correlation
                    corr_matrix.loc[i, j] = 1.0
                    pval_matrix.loc[i, j] = 0.0

                elif is_i_binary and not is_j_binary:
                    # Binary vs continuous → point-biserial
                    r, p = pointbiserialr(x, y)

                elif is_j_binary and not is_i_binary:
                    # Continuous vs binary → point-biserial (swap order)
                    r, p = pointbiserialr(y, x)

                else:
                    # Continuous vs continuous → Pearson
                    r, p = pearsonr(x, y)

                # Store results
                corr_matrix.loc[i, j] = r
                pval_matrix.loc[i, j] = p

            except:
                # Handle edge cases (constant columns, etc.)
                corr_matrix.loc[i, j] = np.nan
                pval_matrix.loc[i, j] = np.nan

    return corr_matrix, pval_matrix


def _prepare_heatmap(matrix):
    """
    Prepare a matrix and mask for triangular heatmap visualization.

    This function:
    - Creates an upper triangular mask to avoid duplicate values
    - Removes redundant first row/last column for cleaner plotting
    """

    # Create upper triangle mask
    mask = np.triu(np.ones_like(matrix, dtype=bool))

    # Trim matrix to avoid redundant mirrored values
    return matrix.iloc[1:, :-1], mask[1:, :-1]


def plot_correlation_with_pvalue(df_train, df_test,
                                train_name="Train Data",
                                test_name="Test Data"):
    """
    Visualize correlation and statistical significance across datasets.

    This function:
    - Computes correlation (r) and p-value matrices for each dataset
    - Plots three types of heatmaps for each dataset:
        1. Correlation heatmap (strength of relationship)
        2. P-value heatmap (statistical significance)
        3. Significant correlations only (p < 0.05)

    It supports mixed numeric and binary features using Pearson and
    point-biserial correlation appropriately.
    """

    # =========================
    # Compute correlation & p-value
    # =========================
    corr_train, p_train = _compute_corr_pval(df_train)
    corr_test, p_test = _compute_corr_pval(df_test)

    # =========================
    # Prepare matrices for plotting
    # =========================
    corr_train, mask_train = _prepare_heatmap(corr_train)
    p_train, _ = _prepare_heatmap(p_train)

    corr_test, mask_test = _prepare_heatmap(corr_test)
    p_test, _ = _prepare_heatmap(p_test)

    # Color map for correlation
    cmap = sns.diverging_palette(0, 230, 90, 60, as_cmap=True)

    # Create subplot grid (3 rows × 2 datasets)
    fig, ax = plt.subplots(3, 2, figsize=(25, 20))

    datasets = [
        (corr_train, p_train, mask_train, train_name),
        (corr_test, p_test, mask_test, test_name)
    ]

    for col, (corr, pval, mask, title) in enumerate(datasets):

        # =========================
        # 1. Correlation heatmap
        # =========================
        sns.heatmap(
            corr,
            mask=mask,
            annot=True,
            fmt=".2f",
            cmap=cmap,
            vmin=-1, vmax=1,
            linewidths=0.5,
            linecolor="white",
            ax=ax[0, col]
        )
        ax[0, col].set_title(f"{title} - Correlation", weight="bold", pad=15, fontsize=12)

        # =========================
        # 2. P-value heatmap
        # =========================
        sns.heatmap(
            pval,
            mask=mask,
            annot=True,
            fmt=".3f",
            cmap=cmap,
            linewidths=0.5,
            linecolor="white",
            ax=ax[1, col]
        )
        ax[1, col].set_title(f"{title} - P-value", weight="bold", pad=15, fontsize=12)

        # =========================
        # 3. Significant correlations only
        # =========================
        sig = pval < 0.05  # significance threshold

        sns.heatmap(
            corr.where(sig),  # mask non-significant values
            mask=mask,
            annot=True,
            fmt=".2f",
            cmap=cmap,
            vmin=-1, vmax=1,
            linewidths=0.5,
            linecolor="white",
            ax=ax[2, col]
        )
        ax[2, col].set_title(f"{title} - Significant (p < 0.05)", weight="bold", pad=15, fontsize=12)

    plt.tight_layout()
    plt.show()

def plot_categorical_distribution_across_datasets(train_data: pd.DataFrame, test_data: pd.DataFrame, 
                                                  original_data: pd.DataFrame, feature: str):
    """
    Plot categorical feature distribution across Train, Original, and Test datasets.

    This function generates:
    1. Count plots (absolute frequency)
    2. Donut pie charts (percentage distribution)

    Parameters
    ----------
    train_data : pd.DataFrame
        Training dataset.
    test_data : pd.DataFrame
        Test dataset.
    original_data : pd.DataFrame
        Original dataset.
    feature : str
        Categorical column name to analyze.

    Notes
    -----
    - Category order is fixed based on the Train dataset to ensure consistency.
    - Pie chart percentages are aligned with the same category order.
    - Useful for checking distribution drift across datasets.
    """

    # Define consistent color palette based on number of categories
    colors = ColorUtils.color(n_colors=train_data[feature].nunique())

    # Dataset labels and list
    dataset_names = ["Train", "Test", "Original"]
    datasets = [train_data, test_data, original_data]

    # Fix category order using Train data to ensure consistent plotting
    order = train_data[feature].unique().tolist()

    # Create 2x3 subplot grid:
    # Row 1 → Count plots
    # Row 2 → Percentage donut charts
    fig, ax = plt.subplots(2, 3, figsize=(18, 10))

    # Row 1: Count Plots
    for i, (data, name) in enumerate(zip(datasets, dataset_names)):
        sns.countplot(y=feature, data=data, ax=ax[0, i], palette=colors, order=order)
        ax[0, i].set_title(f"{name} Data: {feature.title()} Counts", fontsize=12, weight="bold")
        ax[0, i].set_xlabel("")
        ax[0, i].set_ylabel("")
        
        for p in ax[0, i].patches:
            ax[0, i].annotate(f"{int(p.get_width())}", 
                               (p.get_width(), p.get_y() + p.get_height() / 2), 
                               ha="left", va="center", 
                               color="black", fontsize=11)
        ax[0, i].set_axisbelow(True)
        sns.despine(ax=ax[0, i])

    # Row 2: Donut Pie Charts
    for i, (data, name) in enumerate(zip(datasets, dataset_names)):
        counts = data[feature].value_counts().reindex(order)
        wedges, texts, autotexts = ax[1, i].pie(
            counts, labels=order, autopct="%1.1f%%", startangle=90, colors=colors,
            textprops={"fontsize": 12}, radius=1.2,  shadow=True)

        # Create donut hole
        centre_circle = plt.Circle((0, 0), 0.70, fc="white")
        ax[1, i].add_artist(centre_circle)
        ax[1, i].set_title(f"{name} Data: {feature.title()} Distribution (%)", fontsize=12, weight="bold")
        ax[1, i].axis("equal")

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.3)
    plt.show()

def categorical_distribution_across_datasets(
    df_train: pd.DataFrame,
    df_test: pd.DataFrame,
    df_original: pd.DataFrame,
    feature: str,
    logger: logging.Logger
) -> None:

    logger.info(f"Analyzing categorical feature: {feature}")

    # TRAIN
    train_summary = (
        df_train[feature]
        .value_counts()
        .rename_axis("Category")
        .reset_index(name="Train_Count")
    )
    train_summary["Train_%"] = round(
        train_summary["Train_Count"] / train_summary["Train_Count"].sum() * 100, 2
    )

    # TEST
    test_summary = (
        df_test[feature]
        .value_counts()
        .rename_axis("Category")
        .reset_index(name="Test_Count")
    )
    test_summary["Test_%"] = round(
        test_summary["Test_Count"] / test_summary["Test_Count"].sum() * 100, 2
    )

    # ORIGINAL
    original_summary = (
        df_original[feature]
        .value_counts()
        .rename_axis("Category")
        .reset_index(name="Original_Count")
    )
    original_summary["Original_%"] = round(
        original_summary["Original_Count"] / original_summary["Original_Count"].sum() * 100, 2
    )

    # Merge ALL
    summary = train_summary.merge(test_summary, on="Category", how="outer")
    summary = summary.merge(original_summary, on="Category", how="outer")

    logger.debug(f"{feature}: {len(summary)} categories detected")
    summary["Category"] = summary["Category"].astype(str)

    num_cols = [
        "Train_Count", "Train_%",
        "Test_Count", "Test_%",
        "Original_Count", "Original_%"
    ]

    summary[num_cols] = summary[num_cols].fillna(0)
    summary = summary.sort_values(by="Train_Count", ascending=False)

    logger.info(
        f"Categorical Feature Distribution: {feature}:\n"
        f"{summary.to_string()}"
    )

    logger.info(f"Completed analysis for: {feature}")
    logger.info("*" * 80)

def top_ratio(
    df_train: pd.DataFrame,
    df_test: pd.DataFrame,
    cat_features: List[str],
    logger: logging.Logger
) -> None:
    """
    Identify categorical features dominated by a single category (>99%)
    across Train, Test, and Original datasets.

    A feature is considered low-variance if one category accounts for
    more than 99% of its values.
    """

    # Define dataset names and corresponding DataFrames
    dataset_names = ["Train", "Test"]
    datasets = [df_train, df_test]

    # Iterate through each dataset
    for data, name in zip(datasets, dataset_names):

        # Log dataset name
        logger.info(f"{name} Data")

        # Flag to check if any feature is dominated
        flagged = False

        # Iterate through each categorical feature
        for feature in cat_features:

            # Compute normalized frequency (percentage) of each category
            # Drop NA to avoid misleading ratios
            freq = data[feature].dropna().value_counts(normalize=True)

            # Skip if feature is empty after dropping NA
            if freq.empty:
                continue

            # Get top category ratio and category name
            top_ratio_value = freq.iloc[0]
            top_category = freq.index[0]

            # Check if one category dominates (>99%)
            if top_ratio_value > 0.99:
                flagged = True

                # Log feature name, dominant ratio, and category
                logger.info(
                    f"{feature}: {top_ratio_value:.1%} is '{top_category}'"
                )

        # If no feature meets the condition
        if not flagged:
            logger.info("No feature has a category that makes up more than 99% of its values.")

        # Separator for readability
        logger.info("-" * 80)

def plot_feature_importance_comparison(
    feature_importances: dict,
    top_n: int = 20,
    figsize: tuple = (20, 10),
    show_std: bool = False
):
    """
    Compare normalized feature importance across multiple models.

    All subplots use the same features and the same feature order.
    The common feature ranking is determined by the average normalized
    importance across all models.

    Parameters
    ----------
    feature_importances : dict
        Dictionary containing feature importance DataFrames.

        Expected format:
        {
            "CatBoostClassifier": results_cb["feature_importance"],
            "LGBMClassifier": results_lgbm["feature_importance"],
            "XGBClassifier": results_xgb["feature_importance"]
        }

        Each DataFrame must contain:
        - feature
        - importance_mean
        - importance_std

    top_n : int, default=20
        Number of common features displayed.

    figsize : tuple, default=(20, 10)
        Figure size.

    show_std : bool, default=False
        Whether to display standard deviation error bars.

    Returns
    -------
    matplotlib.figure.Figure
        Generated figure.
    """

    # Validate input    
    required_columns = {"feature", "importance_mean", "importance_std"}

    if not feature_importances:
        raise ValueError("feature_importances cannot be empty.")

    normalized_data = {}

    for model_name, importance_df in feature_importances.items():
        missing_columns = required_columns - set(importance_df.columns)
        if missing_columns:
            raise ValueError(
                f"{model_name} is missing required columns: "
                f"{sorted(missing_columns)}"
            )

        df = importance_df.copy()
        
        # Normalize using ALL features of each model        
        total_importance = df["importance_mean"].sum()
        if total_importance > 0:
            df["importance_normalized"] = (df["importance_mean"] / total_importance)
            df["std_normalized"] = (df["importance_std"] / total_importance)
        else:
            df["importance_normalized"] = 0.0
            df["std_normalized"] = 0.0

        normalized_data[model_name] = df
    
    # Build common feature ranking    
    ranking_frames = []
    for model_name, df in normalized_data.items():
        temp = df[["feature", "importance_normalized"]].copy()
        temp = temp.rename(columns={"importance_normalized": model_name})
        ranking_frames.append(temp)

    # Merge importance from all models by feature
    ranking_df = ranking_frames[0]

    for temp in ranking_frames[1:]:
        ranking_df = ranking_df.merge(temp, on="feature", how="outer")

    ranking_df = ranking_df.fillna(0)
    model_columns = list(feature_importances.keys())

    # Average normalized importance across models
    ranking_df["mean_importance"] = (
        ranking_df[model_columns]
        .mean(axis=1)
    )
    
    # Select ONE common Top-N feature list    
    common_features = (
        ranking_df
        .nlargest(top_n, "mean_importance")
        .sort_values(
            "mean_importance",
            ascending=False
        )["feature"]
        .tolist()
    )
    
    # Create subplots    
    n_models = len(feature_importances)
    fig, axes = plt.subplots(1, n_models, figsize=figsize, sharey=True)
    if n_models == 1:
        axes = [axes]
    
    # Plot each model using SAME feature order    
    for ax, (model_name, df) in zip(axes, normalized_data.items()):
        # Reindex guarantees identical feature order
        plot_df = (
            df
            .set_index("feature")
            .reindex(common_features)
            .fillna(0)
            .reset_index()
        )

        sns.barplot(
            data=plot_df,
            x="importance_normalized",
            y="feature",
            hue="importance_normalized",
            palette="viridis_r",
            legend=False,
            order=common_features,
            ax=ax
        )
        
        # Optional standard deviation        
        if show_std:
            ax.errorbar(
                x=plot_df["importance_normalized"],
                y=np.arange(len(plot_df)),
                xerr=plot_df["std_normalized"],
                fmt="none",
                capsize=3
            )
        
        # Styling        
        ax.set_title(model_name, fontsize=15, fontweight="bold", pad=15)
        ax.set_xlabel("Normalized Feature Importance", fontsize=10)
        ax.set_ylabel("")
        ax.grid(axis="x", linestyle="--", alpha=0.3)
        ax.set_axisbelow(True)
    
    # Main title    
    fig.suptitle("Feature Importance Comparison Across Models", fontsize=18, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.show()

    return fig
