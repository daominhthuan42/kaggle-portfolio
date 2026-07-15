# 🏦 Credit Risk Analysis & Default Prediction 💳

## 📌 Overview

In the financial services industry, managing **credit risk** is critical to maintaining profitability and reducing loan defaults.
This project analyzes a **Credit Risk dataset** and builds machine learning models to predict whether a borrower is likely to **default on a loan**.

The goal is to support better **loan approval decisions**, improve **risk segmentation**, and minimize financial losses.

## 📂 Dataset Information

**Dataset size:** 32,581 records, 29 features 

**Target variable:**

* `loan_status`: Loan repayment outcome

  * `0` → Non-Default
  * `1` → Default

### 🔑 Key Features

* **Customer Profile:**
  `person_age`, `gender`, `marital_status`, `education_level`

* **Financial & Employment:**
  `person_income`, `person_emp_length`, `employment_type`, `person_home_ownership`

* **Loan Information:**
  `loan_amnt`, `loan_term_months`, `loan_int_rate`, `loan_grade`, `loan_intent`

* **Risk & Ratios:**
  `loan_percent_income`, `loan_to_income_ratio`, `debt_to_income_ratio`

* **Credit History & Behavior:**
  `cb_person_cred_hist_length`, `cb_person_default_on_file`,
  `open_accounts`, `credit_utilization_ratio`, `past_delinquencies`

* **Geographic Info:**
  `country`, `state`, `city`

* **ID column:**
  `client_ID` (not predictive)

---

## 🎯 Objectives

* Perform **Exploratory Data Analysis (EDA)**:

  * Distribution, skewness, outliers, correlations
* Handle **data quality issues**:

  * Missing values, outliers, skewed features
* Apply **Feature Engineering**:

  * Encoding categorical variables
  * Transform skewed numerical features
* Train ML models:

  * Logistic Regression, Random Forest, Gradient Boosting (XGBoost, LightGBM, CatBoost)
* Evaluate models using:

  * **Accuracy, F1-score, ROC-AUC**
* Improve model performance with:

  * Cross-validation & hyperparameter tuning

---

## 🛠 Methodology & Tools

* **Data Cleaning:**

  * Handle missing values (`loan_int_rate`, `person_emp_length`)
  * No duplicate records found 

* **EDA & Visualization:**

  * Matplotlib, Seaborn
  * Distribution plots, boxplots, correlation heatmaps

* **Feature Engineering:**

  * One-hot encoding for categorical features
  * Log / Box-Cox / Yeo-Johnson for skewed data

* **Modeling:**

  * Logistic Regression, Decision Tree, Random Forest
  * Gradient Boosting: XGBoost, LightGBM, CatBoost
  * Neural Networks, SVM, KNN (benchmark models)

* **Evaluation:**

  * Cross-validation (StratifiedKFold)
  * Confusion matrix, classification report
  * ROC Curve

* **Optimization:**

  * Hyperparameter tuning with **Optuna**

---

## 📊 Key Insights

* **Class Imbalance:**

  * Default rate ~21.8% → moderate imbalance 

* **Strong Risk Indicators:**

  * `debt_to_income_ratio`, `loan_to_income_ratio` → key drivers of default
  * Higher **interest rate** correlates with higher default risk

* **Income & Financial Behavior:**

  * Default customers have **significantly lower income**
  * High **credit utilization** and **past delinquencies** increase risk

* **Feature Characteristics:**

  * Many variables are **highly skewed** (income, debt)
  * Strong multicollinearity:

    * `loan_percent_income` ≈ `loan_to_income_ratio`

* **Customer Profile:**

  * Majority are **young borrowers (~27 avg age)**
  * Most are **full-time employees**
  * Large portion **rent or mortgage homes**

---

## 👤 Author

* **Name:** Đào Minh Thuấn
* **GitHub:** [daominhthuan42](https://github.com/daominhthuan42)
