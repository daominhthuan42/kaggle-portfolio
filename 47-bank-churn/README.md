# 🏦 Bank Customer Churn Analysis & Prediction 📊

## 📌 Overview

In the highly competitive banking industry, retaining existing customers is
just as important as acquiring new ones. Customer churn can significantly
impact profitability, customer lifetime value, and long-term business growth.

This project analyzes customer demographics, financial characteristics,
banking relationships, engagement behavior, and risk profiles to identify
the key factors associated with customer churn.

Machine learning models are then developed to predict whether a customer is
likely to leave the bank, enabling financial institutions to proactively
identify high-risk customers and design more effective retention strategies.

---

## 📂 Dataset Information

**Dataset size:** 80,000 customer records, 26 original features

**Target variable:**

* `exit`: Customer churn status

  * `0` → Retained
  * `1` → Exited

### 🔑 Key Features

* **Customer Profile:**
  `gender`, `age`, `occupation`, `married`, `origin_province`

* **Financial Information:**
  `credit_score`, `balance`, `monthly_income`

* **Banking Relationship:**
  `tenure_years`, `num_cards`, `num_services`, `active_member`

* **Customer Activity:**
  `last_active_date`, `last_transaction_amount`, `created_date`

* **Customer Analytics:**
  `customer_segment`, `engagement_score`, `loyalty_level`,
  `digital_behavior`

* **Risk & Segmentation:**
  `risk_score`, `risk_segment`, `cluster_group`

* **Identifier / Non-Predictive Features:**
  `id`, `full_name`, `address`

> Several original columns were renamed for better readability and consistency:
> `credit_sco` → `credit_score`,
> `monthly_ir` → `monthly_income`,
> `tenure_ye` → `tenure_years`,
> `nums_card` → `num_cards`,
> `nums_service` → `num_services`,
> `last_transaction_month` → `last_transaction_amount`.

---

## 🎯 Objectives

* Perform comprehensive **Exploratory Data Analysis (EDA)**:

  * Customer churn distribution
  * Numerical and categorical feature distributions
  * Outlier and skewness analysis
  * Correlation analysis
  * Statistical comparison between retained and exited customers

* Identify the major **financial, behavioral, engagement, and risk factors**
  associated with customer churn.

* Perform **Feature Engineering**:

  * Convert raw date variables into meaningful customer activity features
  * Create customer relationship duration and inactivity indicators

* Train and optimize gradient boosting models:

  * CatBoost
  * LightGBM
  * XGBoost

* Evaluate model performance using:

  * Stratified cross-validation
  * Out-of-Fold (OOF) predictions
  * ROC-AUC
  * Precision, Recall, F1-score
  * Confusion Matrix

* Build a **weighted ensemble model** to improve prediction robustness.

* Translate model findings into actionable **customer retention strategies**.

---

## 🛠 Methodology & Tools

* **Data Cleaning & Validation:**

  * Checked missing values and duplicate records
  * No missing values detected in the original 80,000 customer records
  * No duplicate rows detected
  * Reviewed numerical outliers using statistical thresholds
  * Removed identifier features that do not provide meaningful predictive value

* **Exploratory Data Analysis:**

  * Distribution plots and boxplots
  * Churn distribution analysis
  * Numerical and categorical feature analysis
  * Correlation analysis with statistical significance testing
  * Churn comparison across customer groups

* **Feature Engineering:**

  * Converted `created_date` and `last_active_date` to datetime
  * Created `active_duration_days`
  * Created `days_since_last_active`
  * Removed raw date columns after extracting useful temporal information

* **Modeling:**

  * CatBoostClassifier
  * LGBMClassifier
  * XGBClassifier
  * Stratified train-validation split
  * 5-Fold Out-of-Fold cross-validation

* **Class Imbalance Handling:**

  * Churn represents approximately 18% of customers
  * Class weighting / imbalance-aware training was applied where appropriate

* **Hyperparameter Optimization:**

  * Optuna-based hyperparameter tuning
  * ROC-AUC used as the optimization objective

* **Ensemble Learning:**

  * Combined CatBoost, LightGBM, and XGBoost predictions
  * Model weights determined from OOF ROC-AUC performance

---

## 📊 Key Insights

### 🔴 Customer Churn

* Approximately **18% of customers exited the bank**, representing
  **14,400 out of 80,000 customers**.

* Around **82% were retained**, indicating a moderate class imbalance.

* Although the majority of customers remain with the bank, losing nearly
  **1 in 5 customers** represents a meaningful retention and revenue risk.

---

### 💰 Financial Profile

* The average customer has a **credit score of approximately 684**,
  representing a generally fair-to-good credit profile.

* Retained customers have noticeably stronger credit profiles:

  * Retained average credit score: **~691**
  * Exited average credit score: **~653**

* `monthly_income` and `credit_score` both show negative relationships with
  churn, indicating that financially stronger customers are generally
  less likely to leave the bank.

* `balance` and `monthly_income` have a relatively strong positive
  correlation (**r ≈ 0.67**), showing that higher-income customers generally
  maintain larger account balances.

* `risk_score` is strongly negatively associated with:

  * `credit_score` (**r ≈ -0.68**)
  * `monthly_income` (**r ≈ -0.66**)

  This indicates that customers with stronger financial profiles generally
  receive lower estimated risk scores.

---

### 👥 Customer Profile

* The customer base has an average age of approximately **49 years**,
  indicating a relatively mature banking population.

* Gender distribution is almost perfectly balanced:

  * Male: ~50%
  * Female: ~50%

* Occupations are distributed relatively evenly across **10 professional
  categories**, providing broad representation across customer professions.

* Approximately **50% of customers originate from Ho Chi Minh City**,
  indicating a strong concentration in Vietnam's largest economic center.

* Demographic factors such as **gender, origin province, and marital status**
  show relatively limited practical influence on churn compared with
  financial, behavioral, and risk-related indicators.

---

### 📱 Engagement & Digital Behavior

* Only approximately **21.5% of customers are active members**, suggesting
  substantial room for customer re-engagement.

* Approximately **78.5% of customers are classified as offline users**,
  while only about **21.5% use mobile banking behavior**.

* Inactive customers show substantially higher churn than active customers.

* Offline customers also exhibit considerably higher churn than mobile
  customers, highlighting the potential retention value of stronger
  digital engagement.

* `engagement_score` provides meaningful predictive information, suggesting
  that declining customer engagement can serve as an early warning signal
  for churn.

---

### 🏅 Loyalty & Customer Segmentation

* The **Emerging segment** represents the largest customer group at
  approximately **39.6%**, followed by Mass, Priority, and Affluent customers.

* The customer portfolio is heavily concentrated in the **Bronze loyalty
  tier (~86.6%)**, while relatively few customers reach Silver or Gold.

* Bronze customers exhibit substantially higher churn than customers in
  higher loyalty tiers.

* **Mass customers show the highest churn**, while Affluent and Priority
  customers demonstrate stronger retention.

* These patterns suggest that churn management should be differentiated by
  customer value and segment rather than using a single retention strategy
  for the entire customer base.

---

### 💳 Banking Relationship & Product Usage

* Customers most commonly own **2 bank cards** and use approximately
  **2–4 banking services**.

* Churn generally declines as customers use more banking services,
  indicating that deeper product relationships are associated with
  stronger retention.

* Customers holding more cards also tend to show better retention.

* Longer customer relationships generally correspond to lower churn,
  making `tenure_years` an important indicator of relationship strength.

* These patterns highlight opportunities for **cross-selling, onboarding,
  and relationship-deepening strategies**.

---

### ⚠️ Customer Risk

* Approximately **93.4% of customers belong to the Low Risk segment**,
  while only around **6.6% are classified as Medium Risk**.

* Despite representing a relatively small part of the portfolio,
  Medium Risk customers exhibit substantially higher churn.

* `risk_score` consistently emerges as one of the strongest predictors
  across CatBoost, LightGBM, and XGBoost.

* Risk indicators should therefore be incorporated into churn early-warning
  systems alongside customer value and engagement metrics.

---

### 📈 Distribution & Data Characteristics

* Several financial and behavioral variables are strongly right-skewed:

  * `last_transaction_amount`
  * `balance`
  * `monthly_income`
  * `engagement_score`

* `last_transaction_amount` shows particularly extreme positive skewness,
  reflecting a large group with little or no recent transaction activity
  alongside a much smaller group of highly active customers.

* `credit_score` and `risk_score` are comparatively symmetric.

* Most numerical relationships are weak to moderate, suggesting limited
  multicollinearity and allowing different variables to contribute
  complementary predictive information.

---

## 🤖 Model Performance

Three gradient boosting models were optimized and evaluated using
**5-Fold Out-of-Fold cross-validation**.

| Model | OOF ROC-AUC |
|---|---:|
| CatBoost | **0.85514** |
| LightGBM | **0.85344** |
| XGBoost | **0.85316** |

* CatBoost achieved the strongest individual OOF performance.

* All three models produced very similar ROC-AUC scores, indicating
  stable predictive performance across different gradient boosting
  algorithms.

### 🔗 Weighted Ensemble

An AUC-weighted ensemble was created using predictions from all three models.

* **Blended OOF ROC-AUC:** `0.85507`
* **Blended Validation ROC-AUC:** `0.85601`

The ensemble provides strong discrimination between customers with lower
and higher churn risk while reducing dependence on a single model.

---

## 📋 Classification Performance

At the default classification threshold of `0.5`:

* **CatBoost**

  * Accuracy: ~74%
  * Churn Recall: **84%**
  * Churn F1-score: **0.54**

* **LightGBM**

  * Accuracy: ~73%
  * Churn Recall: **85%**
  * Churn F1-score: **0.53**

* **XGBoost**

  * Accuracy: ~74%
  * Churn Recall: **83%**
  * Churn F1-score: **0.53**

The models prioritize relatively high **churn recall**, which is valuable
for retention use cases because failing to identify a customer who is
likely to leave may represent a larger business cost than contacting a
customer who ultimately remains.

---

## 💡 Business Recommendations

* **Prioritize high-risk customers**

  Use `risk_score` as a core signal in a churn early-warning system and
  proactively engage customers whose predicted churn probability and risk
  levels are elevated.

* **Protect high-value relationships**

  Combine churn probability with `balance` and `monthly_income` to identify
  financially valuable customers who are at risk of leaving and prioritize
  them for personalized retention offers.

* **Strengthen early-stage relationships**

  Since longer tenure is associated with stronger retention, improve
  onboarding and early-lifecycle engagement before customer relationships
  mature.

* **Improve customer engagement**

  Target low-engagement customers with personalized communication,
  relationship-building programs, and relevant product offers.

* **Promote deeper product adoption**

  Encourage appropriate cross-selling of banking services, as customers
  using more products and services generally demonstrate stronger retention.

* **Increase digital adoption**

  Offline customers show weaker retention than mobile customers.
  Improving digital banking adoption may strengthen convenience,
  engagement, and long-term customer relationships.

* **Use segment-specific retention strategies**

  Customer Segment and Risk Segment show meaningful churn differences.
  Retention campaigns should therefore be tailored to customer value,
  behavior, and risk instead of applying the same strategy to everyone.

* **Avoid over-targeting demographic factors**

  Gender, origin province, and marital status provide relatively limited
  practical churn information. Retention resources should focus primarily
  on financial, behavioral, engagement, and risk-related signals.

---

## 🎯 Recommended Retention Framework

A practical retention workflow can prioritize customers using:

**Predicted Churn Probability**
→ **Risk Score**
→ **Customer Value (Balance / Income)**
→ **Tenure & Engagement**
→ **Customer Segment**

This approach allows the bank to focus retention resources on customers
who are both **likely to churn and economically valuable to retain**.

> **Note:** Feature importance measures how strongly a variable contributes
> to model predictions but does not prove that the variable causes churn.
> Business decisions should therefore combine model outputs with customer
> value, operational context, and business objectives.

---

## 🧰 Tech Stack

* **Language:** Python
* **Data Processing:** Pandas, NumPy
* **Visualization:** Matplotlib, Seaborn
* **Machine Learning:** Scikit-learn
* **Gradient Boosting:** CatBoost, LightGBM, XGBoost
* **Hyperparameter Optimization:** Optuna
* **Evaluation:** ROC-AUC, Precision, Recall, F1-score, Confusion Matrix
* **Validation:** Stratified 5-Fold Cross-Validation / OOF Evaluation

---

## 👤 Author

* **Name:** Đào Minh Thuấn
* **GitHub:** [daominhthuan42](https://github.com/daominhthuan42)
