# 🏦 Bank Customer Churn Analysis

## 📌 Overview

Every bank wants to retain their customers for sustainable growth. Understanding **why customers leave (churn)** is crucial for designing effective retention strategies.

👉 Dataset: [Bank Customer Churn (Kaggle)](https://www.kaggle.com/datasets/radheshyamkollipara/bank-customer-churn)

The goal of this project is to:

* Explore the dataset and uncover key factors influencing churn
* Build predictive models to classify customers at risk
* Provide actionable business insights

## 📂 Dataset Information

**Size:** 10,000 records, 18 features
**Target variable:** `Exited` (1 = churn, 0 = retained)

### 🔑 Key Features

* **Demographic:** `Geography`, `Gender`, `Age`
* **Account Info:** `CreditScore`, `Balance`, `EstimatedSalary`, `Tenure`, `NumOfProducts`
* **Banking Behavior:** `HasCrCard`, `IsActiveMember`, `Complain`, `SatisfactionScore`, `CardType`, `PointsEarned`

## 🎯 Objectives

* Perform **EDA**: distributions, correlations, churn rates by features
* Analyze categorical & numerical features
* Build ML models to predict churn
* Evaluate model performance with Accuracy, F1, ROC-AUC
* Suggest strategies for improving customer retention

## 🛠 Methodology & Tools

* **Data Preprocessing:** feature cleaning, encoding categorical variables
* **EDA:** visualization with Matplotlib, Seaborn
* **Modeling:** Logistic Regression, Random Forest, XGBoost, LightGBM
* **Evaluation:** Confusion matrix, classification metrics (Precision, Recall, F1, ROC-AUC)

## 📊 Key Insights

* **Age & Balance** strongly influence churn: older customers with high balance tend to stay
* **Geography**: churn distribution varies by country (France, Germany, Spain)
* **Activity**: inactive members are far more likely to churn
* **Satisfaction & Complaints**: low satisfaction and more complaints increase churn probability
* **Card Type & Products**: customers with fewer products and lower card tiers are more likely to leave

## 🚀 Next Steps

* Apply **class imbalance handling** (SMOTE, class weights)
* Perform **hyperparameter tuning** with Optuna / GridSearchCV
* Build a **customer churn dashboard** (Streamlit / PowerBI)
* Deploy best model into production

## 👤 Author

* **Name:** Đào Minh Thuấn
* **GitHub:** [daominhthuan42](https://github.com/daominhthuan42)
