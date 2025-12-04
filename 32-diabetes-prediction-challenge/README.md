# 🩺 Predicting Diabetes Likelihood from Health Indicators 🍏

## 📌 Overview

This project explores and models **diabetes diagnosis (`diagnosed_diabetes`)** using a rich set of clinical, lifestyle, and demographic health indicators.
The dataset — a synthetic but realistic health-risk dataset — mirrors variables used in real-world metabolic & cardiovascular risk assessment, enabling robust EDA, statistical inference, and modeling research. 

Competition source: *Kaggle Playground Series – S5E12* 

## 📂 Dataset Information

**Train:** 700,000 rows — **Test:** 300,000 rows
**Target:** `diagnosed_diabetes` (1 = Diagnosed, 0 = Not diagnosed) 

### Features

#### **Numerical Features**

Includes lifestyle metrics, biological measurements, and clinical indicators:
`age`, `physical_activity_minutes_per_week`, `diet_score`, `sleep_hours_per_day`,
`screen_time_hours_per_day`, `bmi`, `waist_to_hip_ratio`, `systolic_bp`,
`diastolic_bp`, `heart_rate`, `cholesterol_total`, `hdl_cholesterol`,
`ldl_cholesterol`, `triglycerides` 

#### **Categorical Features**

`gender`, `ethnicity`, `education_level`, `income_level`, `smoking_status`,
`employment_status`, `alcohol_consumption_per_week`,
`family_history_diabetes`, `hypertension_history`, `cardiovascular_history` 

### Data Integrity

* **No missing values** in both train & test sets.
* **No duplicated rows** found.
* **Outliers present** — but retained, as they reflect real health variability (BMI, BP, triglycerides, etc.). 

## 🎯 Objectives

* Perform comprehensive EDA on lifestyle, clinical, and metabolic indicators
* Examine class imbalance & distribution patterns
* Conduct statistical tests to validate associations
* Prepare data pipelines for future ML modeling
* Enable explainability and interpretability for health-risk analytics

## 🛠 Methodology

* **EDA:** Histograms, boxplots, distribution overlays, variance & skewness checks
* **Categorical Analysis:** Chi-Square independence tests
* **Numerical Analysis:**

  * Skewness–Kurtosis screening
  * Q–Q plots
  * Variance tests (Levene)
  * Kruskal–Wallis, Dunn post-hoc
  * ANOVA & Welch ANOVA (when appropriate)
  * Mann–Whitney U / T-Tests for binary groups
* **Data Handling:**

  * Category conversion for memory optimization
  * Outlier detection via IQR rules

## 📊 Key Insights

### 🔬 Data Insights

* **Class imbalance:**
  ~62% diagnosed vs ~38% non-diabetic → models must consider imbalance.
  (Pie chart & counts shown in PDF) 

* **Lifestyle & metabolic trends:**

  * Average **BMI ~25.8**, in overweight range.
  * **Sleep ~7 hours/day**, stable across sets.
  * **Screen time ~6 hours/day**.
  * **Physical activity** varies significantly between train & test (shift). 

* **Strong prevalence patterns:**

  * Majority have **no hypertension** and **no cardiovascular history**.
  * **Family history of diabetes** may serve as an informative predictor. 

### 📚 Statistical Findings

| Variable Type                                             | Test                                       | Result                                         | Interpretation                                                                  |
| --------------------------------------------------------- | ------------------------------------------ | ---------------------------------------------- | ------------------------------------------------------------------------------- |
| Categorical (gender, ethnicity, education, etc.)          | **Chi-Square**                             | Several features show significant association  | These sociodemographic factors influence diabetes likelihood                    |
| Binary health risk markers                                | **Mann–Whitney U / T-Test**                | Significant differences                        | Lifestyle & metabolic indicators differ between diabetic vs non-diabetic groups |
| Multi-group categorical (income, employment, alcohol use) | **Kruskal–Wallis + Dunn**                  | Multiple groups differ in distributions        | Non-parametric evidence of metabolic or behavioral variation                    |
| Numeric clinical metrics                                  | **Normality checks + ANOVA / Welch ANOVA** | Mostly non-normal → Kruskal–Wallis recommended | Clinical features vary significantly across population segments                 |

(Results summarized from multiple statistical modules in the PDF.) 

## 📌 Top Observed Risk Indicators

Consistent signals observed across distribution analysis & statistical tests:

* Elevated BMI & waist-to-hip ratio
* High blood pressure (systolic & diastolic)
* High triglycerides, LDL; low HDL
* Low physical activity
* High screen time
* Family history of diabetes
* Presence of hypertension or cardiovascular history
  (Insights documented throughout EDA sections.) 

## 👤 Author

**Name:** Đào Minh Thuấn
**GitHub:** [https://github.com/daominhthuan42](https://github.com/daominhthuan42)
