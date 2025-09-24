# 🛡️ Insurance Premium Prediction 🧮

## 📌 Overview

This project is part of the **Kaggle Playground Series (S4E12)**.
The dataset is synthetically generated but designed to mimic **real-world insurance data**, including demographics, lifestyle, financial, and policy-related variables.

Competition link: [Playground Series - S4E12 (Kaggle)](https://www.kaggle.com/competitions/playground-series-s4e12)

**Goal:** Build a machine learning regression model to predict the **Premium Amount** an individual is charged.

## 📂 Dataset Information

**Training set:** 1,200,000 records, 21 features (including target).
**Test set:** 800,000 records, 20 features (no target).
**Target variable:**

* `Premium_Amount` → Insurance premium to be predicted.

### 🔑 Key Features

* **Demographics:** `Age`, `Gender`, `Marital_Status`, `Number_of_Dependents`, `Education_Level`, `Occupation`.
* **Health & Lifestyle:** `Health_Score`, `Smoking_Status`, `Exercise_Frequency`.
* **Financial:** `Annual_Income`, `Credit_Score`.
* **Insurance Info:** `Policy_Type`, `Insurance_Duration`, `Previous_Claims`.
* **Property & Vehicle:** `Property_Type`, `Vehicle_Age`.
* **Customer Feedback:** qualitative ratings (Good/Average/Poor).
* **Other:** `Policy_Start_Date`, `Customer_Feedback` (text-based, optional for NLP).

## 🎯 Objectives

* Perform **EDA**: understand distributions, detect outliers, handle missing values.
* **Feature Engineering**: encode categoricals, transform skewed variables, create new features.
* Train regression models: Linear Regression, Random Forest, XGBoost, LightGBM, CatBoost.
* Evaluate performance with **Root Mean Squared Logarithmic Error (RMSLE)**.
* Generate predictions for Kaggle submission.

## 🛠 Methodology & Tools

* **Data Cleaning:** missing value imputation, drop irrelevant IDs.
* **Visualization:** Seaborn, Matplotlib for correlation & distribution plots.
* **Feature Engineering:**

  * Convert categorical → numerical (Label/One-Hot Encoding).
  * Log transformation for skewed variables.
  * Feature scaling (StandardScaler/MinMax).
* **Modeling:**

  * Baseline models (Linear Regression, Ridge, Lasso).
  * Tree-based models (Random Forest, XGBoost, LightGBM, CatBoost).
  * Cross-validation and hyperparameter tuning.
* **Evaluation Metric:** RMSLE (lower is better for Kaggle leaderboard).

## 📊 Key Insights

* **Age, Annual Income, Health Score, and Credit Score** show strong correlations with Premium Amount.
* **Policy Type** significantly influences premium levels (Premium > Comprehensive > Basic).
* **Smoking Status** and **Exercise Frequency** are key lifestyle predictors.
* **Previous Claims** and **Insurance Duration** also affect pricing.

## 🚀 Next Steps

* Apply **Optuna / GridSearchCV** for hyperparameter optimization.
* Try **stacking/ensembling models** for leaderboard boost.

## 👤 Author

* **Name:** Đào Minh Thuấn
* **GitHub:** [daominhthuan42](https://github.com/daominhthuan42)
