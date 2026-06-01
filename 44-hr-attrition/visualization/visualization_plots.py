import logging
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from utils.colors_utils import ColorUtils
from typing import List
from scipy.stats import pearsonr, pointbiserialr

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

def plot_categorical_distribution_across_datasets(train_data: pd.DataFrame, test_data: pd.DataFrame, feature: str):
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
    dataset_names = ["Train", "Test"]
    datasets = [train_data, test_data]

    # Fix category order using Train data to ensure consistent plotting
    order = train_data[feature].unique().tolist()

    # Create 2x3 subplot grid:
    # Row 1 → Count plots
    # Row 2 → Percentage donut charts
    fig, ax = plt.subplots(2, 2, figsize=(18, 10))

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

    # Merge ALL
    summary = train_summary.merge(test_summary, on="Category", how="outer")

    logger.debug(f"{feature}: {len(summary)} categories detected")
    summary["Category"] = summary["Category"].astype(str)

    num_cols = [
        "Train_Count", "Train_%",
        "Test_Count", "Test_%"
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
