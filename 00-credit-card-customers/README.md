# 📊 Credit Card Customers Analysis

## 📝 Overview

This project analyzes the **Credit Card Customers** dataset from Kaggle. The goal is to perform **exploratory data analysis (EDA)** and build **predictive models** to understand customer behavior, identify patterns, and provide useful business insights.

Dataset link: [Credit Card Customers (Kaggle)](https://www.kaggle.com/datasets/sakshigoyal7/credit-card-customers)

## 📂 Dataset Information

**Source:** Kaggle – Sakshi Goyal
**Records:** 10,127 customers
**Features:** 21 attributes

### Key Features

| Feature Name               | Description                                           |
| -------------------------- | ----------------------------------------------------- |
| `CLIENTNUM`                | Unique customer ID (not used for modeling)            |
| `Attrition_Flag`           | Churn status: Existing or Attrited                    |
| `Customer_Age`             | Age of the customer                                   |
| `Gender`                   | Customer gender                                       |
| `Dependent_count`          | Number of dependents                                  |
| `Education_Level`          | Education level (High School, Graduate, etc.)         |
| `Marital_Status`           | Marital status (Married, Single, etc.)                |
| `Income_Category`          | Income bracket (Less than \$40K, \$40K - \$60K, etc.) |
| `Card_Category`            | Credit card type (Blue, Silver, Gold, Platinum)       |
| `Months_on_book`           | Tenure with the bank (in months)                      |
| `Total_Relationship_Count` | Total number of bank products held                    |
| `Months_Inactive_12_mon`   | Inactive months in the past 12 months                 |
| `Contacts_Count_12_mon`    | Customer service contacts in the past 12 months       |
| `Credit_Limit`             | Credit card limit                                     |
| `Total_Revolving_Bal`      | Revolving balance on the card                         |
| `Avg_Open_To_Buy`          | Average available credit                              |
| `Total_Trans_Amt`          | Total transaction amount in last 12 months            |
| `Total_Trans_Ct`           | Total transaction count in last 12 months             |
| `Total_Ct_Chng_Q4_Q1`      | Change in transaction count Q4 vs Q1                  |
| `Total_Amt_Chng_Q4_Q1`     | Change in transaction amount Q4 vs Q1                 |
| `Avg_Utilization_Ratio`    | Average card utilization rate                         |

## 🎯 Objectives

* Perform **EDA** to uncover trends and anomalies
* Visualize demographic and transactional behaviors
* Identify potential **churn customers** and spending groups
* Build predictive models to classify **Credit card churn**.

## 🛠 Methodology & Tools

* **Data Preprocessing:** Missing values, encoding categorical variables, scaling
* **Visualization:** `Matplotlib`, `Seaborn`.
* **Modeling:** Logistic Regression, Random Forest, XGBoost, LightGBM, Clustering.
* **Evaluation Metrics:** Accuracy, Precision, Recall, F1, ROC-AUC

## 📊 Results & Insights

* Identified key demographic segments (e.g., age groups, income levels) influencing spending
* Detected patterns of **inactive vs active customers**
* Models show promising performance in predicting customer churn
* Insights can help banks design **targeted campaigns** and **risk management strategies**

## 👤 Author

* **Name:** Đào Minh Thuấn
* **GitHub:** [daominhthuan42](https://github.com/daominhthuan42)
