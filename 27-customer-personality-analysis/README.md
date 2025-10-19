# 🧑‍🤝‍🧑 Customer Personality Analysis (Segmentation) 📊

## 📌 Overview

This project performs **Customer Personality Analysis** to understand customer behavior, segment the user base, and inform targeted marketing strategies. We explore demographics, spending patterns, engagement, and campaign response; engineer features; run **RFM analysis**; and build **K-Means** clustering with clear business profiles for each segment. 

**Dataset link:** Customer Personality Analysis (Kaggle)

**Goals**

* Uncover drivers of **purchase behavior** and **campaign success**.
* Build **RFM** and **unsupervised clustering** (K-Means) to segment customers.
* Identify **high-value** and **at-risk** groups and provide **actionable playbooks**.

## 📂 Dataset Information

**Raw size:** **2,240** rows, **29** columns.
**Main themes:** demographics, household composition, product spend (last 2 years), shopping channels, web activity, and campaign flags. 

### 🔑 Key Raw Features

`ID`, `Year_Birth`, `Education`, `Marital_Status`, `Income`, `Kidhome`, `Teenhome`, `Dt_Customer`, `Recency`,
`MntWines`, `MntFruits`, `MntMeatProducts`, `MntFishProducts`, `MntSweetProducts`, `MntGoldProds`,
`NumDealsPurchases`, `NumWebPurchases`, `NumCatalogPurchases`, `NumStorePurchases`, `NumWebVisitsMonth`,
`AcceptedCmp1–5`, `Response`, `Complain`, `Z_CostContact`, `Z_Revenue`, `Country`. 

**Data quality (highlights)**

* `Income` has **24 missing values (~1.07%)** → impute (median).
* `Z_CostContact`, `Z_Revenue` are constants → drop.
* Duplicates by full-row equality after dropping `ID` are present but treated as genuine look-alikes. 

### 🧪 Engineered Features

* `Kids = Kidhome + Teenhome` → binned to **No Kid / Has Kids**
* `Expenses = MntWines + … + MntGoldProds`
* `TotalAcceptedCmp = sum(AcceptedCmp1…5)` → **0 / >0**
* `TotalNumPurchases = NumWebPurchases + NumCatalogPurchases + NumStorePurchases + NumDealsPurchases`
* Skew handling: **Yeo-Johnson** for `Income`, `Expenses` (log/indicator for ultra-sparse if needed). 

## 🎯 Objectives

* **EDA**: distributions, skew/outliers; categorical composition; channel usage.
* **Feature Engineering**: clean categories, create spending/engagement aggregates; transform skew.
* **Segmentation**:

  * **RFM** scoring and labeling (Best, Loyal, Potential Loyalists, At Risk, New, Churn, Other).
  * **K-Means** with standardized numeric + one-hot categorical features.
* **Evaluation & Explainability**: elbow/silhouette for k, PCA visualization; profile clusters and map to business actions. 

## 🛠 Methodology & Stack

* **Preprocessing**: `SimpleImputer(median/most_frequent)`, `StandardScaler`, `OneHotEncoder`.
* **Skew**: `PowerTransformer (Yeo-Johnson)` for heavy-tailed money features.
* **Modeling**: **K-Means**; **Elbow** suggests *k = 3*; **Silhouette** peaks near *k = 2* → we use **k = 3** for better business separation; **PCA (2D)** to visualize separability. 

## 📊 Key EDA Insights

* **Income** is **highly right-skewed** (few very high earners).
* **Expenses** moderately skewed; **Wines** and **Meat** dominate spend.
* **Store purchases** slightly exceed **web purchases**; **web visits** ≈ 5–6/month.
* Campaign engagement is **low** overall (≈15% response; most never accepted prior campaigns).
* Majority are **Graduation-level** and **Married/Together**; complaints are **rare (<1%)**. 

## 🧮 RFM Analysis (Summary)

* **Best & Loyal Customers** contribute the **majority of value** (low Recency, high Frequency/Monetary).
* **Potential Loyalists** are sizable and convertible with consistent nudges.
* **At Risk** show high Recency and declining Monetary → re-engage to prevent churn. 

## 🧭 Cluster Profiles (K = 3)

**Based on our analysis:**

### 🟢 Cluster 0

* **Low income group**; **high Recency** (less recent activity)
* **Low spending** and **few purchases**
* **Many web visits** (browse more than buy)
* Mostly **Married/Together**; often **has kids**
* **Graduation** education level
* **Rarely** accepts promotions; **higher** complaint rate
  ➡️ **Risk / Re-activation pool** (price-sensitive, consider discounts & bundles). 

### 🟡 Cluster 1

* **Medium income**, **moderate Recency**
* **Medium expenses** and **purchase frequency**
* **Moderate web visits**
* **Married** with **1–2 children**; Graduate/Postgraduate
* **Sometimes** accepts promotions; **few** complaints
  ➡️ **Mass-market steady buyers** (seasonal promos, convenience, family bundles). 

### 🟣 Cluster 2

* **High income**; **low Recency** (recent & frequent purchases)
* **Highest expenses** and **most purchases**
* **Fewer web visits** (stable, decisive)
* **No kids / fewer kids**; more **Master’s/PhD**
* **Actively accepts** campaigns; **very low** complaints
  ➡️ **Loyal high-value customers** (VIP perks, premium cross-sell, early access).

## 👤 Author

**Name:** Đào Minh Thuấn
**GitHub:** [daominhthuan42](https://github.com/daominhthuan42)
