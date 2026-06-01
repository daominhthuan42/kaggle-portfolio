# ridge_tuning.py
import logging
import numpy as np
import optuna
from sklearn.linear_model import RidgeClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score

def objective_ridge(
    trial: optuna.Trial,
    X,
    y,
    logger: logging.Logger,
    n_splits: int = 5,
    random_state: int = 42
) -> float:
    """
    Optuna objective function for tuning RidgeClassifier
    using Stratified K-Fold cross-validation.

    This function performs cross-validation and returns
    the mean ROC-AUC score across folds.

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
        Number of folds used in Stratified K-Fold CV.

    random_state : int, default=42
        Random seed used for reproducibility.

    Returns
    -------
    float
        Mean ROC-AUC score across all folds.
    """


    # Hyperparameter Search Space
    params = {
        "alpha": trial.suggest_float("alpha", 1e-3, 100, log=True),
        "solver": trial.suggest_categorical("solver", [ "auto", "svd", "cholesky", "lsqr", "sag", "sparse_cg"]),
        "fit_intercept": trial.suggest_categorical("fit_intercept", [True, False]),
        "class_weight": trial.suggest_categorical("class_weight", [None, "balanced"]),
        "random_state": random_state
    }

    # Stratified KFold
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    auc_scores = []

    # Cross Validation Loop
    for fold, (train_idx, valid_idx) in enumerate(skf.split(X, y)):
        X_train = X[train_idx]
        X_valid = X[valid_idx]
        y_train = y.iloc[train_idx]
        y_valid = y.iloc[valid_idx]

        # Model
        model = RidgeClassifier(**params)

        # Train
        model.fit(X_train, y_train)

        # Predict Scores
        preds = model.decision_function(X_valid)

        # ROC AUC
        auc = roc_auc_score(y_valid, preds)
        auc_scores.append(auc)

    # Mean AUC
    mean_auc = np.mean(auc_scores)
    logger.info(
        f"Trial {trial.number} finished | "
        f"Mean AUC: {mean_auc:.5f}"
    )

    return mean_auc
