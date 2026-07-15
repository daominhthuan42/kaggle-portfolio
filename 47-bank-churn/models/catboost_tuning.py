import logging
import numpy as np
import optuna
from catboost import CatBoostClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score


def objective_catboost(
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
    bootstrap_type = trial.suggest_categorical(
        "bootstrap_type", ["Bayesian", "Bernoulli"]
    )
    params = {
        "iterations": trial.suggest_int("iterations", 1000, 5000),
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.08, log=True),
        "depth": trial.suggest_int("depth", 4, 8),
        "l2_leaf_reg": trial.suggest_float("l2_leaf_reg", 1e-3, 10, log=True),
        "random_strength": trial.suggest_float("random_strength", 1e-3, 10, log=True),
        "border_count": trial.suggest_int("border_count", 32, 255),
        "loss_function": "Logloss",
        "eval_metric": "AUC",
        "auto_class_weights": "Balanced",
        "random_seed": random_state,
        "verbose": 0,
        "allow_writing_files": False,
        "thread_count": -1,
        "bootstrap_type": bootstrap_type
    }

    if bootstrap_type == "Bayesian":
        params["bagging_temperature"] = trial.suggest_float("bagging_temperature", 0, 10)

    if bootstrap_type == "Bernoulli":
        params["subsample"] = trial.suggest_float("subsample", 0.6, 1.0)

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

        model = CatBoostClassifier(**params)

        model.fit(
            X_train,
            y_train,
            eval_set=(X_valid, y_valid),
            early_stopping_rounds=300,
            verbose=False
        )

        preds = model.predict_proba(X_valid)[:, 1]
        auc = roc_auc_score(y_valid, preds)
        auc_scores.append(auc)
        # logger.info(f"Trial {trial.number} | Fold {fold+1} AUC: {auc:.5f}")

    mean_auc = np.mean(auc_scores)
    logger.info(f"Trial {trial.number} finished | Mean AUC: {mean_auc:.5f}")

    return mean_auc
