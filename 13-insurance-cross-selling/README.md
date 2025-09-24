# 📑 Insurance Cross-Sell Prediction 🤝

## 📌 Overview

This project is based on the **Kaggle Playground Series - Season 4, Episode 7** competition.
The dataset simulates a business case where an insurance company wants to predict whether a customer will be interested in purchasing **vehicle insurance** as a **cross-sell** offer.

Competition link: [Playground Series - S4E7 (Kaggle)](https://www.kaggle.com/competitions/playground-series-s4e7)
Related dataset: [Health Insurance Cross-Sell Prediction](https://www.kaggle.com/datasets/annantkumarsingh/health-insurance-cross-sell-prediction-data)

**Goal:** Build a **binary classification model** to predict if a customer will respond positively (`1`) or negatively (`0`) to the insurance cross-sell offer.

## 📂 Dataset Information

**Training set:** 11,504,798 samples (with target `Response`).
**Test set:** 7,669,866 samples (without target).
**Original dataset:** 381,109 samples.

**Target variable:**

* `Response` → 1 = Interested, 0 = Not interested.

### 🔑 Key Features

* **Demographics:** `Gender`, `Age`, `Driving_License`.
* **Region:** `Region_Code` (encoded location).
* **Insurance History:** `Previously_Insured` (whether the customer already has vehicle insurance).
* **Vehicle Info:** `Vehicle_Age`, `Vehicle_Damage`.
* **Policy Info:** `Annual_Premium`, `Policy_Sales_Channel`, `Vintage` (days associated with company).
* **ID column:** `id` (unique identifier, not used for modeling).

## 🎯 Objectives

* Perform **EDA**: distributions, patterns, categorical balances.
* **Feature Engineering**: encode categoricals, scale numeric, derive new ratios (e.g., premium per vintage).
* Train classification models: Logistic Regression, Random Forest, Gradient Boosting (XGBoost, LightGBM, CatBoost).
* Evaluate with **ROC-AUC, Accuracy, F1-score**.
* Generate predictions for Kaggle submission.

## 🛠 Methodology & Tools

* **Data Cleaning:** drop irrelevant `id`, handle outliers in premium.
* **EDA & Visualization:** Seaborn, Matplotlib.
* **Feature Engineering:** One-Hot Encoding, scaling, derived features.
* **Modeling:** Logistic Regression, Random Forest, XGBoost, LightGBM, CatBoost.
* **Evaluation:** Cross-validation, ROC-AUC, Confusion Matrix.

## 📊 Key Insights

* Customers with **`Vehicle_Damage = Yes`** are more likely to buy vehicle insurance.
* Customers who are **not previously insured** (`Previously_Insured = 0`) are primary targets.
* **Age** and **Vintage** correlate with interest level.
* **Annual\_Premium** has extreme outliers and requires scaling/log transformation.
* **Policy\_Sales\_Channel** shows variation, some channels outperform others.

## 🚀 Next Steps

* Handle class imbalance with **SMOTE** or class weights.
* Hyperparameter tuning with **Optuna**.
* Build ensemble/stacking models for leaderboard improvement.
* Create **business insights** for marketing campaign targeting.

## 👤 Author

* **Name:** Đào Minh Thuấn.
* **GitHub:** [daominhthuan42](https://github.com/daominhthuan42)
