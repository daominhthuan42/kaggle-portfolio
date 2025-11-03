# 🩺 Prediction of Cirrhosis Outcomes ⚕️

## 📌 Overview

**Liver cirrhosis** is a chronic liver disease that can progress to severe complications or death if not managed properly.
This project aims to **predict the survival outcome (Status)** of cirrhosis patients using demographic, clinical, and biochemical data — helping clinicians identify **high-risk patients** and optimize treatment strategies.

Competition link: [Playground Series - S3E26 (Kaggle)](https://www.kaggle.com/competitions/playground-series-s3e26)

## 📂 Dataset Information

**Training set:** 7,905 samples, 20 columns
**Test set:** 5,271 samples, 19 columns
**Target variable:** `Status` — patient survival outcome:

| Code | Meaning                            |
| ---- | ---------------------------------- |
| C    | Censored (alive at last follow-up) |
| CL   | Censored due to liver transplant   |
| D    | Death                              |

### 🔑 Key Features

**Demographic Attributes**

* `id`: patient identifier
* `Age`: age in days at registration
* `Sex`: biological sex (M/F)
* `N_Days`: days from registration to event (death/transplant/study end)

**Treatment**

* `Drug`: D-penicillamine / Placebo

**Clinical Indicators**

* `Ascites`, `Hepatomegaly`, `Spiders`, `Edema`: clinical signs (Y/N/S)

**Laboratory Measurements**

* `Bilirubin`, `Cholesterol`, `Albumin`, `Copper`, `Alk_Phos`, `SGOT`,
  `Tryglicerides`, `Platelets`, `Prothrombin`, `Stage`

## 🎯 Objectives

* Perform **EDA** to assess class distribution, skewness, outliers, and correlations.
* Apply **statistical testing** (Chi-Square, Kruskal-Wallis, ANOVA, Levene’s).
* Conduct **feature transformation** to handle skewed variables (Yeo-Johnson).
* Build and evaluate multiple **ML models** for multiclass classification.
* Optimize performance using **cross-validation**, **Optuna tuning**, and **ensemble voting**.

## 🛠 Methodology & Tools

* **Libraries:** Pandas, NumPy, Matplotlib, Seaborn, Scikit-Learn, Optuna, CatBoost, LightGBM, XGBoost, SHAP.
* **Data Quality Checks:** no missing or duplicate entries; consistent schema.
* **Feature Engineering:**

  * Transformation: PowerTransformer (Yeo-Johnson).
  * Encoding: One-Hot Encoding for categorical variables.
  * Scaling: StandardScaler for numerical features.
* **Evaluation Metric:** Multi-class Log Loss (competition metric).
* **Cross-Validation:** Stratified K-Fold (n=5) for balanced class evaluation.

## 📊 Key Insights

### 🔬 Data Insights

* No missing values or duplicates across train/test sets.
* High right-skew in biochemical features (`Bilirubin`, `Cholesterol`, `Copper`) corrected by Yeo-Johnson transformation.
* Moderate outliers retained due to clinical relevance.

### 🧠 Statistical Analysis

* **Significant relationships** found between `Status` and:

  * `Ascites`, `Hepatomegaly`, `Spiders`, `Edema`, `Sex`
  * Numerical variables like `Bilirubin`, `Albumin`, `Copper`, `Prothrombin`
* Non-parametric tests (Kruskal-Wallis + Dunn’s post-hoc) revealed strong inter-group differences.

### 💡 Modeling Results

| Model             | Mean LogLoss      | Notes                 |
| ----------------- | ----------------- | --------------------- |
| Gradient Boosting | **0.461**         | Best single model     |
| LightGBM          | 0.487             | Strong generalization |
| CatBoost          | 0.492             | Balanced performance  |
| Voting Ensemble   | **0.445 ± 0.014** | Best overall          |

**Final Ensemble:** Weighted soft voting of (CatBoost + LGBM + GradientBoosting) optimized via Optuna.
**Final Accuracy:** ~83% | **Macro AUC:** 0.90

### 🔍 SHAP Interpretability

Top predictive features:

* **Bilirubin**, **Prothrombin**, **Copper**, **N_Days**, **SGOT**, **Albumin**
* Clinical indicators like `Hepatomegaly` and `Spiders` also contributed meaningfully.

## 🚀 Next Steps

* Apply **model calibration** to refine probability outputs.
* Explore **stacking ensembles** and interpret SHAP clusters.
* Derive **clinical insights**: identify biomarker thresholds for early intervention.

## 👤 Author

**Name:** Đào Minh Thuấn
**GitHub:** [daominhthuan42](https://github.com/daominhthuan42)
