import logging
import numpy as np
import optuna
import lightgbm as lgb
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score

def objective_lgbm(
    trial: optuna.Trial,
    X,
    y,
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

    y : array-like or pandas.Series
        Target labels.

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
        "n_estimators": trial.suggest_int("iterations", 1000, 5000)
    }

    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)

    auc_scores = []

    # Cross-validation loop
    for train_idx, valid_idx in cv.split(X, y):
        X_train, X_valid = X[train_idx], X[valid_idx]
        y_train, y_valid = y.iloc[train_idx], y.iloc[valid_idx]

        model = lgb.LGBMClassifier(**params)

        model.fit(
            X_train,
            y_train,
            eval_set=[(X_valid, y_valid)],
            eval_metric="auc",
            callbacks=[lgb.early_stopping(300, verbose=False)]
        )

        preds = model.predict_proba(X_valid)[:,1]
        auc = roc_auc_score(y_valid, preds)
        auc_scores.append(auc)

    mean_auc = np.mean(auc_scores)
    logger.info(f"Trial {trial.number} finished | Mean AUC: {mean_auc:.5f}")

    return mean_auc
