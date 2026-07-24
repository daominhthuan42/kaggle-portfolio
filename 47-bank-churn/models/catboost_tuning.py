# catboost_tuning.py
import logging
import gc
import numpy as np
import pandas as pd
import optuna

from catboost import CatBoostClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold

def objective_catboost(
    trial: optuna.Trial,
    X,
    y,
    cat_features: list[str],
    logger: logging.Logger,
    n_splits: int = 5,
    random_state: int = 42
) -> float:
    """
    Optuna objective function for tuning CatBoostClassifier
    using Stratified K-Fold cross-validation.

    Parameters
    ----------
    trial : optuna.Trial
        Optuna trial used to suggest hyperparameters.

    X : pandas.DataFrame
        Training feature matrix.

    y : pandas.Series
        Binary target:
            0 = Retained
            1 = Exited

    cat_features : list[str]
        List of categorical feature names.

    logger : logging.Logger
        Logger used to record tuning progress.

    n_splits : int, default=5
        Number of folds for Stratified K-Fold cross-validation.

    random_state : int, default=42
        Random seed for reproducibility.

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
    invalid_cat_features = [
        col for col in cat_features if not isinstance(X[col].dtype, pd.CategoricalDtype)
    ]

    if invalid_cat_features:
        raise TypeError(
            f"The following categorical features are not category dtype: "
            f"{invalid_cat_features}"
        )
    
    # Hyperparameter search space
    bootstrap_type = trial.suggest_categorical("bootstrap_type", ["Bayesian", "Bernoulli"])
    params = {
        "iterations": trial.suggest_int("iterations", 1000, 2500),
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.08, log=True),
        "depth": trial.suggest_int("depth", 4, 8),
        "l2_leaf_reg": trial.suggest_float("l2_leaf_reg", 1e-3, 10.0, log=True),
        "random_strength": trial.suggest_float("random_strength", 1e-3, 10.0, log=True),
        "border_count": trial.suggest_int("border_count", 32, 255),
        # Fixed parameters
        "loss_function": "Logloss",
        "eval_metric": "Logloss",
        "auto_class_weights": "Balanced",
        "random_seed": random_state,
        "allow_writing_files": False,
        "verbose": False,
        "thread_count": -1,
        # GPU configuration
        "task_type": "GPU",
        "devices": "0"
    }
    
    # Bootstrap-specific parameters
    if bootstrap_type == "Bayesian":
        params["bootstrap_type"] = "Bayesian"
        params["bagging_temperature"] = trial.suggest_float("bagging_temperature", 0.0, 10.0)
    elif bootstrap_type == "Bernoulli":
        params["bootstrap_type"] = "Bernoulli"
        params["subsample"] = trial.suggest_float("subsample", 0.6, 1.0)
    
    # Stratified K-Fold
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)

    auc_scores = []
    
    # Cross-validation
    for fold, (train_idx, valid_idx) in enumerate(skf.split(X, y), start=1):
        X_train_fold = X.iloc[train_idx]
        X_valid_fold = X.iloc[valid_idx]
        y_train_fold = y.iloc[train_idx]
        y_valid_fold = y.iloc[valid_idx]
        
        # Train model
        model = CatBoostClassifier(**params)

        model.fit(
            X_train_fold,
            y_train_fold,
            cat_features=cat_features,
            eval_set=(X_valid_fold, y_valid_fold),
            early_stopping_rounds=300,
            use_best_model=True,
            verbose=False
        )
        
        # Validation prediction
        y_pred_proba = model.predict_proba(X_valid_fold)[:, 1]
        
        # ROC-AUC
        fold_auc = roc_auc_score(y_valid_fold, y_pred_proba)
        auc_scores.append(fold_auc)
        logger.debug(
            f"Trial {trial.number} | "
            f"Fold {fold}/{n_splits} | "
            f"AUC: {fold_auc:.5f} | "
            f"Best iteration: {model.get_best_iteration()}"
        )

        # Clean memory
        del model
        gc.collect()
    
    # Mean CV ROC-AUC
    mean_auc = float(np.mean(auc_scores))
    std_auc = float(np.std(auc_scores))

    logger.info(
        f"Trial {trial.number} finished | "
        f"Mean AUC: {mean_auc:.5f} | "
        f"Std: {std_auc:.5f}"
    )

    return mean_auc
