# xgboost_tuning.py

import logging
import gc
import numpy as np
import pandas as pd
import optuna

from xgboost import XGBClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score

def objective_xgb(
    trial: optuna.Trial,
    X: pd.DataFrame,
    y: pd.Series,
    cat_features: list[str],
    logger: logging.Logger,
    n_splits: int = 5,
    random_state: int = 42,
) -> float:
    """
    Optuna objective function for tuning XGBClassifier using
    Stratified K-Fold cross-validation.

    This function:
    - Uses native XGBoost categorical feature support
    - Performs Stratified K-Fold cross-validation
    - Applies early stopping on each validation fold
    - Calculates ROC-AUC for each fold
    - Returns mean ROC-AUC for Optuna optimization

    Parameters
    --
    trial : optuna.Trial
        Optuna trial object used to suggest hyperparameters.

    X : pandas.DataFrame
        Training feature matrix.

    y : pandas.Series
        Binary target:
            0 = Retained
            1 = Exited.

    cat_features : list[str]
        List of categorical feature names.

    logger : logging.Logger
        Logger instance used to record tuning progress.

    n_splits : int, default=5
        Number of folds used in Stratified K-Fold cross-validation.

    random_state : int, default=42
        Random seed used for reproducibility.

    Returns
    ---
    float
        Mean ROC-AUC score across all folds.
    """

    # Validate input data
    if not isinstance(X, pd.DataFrame):
        raise TypeError(
            f"X must be a pandas DataFrame for native categorical support. "
            f"Received: {type(X)}"
        )

    if not isinstance(y, pd.Series):
        y = pd.Series(y, index=X.index)

    # Check whether all declared categorical features exist
    missing_cat_features = [col for col in cat_features if col not in X.columns]

    if missing_cat_features:
        raise ValueError(f"Categorical features not found in X: " f"{missing_cat_features}")

    # Check categorical dtype
    invalid_cat_features = [col for col in cat_features if not isinstance(X[col].dtype, pd.CategoricalDtype)]

    if invalid_cat_features:
        raise TypeError(
            f"The following categorical features are not category dtype: "
            f"{invalid_cat_features}"
        )

    # XGBoost should not receive raw object/string columns
    invalid_string_features = X.select_dtypes(
        include=["object", "string"]
    ).columns.tolist()

    if invalid_string_features:
        raise TypeError(
            f"Unsupported object/string columns detected: "
            f"{invalid_string_features}. "
            f"Convert them to category dtype before training."
        )

    # Calculate class imbalance
    n_negative = (y == 0).sum()
    n_positive = (y == 1).sum()

    if n_positive == 0:
        raise ValueError("Target contains no positive samples.")

    scale_pos_weight = n_negative / n_positive
    logger.debug(f"Trial {trial.number} | " f"scale_pos_weight: {scale_pos_weight:.4f}")

    # Hyperparameter search space
    params = {
        # Boosting configuration
        "n_estimators": trial.suggest_int("n_estimators", 500, 2000),
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.08, log=True),
        # Tree complexity
        "max_depth": trial.suggest_int("max_depth", 3, 10),
        "min_child_weight": trial.suggest_float("min_child_weight", 1.0, 10.0, log=True),
        # Row sampling
        "subsample": trial.suggest_float("subsample", 0.6, 1.0),
        # Feature sampling
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
        # Split regularization
        "gamma": trial.suggest_float("gamma", 1e-3, 10.0, log=True),
        # L1 regularization
        "reg_alpha": trial.suggest_float("reg_alpha", 1e-3, 10.0, log=True),
        # L2 regularization
        "reg_lambda": trial.suggest_float("reg_lambda", 1e-3, 10.0, log=True),
        # Binary classification
        "objective": "binary:logistic",
        # Evaluation metric for early stopping
        "eval_metric": "auc",
        # Native categorical support
        "enable_categorical": True,
        # Control categorical split strategy
        # "max_cat_to_onehot": 4,
        # Histogram tree construction
        "tree_method": "hist",
        # GPU
        "device": "cuda",
        # Class imbalance
        "scale_pos_weight": scale_pos_weight,
        # Reproducibility
        "random_state": random_state,
        # Runtime
        "n_jobs": -1,
    }

    # Stratified K-Fold
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)

    auc_scores = []

    # Cross-validation
    for fold, (train_idx, valid_idx) in enumerate(skf.split(X, y), start=1):
        logger.debug(f"Trial {trial.number} | " f"Starting Fold {fold}/{n_splits}")
        # Split fold data

        X_train = X.iloc[train_idx].copy()
        X_valid = X.iloc[valid_idx].copy()

        y_train = y.iloc[train_idx]
        y_valid = y.iloc[valid_idx]

        # Convert categorical columns to pandas category dtype
        for col in cat_features:
            X_train[col] = X_train[col].astype("category")
            X_valid[col] = X_valid[col].astype("category")

        # Verify categorical dtypes after split
        invalid_train_cat = [
            col
            for col in cat_features
            if not isinstance(X_train[col].dtype, pd.CategoricalDtype)
        ]

        invalid_valid_cat = [
            col
            for col in cat_features
            if not isinstance(X_valid[col].dtype, pd.CategoricalDtype)
        ]

        if invalid_train_cat or invalid_valid_cat:
            raise TypeError(
                "Categorical dtype was not preserved after "
                f"fold split. Train: {invalid_train_cat}, "
                f"Valid: {invalid_valid_cat}"
            )

        # Initialize XGBoost
        model = XGBClassifier(**params, early_stopping_rounds=300)

        # Train model
        model.fit(X_train, y_train, eval_set=[(X_valid, y_valid)], verbose=False)

        # Validation prediction
        preds = model.predict_proba(X_valid)[:, 1]

        # Fold ROC-AUC
        auc = roc_auc_score(y_valid, preds)
        auc_scores.append(auc)
        logger.debug(
            f"Trial {trial.number} | "
            f"Fold {fold}/{n_splits} | "
            f"AUC: {auc:.5f} | "
            f"Best iteration: {model.best_iteration}"
        )

        # Clean memory
        del model
        gc.collect()

    # Final trial score
    mean_auc = float(np.mean(auc_scores))
    std_auc = float(np.std(auc_scores))

    logger.info(
        f"Trial {trial.number} finished | "
        f"Mean AUC: {mean_auc:.5f} | "
        f"Std: {std_auc:.5f}"
    )

    return mean_auc
