# lgbm_tuning.py
import logging
import gc
import numpy as np
import pandas as pd
import optuna

import lightgbm as lgb
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score

def objective_lgbm(
    trial: optuna.Trial,
    X,
    y,
    cat_features,
    logger: logging.Logger,
    n_splits: int = 5,
    random_state: int = 42
) -> float:
    """
    Optuna objective function for tuning LGBMClassifier using cross-validation.

    This function performs Stratified K-Fold cross-validation and returns the
    mean ROC-AUC score across folds. Optuna will attempt to maximize this score
    by searching for the best hyperparameter combination.

    Parameters
    ----------
    trial : optuna.Trial
        Optuna trial object used to suggest hyperparameters.

    X : array-like or pandas.DataFrame
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
    -------
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

    params = {
        "objective": "binary",
        "metric": "auc",
        "verbosity": -1,
        "n_jobs": -1,
        "boosting_type": "gbdt",
        "learning_rate": trial.suggest_float("learning_rate", 0.005, 0.05, log=True),
        "num_leaves": trial.suggest_int("num_leaves", 16, 256),
        "max_depth": trial.suggest_int("max_depth", 3, 10),
        "class_weight": "balanced",
        "min_child_samples": trial.suggest_int("min_child_samples", 5, 100),
        "subsample": trial.suggest_float("subsample", 0.6, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
        "max_bin": 255,
        "reg_alpha": trial.suggest_float("reg_alpha", 1e-3, 10, log=True),
        "reg_lambda": trial.suggest_float("reg_lambda", 1e-3, 10, log=True),
        "random_state": random_state,
        "n_estimators": trial.suggest_int("iterations", 500, 2500)
    }

    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)

    auc_scores = []

    # Cross-validation loop
    for fold, (train_idx, valid_idx) in enumerate(skf.split(X, y), start=1):
        # Split fold data
        X_train = X.iloc[train_idx].copy()
        X_valid = X.iloc[valid_idx].copy()

        y_train = y.iloc[train_idx]
        y_valid = y.iloc[valid_idx]

        # Convert categorical columns to pandas category dtype
        for col in cat_features:
            X_train[col] = X_train[col].astype("category")
            X_valid[col] = X_valid[col].astype("category")

        # Initialize LightGBM
        model = lgb.LGBMClassifier(**params)

        model.fit(
            X_train,
            y_train,
            categorical_feature=cat_features,
            eval_set=[(X_valid, y_valid)],
            callbacks=[lgb.early_stopping(300, verbose=False), 
                       lgb.log_evaluation(period=0)]
        )

        preds = model.predict_proba(X_valid)[:,1]
        auc = roc_auc_score(y_valid, preds)
        auc_scores.append(auc)

        logger.debug(
            f"Trial {trial.number} | "
            f"Fold {fold}/{n_splits} | "
            f"AUC: {auc:.5f} | "
            f"Best iteration: {model.best_iteration_}"
        )

        # Clean memory
        del model
        gc.collect()

    # Final Trial Score
    mean_auc = np.mean(auc_scores)
    std_auc = np.std(auc_scores)

    logger.info(
        f"Trial {trial.number} finished | "
        f"Mean AUC: {mean_auc:.5f} | "
        f"Std: {std_auc:.5f}"
    )

    return mean_auc
