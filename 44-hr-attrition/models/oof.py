# oof.py
import logging
import numpy as np
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

def _get_n_rows(X):
    return X.shape[0]

def _get_prediction_scores(model, X):
    """
    Return prediction scores for binary classification.

    Uses:
    - predict_proba if available
    - otherwise decision_function

    Parameters
    ----------
    model : estimator
        Trained sklearn-compatible model.

    X : array-like
        Feature matrix.

    Returns
    -------
    np.ndarray
        Prediction scores.
    """

    if hasattr(model, "predict_proba"):
        return model.predict_proba(X)[:, 1]
    return model.decision_function(X)

def run_oof(model, X, y, X_val, y_val, 
            logger: logging.Logger, n_splits=5, threshold =0.5):
    """
    Perform Out-of-Fold (OOF) training using Stratified K-Fold cross-validation.

    This function trains a model across multiple folds, generates out-of-fold
    predictions for the training data, and averaged predictions for the test set.
    It also computes fold-level evaluation metrics and visualizes ROC curves,
    Precision–Recall curves, and a confusion matrix based on OOF predictions.

    Parameters
    ----------
    model : estimator
        A machine learning model compatible with scikit-learn API that supports
        `fit()` and `predict_proba()`.

    X : array-like of shape (n_samples, n_features)
        Training feature matrix.

    y : array-like of shape (n_samples,)
        Target labels for training data.

    X_val : array-like of shape (n_test_samples, n_features)
        Test feature matrix used to generate averaged predictions across folds.

    y_val : array-like of shape (n_test_samples,)
        Target labels for test data.

    logger : logging.Logger
        Logger instance used to record training progress and evaluation metrics.

    n_splits : int, default=5
        Number of folds used in StratifiedKFold cross-validation.

    threshold : float, default=0.5
        Decision threshold applied to OOF predicted probabilities to convert them
        into binary class labels for computing the confusion matrix.

    Returns
    -------
    oof_pred : np.ndarray of shape (n_samples,)
        Out-of-fold predicted probabilities for the training set.

    test_pred : np.ndarray of shape (n_test_samples,)
        Averaged predicted probabilities for the test set across all folds.

    fold_auc : list
    List containing the value auc from each fold.

    fold_models : list
        List containing the trained model from each fold.
    """

    logger.info(f"Starting OOF training with {model.__class__.__name__}")

    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

    # store predictions
    oof_pred = np.zeros(_get_n_rows(X))
    test_pred = np.zeros(_get_n_rows(X_val))

    fold_models = []
    fold_auc = []

    # for visualization
    roc_curves = []
    pr_curves = []
    ap_values = []

    for fold, (train_idx, valid_idx) in enumerate(skf.split(X, y), 1):

        logger.info(f"Fold {fold}/{n_splits}")

        # split data
        X_train, X_valid = X[train_idx], X[valid_idx]
        y_train, y_valid = y[train_idx], y[valid_idx]

        # clone model to avoid overwriting previous folds
        model_fold = clone(model)

        # train model
        model_fold.fit(X_train, y_train)

        fold_models.append(model_fold)

        # predict validation set
        fold_pred = _get_prediction_scores(model=model_fold, X=X_valid)
        oof_pred[valid_idx] = fold_pred

        # accumulate test predictions
        test_pred += _get_prediction_scores(model=model_fold, X=X_val) / n_splits

        # compute AUC
        auc_fold = roc_auc_score(y_valid, fold_pred)
        fold_auc.append(auc_fold)

        logger.info(f"Fold {fold} AUC: {auc_fold:.5f}")

        # ROC curve
        fpr, tpr, _ = roc_curve(y_valid, fold_pred)
        roc_curves.append((fpr, tpr))

        # Precision–Recall curve
        precision, recall, _ = precision_recall_curve(y_valid, fold_pred)
        pr_curves.append((recall, precision))

        # Average Precision
        ap = average_precision_score(y_valid, fold_pred)
        ap_values.append(ap)

    # final OOF AUC
    oof_auc = roc_auc_score(y, oof_pred)

    logger.info("OOF training completed")
    logger.info(f"OOF AUC: {oof_auc:.5f}")
    logger.info(f"Fold AUCs: {fold_auc}")

    # ================= Visualization =================

    fig, axes = plt.subplots(2, 2, figsize=(16, 14))

    # ROC Curve
    ax = axes[0, 0]

    for i, (fpr, tpr) in enumerate(roc_curves):
        ax.plot(fpr, tpr, label=f"Fold {i+1} AUC = {fold_auc[i]:.4f}")

    ax.plot([0, 1], [0, 1], "--", color="gray")

    ax.set_title("ROC Curve (Each Fold)", weight="bold", pad=15, fontsize=12)
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")

    ax.legend()
    ax.grid(True)

    # Precision Recall Curve
    ax = axes[0, 1]

    for i, (recall, precision) in enumerate(pr_curves):
        ax.plot(recall, precision, label=f"Fold {i+1} AP = {ap_values[i]:.4f}")

    ax.set_title("Precision–Recall Curve (Each Fold)", weight="bold", pad=15, fontsize=12)
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.legend()
    ax.grid(True)

    # Confusion Matrix
    ax = axes[1, 0]
    y_pred_label = (oof_pred >= threshold).astype(int)
    cm = confusion_matrix(y, y_pred_label)
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
    ax.set_title(f"Confusion Matrix (Threshold = {threshold} - Train Set)", weight="bold", pad=15, fontsize=12)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("True")

    # Confusion Matrix
    ax = axes[1, 1]
    y_val_label = (test_pred >= threshold).astype(int)
    cm = confusion_matrix(y_val, y_val_label)
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
    ax.set_title(f"Confusion Matrix (Threshold = {threshold}) - Test Set", weight="bold", pad=15, fontsize=12)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("True")
    plt.tight_layout()
    plt.show()

    return oof_pred, test_pred, fold_auc, fold_models

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
