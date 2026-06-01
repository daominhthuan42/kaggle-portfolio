# benchmark.py
import pandas as pd
import seaborn as sns
import logging
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score

def benchmark_models(models, X, y, logger: logging.Logger,
                              metric: str = "roc_auc",
                              cv=None,
                              plot_result: bool = False) -> None:
    """
    Evaluate multiple machine learning models using cross-validation
    and return a summary comparison of their performance.

    This function is typically used in the *model benchmarking stage*
    to identify strong candidate models before hyperparameter tuning.

    Parameters
    ----------
    models : list
        List of initialized model objects (e.g., sklearn estimators).

    X : array-like or pandas.DataFrame
        Feature matrix.

    y : array-like or pandas.Series
        Target variable.

    logger : logging.Logger
        Logger used to record processing steps.

    metric : str, default="roc_auc"
        Scoring metric used in cross-validation (must be compatible with sklearn scoring).

    cv : cross-validation generator
        Cross-validation strategy (e.g., KFold, StratifiedKFold).

    plot_result : bool, default=False
        If True, visualize model performance using a bar plot with standard deviation.

    Returns
    -------
    None
    """

    logger.info("Starting model benchmarking using cross-validation")

    entries = []

    for model in models:
        model_name = getattr(model, "name", model.__class__.__name__)
        logger.info(f"Evaluating model: {model_name}")
        try:
            scores = cross_val_score(model, X, y, scoring=metric, cv=cv, n_jobs=-1)
            logger.info(f"{model_name} | mean={scores.mean():.4f} | std={scores.std():.4f}")

            for fold_idx, s in enumerate(scores, start=1):
                entries.append((model_name, fold_idx, s))
        except Exception as e:
            logger.exception(f"Model {model_name} failed during evaluation")
            continue
        logger.info("*" * 80)

    cv_df = pd.DataFrame(entries, columns=["model_name", "fold_id", "score"])

    summary = (cv_df.groupby("model_name")["score"]
                    .agg(Mean="mean", Std="std", N="size")
                    .sort_values("Mean", ascending=False))

    logger.info("Benchmarking completed")
    logger.info("\n%s", summary)

    if plot_result:
        order = summary.index.tolist()
        plt.figure(figsize=(18, 8))
        sns.barplot(data=cv_df, x="model_name", y="score", order=order, errorbar=("sd"), palette="viridis")
        title_metric = metric.upper() if isinstance(metric, str) else "Score"
        nfolds = getattr(cv, "n_splits", "CV")
        plt.title(f"Baseline {title_metric} using {nfolds}-fold cross-validation", fontsize=14, weight="bold", pad=20)
        plt.xlabel("Model")
        plt.ylabel(title_metric)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
