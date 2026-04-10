import numpy as np
import pandas as pd
import logging
from scipy.stats import skew
from sklearn.preprocessing import PowerTransformer

class FeatureUtils:

    @staticmethod
    def fea_HandleSkewedFeatures(
            df: pd.DataFrame,
            num_features: list[str],
            logger: logging.Logger,
            zero_threshold: float = 0.9,
            skew_threshold: float = 0.5,
            exclude_cols: list[str] | None = None
    ) -> tuple[pd.DataFrame, list[str], list[str], list[str]]:
        """
        Detect and transform skewed numerical features.

        The function identifies skewed numerical features based on a skewness
        threshold and applies appropriate transformations. Sparse features
        (high proportion of zeros) are handled using binary indicators and
        log transformation, while other skewed features are transformed using
        the Yeo-Johnson method.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataset.

        num_features : list[str]
            List of numerical features to evaluate.

        logger : logging.Logger
            Logger used to record processing steps.

        zero_threshold : float, optional (default=0.9)
            Threshold to identify sparse features (high proportion of zeros).

        skew_threshold : float, optional (default=0.5)
            Absolute skewness threshold used to detect skewed features.

        exclude_cols : list[str] or None, optional
            Columns to exclude from transformation.

        Returns
        -------
        df : pd.DataFrame
            Transformed dataset.

        transformed_cols : list[str]
            Names of newly created transformed features.

        high_zero_cols : list[str]
            Features identified as sparse.

        auto_skewed : list[str]
            Features detected as skewed.

        Notes
        -----
        - Sparse features → create ``Has_<col>`` and ``Log_<col>``.
        - Continuous skewed features → apply ``Yeo-Johnson`` transformation.
        - Low-cardinality features (≤ 5 unique values) are kept unchanged.
        """

        logger.info("Starting skewed feature handling")

        df = df.copy()

        if num_features is None:
            logger.error("num_features parameter is required")
            raise ValueError("`num_features` must be provided")
        if exclude_cols is None:
            exclude_cols = []

        logger.debug(f"Total numerical features provided: {len(num_features)}")
        logger.debug(f"Excluded columns: {exclude_cols}")

        # 1) pick the numeric cols to scan
        numerical_cols = [c for c in num_features if c not in exclude_cols]
        logger.info(f"Scanning {len(numerical_cols)} numerical columns")

        # 2) detect ultra‑sparse
        zero_ratios = (df[numerical_cols] == 0).sum() / len(df)
        high_zero_cols = zero_ratios[zero_ratios > zero_threshold].index.tolist()

        if high_zero_cols:
            logger.info(f"Detected {len(high_zero_cols)} high-zero columns: {high_zero_cols}")

        # 3) compute skew
        skew_vals = df[numerical_cols].apply(lambda s: skew(s.dropna()))
        auto_skewed = skew_vals[abs(skew_vals) > skew_threshold].index.tolist()

        logger.info(f"Detected {len(auto_skewed)} skewed features")

        # 4) union these with your forced list
        to_transform = list(set(auto_skewed))

        transformed_cols = []
        dropped_cols     = []

        for col in to_transform:
            logger.debug(f"Processing column: {col}")
            # if it's sparse → binary+log
            if col in high_zero_cols:
                logger.info(f"{col}: sparse feature detected → applying binary + log transform")
                df[f"Has_{col}"] = (df[col] > 0).astype(int)
                df[f"Log_{col}"] = df[col].map(lambda x: np.log1p(x) if x > 0 else 0)
                transformed_cols += [f"Has_{col}", f"Log_{col}"]
                dropped_cols.append(col)
            # if it's discrete small‑cardinality, skip transform but keep
            elif df[col].nunique() <= 5:
                logger.debug(f"{col}: small cardinality ({df[col].nunique()}) → skipping transform")
                # do nothing (we still keep raw col in df)
                continue
            # otherwise apply Yeo‑Johnson
            else:
                logger.info(f"{col}: applying Yeo-Johnson transformation")
                pt = PowerTransformer(method="yeo-johnson")
                arr = df[[col]].values  # shape (n,1)
                df[f"PT_{col}"] = pt.fit_transform(arr)
                transformed_cols.append(f"PT_{col}")
                dropped_cols.append(col)

        # drop originals for any column we did transform
        if dropped_cols:
            logger.info(f"Dropping original columns after transformation: {dropped_cols}")
            df.drop(columns=dropped_cols, inplace=True)

        logger.info(f"Feature transformation completed. Generated {len(transformed_cols)} new features")
        return df, transformed_cols, high_zero_cols, auto_skewed
