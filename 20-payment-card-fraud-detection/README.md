# 💳 Payment Card Fraud Detection 2025 🛡️

## 📌 Overview

Fraud detection is a top priority in the **luxury retail industry**, where transactions often involve **high-value products, diverse payment methods, and cross-border activity**.
This project uses a dataset of **luxury cosmetics transactions** to analyze patterns of fraudulent behavior and build **machine learning models** for fraud detection.

Dataset link: [Payment Card Fraud Detection with ML Models 2025 (Kaggle)](https://www.kaggle.com/datasets/pratyushpuri/payment-card-fraud-detection-with-ml-models-2025)

**Goals:**

* Detect fraudulent transactions using **transactional, customer, and device attributes**.
* Build ML models for classification (fraud vs. legitimate).
* Provide insights to strengthen fraud monitoring systems.

## 📂 Dataset Information

**Size:** 2,133 transactions, 16 features.
**Target variable:**

* `Fraud_Flag` → 1 = Fraudulent, 0 = Legitimate.

### 🔑 Key Features

| Feature                                 | Description                                            |
| --------------------------------------- | ------------------------------------------------------ |
| `Transaction_ID`                        | Unique transaction identifier                          |
| `Customer_ID`                           | Unique customer ID                                     |
| `Transaction_Date` & `Transaction_Time` | Timestamp of transaction                               |
| `Customer_Age`                          | Age of customer                                        |
| `Customer_Loyalty_Tier`                 | Loyalty tier (Bronze, Silver, Gold, Platinum, Diamond) |
| `Location`                              | Transaction location (city/region)                     |
| `Store_ID`                              | Store identifier                                       |
| `Product_SKU` & `Product_Category`      | Product details                                        |
| `Purchase_Amount`                       | Value of purchase                                      |
| `Payment_Method`                        | Credit Card, Debit Card, Mobile Payment, Gift Card     |
| `Device_Type`                           | Desktop, Mobile, Tablet                                |
| `IP_Address`                            | Customer IP address                                    |
| `Footfall_Count`                        | Number of customers present at the store               |
| `Fraud_Flag`                            | Fraud indicator (target)                               |

## 🎯 Objectives

* Perform **EDA**: analyze purchase behavior, payment channels, fraud distribution.
* **Feature Engineering**: categorical encoding, anomaly features (e.g., high purchase per footfall).
* Train fraud detection models:

  * Logistic Regression.
  * Random Forest.
  * Gradient Boosting (XGBoost/LightGBM).
* Evaluate with fraud-sensitive metrics:

  * ROC-AUC.
  * Precision / Recall.
  * F1-Score.

## 🛠 Methodology & Tools

* **Data Cleaning:** handle missing values, outliers, type conversions.
* **EDA & Visualization:** Seaborn, Matplotlib.
* **Modeling:** baseline models + ensemble methods.
* **Evaluation:** emphasize Recall & AUC (catching fraud is more important than overall accuracy).

## 📊 Key Insights

* **High purchase amounts** are more likely to be flagged fraudulent.
* Certain **locations & stores** show higher fraud concentration.
* **Device\_Type & Payment\_Method** combinations are strong fraud indicators.
* Lower **loyalty tiers** correlate with more suspicious transactions.
* Fraud transactions often occur when **Footfall\_Count** is unusually low.

## 🚀 Next Steps

* Apply **SMOTE/class weights** for fraud class imbalance.
* Hyperparameter tuning with Optuna.

## 👤 Author

* **Name:** Đào Minh Thuấn.
* **GitHub:** [daominhthuan42](https://github.com/daominhthuan42)
