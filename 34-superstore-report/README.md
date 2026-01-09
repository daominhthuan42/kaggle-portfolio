# 🏬 Superstore Sales Analytics 🔍

**Notebook:** `superstore-sales-analysis.ipynb`
**Author:** Đào Minh Thuấn
**Project Type:** Python (EDA, Customer Analytics, Business Insights)

## 🧭 Project Overview

* This project analyzes a **retail Superstore dataset** containing transaction-level sales data across products, customers, and geographic regions.
* The analysis focuses on **sales performance, profitability, customer behavior, and retention**, using both descriptive analytics and customer-centric models.
* Advanced analytics techniques such as **RFM Segmentation, Cohort Analysis, Pareto (80/20) Analysis, and QoQ Growth Analysis** are applied.
* Interactive and static visualizations are used to support **data-driven business decisions**.

Dataset original: *Sample - Superstore.csv* 

**Goal:**

* Exploratory Data Analysis (EDA).
* Customer segmentation and value analysis.
* Retention & churn analysis.
* Business insight generation for sales and marketing strategy.

## 📂 Dataset Information

**Size:** 9,994 transaction records
**Features:** 20 variables
**Granularity:** Order line-item level
**Target:** ***Unsupervised*** (no predefined labels)

## 🔑 Key Features

* **Order & Time**

  * `OrderID`, `OrderDate`, `ShipDate`, `ShipMode`
* **Customer**

  * `CustomerID`, `CustomerName`, `Segment`
* **Geography**

  * `Country`, `Region`, `State`, `City`, `PostalCode`
* **Product**

  * `ProductID`, `Category`, `Sub-Category`, `ProductName`
* **Business Metrics**

  * `Sales`, `Quantity`, `Discount`, `Profit`

## 🧪 Data Quality Summary

* **Missing Values:** None detected → dataset is complete.
* **Duplicates:** Only 1 duplicated row (~0.01%) → negligible impact.
* **Outliers:** Present in Sales, Quantity, Discount, and Profit.

  * These are **business-driven outliers** (large orders, bulk purchases, aggressive discounts), not data errors.

👉 Dataset is suitable for **EDA, segmentation, and modeling without heavy cleaning**.

## 🎯 Analysis & Key Outputs

### 📊 Exploratory Data Analysis (EDA)

* Strong **right-skewness** in all numerical features (Sales, Profit, Quantity, Discount).
* Sales and profit are dominated by a **small number of large transactions**.
* Office Supplies and Consumer segment account for the majority of transactions.
* Sales are geographically concentrated in **large states and metropolitan cities**.

### 🧠 RFM Customer Segmentation

* Customers are segmented using **Recency – Frequency – Monetary (RFM)** scoring.
* Segments include:

  * Champions
  * Loyal
  * Potential Loyalist
  * At Risk
  * Hibernating
  * Lost Customers

**Key Insight:**

* ~**80% of total sales, profit, and volume come from only 4 RFM segments**.
* **At Risk customers generate very high profit but face churn risk** → top retention priority.

### 📈 Pareto (80/20) Analysis

* Confirms strong **value concentration**:

  * A small subset of customer segments drives the majority of revenue and profit.
* Segment size ≠ profitability.
* Some large segments generate low or even negative profit.

### 🔄 Cohort Analysis (Retention & Churn)

* Monthly cohort tracking based on first purchase date.
* Findings:

  * **Churn is front-loaded** (early periods).
  * Customers who survive early months tend to stay long-term.
  * Early cohorts show stronger retention than later cohorts.

**Business Implication:**

* Early-stage engagement (first 3–6 months) is critical.

### 📉 QoQ (Quarter-over-Quarter) Analysis

* Quarterly trends analyzed for:

  * Sales
  * Quantity
  * Discount
  * Profit
  * Customer Spend
* Identifies:

  * Growth cycles
  * Seasonal volatility
  * Sharp contractions followed by recovery phases

## 🧠 Business Insights (Executive Summary)

* Sales and profit are **highly skewed** → focus on high-value customers and transactions.
* **At Risk & Champions** are the most valuable segments → prioritize retention.
* Discount strategy has a **direct impact on profitability**.
* Customer retention drops early → improve onboarding & early engagement.
* Geographic concentration suggests opportunities for **regional optimization**.

## 🚀 Future Improvements

* Build **regression models** to predict Sales or Profit.
* Apply **clustering (KMeans + PCA)** for advanced customer segmentation.
* Integrate **interactive dashboards** (Power BI / Plotly Dash).
* Evaluate **CLV prediction models**.

## 👤 Author

**Name:** Đào Minh Thuấn
**GitHub:** [daominhthuan42](https://github.com/daominhthuan42)
