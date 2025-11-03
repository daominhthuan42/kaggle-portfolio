# 🛍️ Customer Purchase Behaviour Analysis 💳

## 📌 Overview

In today’s retail landscape, understanding **how and why customers buy** is crucial for driving growth, loyalty, and product optimization.
This project analyzes the **Customer Purchase Behaviour dataset** to uncover key patterns in **demographics, purchase frequency, and spending**, helping design data-driven marketing and retention strategies.

Dataset link: [Customer Purchase Behaviour (Kaggle)](https://www.kaggle.com/datasets/mubeenshehzadi/customer-purchase-behaviour)

## 📂 Dataset Information

**Records:** 3,900 rows
**Features:** 18 columns
**Scope:** Covers customer demographics, product details, transaction behaviors, and engagement attributes.

Each row represents one **purchase event** made by a unique customer.

### 🔑 Key Features

| Category                 | Features                                                                               |
| ------------------------ | -------------------------------------------------------------------------------------- |
| **Demographics**         | `Age`, `Gender`, `Location`                                                            |
| **Product Attributes**   | `Item_Purchased`, `Category`, `Size`, `Color`, `Season`                                |
| **Transaction Behavior** | `Purchase_Amount_(USD)`, `Payment_Method`, `Discount_Applied`, `Promo_Code_Used`       |
| **Customer Engagement**  | `Subscription_Status`, `Review_Rating`, `Previous_Purchases`, `Frequency_of_Purchases` |

### 🧾 Data Quality

✅ No missing or duplicate values
✅ Balanced numeric distributions (no heavy skewness)
✅ Consistent feature types (13 categorical, 4 numeric, 1 identifier)

## 🎯 Objectives

* Explore **customer demographics and spending behavior**
* Identify **purchase frequency** and **subscription patterns**
* Cluster customers into **distinct behavioral segments**
* Generate **actionable business insights** for marketing and retention

## 🛠 Methodology & Tools

**Libraries:** Pandas, NumPy, Matplotlib, Seaborn, Scikit-Learn, KMeans, PCA, Folium

**Data Preparation:**

* Clean and reformat column names
* Encode categoricals with `OneHotEncoder`
* Scale numericals using `StandardScaler`
* Apply dimensionality reduction with **PCA**

**Modeling & Analysis:**

* **Elbow** and **Silhouette** methods to select optimal clusters
* **K-Means clustering** to segment customers
* **Visualization:** Violin plots, Count plots, PCA 2D scatter, and Folium maps

## 📊 Key Insights

### 👥 Demographic Trends

* **Majority male customers (~68%)**, mostly aged 30–57 years.
* **Clothing** dominates purchases (45%), especially M-size products.
* **Spring** is the most active shopping season (~26%).
* Customers span **50 U.S. states**, with strong diversity across regions.

### 💵 Transaction Behaviour

* Average spend: **$59.8 per purchase**.
* Most buyers do **not rely on discounts or promo codes**.
* **PayPal, Credit Card, and Cash** are top payment methods.
* Median rating: **3.7/5**, indicating overall satisfaction.

### 📈 Clustering (K-Means)

| Cluster       | Description                       | Behaviour Summary                                                                                                           |
| ------------- | --------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Cluster 0** | 🟢 **Active, Engaged Buyers**     | High spending, frequent purchases (weekly–fortnightly), more likely subscribers, use Free/Express shipping, and promotions. |
| **Cluster 1** | 🟠 **Passive, Occasional Buyers** | Lower spending, monthly–quarterly purchases, non-subscribers, less discount usage, older demographics.                      |

**Optimal Clusters:** `k = 2`
**Validation:** PCA visualization confirms distinct and stable cluster boundaries.

### 🌍 Geographical Mapping

Folium mapping shows both clusters evenly distributed across states, with **Cluster 0 more concentrated in urban centers** — suggesting metropolitan customers are more frequent shoppers.

## 💡 Business Insights

* Encourage **subscription programs** targeting non-subscribers (~73% of users).
* Personalize **discounts and loyalty rewards** for Cluster 0 (active spenders).
* Re-engage Cluster 1 customers via **email marketing** or **seasonal promotions**.
* Optimize **inventory planning** for high-demand product types (Clothing, M-size).
* Leverage **review feedback (≥ 4 stars)** to promote top-rated products.

## 👤 Author

* **Name:** Đào Minh Thuấn
* **GitHub:** [daominhthuan42](https://github.com/daominhthuan42)
