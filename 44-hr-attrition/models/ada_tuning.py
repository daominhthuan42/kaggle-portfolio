# adaboost_tuning.py
import logging
import numpy as np
import optuna
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score

def objective_adaboost(
    trial: optuna.Trial,
    X,
    y,
    logger: logging.Logger,
    n_splits: int = 5,
    random_state: int = 42
) -> float:
    """
    Optuna objective function for tuning AdaBoostClassifier
    using Stratified K-Fold cross-validation.

    This function performs cross-validation and returns the
    mean ROC-AUC score across folds.

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
    estimator_max_depth = trial.suggest_int("estimator_max_depth", 1, 5)
    estimator_min_samples_split = trial.suggest_int("estimator_min_samples_split", 2, 20)
    estimator_min_samples_leaf = trial.suggest_int("estimator_min_samples_leaf", 1, 20)

    base_estimator = DecisionTreeClassifier(
        max_depth=estimator_max_depth,
        min_samples_split=estimator_min_samples_split,
        min_samples_leaf=estimator_min_samples_leaf,
        class_weight="balanced",
        random_state=random_state
    )

    params = {
        "estimator": base_estimator,
        "n_estimators": trial.suggest_int("n_estimators", 50, 1000),
        "learning_rate": trial.suggest_float("learning_rate", 0.001, 1.0, log=True),
        "algorithm": trial.suggest_categorical("algorithm", ["SAMME"]),
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
        model = AdaBoostClassifier(**params)

        # Train
        model.fit(X_train, y_train)

        # Predict
        preds = (model.predict_proba(X_valid)[:, 1])

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
