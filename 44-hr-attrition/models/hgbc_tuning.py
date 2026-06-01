# hgbc_tuning.py
import logging
import numpy as np
import optuna
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score

def objective_histgb(
    trial: optuna.Trial,
    X,
    y,
    logger: logging.Logger,
    n_splits: int = 5,
    random_state: int = 42
) -> float:
    """
    Optuna objective function for tuning CatBoostClassifier using cross-validation.

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

    # -------------------------
    # Hyperparameter search space
    # -------------------------

    params = {
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.1, log=True),
        "max_depth": trial.suggest_int("max_depth", 3, 10),
        "max_leaf_nodes": trial.suggest_int("max_leaf_nodes", 15, 255),
        "min_samples_leaf": trial.suggest_int("min_samples_leaf", 10, 200),
        "l2_regularization": trial.suggest_float("l2_regularization", 1e-4, 10, log=True),
        "max_bins": trial.suggest_int("max_bins", 64, 255),
        "max_iter": trial.suggest_int("max_iter", 1000, 5000),
        "early_stopping": True,
        "validation_fraction": 0.1,
        "n_iter_no_change": 50,
        "random_state": random_state,
        "class_weight": "balanced"
    }

    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    auc_scores = []

    # -------------------------
    # Cross-validation loop
    # -------------------------

    for fold, (train_idx, valid_idx) in enumerate(skf.split(X, y)):
        X_train = X[train_idx]
        X_valid = X[valid_idx]

        y_train = y.iloc[train_idx]
        y_valid = y.iloc[valid_idx]

        model = HistGradientBoostingClassifier(**params)
        model.fit(X_train, y_train)

        preds = model.predict_proba(X_valid)[:, 1]
        auc = roc_auc_score(y_valid, preds)
        auc_scores.append(auc)

        # logger.info(f"Trial {trial.number} | Fold {fold+1} AUC: {auc:.5f}")

    mean_auc = np.mean(auc_scores)
    logger.info(f"Trial {trial.number} finished | Mean AUC: {mean_auc:.5f}")

    return mean_auc
