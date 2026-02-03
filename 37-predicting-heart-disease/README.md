# ❤️ Predicting Heart Disease from Clinical Indicators 🫀

## 📌 Overview

This project focuses on analyzing and modeling **heart disease diagnosis (`heart_disease`)** using a comprehensive set of demographic, physiological, electrocardiographic, and clinical examination features.

The dataset is derived from real-world medical records commonly used in cardiology research and risk stratification studies. It reflects typical indicators applied in cardiovascular screening and clinical decision support systems.

Competition source: *Kaggle Playground Series – S6E2 / UCI Heart Disease Dataset*

---

## 📂 Dataset Information

**Train:** 630,000 rows — **Test:** 270,000 rows
**Target:** `heart_disease` (Presence / Absence)

### Features

#### **Numerical Features**

Includes core physiological and cardiac performance indicators:

`age`, `bp`, `cholesterol`, `max_hr`, `st_depression`

#### **Categorical Features (Encoded)**

Diagnostic and demographic attributes encoded as integers:

`sex`, `chest_pain_type`, `fbs_over_120`, `ekg_results`,
`exercise_angina`, `slope_of_st`, `number_of_vessels_fluro`, `thallium`

> Most categorical variables are numerically encoded and converted to category type during preprocessing.

---

### Data Integrity

* **No missing values** in both train & test sets.
* **No duplicated rows** detected.
* **Outliers present** in major clinical features (age, BP, cholesterol, HR, ST depression).
* Outliers were **retained** as they reflect real high-risk patient profiles.

---

## 🎯 Objectives

* Perform large-scale EDA on cardiovascular risk indicators
* Examine target distribution and potential imbalance
* Validate associations using statistical hypothesis testing
* Build reusable statistical analysis utilities
* Prepare high-quality pipelines for ML modeling
* Support explainable medical risk analytics

---

## 🛠 Methodology

### 📊 Exploratory Data Analysis (EDA)

* Distribution analysis (histograms, KDE, boxplots)
* Skewness & kurtosis screening
* Q–Q plots for normality diagnostics
* Train–test distribution consistency checks

### 📈 Categorical Analysis

* Chi-Square Test of Independence
* Residual analysis via heatmaps
* Category frequency stability checks

### 📐 Numerical Analysis

* Skewness–Kurtosis evaluation
* Levene’s test for variance homogeneity
* Normality assessment
* IQR-based outlier detection

### 📑 Statistical Testing

* Kruskal–Wallis + Dunn post-hoc
* One-Way ANOVA + Tukey HSD
* Welch ANOVA + Games–Howell
* Mann–Whitney U Test
* Independent T-Test + Cohen’s d

### ⚙️ Data Handling

* Column standardization
* Memory optimization via downcasting
* Category conversion
* Safe CSV loading with encoding checks
* Custom logging system

---

## 📊 Key Insights

### 🔬 Data Insights

* **Dataset scale:**

  * Large-scale training set (630K samples) enables robust modeling.
  * Train and test distributions are highly consistent.

* **Demographic & clinical profile:**

  * Mean age ≈ **54 years** → middle-aged to elderly population.
  * Average BP ≈ **130 mmHg** → pre-hypertension range.
  * Mean cholesterol ≈ **245 mg/dL** → above healthy threshold.
  * Max heart rate ≈ **150 bpm** → reflects exercise capacity.

* **Feature stability:**

  * All categorical features show identical category structures.
  * No unseen categories in test set.
  * High structural integrity.

* **Outlier behavior:**

  * Strong outliers in BP, HR, cholesterol, ST depression.
  * Represent high-risk cardiac patients.
  * Preserved for realistic modeling.

---

### 📚 Statistical Findings

| Variable Type                    | Test Method                             | Result                              | Interpretation                                                      |
| -------------------------------- | --------------------------------------- | ----------------------------------- | ------------------------------------------------------------------- |
| Categorical variables            | **Chi-Square**                          | Significant associations detected   | Diagnostic and demographic factors influence heart disease presence |
| Binary risk indicators           | **Mann–Whitney U / T-Test**             | Significant differences             | Clear separation between disease and non-disease groups             |
| Multi-group categorical features | **Kruskal–Wallis + Dunn**               | Multiple groups differ              | Behavioral and clinical patterns vary across groups                 |
| Numerical clinical indicators    | **Normality + ANOVA / Welch / Kruskal** | Mostly non-normal distributions     | Non-parametric methods recommended                                  |
| Variance comparison              | **Levene’s Test**                       | Heteroscedasticity in some features | Welch ANOVA preferred in several cases                              |

(Results consolidated from statistical modules in the notebook.)

---

## 📌 Top Observed Risk Indicators

Consistent signals across EDA and statistical testing:

* Elevated blood pressure
* High cholesterol levels
* Reduced maximum heart rate
* Increased ST depression
* Presence of exercise-induced angina
* Abnormal thallium scan results
* Multiple affected coronary vessels
* Severe chest pain types
* Fasting blood sugar abnormalities

These indicators show strong associations with heart disease presence.

---

## 🚀 Modeling Framework (Prepared)

The notebook includes configurations for advanced modeling:

* XGBoost
* LightGBM
* CatBoost
* Stratified K-Fold Cross Validation
* Optuna Hyperparameter Optimization
* ROC-AUC / PR-AUC Evaluation

Ready for future supervised learning experiments.

---

## 👤 Author

**Name:** Đào Minh Thuấn
**GitHub:** [https://github.com/daominhthuan42](https://github.com/daominhthuan42)
