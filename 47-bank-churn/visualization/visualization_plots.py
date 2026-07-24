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

def categorical_distribution(
    df: pd.DataFrame,
    feature: str,
    logger: logging.Logger
) -> pd.DataFrame:
    """
    Analyze the distribution of a categorical feature.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataset.
    feature : str
        Categorical feature name.
    logger : logging.Logger
        Logger object.

    Returns
    -------
    pd.DataFrame
        Summary table containing count and percentage.
    """

    logger.info("-" * 80)
    logger.info(f"Analyzing categorical feature: {feature}")

    summary = (
        df[feature]
        .value_counts(dropna=False)
        .rename_axis("Category")
        .reset_index(name="Count")
    )

    summary["Percentage (%)"] = (
        summary["Count"] / len(df) * 100
    ).round(2)

    summary["Category"] = summary["Category"].astype(str)

    logger.info(f"Number of categories: {summary.shape[0]}")
    logger.info(
        f"\nCategorical Distribution - {feature}\n"
        f"{summary.to_string(index=False)}"
    )

    logger.info(f"Completed analysis for: {feature}")
    logger.info("-" * 80)

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

def plot_churn_by_province(
    df: pd.DataFrame,
    province_coordinates: dict,
    mapbox_token: str,
    logger: logging.Logger,
    province_col: str = "origin_province",
    target_col: str = "exit",
    map_style: str = "dark",
    zoom: float = 4.5,
    height: int = 650
):
    """
    Plot customer churn distribution by province on a Mapbox map.

    Bubble size represents the number of customers in each province,
    while bubble color represents the churn rate.

    Parameters
    ----------
    df : pd.DataFrame
        Customer dataset.

    province_coordinates : dict
        Dictionary containing latitude and longitude for each province.

        Expected format:
        {
            "TP. Hồ Chí Minh": {
                "lat": 10.8231,
                "lon": 106.6297
            }
        }

    mapbox_token : str
        Mapbox access token.

    logger : logging.Logger
        Logger used for reporting progress and errors.

    province_col : str, default="origin_province"
        Column containing province names.

    target_col : str, default="exit"
        Binary churn target where:
            0 = Retained
            1 = Exited

    map_style : str, default="dark"
        Mapbox map style.

    zoom : float, default=4.5
        Initial map zoom level.

    height : int, default=650
        Figure height in pixels.

    Returns
    -------
    plotly.graph_objects.Figure
        Plotly geographic churn map.
    """
    
    # Validate required columns    
    required_cols = [province_col, target_col]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required column(s): {missing_cols}")
    
    # Aggregate customer information by province    
    province_summary = (
        df.groupby(province_col, observed=True)
          .agg(
              customers=(target_col, "size"),
              exited=(target_col, "sum")
          )
          .reset_index()
    )

    province_summary["retained"] = (
        province_summary["customers"]
        - province_summary["exited"]
    )

    province_summary["churn_rate"] = (
        province_summary["exited"]
        / province_summary["customers"]
        * 100
    )
    
    # Add geographic coordinates    
    province_summary["lat"] = province_summary[province_col].map(
        lambda province:
        province_coordinates.get(province, {}).get("lat")
    )

    province_summary["lon"] = province_summary[province_col].map(
        lambda province:
        province_coordinates.get(province, {}).get("lon")
    )

    # Detect provinces without coordinates
    missing_coordinates = province_summary.loc[
        province_summary[["lat", "lon"]].isna().any(axis=1),
        province_col
    ].tolist()

    if missing_coordinates:
        logger.warning("Warning: Missing coordinates for: " + ", ".join(map(str, missing_coordinates)))

    # Remove provinces without coordinates
    province_summary = province_summary.dropna(subset=["lat", "lon"]).copy()

    if province_summary.empty:
        raise ValueError("No valid province coordinates available for plotting.")
    
    # Scale bubble size    
    province_summary["customer_scaling"] = (
        province_summary["customers"]
        / province_summary["customers"].max()
    )

    province_summary["bubble_size"] = (
        15 + province_summary["customer_scaling"] * 55
    )
    
    # Hover information    
    hover_text = (
        "<b>"
        + province_summary[province_col].astype(str)
        + "</b><br>"
        + "Customers: "
        + province_summary["customers"].map("{:,.0f}".format)
        + "<br>"
        + "Retained: "
        + province_summary["retained"].map("{:,.0f}".format)
        + "<br>"
        + "Exited: "
        + province_summary["exited"].map("{:,.0f}".format)
        + "<br>"
        + "Churn Rate: "
        + province_summary["churn_rate"].map("{:.2f}%".format)
    )
    
    # Create map    
    fig = go.Figure(
        go.Scattermapbox(
            lat=province_summary["lat"],
            lon=province_summary["lon"],
            mode="markers",
            marker=go.scattermapbox.Marker(
                # Bubble size -> customer population
                size=province_summary["bubble_size"],
                # Bubble color -> churn rate
                color=province_summary["churn_rate"],
                cmin=province_summary["churn_rate"].min(),
                cmax=province_summary["churn_rate"].max(),
                colorscale="teal",
                showscale=False,
                opacity=0.80
            ),
            hoverinfo="text",
            hovertext=hover_text
        )
    )
    
    # Configure layout    
    fig.update_layout(
        autosize=True,
        height=height,
        margin={
            "r": 5,
            "t": 40,
            "l": 5,
            "b": 5
        },

        hovermode="closest",
        showlegend=False,
        title=dict(
            text="<b>Customer Churn Distribution by Province</b>",
            font=dict(
                size=12,
                family="Arial",
                color="white"
            ),
            x=0.01,
            y=0.98
        ),

        mapbox=dict(
            accesstoken=mapbox_token,
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=16.0,
                lon=106.0
            ),
            pitch=0,
            zoom=zoom,
            style=map_style
        )
    )

    return fig

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
