# 🎓 Predicting Student Exam Scores from Academic & Lifestyle Factors 📚

## 📌 Overview

This project focuses on **predicting students’ final exam scores (`exam_score`)** using a diverse set of **demographic, behavioral, lifestyle, and academic environment features**.

The dataset is a **large-scale, synthetically expanded educational dataset** derived from a realistic student performance source.
It enables **in-depth Exploratory Data Analysis (EDA)**, **statistical inference**, and **robust regression modeling** at scale.

**Competition source:**
*Kaggle Playground Series – Season 6, Episode 1*
*Predicting Student Test Scores*

## 📂 Dataset Information

**Train:** 630,000 rows
**Test:** 270,000 rows
**Original source:** 20,000 rows

**Target variable:**
`exam_score` — Continuous numeric value representing the student’s final exam score.

### 🔢 Numerical Features

Academic engagement & lifestyle indicators:

* `age`
* `study_hours` (average daily study hours)
* `class_attendance` (attendance percentage)
* `sleep_hours` (average daily sleep duration)

### 🏷 Categorical Features

Demographic, behavioral & environment-related variables:

* `gender`
* `course`
* `internet_access`
* `sleep_quality`
* `study_method`
* `facility_rating`
* `exam_difficulty`

### 🧾 Identifiers (Dropped before modeling)

* `id`, `student_id`

## 🧪 Data Integrity & Quality

✔ **No missing values** across Train, Test, and Original datasets
✔ **No duplicate rows detected**
✔ **No numerical outliers** (validated via IQR method)

> The datasets exhibit **exceptionally clean structure**, indicating a controlled and reliable data generation process.

Memory optimization opportunities were identified:

* Convert categorical `object` columns → `category`
* Downcast numerical dtypes where applicable

## 🎯 Project Objectives

* Perform **comprehensive EDA** on student performance drivers
* Analyze **study habits, attendance, sleep, and learning environments**
* Validate relationships using **statistical hypothesis testing**
* Engineer meaningful interaction features
* Train a **high-performance regression model**
* Ensure **robust generalization** through cross-validation

## 🛠 Methodology

### 📊 Exploratory Data Analysis (EDA)

* Distribution analysis (histograms, skewness, kurtosis)
* Q–Q plots for normality inspection
* Outlier detection via IQR
* Cross-dataset distribution consistency checks

### 📐 Statistical Analysis Framework

**Categorical vs Target**

* Chi-Square tests of independence
* Standardized residual heatmaps for group-level insights

**Numerical vs Categorical**

* Normality checks (Skewness, Kurtosis, Q–Q plots)
* Levene’s test (variance homogeneity)
* One-Way ANOVA / Welch ANOVA
* Kruskal–Wallis + Dunn post-hoc tests
* Mann–Whitney U & Independent T-Tests (binary cases)
* Effect size reporting (Cohen’s d, r)

> Statistical test selection is **automatically guided by distributional assumptions**, ensuring methodological correctness.

## 🧠 Feature Engineering

* Label encoding for categorical variables
* Feature scaling for numerical columns
* Interaction features (e.g. `study_hours × sleep_quality`)
* Removal of non-informative identifiers

## 🤖 Modeling Approach

* **Model:** LightGBM Regressor (CPU-optimized)
* **Validation:** K-Fold Cross-Validation (K = 5)
* **Metric:** RMSE
* **Optimization:** Manual tuning + Optuna-ready configuration
* **Explainability:** SHAP values for feature importance analysis

## 📊 Key Data Insights

### 📌 Numerical Feature Patterns

* **Age:**
  Mean ≈ 20.5 (range 17–24)
  → Homogeneous undergraduate-level population

* **Study Hours:**
  Mean ≈ 4.0 hrs/day (0.08 – 7.9)
  → High behavioral variability

* **Class Attendance:**
  Mean ≈ 71% (≈41% – 99%)
  → Strong engagement signal with wide dispersion

* **Sleep Hours:**
  Mean ≈ 7.0 hrs/day (4.1 – 9.9)
  → Mostly healthy sleep patterns, but still impactful

### 📌 Categorical Feature Stability

* No unseen categories in Test set
* Category cardinality consistent across all datasets
* Most stable features:

  * `exam_difficulty`
  * `facility_rating`
* Most imbalanced features:

  * `internet_access`
  * `exam_difficulty`

> No distributional drift detected → **train–test alignment is strong**

## 📈 Key Takeaways

* Student performance is driven by a **combination of behavior, environment, and lifestyle**
* Attendance and study habits show **strong explanatory power**
* Dataset quality allows focus on **modeling & insight generation**, not cleaning
* Large-scale structure supports **robust generalization**

## 👤 Author

**Name:** Đào Minh Thuấn
**GitHub:** [https://github.com/daominhthuan42](https://github.com/daominhthuan42)
