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

def run_oof(model, X, y, X_test, y_test, logger: logging.Logger, n_splits=5, threshold =0.5):
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

    X_test : array-like of shape (n_test_samples, n_features)
        Test feature matrix used to generate averaged predictions across folds.

    y_test : array-like of shape (n_test_samples,)
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
    test_pred = np.zeros(_get_n_rows(X_test))

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
        fold_pred = model_fold.predict_proba(X_valid)[:, 1]

        oof_pred[valid_idx] = fold_pred

        # accumulate test predictions
        test_pred += model_fold.predict_proba(X_test)[:, 1] / n_splits

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
    y_test_label = (test_pred >= threshold).astype(int)
    cm = confusion_matrix(y_test, y_test_label)
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
    ax.set_title(f"Confusion Matrix (Threshold = {threshold}) - Test Set", weight="bold", pad=15, fontsize=12)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("True")
    plt.tight_layout()
    plt.show()

    return oof_pred, test_pred, fold_auc, fold_models
