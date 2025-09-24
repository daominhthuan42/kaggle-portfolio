# 🏦 Bank Customer Churn Prediction 📉

## 📌 Overview

Customer churn is a major challenge in the banking sector.
This project is based on the **Kaggle Playground Series - Season 4, Episode 1** competition, which provides an extended dataset inspired by the **Bank Customer Churn Prediction** dataset.

Competition link: [Playground Series - S4E1 (Kaggle)](https://www.kaggle.com/competitions/playground-series-s4e1)
Related dataset: [Bank Customer Churn Prediction](https://www.kaggle.com/datasets/shubhammeshram579/bank-customer-churn-prediction)

**Goal:** Build a machine learning model to predict whether a customer will **exit the bank** (`Exited` = 1) or **stay** (`Exited` = 0).

## 📂 Dataset Information

**Training set:** 165,034 samples, 13 features + target.
**Test set:** 110,023 samples, 13 features (no target).
**Original dataset:** 10,002 samples.

**Target variable:**

* `Exited` → 1 = customer left, 0 = customer stayed.

### 🔑 Key Features

* **Demographics:** `Geography`, `Gender`, `Age`.
* **Bank Relationship:** `Tenure`, `NumOfProducts`, `IsActiveMember`, `HasCrCard`.
* **Financial:** `CreditScore`, `Balance`, `EstimatedSalary`, `Card Type`, `Points Earned`.
* **Other:** `Complain`, `Satisfaction Score`.
* **IDs:** `RowNumber`, `CustomerId`, `Surname` (not predictive, can be dropped).

## 🎯 Objectives

* Perform **EDA**: explore distributions, detect churn drivers.
* **Feature Engineering**: encode categorical vars, scale numerical, handle imbalances.
* Train models: Logistic Regression, Random Forest, XGBoost, LightGBM, Neural Nets.
* Evaluate with **ROC-AUC, Accuracy, F1-score, Confusion Matrix**.
* Generate Kaggle submissions

## 🛠 Methodology & Tools

* **Data Cleaning:** drop irrelevant columns, handle missing values in original dataset.
* **EDA & Visualization:** Seaborn, Matplotlib for feature impact analysis.
* **Feature Engineering:** encoding, transformations, derived features (age bands, tenure categories).
* **Modeling:** Logistic Regression, Random Forest, XGBoost, LightGBM, MLP.
* **Evaluation:** ROC-AUC, Precision/Recall, F1-score, cross-validation.

## 📊 Key Insights

* **Age, Balance, and Products** strongly correlate with churn.
* Customers in **Germany** churn more compared to France/Spain.
* **Inactive members** are more likely to leave.
* **Higher balance & higher satisfaction score** → lower churn probability.
* **Multiple product holders** sometimes show higher churn → possible cross-sell fatigue.

## 🚀 Next Steps

* Handle **class imbalance** (SMOTE, weighted loss).
* Hyperparameter tuning with Optuna.
* Try **stacking models** for leaderboard improvement.
* Add **business insights** for churn reduction strategies.

## 👤 Author

* **Name:** Đào Minh Thuấn.
* **GitHub:** [daominhthuan42](https://github.com/daominhthuan42)
