# validation.py
import numpy as np
import pandas as pd
import logging
from typing import List

class DataValidator:
    """
    Utility class for performing basic data quality validation on pandas DataFrames.

    This class provides static methods to detect common data issues during
    exploratory data analysis (EDA) or data validation stages in a data pipeline.

    Main checks include:
    - Missing values
    - Duplicate rows
    - Outliers (IQR method)
    - Feature skewness

    Results are reported through a configurable logger for monitoring and debugging.
    """

    @staticmethod
    def checkNULL(df: pd.DataFrame, logger: logging.Logger) -> None:
        """
        Display and log missing value statistics for a given dataset.

        This function checks for missing values (including blank strings),
        summarizes missing counts and percentages per feature, and reports
        the results using logging and formatted tables when available.

        Parameters
        ----------
        df : pandas.DataFrame
            Input dataset to be inspected for missing values.

        logger : logging.Logger
            Logger used for reporting progress and errors.

        Returns
        -------
        None
            Prints missing value summary and logs overall statistics.
        """

        # Get total number of rows
        total_rows = len(df)

        # Replace blank strings with NaN for completeness
        df_null_check = df.replace(r"^\s*$", np.nan, regex=True)

        # Compute missing value statistics per column
        missing_df = df_null_check.isnull().sum().reset_index()
        missing_df.columns = ["Feature", "Missing_Count"]

        # Keep only columns with missing values
        missing_df = missing_df[missing_df["Missing_Count"] > 0]

        # Calculate missing percentage
        missing_df["Missing_%"] = (missing_df["Missing_Count"] / total_rows * 100).round(2)

        # Sort by missing count (descending)
        missing_df = missing_df.sort_values(by="Missing_Count", ascending=False).reset_index(drop=True)

        # Calculate total missing value
        total_missing = missing_df["Missing_Count"].sum()

        # Log and display results
        if total_missing == 0:
            logger.info(f"No missing values detected in {total_rows:,} rows.")
        else:
            # Try to print nicely formatted table
            try:
                from tabulate import tabulate
                table_str = tabulate(missing_df, headers="keys", tablefmt="pretty", showindex=False, 
                            colalign=("left", "left", "left"))
                logger.warning("\n" + table_str)
            except ImportError:
                logger.error(missing_df.to_string(index=False))

            logger.warning(f"Total missing values: {total_missing:,} out of {total_rows:,} rows.")

    @staticmethod
    def checkDuplicate(df: pd.DataFrame, logger: logging.Logger) -> None:
        """
        Check and log duplicate rows in a dataset.

        This function identifies fully duplicated rows in the input DataFrame
        and reports the results using the configured logger.

        Parameters
        ----------
        df : pandas.DataFrame
            Input dataset to be checked for duplicate rows.

        logger : logging.Logger
            Logger used for reporting progress and errors.

        Returns
        -------
        None
            Logs duplicate statistics to the console or log file.
        """

        duplicates_count = df.duplicated().sum()
        total_rows = len(df)

        if duplicates_count == 0:
            logger.info(f"No duplicate rows found out of {total_rows:,} total rows.")
        else:
            logger.warning(f"{duplicates_count:,} duplicate rows detected ({duplicates_count/total_rows:.2%}).")
            logger.warning(f"Rows affected: {duplicates_count:,} out of {total_rows:,}.")

    @staticmethod
    def checkOutlier(df: pd.DataFrame, dataset_name: str, list_feature: List, 
                        logger: logging.Logger) -> pd.DataFrame:
        """
        Detect and report outliers using the IQR (Interquartile Range) method.

        This function identifies outliers for specified numerical features
        based on the 1.5 × IQR rule, logs detailed statistics, and returns
        a summary table for reporting and monitoring purposes.

        Parameters
        ----------
        df : pandas.DataFrame
            Input dataset to be inspected for outliers.

        dataset_name : str
            Name of the dataset (used for logging context).

        num_features : List
            List of numerical feature names to be checked.

        logger : logging.Logger
            Logger instance for recording inspection results.

        Returns
        -------
        pandas.DataFrame
            Summary table containing:
            - feature (str): Feature name
            - outlier_count (int): Number of detected outliers
        """

        # Log inspection start
        logger.info(f"Checking outliers for {dataset_name}...")
        logger.info("-" * 80)

        outlier_info = []

        # Iterate through numerical features
        for feature in list_feature:
            # Compute quartiles
            Q1 = df[feature].quantile(0.25)
            Q3 = df[feature].quantile(0.75)
            IQR = Q3 - Q1

            # Define outlier boundaries
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            # Identify outliers
            outliers = df[(df[feature] < lower_bound) | (df[feature] > upper_bound)][feature]
            outlier_count = len(outliers)

            # Log results for each feature
            if outlier_count == 0:
                logger.debug(f"[{dataset_name}] {feature}: No outliers detected")
            else:
                logger.warning(
                    f"[{dataset_name}] {feature}: {outlier_count:,} outliers detected "
                    f"(lower={lower_bound:.3f}, upper={upper_bound:.3f})"
                )
                outlier_info.append({
                    "Feature": feature,
                    "Outlier_Count": outlier_count
                })
        return pd.DataFrame(outlier_info)

    @staticmethod
    def check_skewness(data: pd.DataFrame, dataset_name: str, numerical_features: List[str], 
                       logger: logging.Logger, sort=True) -> List:
        """
        Analyze skewness of numerical features in a dataset and log summary insights.

        This function computes the skewness for each numerical feature, optionally
        sorts them by absolute skewness, and categorizes features based on the
        degree of skewness. Detailed results are logged at DEBUG level, while
        high-level insights and recommendations are logged at INFO level.

        Parameters
        ----------
        data : pandas.DataFrame
            The input dataset containing numerical features to be analyzed.

        dataset_name : str
            A descriptive name of the dataset, used for logging and reporting.

        numerical_features : list of str, optional
            List of numerical feature names to evaluate.
            Default is `num_features`.

        logger : logging.Logger
            Logger object used to output analysis results and insights.

        sort : bool, optional (default=True)
            If True, sort features by absolute skewness in descending order.

        Returns
        -------
        list of str
            A list of feature names that are considered highly skewed
            (|skewness| > 1).

        Notes
        -----
        - Skewness interpretation:
            * |skew| ≤ 0.5  : Approximately symmetric
            * 0.5 < |skew| ≤ 1 : Moderately skewed
            * |skew| > 1   : Highly skewed
        - Highly skewed features may benefit from transformations such as:
            log, Box-Cox, or Yeo-Johnson.
        - This function is intended for exploratory data analysis (EDA)
        and feature preprocessing stages.
        """

        skewness_dict = {}
        skew_features = []
        for feature in numerical_features:
            skew = data[feature].skew(skipna=True)
            skewness_dict[feature] = skew

        skew_df = pd.DataFrame.from_dict(skewness_dict, orient="index", columns=["Skewness"])
        if sort:
            skew_df = skew_df.reindex(skew_df["Skewness"].abs().sort_values(ascending=False).index)

        # ===== Summary header =====
        logger.info(f"Skewness analysis for {dataset_name}")
        logger.info(f"Total numerical features checked: {len(skew_df)}")

        # ===== Detailed table (DEBUG) =====
        logger.debug("-"*70)
        logger.debug(f"{'Feature':<30} | {'Skewness':<9} | {'Remark'}")
        logger.debug("-"*70)
        for feature, row in skew_df.iterrows():
            skew = row["Skewness"]
            abs_skew = abs(skew)
            if abs_skew > 1:
                remark = "Highly skewed"
                skew_features.append(feature)
            elif abs_skew > 0.5:
                remark = "Moderately skewed"
                skew_features.append(feature)
            else:
                remark = "Approximately symmetric"
            logger.debug(f"{feature:<30} | {skew:>+9.4f} | {remark}")
        logger.debug("-" * 70)

        # ===== Summary insight =====
        if skew_features:
            logger.info(f"{len(skew_features)} features are skewed (|skew| > 0.5).")
            logger.info(f"Recommendation: Consider log / Box-Cox / Yeo-Johnson transformation.")
        else:
            logger.info("No highly skewed features detected.")

        return skew_features
