# linearsvc_tuning.py
import logging
import numpy as np
import optuna
from sklearn.svm import LinearSVC
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score

def objective_linearsvc(
    trial: optuna.Trial,
    X,
    y,
    logger: logging.Logger,
    n_splits: int = 5,
    random_state: int = 42
) -> float:
    """
    Optuna objective function for tuning LinearSVC
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
        "C": trial.suggest_float("C", 1e-5, 1e3, log=True),
        "penalty": trial.suggest_categorical("penalty", ["l1", "l2"]),
        "loss": trial.suggest_categorical("loss", ["hinge", "squared_hinge"]),
        "class_weight": trial.suggest_categorical("class_weight", [None, "balanced"]),
        "max_iter": trial.suggest_int("max_iter", 1000, 10000),
        "random_state": random_state
    }

    # l1 only supports squared_hinge
    if params["penalty"] == "l1":
        params["loss"] = "squared_hinge"
        params["dual"] = False
    # l2 supports multiple configs
    else:
        # l2 + hinge -> dual must be True
        if params["loss"] == "hinge":
            params["dual"] = True
        # l2 + squared_hinge
        else:
            params["dual"] = trial.suggest_categorical("dual", [True, False])

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
        model = LinearSVC(**params)

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
