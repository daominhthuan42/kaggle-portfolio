# 🏦 Bank Marketing Campaign Analysis 💵

## 📌 Overview

In a competitive financial environment, banks need to optimize marketing campaigns to increase **term deposit subscriptions**.
This project analyzes the **Bank Marketing dataset** and builds machine learning models to predict whether a customer will subscribe to a term deposit.

Competition link: [Playground Series - S5E8 (Kaggle)](https://www.kaggle.com/competitions/playground-series-s5e8)
Full dataset: [Bank Marketing Dataset (UCI/Kaggle)](https://www.kaggle.com/datasets/sushant097/bank-marketing-dataset-full/data)

## 📂 Dataset Information

**Training set:** 750,000 samples, 18 columns.
**Test set:** 250,000 samples, 17 columns.
**Original dataset:** 45,211 samples.

**Target variable:**

* `y`: whether the client subscribed to a term deposit (`yes` / `no`).

### 🔑 Key Features

* **Customer Attributes:** `age`, `job`, `marital`, `education`, `default`, `balance`, `housing`, `loan`.
* **Contact Info:** `contact`, `day`, `month`, `duration` (last call duration in seconds).
* **Campaign Info:** `campaign`, `pdays`, `previous`, `poutcome`.
* **ID column:** unique identifier in training data (not predictive).

## 🎯 Objectives

* Perform **EDA**: distributions, correlations, imbalances, outliers.
* **Feature Engineering**: encode categoricals, scale numerical features, handle `duration` carefully (risk of data leakage).
* Train ML models: Logistic Regression, Random Forest, Gradient Boosting (XGBoost/LightGBM).
* Evaluate with **Accuracy, F1-score, ROC-AUC**.
* Generate Kaggle submissions.

## 🛠 Methodology & Tools

* **Data Cleaning:** drop irrelevant ID column, check duplicates.
* **Visualization:** Matplotlib, Seaborn (age distribution, balance skew, call duration patterns).
* **Feature Engineering:** one-hot encoding, transformation of skewed variables.
* **Modeling:** Logistic Regression, Decision Trees, Random Forest, XGBoost, LightGBM.
* **Evaluation:** cross-validation, confusion matrix, ROC Curve.

## 📊 Key Insights

* **Duration** of last call is highly correlated with subscription but can cause leakage → handled with caution.
* **Job & Education** play significant roles in deposit subscription probability.
* Customers with **housing or personal loans** show different behavior patterns.
* **Balance** distribution is skewed with many outliers (important for preprocessing).
* Most marketing contacts happened in **May**, creating temporal imbalance.

## 🚀 Next Steps

* Apply **class imbalance handling** (SMOTE, class weights).
* Hyperparameter tuning with Optuna.
* Add **business insights**: campaign optimization, target customer segmentation.

## 👤 Author

* **Name:** Đào Minh Thuấn.
* **GitHub:** [daominhthuan42](https://github.com/daominhthuan42)
