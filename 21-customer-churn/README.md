# 👥 Customer Churn Prediction 🏃‍♂️

## 📌 Overview

Churn prediction is critical for **telecommunications companies**, where retaining existing customers is far more cost-effective than acquiring new ones.
This project analyzes customer demographics, subscription details, and billing information to build a **churn prediction model**.

Dataset link: [Customer Churn Dataset (Kaggle)](https://www.kaggle.com/datasets/rashadrmammadov/customer-churn-dataset)

**Goals:**

* Identify factors that drive customer churn.
* Build ML models to predict churn (`Yes` / `No`).
* Provide insights to improve retention strategies.

## 📂 Dataset Information

**Size:** 5,880 records, 20 features.
**Target variable:**

* `Churn` → Yes = churned, No = retained.

### 🔑 Key Features

| Feature                                                             | Description                                                       |
| ------------------------------------------------------------------- | ----------------------------------------------------------------- |
| `customerID`                                                        | Unique customer identifier                                        |
| `gender`                                                            | Male / Female                                                     |
| `SeniorCitizen`                                                     | Whether the customer is a senior (1 = Yes, 0 = No)                |
| `Partner`                                                           | Has a partner (Yes/No)                                            |
| `Dependents`                                                        | Has dependents (Yes/No)                                           |
| `tenure`                                                            | Months stayed with the company                                    |
| `PhoneService`                                                      | Phone service (Yes/No)                                            |
| `MultipleLines`                                                     | Multiple phone lines                                              |
| `InternetService`                                                   | DSL, Fiber optic, or None                                         |
| `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport` | Add-on services (Yes/No)                                          |
| `StreamingTV`, `StreamingMovies`                                    | Entertainment services                                            |
| `Contract`                                                          | Month-to-month, One year, Two year                                |
| `PaperlessBilling`                                                  | Yes/No                                                            |
| `PaymentMethod`                                                     | Payment type (Credit card, Bank transfer, Electronic check, etc.) |
| `MonthlyCharges`                                                    | Monthly bill                                                      |
| `TotalCharges`                                                      | Total charges over tenure                                         |
| `Churn`                                                             | Target variable                                                   |

## 🎯 Objectives

* Perform **EDA**: analyze demographics, contracts, billing patterns.
* Engineer meaningful features from tenure, services, and billing.
* Train classification models:

  * Logistic Regression.
  * Random Forest.
  * XGBoost.
* Evaluate using metrics focused on churn prediction:

  * ROC-AUC.
  * Precision, Recall, F1-score.

## 🛠 Methodology & Tools

* **Data Cleaning:** handle missing values, convert `TotalCharges`.
* **EDA & Visualization:** churn distribution, service correlations, billing trends.
* **Feature Engineering:** categorical encoding, scaling, tenure buckets.
* **Modeling:** baseline logistic regression → tree-based ensemble methods.
* **Evaluation:** focus on Recall (catching churners) + ROC-AUC.

## 📊 Key Insights

* **Contract type** is a strong churn driver → month-to-month customers churn more.
* **Electronic check** payment method has the highest churn rate.
* Customers without **value-added services** (e.g., OnlineSecurity, TechSupport) are more likely to churn.
* Higher **MonthlyCharges** correlates with higher churn probability.
* **Senior citizens** have slightly higher churn tendency.

## 🚀 Next Steps

* Apply **SMOTE or class weighting** for class imbalance.
* Hyperparameter tuning with **Optuna**.
* Provide **business recommendations** for retention.

## 👤 Author

* **Name:** Đào Minh Thuấn.
* **GitHub:** [daominhthuan42](https://github.com/daominhthuan42)