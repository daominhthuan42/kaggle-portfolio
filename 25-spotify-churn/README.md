# 🎵 Spotify Churn Analysis 📉

## 📌 Overview

This project analyzes **Spotify user behavior and engagement patterns** to predict **customer churn** (service dropout).
The dataset includes demographic information, engagement metrics (listening time, songs per day, skip rate), subscription type, and device usage.

Dataset link: [Spotify Dataset for Churn Analysis (Kaggle)](https://www.kaggle.com/datasets/nabihazahid/spotify-dataset-for-churn-analysis).

**Goals:**

* Explore key factors driving **churn behavior**.
* Train machine learning models to predict **`is_churned`** (0 = active, 1 = churned).
* Provide actionable insights for **retention, marketing,** and **product experience** improvement.

## 📂 Dataset Information

**Size:** 8,000 records, **12 columns**.
The cleaned dataset contains **no missing or duplicate values**.
**Churn rate:** Active ≈ **74.1% (5,929)**, Churned ≈ **25.9% (2,071)** → **moderate imbalance**.

**Target variable:**

* `is_churned` → binary classification: **0 (Active)** / **1 (Churned)**.

### 🔑 Key Features

| Feature                 | Description                                      |
| ----------------------- | ------------------------------------------------ |
| `user_id`               | Unique user identifier (not used for modeling)   |
| `gender`                | Gender (Male / Female / Other)                   |
| `age`                   | User’s age                                       |
| `country`               | Country or region                                |
| `subscription_type`     | Plan type (Free, Premium, Family, Student, etc.) |
| `listening_time`        | Total minutes listened per day                   |
| `songs_played_per_day`  | Average number of songs played daily             |
| `skip_rate`             | Proportion of skipped tracks                     |
| `device_type`           | Device used (Desktop / Mobile / Web, etc.)       |
| `ads_listened_per_week` | Number of ads listened per week (for Free users) |
| `offline_listening`     | Whether the user listens offline (1/0)           |
| `is_churned`            | Target label (0 = Active / 1 = Churned)          |

> EDA note: numeric variables are well-distributed, **no multicollinearity**, but `ads_listened_per_week` shows strong right-skewness.

## 🎯 Objectives

* Perform **EDA**: distribution, outliers, and correlation analyses; churn patterns by feature groups.
* **Feature Engineering**: encode categorical variables, normalize skewed monetary features, derive engagement ratios (e.g., session intensity).
* **Modeling**:

  * Logistic Regression, Random Forest, XGBoost; optional ensemble comparison.
* **Evaluation**: Stratified cross-validation with **ROC-AUC**, **F1**, and **Confusion Matrix** metrics; focus on churn class performance.

## 🛠 Methodology & Tools

* **Data Quality:** No missing or duplicate rows; outliers inspected (especially `ads_listened_per_week`).
* **EDA & Visualization:** Histograms, boxplots, correlation heatmaps; churn group comparison via **Chi-Square** (categorical) and **T-Test/Welch/Kruskal** (numerical).
* **Modeling Pipeline:** scikit-learn pipeline (impute → encode → scale → model); compare model families under stratified CV.
* **Explainability:** Apply **SHAP** for feature importance and interpretability.

## 📊 Key Insights

* **Class Imbalance:** Active ~74%, Churned ~26% → use **stratification**, **class weighting**, or **threshold tuning** to optimize F1 for churn prediction.
* **Numerical:** Variables such as `age`, `listening_time`, `songs_played_per_day` show **no statistically significant difference** between churned and active users; `ads_listened_per_week` is highly skewed but not strongly discriminative (Mann-Whitney U insignificant).
* **Categorical:** `offline_listening`, `gender`, `country`, `subscription_type`, and `device_type` show **no strong statistical association** with churn (Chi-Square p ≥ 0.05).
* **Correlation:** All numerical features are **nearly independent** (|r| < 0.05), minimizing multicollinearity risk.

> Note: The dataset is **synthetic** and designed for educational EDA and ML churn modeling purposes.

## 🚀 Next Steps

* Address **class imbalance** using weights, focal loss, or threshold optimization; report **PR-AUC**.
* Enhance features: create **activity ratios** (songs/time), **consistency measures** (daily variance), **skip bursts**, and interactions (`plan × offline`).
* Test **advanced models** (LightGBM/XGBoost + Optuna) with **probability calibration** (Platt/Isotonic).
* Add **RFM-style segmentation** (Recency, Frequency, Minutes listened).
* Implement **SHAP explainability** and define business rules for **marketing triggers**.

## 👤 Author

* **Name:** Đào Minh Thuấn
* **GitHub:** [daominhthuan42](https://github.com/daominhthuan42)
