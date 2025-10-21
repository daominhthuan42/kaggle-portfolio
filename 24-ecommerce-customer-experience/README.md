# 🛍️ Customer Segmentation in E-Commerce

## 📌 Overview

In today’s competitive **e-commerce landscape**, understanding customer behavior is crucial for improving **sales performance**, **retention**, and **service quality**.
This project analyzes **multi-channel transactional data** collected over a 3-month period to uncover **hidden customer segments** and their behavioral patterns.

**Goal:**
Perform **EDA** and apply **unsupervised clustering (K-Means)** to:

* Identify distinct **customer groups**.
* Explore drivers of **satisfaction and complaints**.
* Support **data-driven marketing** and **personalized engagement** strategies.

## 📂 Dataset Information

**File:** `Chapter_2_Dataset_TDGroup_3 months.xlsx`
**Records:** 3,357 rows × 24 columns
**Scope:** 3 months of multi-channel e-commerce transactions

### 🔑 Key Feature Categories

**Customer & Demographics**

* `Giới_tính` → Gender
* `Độ_tuổi` → Age
* `Khu_vực` → Region (North, Central, South)

**Order & Transaction Attributes**

* `SL_mua` → Quantity purchased
* `Tổng_giá_trị` → Total order value
* `PT_thanh_toán` → Payment method
* `Kênh_bán` → Sales channel (Shopee, Lazada, Website, TikTok)
* `TG_giao_hàng_(ngày)` → Delivery time (days)

**Customer Experience**

* `Đánh_giá_sao` → Rating (1–5)
* `Số_lượt_chat` → Chat interactions
* `Khiếu_nại` → Complaint flag

> ✅ Missing values only in `Mã_chiến_dịch` (~25%), filled as `"No_Campaign"`.
> No duplicate rows detected.

## 🧭 Methodology

### 1. **Exploratory Data Analysis (EDA)**

* Numerical analysis: histograms, boxplots, skewness checks.
* Categorical distributions: gender, payment, region, ratings.
* Outlier detection via **IQR method**.

### 2. **Feature Engineering**

* Aggregation to customer level: avg. order value, complaint ratio, satisfaction score.
* **RFM Analysis:** Recency, Frequency, Monetary segmentation.
* **CLV Calculation:** Estimate customer lifetime value and classify into *Low, Medium, High Value*.

### 3. **Data Processing & Transformation**

* Handled skew using **Yeo-Johnson transform**.
* Scaled numerical features with **StandardScaler**.
* One-hot encoded categorical variables.

### 4. **Modeling: K-Means Clustering**

* Optimal `k = 3` (validated by **Elbow** and **Silhouette** methods).
* PCA used for 2D visualization → clear cluster separation.

## 📊 Key Insights

### 🔹 **Numerical Features (Boxplot)**

* **Cluster 1** → Highest order value & CLV → **High-value loyal customers**.
* **Cluster 2** → Low spending & few purchases → **Low-value / churn-prone**.
* **Cluster 0** → Moderate values → **Stable, average customers**.

### 🔹 **Categorical Features (Countplot)**

* Gender & region are balanced.
* **Cluster 1:** More *successful orders, no complaints, high ratings*.
* **Cluster 2:** Dominates *Low Value* & *At-Risk* RFM segments.
* Sales channel & payment method → evenly distributed across clusters.

## 💡 Business Insights

* **24%** of customers (Best + Loyal) generate the highest revenue share.
* **15%** (At Risk + Churn) require retention focus.
* **Potential Loyalists (22%)** show strong conversion potential.
* **CLV analysis:** small group of high-value customers drives major revenue.

## 👤 Author

**Name:** Đào Minh Thuấn
**Project:** *E-Commerce Customer Segmentation & Insights*
**GitHub:** [daominhthuan42](https://github.com/daominhthuan42)
