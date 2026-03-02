# 📞 Telco Customer Churn Prediction 📉

## 📌 Overview

This project focuses on analyzing and modeling **customer churn (`Churn`)** using demographic information, subscription services, contract details, and billing behavior from a telecommunications company.

The dataset represents real-world telco customer data and is widely used for churn modeling and retention strategy research.

Dataset source: Kaggle – *Telco Customer Churn Dataset*

## 📂 Dataset Information

**Train:** 594,194 rows — **Test:** 254,655 rows - **Original:** 7,043 rows
**Target:** `Churn` (Yes / No)
**Problem Type:** Binary Classification

Each row represents one telecom customer, including service subscriptions, billing structure, tenure, and payment patterns.

## 🧾 Feature Overview

### 🔢 Numerical Features

Core quantitative indicators:

* `tenure` – Number of months customer has stayed
* `MonthlyCharges` – Monthly subscription cost
* `TotalCharges` – Total amount charged to customer

### 🔠 Categorical Features

#### 👤 Demographic

* `gender`
* `SeniorCitizen`
* `Partner`
* `Dependents`

#### 📡 Service Subscriptions

* `PhoneService`
* `MultipleLines`
* `InternetService`
* `OnlineSecurity`
* `OnlineBackup`
* `DeviceProtection`
* `TechSupport`
* `StreamingTV`
* `StreamingMovies`

#### 📑 Contract & Billing

* `Contract`
* `PaperlessBilling`
* `PaymentMethod`

> Most categorical variables are string-based and require encoding during preprocessing.

## 🧹 Data Integrity

From the EDA notebook:

* ✅ No duplicated customer IDs
* ⚠️ `TotalCharges` contained blank values → converted to numeric and handled
* ⚠️ Some features show class imbalance (notably Churn distribution)
* Data types corrected (especially `TotalCharges`)

Dataset required light cleaning before modeling.

## 📊 Exploratory Data Analysis (EDA)

### 🎯 Target Distribution

* ~26–27% customers churned
* ~73–74% retained

→ Moderate class imbalance.

### 📈 Key Behavioral Patterns

#### 📆 Tenure

* Short-tenure customers show significantly higher churn rates.
* Long-term customers are more stable and less likely to churn.

#### 💳 Monthly Charges

* Higher monthly charges correlate with increased churn probability.

#### 📑 Contract Type

* Month-to-month contracts have the highest churn rate.
* One-year and two-year contracts show significantly lower churn.

#### 🛠 Tech Support & Security Services

* Customers without:

  * OnlineSecurity
  * TechSupport
  * DeviceProtection
    are more likely to churn.

#### 💰 Payment Method

* Electronic check users show higher churn rates compared to automatic payments.

## 📐 Statistical Analysis

Based on the EDA & testing in the PDF:

| Feature Type         | Test Applied          | Result                         | Interpretation                                            |
| -------------------- | --------------------- | ------------------------------ | --------------------------------------------------------- |
| Categorical vs Churn | Chi-Square Test       | Significant associations       | Contract, internet type, support services influence churn |
| Numerical vs Churn   | T-Test / Mann-Whitney | Significant differences        | Tenure and MonthlyCharges differ across churn groups      |
| Variance comparison  | Levene’s Test         | Unequal variance in some cases | Robust methods preferred                                  |

Key conclusion:
Multiple service-level and billing-related variables show statistically significant relationships with churn behavior.

## 📌 Strongest Churn Indicators

Consistent signals across EDA and statistical testing:

* Month-to-month contract
* Short tenure
* High monthly charges
* Fiber optic internet
* No tech support
* No online security
* Electronic check payment method
* Paperless billing enabled

These variables provide strong predictive power.

## 🛠 Data Processing Steps

* Column name standardization
* `TotalCharges` cleaned and converted to numeric
* Missing handling for blank values
* One-hot encoding for categorical variables
* Label encoding for binary features
* Feature scaling (for linear models)

## 🚀 Modeling Framework (Prepared)

The notebook structure supports:

* Logistic Regression
* Random Forest
* XGBoost
* LightGBM
* Stratified K-Fold Cross Validation
* ROC-AUC Evaluation
* Feature Importance Analysis

Designed for interpretable churn modeling and retention strategy insights.

## 💼 Business Implications

The analysis supports:

* Targeting short-tenure customers with retention campaigns
* Promoting long-term contracts
* Bundling tech support and security services
* Encouraging automatic payment methods
* Monitoring high monthly charge segments

## 👤 Author

**Name:** Đào Minh Thuấn
**GitHub:** [https://github.com/daominhthuan42](https://github.com/daominhthuan42)
