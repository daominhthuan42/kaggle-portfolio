# 💰 Loan Approval Prediction ✅

## 📌 Overview

This project is part of the **Kaggle Playground Series (S4E10)**.
The dataset is **synthetically generated** but simulates real-world loan application scenarios with both **categorical** and **numerical** features.

Competition link: [Playground Series - S4E10 (Kaggle)](https://www.kaggle.com/competitions/playground-series-s4e10)

**Goal:** Build a machine learning model to **predict whether a loan will be approved** (`loan_status`: 1 = approved, 0 = rejected).

## 📂 Dataset Information

**Training set:** 58,645 samples, 13 features (with target).
**Test set:** 39,098 samples, 12 features (no target).
**Target variable:**

* `loan_status`: 1 (approved), 0 (rejected).

### 🔑 Key Features

| Feature                      | Description                                 |
| ---------------------------- | ------------------------------------------- |
| `person_age`                 | Age of the applicant                        |
| `person_income`              | Annual income                               |
| `person_home_ownership`      | Home ownership status (RENT, OWN, MORTGAGE) |
| `person_emp_length`          | Employment length (years)                   |
| `loan_intent`                | Loan purpose (Education, Medical, etc.)     |
| `loan_grade`                 | Credit grade (A–G)                          |
| `loan_amnt`                  | Loan amount                                 |
| `loan_int_rate`              | Interest rate (%)                           |
| `loan_percent_income`        | Loan amount as a % of income                |
| `cb_person_default_on_file`  | Default history (Y/N)                       |
| `cb_person_cred_hist_length` | Credit history length (years)               |

## 🎯 Objectives

* Perform **EDA**: distributions, outliers, feature relationships.
* **Feature Engineering**: encode categorical vars, scale numerical, derive ratios.
* Train models: Logistic Regression, Random Forest, XGBoost, MLPClassifier.
* Evaluate with Accuracy, F1-score, ROC-AUC.
* Generate Kaggle submissions.

## 🛠 Methodology & Tools

* **Data Preprocessing:** drop irrelevant columns (`id`), encode categorical variables, scale numerical features.
* **Visualization:** Matplotlib, Seaborn.
* **Feature Engineering:** ratios (`loan_percent_income`), interaction terms.
* **Modeling:** Logistic Regression, Random Forest, Gradient Boosting (XGBoost, LightGBM), Neural Networks (MLPClassifier).
* **Evaluation:** cross-validation, confusion matrix, classification metrics.

## 📊 Key Insights

* **Income & Loan Percent Income** strongly impact approval chances.
* Applicants with **longer employment history** have higher approval rates.
* **Credit grade** (`loan_grade`) is highly predictive — higher grades link to approvals.
* **Past defaults** (`cb_person_default_on_file`) negatively affect approvals.
* **Loan purpose** (`loan_intent`) shows varying approval rates (Medical/Education loans more sensitive).

## 🚀 Next Steps

* Apply **hyperparameter tuning** (Optuna).
* Try **stacking/ensembling models** for higher accuracy.

## 👤 Author

* **Name:** Đào Minh Thuấn.
* **GitHub:** [daominhthuan42](https://github.com/daominhthuan42)
