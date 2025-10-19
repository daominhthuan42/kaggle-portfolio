# 💳 Credit Score Classification (Cleaned) 🧮

## 📌 Overview

This project builds machine-learning models to classify **customer credit score** into **Good / Standard / Poor** using **demographic, financial, and behavioral** features (income, credit history age, utilization ratio, delays, inquiries, etc.).

Dataset link: [Credit Score Classification — Cleaned (Kaggle)](https://www.kaggle.com/datasets/iremnurtokuroglu/credit-score-classification-cleaned-dataset) ([Kaggle][1])

**Goals:**

* Explore drivers of **credit score** and customer risk.
* Train robust classifiers to predict **`credit_score`** (Good / Standard / Poor).
* Provide actionable insights for **loan approval**, **risk policy**, and **customer segmentation**.

## 📂 Dataset Information

**Size:** ~96,696 rows, **28** columns (after cleaning). Target labels are **imbalanced**: Standard ~53%, Poor ~28%, Good ~18%. 

**Target variable:**

* `credit_score` → categorical: **Poor (0) / Standard (1) / Good (2)**. 

### 🔑 Key Features

| Feature Name               | Description                                                        |
| -------------------------- | ------------------------------------------------------------------ |
| `id`                       | Row identifier (technical index, not used for modeling)            |
| `customer_id`              | Unique customer identifier (keep for customer-level analysis)      |
| `month`                    | Month of record (financial data timestamp)                         |
| `name`                     | Customer name (identifier only)                                    |
| `age`                      | Customer’s age                                                     |
| `ssn`                      | Social security number (unique personal ID, not used for modeling) |
| `occupation`               | Customer’s occupation (e.g., Engineer, Lawyer, Scientist)          |
| `annual_income`            | Customer’s annual income                                           |
| `monthly_inhand_salary`    | Average monthly income credited to the account                     |
| `credit_history_age`       | Duration of the customer’s credit history (in months)              |
| `total_emi_per_month`      | Total monthly EMI payments made by the customer                    |
| `num_bank_accounts`        | Number of bank accounts held by the customer                       |
| `num_credit_card`          | Number of credit cards owned                                       |
| `interest_rate`            | Interest rate on current credit products                           |
| `num_of_loan`              | Number of active loans                                             |
| `type_of_loan`             | Types of loans held (text field containing multiple categories)    |
| `delay_from_due_date`      | Average number of days delayed in payments                         |
| `num_of_delayed_payment`   | Total number of delayed payments                                   |
| `changed_credit_limit`     | Amount by which the credit limit has changed                       |
| `num_credit_inquiries`     | Number of credit inquiries made                                    |
| `credit_mix`               | Type of credit mix (Good / Standard / Bad)                         |
| `outstanding_debt`         | Total unpaid debt amount                                           |
| `credit_utilization_ratio` | Ratio of used credit to total credit limit                         |
| `payment_of_min_amount`    | Whether the customer pays only the minimum amount due              |
| `amount_invested_monthly`  | Average monthly investment made by the customer                    |
| `payment_behaviour`        | Customer’s payment pattern or spending behavior                    |
| `monthly_balance`          | Average monthly balance maintained                                 |
| `credit_score` (🎯 Target) | Credit score class: 🟢 Good, 🟡 Standard, 🔴 Poor                  |

(IDs like `id`, `name`, `ssn`, `customer_id` are not used for modeling.) 

## 🎯 Objectives

* **EDA**: distributions, outliers, correlations; class imbalance assessment.
* **Feature Engineering**: encode categoricals (`occupation`, `credit_mix`, …), normalize skewed monetary fields, derive ratios (e.g., **Debt-to-Income**, **Delay rate**).
* **Modeling**:

  * Logistic Regression, Random Forest, XGBoost, LightGBM, CatBoost, MLP,...
* **Evaluation**: Stratified CV; ROC-AUC, **Confusion Matrix**. 

## 🛠 Methodology & Tools

* **Data quality**: no missing/duplicate rows in the cleaned file; notable outliers remain by design (reflecting real behavior). 
* **EDA & Viz**: histograms/boxplots for skew, correlation heatmap; target distribution shows class imbalance. 
* **Modeling stack**: scikit-learn pipelines, tree/boosting models, and ANN baselines; compare via stratified K-fold. 
* **Statistical tests** (for feature–target relations): **Chi-square** (categoricals), **Kruskal–Wallis / Dunn**, **Welch-ANOVA / Games–Howell**, **Levene** for variance homogeneity. 

## 📊 Key Insights

* **Imbalance**: `Standard` dominates (~53%); handle with stratification and, if needed, class weights/thresholding. 
* **Income block**: `monthly_inhand_salary` ~ **perfectly correlated** with `annual_income` → redundancy; keep one. 
* **Behavioral risk**: higher **delays**, **delayed_payment count**, **inquiries**, and **utilization ratio** align with worse credit classes. 
* **Skewness/outliers**: financial features (`amount_invested_monthly`, `total_emi_per_month`, `outstanding_debt`) are **right-skewed** → consider log/robust scaling. 

## 🚀 Next Steps

* Address class imbalance (class weights, focal loss, threshold tuning).
* Try **LightGBM/XGBoost** with monotonic constraints & calibration for decision support. (This family commonly performs strongly on tabular credit data.) ([IJSAT][2])
* Add domain features: **DTI**, **utilization buckets**, **recent delay rate**, **loan mix richness**.
* Build **explainability**: SHAP for global/local attributions, and scorecards for policy.

## 👤 Author

* **Name:** Đào Minh Thuấn
* **GitHub:** [daominhthuan42](https://github.com/daominhthuan42)
