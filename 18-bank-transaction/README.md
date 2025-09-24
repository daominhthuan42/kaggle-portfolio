# 🏦 Bank Transaction Fraud Detection 🛡️

## 📌 Overview

Fraud detection is a critical challenge in banking, but real datasets are often **unlabeled** due to privacy and data scarcity.
This project analyzes a **synthetic bank transaction dataset** and applies **unsupervised anomaly detection & clustering** to identify potentially fraudulent transactions.

Dataset link: [Bank Transaction Dataset for Fraud Detection (Kaggle)](https://www.kaggle.com/datasets/valakhorasani/bank-transaction-dataset-for-fraud-detection)

**Goal:**

* Explore transaction patterns and anomalies.
* Apply unsupervised models (Clustering + Isolation Forest) to detect suspicious activities.
* Provide insights for **fraud risk management**.

## 📂 Dataset Information

**Size:** 2,512 transactions, 16 features.
**Target:** *Unsupervised* (no fraud labels provided).

### 🔑 Key Features

* **Transaction:** `TransactionID`, `TransactionAmount`, `TransactionDate`, `TransactionDuration`.
* **Account:** `AccountID`, `AccountBalance`, `PreviousTransactionDate`.
* **Customer Info:** `CustomerAge`, `CustomerOccupation`.
* **Channel & Devices:** `Channel`, `DeviceID`, `IP Address`, `Location`, `MerchantID`.
* **Security:** `LoginAttempts`.

## 🎯 Objectives

* Perform **EDA** to understand transaction distributions and detect anomalies.
* **Feature Engineering**: transaction frequency, time gaps, spending ratios.
* Apply **Unsupervised Models**:

  * **K-Means** (with Elbow Method + Silhouette Score to find optimal clusters).
  * **DBSCAN** (density-based clustering for anomaly detection).
  * **Isolation Forest** (tree-based anomaly detection).
* Compare anomaly scores and clustering outcomes

## 🛠 Methodology & Tools

* **Data Preprocessing:** datetime parsing, categorical encoding, scaling features.
* **Visualization:** anomaly score distributions, clustering plots (PCA/t-SNE).
* **Models Used:**

  * **K-Means:** cluster customers/transactions, detect outliers from cluster centers.
  * **DBSCAN:** identify noise points as anomalies.
  * **Isolation Forest:** flag anomalies using tree isolation principle.
* **Evaluation:**

  * Elbow Method & Silhouette for K-Means.
  * Cluster density & noise points for DBSCAN.
  * Contamination rate for Isolation Forest.

## 📊 Key Insights

* **High-value unusual transactions** often detected as anomalies across models.
* **Multiple device/IP changes** linked to the same account flagged frequently.
* **Transaction duration outliers** appear in DBSCAN as noise points.
* **Unusually frequent login attempts** highlighted by Isolation Forest.

## 🚀 Next Steps

* Apply **ensemble anomaly scoring** combining K-Means, DBSCAN, Isolation Forest.
* Extend to **time-series anomaly detection**.

## 👤 Author

* **Name:** Đào Minh Thuấn.
* **GitHub:** [daominhthuan42](https://github.com/daominhthuan42)
