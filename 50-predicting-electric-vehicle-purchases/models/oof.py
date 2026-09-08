# oof.py
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.base import clone
from sklearn.metrics import (
    roc_auc_score,
    roc_curve,
    precision_recall_curve,
    average_precision_score,
    confusion_matrix
)
from sklearn.model_selection import StratifiedKFold
from models.lgbm_tunning import lgb
import gc

def _get_n_rows(X):
    return X.shape[0]

def _get_prediction_scores(model, X):
    """
    Return prediction scores for binary classification.
    """
    if hasattr(model, "predict_proba"):
        return model.predict_proba(X)[:, 1]

    return model.decision_function(X)

def _get_best_iteration(model):
    """
    Return the best iteration from a trained boosting model.

    Supports:
    - CatBoost
    - LightGBM
    - XGBoost
    """

    # CatBoost
    if hasattr(model, "get_best_iteration"):
        return model.get_best_iteration()

    # LightGBM
    if hasattr(model, "best_iteration_"):
        return model.best_iteration_

    # XGBoost
    if hasattr(model, "best_iteration"):
        return model.best_iteration

    return None

def run_oof(
    model,
    X,
    y,
    X_val,
    y_val,
    cat_features,
    logger: logging.Logger,
    n_splits: int = 5,
    threshold: float = 0.5,
    random_state: int = 42
):
    """
    Perform Out-of-Fold (OOF) training using Stratified K-Fold
    cross-validation for CatBoost.

    The function:
    - Generates OOF predictions for the training dataset
    - Generates averaged predictions for the external validation dataset
    - Calculates ROC-AUC and Average Precision across folds
    - Calculates averaged feature importance across folds
    - Visualizes ROC, Precision-Recall, and Confusion Matrices
    - Releases fold models after each fold to reduce memory usage

    Parameters
    ----------
    model : estimator
        CatBoost-compatible classification model.

    X : pandas.DataFrame
        Training feature matrix.

    y : pandas.Series
        Training target labels.

    X_val : pandas.DataFrame
        External validation feature matrix.

    y_val : pandas.Series
        External validation target labels.

    cat_features : list[str]
        List of categorical feature names.

    logger : logging.Logger
        Logger instance used to record training progress.

    n_splits : int, default=5
        Number of folds used in StratifiedKFold.

    threshold : float, default=0.5
        Classification probability threshold.

    random_state : int, default=42
        Random seed for reproducibility.

    Returns
    -------
    dict
        Dictionary containing OOF predictions, validation predictions,
        fold metrics, and averaged feature importance.
    """

    logger.info("=" * 80)
    logger.info(f"Starting OOF training with {model.__class__.__name__}")
    logger.info(
        f"Training samples: {len(X):,} | "
        f"Validation samples: {len(X_val):,} | "
        f"Features: {X.shape[1]} | "
        f"Categorical features: {len(cat_features)} | "
        f"CV Folds: {n_splits}"
    )
    
    # Stratified K-Fold
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    
    # Prediction containers    
    oof_pred = np.zeros(_get_n_rows(X))
    val_pred = np.zeros(_get_n_rows(X_val))
    
    # Metric containers
    fold_auc = []
    roc_curves = []
    pr_curves = []
    ap_values = []

    # Store feature importance from each fold
    fold_feature_importances = []
    
    # Cross-validation    
    for fold, (train_idx, valid_idx) in enumerate(skf.split(X, y), 1):
        logger.info("-" * 80)
        logger.info(f"Starting Fold {fold}/{n_splits}")
        
        # Split fold data        
        X_train = X.iloc[train_idx]
        X_valid = X.iloc[valid_idx]

        y_train = y.iloc[train_idx]
        y_valid = y.iloc[valid_idx]

        logger.debug(
            f"Fold {fold} | "
            f"Train samples: {len(X_train):,} | "
            f"Validation samples: {len(X_valid):,}"
        )
        
        # Clone model to keep each fold independent
        model_fold = clone(model)
        
        # Train CatBoost
        if model_fold.__class__.__name__ == "CatBoostClassifier":
            model_fold.fit(
                X_train,
                y_train,
                cat_features=cat_features,
                eval_set=(X_valid, y_valid),
                early_stopping_rounds=300,
                verbose=False
            )
        elif model_fold.__class__.__name__ == "LGBMClassifier":
            model_fold.fit(
                X_train,
                y_train,
                categorical_feature=cat_features,
                eval_set=[(X_val, y_val)],
                callbacks=[
                    lgb.early_stopping(
                        stopping_rounds=300,
                        verbose=False
                    ),
                    lgb.log_evaluation(500)
                ]
            )
        elif model_fold.__class__.__name__ == "XGBClassifier":
            model_fold.fit(
                X_train,
                y_train,
                eval_set=[
                    (X_train, y_train),
                    (X_val, y_val)
                ],
                verbose=False
            )

        logger.info(
            f"Fold {fold} training completed | "
            f"Best iteration: {_get_best_iteration(model_fold)}"
        )
        
        # OOF prediction        
        fold_pred = _get_prediction_scores(model=model_fold, X=X_valid)
        oof_pred[valid_idx] = fold_pred
        
        # External validation prediction
        # Average predictions across folds
        val_pred += (_get_prediction_scores(model=model_fold, X=X_val) / n_splits)
        
        # Fold ROC-AUC
        auc_fold = roc_auc_score(y_valid, fold_pred)
        fold_auc.append(auc_fold)
        logger.info(f"Fold {fold} AUC: {auc_fold:.5f}")
        
        # ROC Curve
        fpr, tpr, _ = roc_curve(y_valid, fold_pred)
        roc_curves.append((fpr, tpr))
        
        # Precision-Recall Curve
        precision, recall, _ = precision_recall_curve(y_valid, fold_pred)
        pr_curves.append((recall, precision))
        
        # Average Precision
        ap = average_precision_score(y_valid, fold_pred)
        ap_values.append(ap)
        
        # Feature Importance
        try:
            if model.__class__.__name__ == "CatBoostClassifier":
                feature_importance = model_fold.get_feature_importance()
            else:
                feature_importance = model_fold.feature_importances_
        except:
            pass

        fold_importance = pd.DataFrame({
            "feature": X.columns,
            "importance": feature_importance,
            "fold": fold
        })
        fold_feature_importances.append(fold_importance)
        logger.debug(f"Fold {fold} feature importance collected successfully")
        
        # Release temporary fold objects
        del model_fold
        del X_train, X_valid
        del y_train, y_valid
        del fold_pred
        del feature_importance
        del fold_importance

        gc.collect()
        logger.debug(f"Fold {fold} temporary memory released")
    
    # Final OOF Evaluation    
    oof_auc = roc_auc_score(y, oof_pred)
    mean_auc = np.mean(fold_auc)
    std_auc = np.std(fold_auc)
    logger.info("=" * 80)
    logger.info("OOF training completed")
    logger.info(f"OOF AUC: {oof_auc:.5f}")
    logger.info(f"Mean Fold AUC: {mean_auc:.5f} +/- {std_auc:.5f}")
    
    # Aggregate Feature Importance    
    feature_importance_all = pd.concat(fold_feature_importances, ignore_index=True)
    feature_importance = (
        feature_importance_all
        .groupby("feature", as_index=False)
        .agg(
            importance_mean=("importance", "mean"),
            importance_std=("importance", "std")
        )
        .reset_index(drop=True)
    )

    logger.info("Feature importance successfully aggregated across folds")
    logger.info(
        "\nTop 10 Feature Importance:\n"
        f"{feature_importance.head(10).to_string(index=False)}"
    )

    # Raw fold-level importance is no longer needed
    del feature_importance_all
    del fold_feature_importances

    gc.collect()
    
    # Visualization    
    fig, axes = plt.subplots(2, 2, figsize=(16, 14))
    
    # ROC Curve    
    ax = axes[0, 0]
    for i, (fpr, tpr) in enumerate(roc_curves):
        ax.plot(fpr, tpr, label=f"Fold {i + 1} AUC = {fold_auc[i]:.4f}")
    ax.plot([0, 1], [0, 1], "--", color="gray")
    ax.set_title("ROC Curve (Each Fold)", weight="bold", pad=15, fontsize=12)
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.legend()
    ax.grid(True)
    
    # Precision-Recall Curve    
    ax = axes[0, 1]
    for i, (recall, precision) in enumerate(pr_curves):
        ax.plot(recall, precision, label=f"Fold {i + 1} AP = {ap_values[i]:.4f}")
    ax.set_title("Precision-Recall Curve (Each Fold)", weight="bold", pad=15, fontsize=12)
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.legend()
    ax.grid(True)
    
    # OOF Confusion Matrix    
    ax = axes[1, 0]
    y_pred_label = (oof_pred >= threshold).astype(int)
    cm = confusion_matrix(y, y_pred_label)
    sns.heatmap(cm, annot=True, fmt="d", cmap="Greens", ax=ax)
    ax.set_title(f"OOF Confusion Matrix (Threshold = {threshold})", weight="bold", pad=15, fontsize=12)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("True")
    
    # External Validation Confusion Matrix    
    ax = axes[1, 1]
    y_val_label = (val_pred >= threshold).astype(int)
    cm_val = confusion_matrix(y_val, y_val_label)
    sns.heatmap(cm_val, annot=True, fmt="d", cmap="Greens", ax=ax)
    ax.set_title(f"Validation Confusion Matrix (Threshold = {threshold})", weight="bold", pad=15, fontsize=12)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("True")
    plt.tight_layout()
    plt.show()
    
    # Return Results    
    return {
        "oof_pred": oof_pred,
        "val_pred": val_pred,
        "fold_auc": fold_auc,
        "mean_auc": mean_auc,
        "std_auc": std_auc,
        "oof_auc": oof_auc,
        "feature_importance": feature_importance
    }

def run_oof_v2(
    model,
    X,
    y,
    X_val=None,
    y_val=None,
    X_test=None,
    logger: logging.Logger = None,
    n_splits: int = 5,
    threshold: float = 0.5,
    random_state: int = 42
):
    """
    Perform Out-of-Fold (OOF) training using Stratified K-Fold
    cross-validation.

    This function:
    - Generates OOF predictions for training data
    - Evaluates optional validation dataset
    - Generates predictions for unseen test dataset
    - Visualizes ROC, PR Curve, Confusion Matrix,
      and prediction distributions

    Parameters
    ----------
    model : estimator
        Scikit-learn compatible model.

    X : array-like
        Training feature matrix.

    y : array-like
        Training target labels.

    X_val : array-like, optional
        Validation feature matrix.

    y_val : array-like, optional
        Validation target labels.

    X_test : array-like, optional
        Unseen test feature matrix.

    logger : logging.Logger, optional
        Logger instance.

    n_splits : int, default=5
        Number of folds for Stratified K-Fold.

    threshold : float, default=0.5
        Probability threshold for classification.

    random_state : int, default=42
        Random seed used for reproducible
        Stratified K-Fold splitting.

    Returns
    -------
    dict
        Dictionary containing:
        - oof_pred
        - val_pred
        - test_pred
        - fold_auc
        - fold_models
    """

    # Logger
    if logger is None:
        logger = logging.getLogger(__name__)
    logger.info(f"Starting OOF training with {model.__class__.__name__}")

    # Stratified KFold
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)

    # Prediction Containers
    oof_pred = np.zeros(_get_n_rows(X))
    val_pred = (np.zeros(_get_n_rows(X_val)) if X_val is not None else None)
    test_pred = (np.zeros(_get_n_rows(X_test)) if X_test is not None else None)

    # Store Results
    fold_models = []
    fold_auc = []
    roc_curves = []
    pr_curves = []
    ap_values = []

    # Cross Validation Loop
    for fold, (train_idx, valid_idx) in enumerate(skf.split(X, y), 1):
        logger.info(f"Fold {fold}/{n_splits}")

        # Split Data
        X_train = X[train_idx]
        X_valid = X[valid_idx]
        y_train = y[train_idx]
        y_valid = y[valid_idx]

        # Clone Model
        model_fold = clone(model)

        # Train
        model_fold.fit(X_train, y_train)
        fold_models.append(model_fold)

        # Validation Prediction
        fold_pred = _get_prediction_scores(model=model_fold, X=X_valid)
        oof_pred[valid_idx] = fold_pred

        # External Validation Prediction 
        if X_val is not None:
            val_pred += (_get_prediction_scores(model=model_fold, X=X_val) / n_splits)

        # Unseen Test Prediction
        if X_test is not None:
            test_pred += (_get_prediction_scores(model=model_fold, X=X_test) / n_splits)

        # Fold AUC
        auc_fold = roc_auc_score(y_valid, fold_pred)
        fold_auc.append(auc_fold)
        logger.info(f"Fold {fold} AUC: {auc_fold:.5f}")

        # ROC Curve
        fpr, tpr, _ = roc_curve(y_valid, fold_pred)
        roc_curves.append((fpr, tpr))

        # Precision Recall Curve
        precision, recall, _ = precision_recall_curve(y_valid, fold_pred)
        pr_curves.append((recall, precision))

        # Average Precision
        ap = average_precision_score(y_valid, fold_pred)
        ap_values.append(ap)

    # Final OOF Score
    oof_auc = roc_auc_score(y, oof_pred)
    logger.info("OOF training completed")
    logger.info(f"OOF AUC: {oof_auc:.5f}")
    logger.info(f"Fold AUCs: {fold_auc}")

    # Visualization
    fig, axes = plt.subplots(3, 2, figsize=(16, 20))

    # ROC Curve
    ax = axes[0, 0]
    for i, (fpr, tpr) in enumerate(roc_curves):
        ax.plot(fpr, tpr, label=f"Fold {i+1}: AUC = {fold_auc[i]:.4f}")
    ax.plot([0, 1], [0, 1], "--", color="gray")
    ax.set_title("ROC Curve (Each Fold)", weight="bold", fontsize=12, pad=15)
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.legend()
    ax.grid(True)

    # Precision Recall Curve
    ax = axes[0, 1]
    for i, (recall, precision) in enumerate(pr_curves):
        ax.plot(recall, precision, label=f"Fold {i+1}: AP = {ap_values[i]:.4f}")
    ax.set_title("Precision-Recall Curve", weight="bold", fontsize=12, pad=15)
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.legend()
    ax.grid(True)

    # Train Confusion Matrix
    ax = axes[1, 0]
    y_pred_label = (oof_pred >= threshold).astype(int)
    cm = confusion_matrix(y, y_pred_label)
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
    ax.set_title(f"Train Confusion Matrix (Threshold={threshold})", weight="bold",fontsize=12, pad=15)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("True")

    # Validation Confusion Matrix
    ax = axes[1, 1]
    if X_val is not None and y_val is not None:
        y_val_label = (val_pred >= threshold).astype(int)
        cm = confusion_matrix(y_val, y_val_label)
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
        ax.set_title(f"Validation Confusion Matrix (Threshold={threshold})", weight="bold", fontsize=12, pad=15)
        ax.set_xlabel("Predicted")
        ax.set_ylabel("True")
    else:
        ax.axis("off")

    # Test Prediction Distribution
    ax = axes[2, 0]
    if X_test is not None and test_pred is not None:
        sns.histplot(test_pred, bins=30, kde=True, color="#4C72B0", ax=ax)
        # threshold line
        ax.axvline(threshold, color="red", linestyle="--", label=f"Threshold = {threshold}")
        # mean probability line
        ax.axvline(test_pred.mean(), color="green", linestyle="--", label=f"Mean Prob = {test_pred.mean():.3f}")
        ax.set_title("Test Prediction Probability Distribution", weight="bold", fontsize=12, pad=15)
        ax.set_xlabel("Predicted Probability")
        ax.set_ylabel("Frequency")
        ax.legend()
        pred_ratio = ((test_pred >= threshold).mean())
        logger.info(f"Predicted positive ratio on test set: {pred_ratio:.4f}")
    else:
        ax.axis("off")

    # Test Predicted Class Distribution
    ax = axes[2, 1]
    if X_test is not None and test_pred is not None:
        predicted_labels = (test_pred >= threshold).astype(int)
        sns.countplot(x=predicted_labels, ax=ax)
        ax.set_title("Test Predicted Class Distribution", weight="bold", fontsize=12, pad=15)
        ax.set_xlabel("Predicted Class")
        ax.set_ylabel("Count")
        ax.set_xticklabels(["Stayed (0)", "Left (1)"])

        # Add value labels on bars
        for p in ax.patches:
            height = int(p.get_height())
            ax.annotate(
                f"{height:,}",
                (
                    p.get_x() + p.get_width() / 2,
                    height
                ),
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold",
                xytext=(0, 5),
                textcoords="offset points"
            )
    else:
        ax.axis("off")
    # Final Layout
    plt.tight_layout()
    plt.show()

    # Return Results
    return {
        "oof_pred": oof_pred,
        "val_pred": val_pred,
        "test_pred": test_pred,
        "fold_auc": fold_auc,
        "fold_models": fold_models
    }
