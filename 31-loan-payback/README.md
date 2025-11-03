# 🏦 Predicting Loan Payback Outcomes 💳

## 📌 Overview

Accurately predicting loan repayment is crucial for credit risk management and financial decision-making.
This project models **loan repayment likelihood (`loan_paid_back`)** using borrower demographic, financial, credit, and loan-level variables.

Competition link: *Playground Series – S5E11 (Kaggle)*

## 📂 Dataset Information

**Train:** 593,994 rows — **Test:** 254,569 rows
**Target:** `loan_paid_back` (1 = Paid, 0 = Not paid)

### Features

**Numerical**
`annual_income`, `debt_to_income_ratio`, `credit_score`, `loan_amount`, `interest_rate`

**Categorical**
`gender`, `marital_status`, `education_level`, `employment_status`, `loan_purpose`, `grade_subgrade`

**Feature Engineering**

* `grade_subgrade` → `grade_category` (High / Medium / Low)
* Derived credit-risk ratios (credit-to-income, interest burden, DTI-credit score interactions, etc.)

### Data Integrity

* No missing values
* No duplicates
* Outliers retained (financial realism)

## 🎯 Objectives

* EDA & distribution checks
* Statistical inference on repayment drivers
* Train, tune, and validate classification models
* Explainability via SHAP
* Build practical credit-risk insights

## 🛠 Methodology

* **Encoding:** One-Hot Encoding
* **Scaling:** StandardScaler
* **Validation:** Stratified K-Fold
* **Optimization:** Optuna
* **Evaluation:** ROC-AUC, LogLoss, PR curve, Confusion Matrix

**Models tested**
LightGBM, XGBoost, CatBoost, Voting Ensemble

## 📊 Key Insights

### 🔬 Data Insights

* Significant **class imbalance** (≈80% Paid vs 20% Not Paid)
* Skew in `annual_income` & `debt_to_income_ratio`
* Strong negative correlation:
  `credit_score ↘` ⇢ `interest_rate ↗` (≈ −0.54)

## 📚 Statistical Findings (Expanded & Verified)

### ✅ Summary of Significant Variables

| Variable                   | Test                 | Result                                | Interpretation                                                |
| -------------------------- | -------------------- | ------------------------------------- | ------------------------------------------------------------- |
| `employment_status`        | Chi-Square           | p < 0.001                             | Unemployed/Student default higher                             |
| `grade_category`           | Chi-Square           | p < 0.001                             | Low-grade loans default more                                  |
| `education_level`          | Chi-Square           | p < 0.001                             | Bachelor's group default slightly higher                      |
| `loan_purpose`             | Chi-Square           | p < 0.001                             | Education/Medical riskier; Home/Business safer                |
| `gender`                   | Chi-Square           | p < 0.05                              | Small effect; males default slightly more                     |
| `marital_status`           | Chi-Square           | **Not significant**                   | No repayment relationship                                     |
| `credit_score`             | Welch T-Test         | p < 0.001 — **large effect (d≈0.61)** | Higher score → higher repayment                               |
| `annual_income`            | Mann–Whitney U       | p < 0.001                             | Higher income → higher repayment                              |
| `debt_to_income_ratio`     | Mann–Whitney U       | p < 0.001                             | High DTI → higher default                                     |
| `interest_rate`            | Welch T-Test         | p < 0.001 — medium effect             | Higher rate ↗ default risk                                    |
| `loan_amount`              | T-Test               | p < 0.01 — **very small effect**      | Practically neutral                                           |
| Derived credit-risk ratios | Mann–Whitney / ANOVA | p < 0.001                             | Strong predictors (DTI × credit score × interest interaction) |

### 🎯 Top Predictive Drivers (ranked)

1. `grade_category`
2. `employment_status`
3. `credit_score` & adjusted credit metrics
4. `debt_to_income_ratio` & ratio derivatives
5. `interest_rate` (especially high-rate loans)

### 🔁 Interaction Effects

| Interaction             | Finding                                              |
| ----------------------- | ---------------------------------------------------- |
| Interest × Loan Purpose | High interest + education/medical loans default more |
| Credit Score × Interest | Poor credit amplified by high interest               |
| DTI × Credit × Rate     | Stress compounds default probability                 |

## 🤖 Modeling Results

| Model                          | Performance                      |
| ------------------------------ | -------------------------------- |
| Gradient Boosting / XGB / LGBM | Strong individual performance    |
| Logistic Regression            | Robust baseline                  |
| Voting Ensemble                | **Best overall stability & AUC** |

## 🔍 SHAP Key Features

Most influential predictors:

* Credit strength (raw & engineered)
* DTI & debt-related ratios
* Interest burden
* Income level
* Grade risk band
* Employment status
* Loan purpose

## 👤 Author

**Name:** Đào Minh Thuấn
**GitHub:** [https://github.com/daominhthuan42](https://github.com/daominhthuan42)
