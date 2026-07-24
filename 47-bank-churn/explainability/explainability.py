# explainability.py
import logging
from typing import List, Optional
import shap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def shap_compare_models(
    models: List,
    X_test,
    logger: logging.Logger,
    feature_names: List[str],
    model_names: Optional[List[str]] = None,
    sample_size: int = 1000,
) -> None:
    """
    Compute and compare SHAP feature importance for multiple models.

    The function generates a subplot (1 row × N columns) showing
    SHAP feature importance for each model.

    Parameters
    ----------
    models : List
        List of trained models supporting `predict_proba`.
    X_test : array-like or sparse matrix
        Test feature matrix.
    logger : logging.Logger
        Logger used for reporting progress.
    feature_names : List[str]
        Feature names corresponding to X_test columns.
    model_names : List[str], optional
        Names of the models for plot titles.
    sample_size : int, default=1000
        Number of rows sampled from X_test to compute SHAP.

    Returns
    -------
    None
    """

    logger.info("Starting SHAP comparison across models")

    if hasattr(X_test, "toarray"):
        logger.debug("Converting sparse matrix to dense")
        X_test = X_test.toarray()

    X_df = pd.DataFrame(X_test, columns=feature_names)

    sample_size = min(sample_size, len(X_df))

    if len(X_df) > sample_size:
        logger.info(f"Sampling {sample_size} rows for SHAP computation")
        X_df = X_df.sample(sample_size, random_state=42)

    n_models = len(models)
    name_model = []
    if model_names is None:
        for model in models:
            name_model.append(getattr(model, "name", model.__class__.__name__))

    fig, axes = plt.subplots(1, n_models, figsize=(6 * n_models, 8))

    if n_models == 1:
        axes = [axes]

    importance_results = []

    for i, model in enumerate(models):

        logger.info(f"Computing SHAP values for {name_model[i]}")

        explainer = shap.Explainer(model.predict_proba, X_df)
        shap_values = explainer(X_df)

        values = shap_values.values

        # classification output shape handling
        if values.ndim == 3:
            values = values[:, :, 1]

        shap_importance = np.abs(values).mean(axis=0)

        shap_df = (
            pd.DataFrame(
                {
                    "feature": feature_names,
                    "importance": shap_importance,
                }
            )
            .sort_values("importance", ascending=False)
            .head(20)
        )
        logger.info("\n%s", shap_df)
        logger.info("*" * 80)

        sns.barplot(
            data=shap_df,
            x="importance",
            y="feature",
            ax=axes[i],
            palette="viridis"
        )

        axes[i].set_title(name_model[i], fontsize=12, weight="bold", pad=15)
        axes[i].set_xlabel("mean(|SHAP value|)")
        axes[i].set_ylabel("")

    plt.tight_layout()
    plt.show()

    logger.info("SHAP comparison completed")
