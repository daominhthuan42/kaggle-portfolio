# 🌌 Stellar Object Classification & Astronomical Pattern Analysis

# 📑 Table of Contents

* [📌 Overview](#-overview)
* [🎯 Project Objectives](#-project-objectives)
* [📂 Dataset Overview](#-dataset-overview)
* [🧾 Feature Description](#-feature-description)
* [🛠️ Tech Stack](#️-tech-stack)
* [🔍 Exploratory Data Analysis (EDA)](#-exploratory-data-analysis-eda)
* [📊 Data Quality Insights](#-data-quality-insights)
* [📈 Statistical Analysis](#-statistical-analysis)
* [🤖 Machine Learning Modeling](#-machine-learning-modeling)
* [🧠 Astronomical Insights](#-astronomical-insights)
* [✅ Conclusion](#-conclusion)
* [🚀 Future Improvements](#-future-improvements)
* [👨‍💻 Author](#-author)

---

# 📌 Overview

Modern astronomical surveys collect enormous amounts of observational data describing stars, galaxies, and quasars. As datasets continue growing, manual classification becomes increasingly difficult and inefficient.

This project focuses on analyzing stellar observations and building a machine learning framework for automatic celestial object classification using:

* Exploratory Data Analysis (EDA)
* Statistical hypothesis testing
* Astronomy-oriented feature engineering
* Machine learning classification
* Astrophysical interpretation

The project aims to discover astronomical patterns and improve automated classification performance for large-scale sky surveys.

---

# 🎯 Project Objectives

Primary goals:

* Explore stellar observation patterns
* Understand relationships between photometric features
* Analyze redshift and spectral characteristics
* Apply statistical testing for feature significance
* Build predictive classification models
* Extract meaningful astrophysical insights

---

# 📂 Dataset Overview

## Dataset Information

| Dataset               |    Rows | Columns |
| --------------------- | ------: | ------: |
| Train                 | 577,347 |      11 |
| Test                  | 247,435 |      10 |
| Original SDSS Dataset | 100,000 |      17 |

Dataset includes:

* Sky coordinate measurements
* Multi-band photometric magnitudes
* Redshift information
* Spectral classifications
* Galaxy population indicators

### 🎯 Target Variable

```python
class = STAR / GALAXY / QSO
```

---

# 🧾 Feature Description

| Feature             | Description                | Astronomy Meaning                      |
| ------------------- | -------------------------- | -------------------------------------- |
| `alpha`             | Right ascension coordinate | Celestial object position              |
| `delta`             | Declination coordinate     | Sky location coordinate                |
| `u`                 | Ultraviolet magnitude      | Photometric brightness                 |
| `g`                 | Green magnitude            | Photometric brightness                 |
| `r`                 | Red magnitude              | Photometric brightness                 |
| `i`                 | Near-infrared magnitude    | Photometric brightness                 |
| `z`                 | Infrared magnitude         | Photometric brightness                 |
| `redshift`          | Redshift value             | Relative distance and expansion effect |
| `spectral_type`     | Stellar spectral category  | Physical stellar properties            |
| `galaxy_population` | Galaxy type category       | Evolutionary population grouping       |
| `class`             | Stellar object type        | Target variable                        |

---

# 🛠️ Tech Stack

## Programming & Processing

* Python
* Pandas
* NumPy
* CuPy

## Visualization

* Matplotlib
* Seaborn

## Statistical Analysis

* Scipy
* Statsmodels
* Pingouin
* Scikit-posthocs

## Astronomy

* Astropy

## Machine Learning

* Scikit-learn
* CatBoost
* XGBoost
* Optuna

---

# 🔍 Exploratory Data Analysis (EDA)

EDA focused on identifying patterns in celestial observations.

Main exploration areas:

### Coordinate Analysis

* `alpha` spans nearly the entire sky coordinate range
* `delta` includes both northern and southern celestial hemispheres

### Photometric Analysis

* Magnitude features (`u`, `g`, `r`, `i`, `z`) show relatively stable distributions
* Different stellar classes exhibit distinct photometric behavior

### Redshift Analysis

* Redshift distribution is strongly right-skewed
* Extreme values likely correspond to distant galaxies and quasars

### Stellar Class Distribution

Observed classes:

* STAR
* GALAXY
* QSO (Quasar)

Each class demonstrates distinguishable observational characteristics.

---

# 📊 Data Quality Insights

## Missing Values

Results:

* Train → No missing values
* Test → No missing values
* Original → No missing values

No imputation process required.

---

## Duplicate Analysis

Results:

* No duplicate records identified
* Each observation appears unique

---

## Outlier Analysis

Important findings:

* `redshift` contains the highest concentration of extreme observations
* Photometric variables show moderate variation
* Outliers likely represent astrophysical phenomena rather than data errors

Because astronomical outliers often contain valuable information, aggressive removal was avoided.

---

# 📈 Statistical Analysis

Statistical methods used:

### Normality Analysis

* Skewness
* Kurtosis
* Q-Q plots

### Variance Testing

* Levene Test

### Group Comparison Tests

* ANOVA
* Welch ANOVA
* Kruskal-Wallis
* Mann-Whitney U
* Tukey HSD
* Dunn Post-hoc Analysis

### Association Testing

* Chi-Square Test

These tests help determine whether observed differences between stellar classes are statistically meaningful.

---

# 🤖 Machine Learning Modeling

Model pipeline:

* Data preprocessing
* Feature engineering
* Encoding
* Stratified K-Fold Cross Validation
* Hyperparameter tuning using Optuna

Models explored:

* CatBoost Classifier
* XGBoost

Evaluation metrics:

```python
Balanced Accuracy Score
Confusion Matrix
Classification Report
```

CatBoost was selected due to:

* Strong performance on tabular data
* Native handling of categorical features
* Reduced preprocessing complexity

---

# 🧠 Astronomical Insights

Key findings:

### Redshift Behavior

* Higher redshift values frequently correspond to distant objects
* Quasars tend to occupy more extreme ranges

### Spectral Distribution

* Spectral characteristics differ substantially across stellar classes

### Dataset Stability

* Train and test datasets maintain highly consistent distributions
* Synthetic competition data appears reliable

### Astrophysical Interpretation

* Photometric features and redshift contain strong predictive information
* Classification depends on combined observational characteristics rather than a single feature

---

# ✅ Conclusion

This project demonstrates how machine learning and statistical analysis can support astronomical research and large-scale sky survey systems.

Main findings:

* High-quality datasets
* Strong class separation patterns
* Meaningful astrophysical outliers
* Useful predictive features for automated classification

The framework provides a scalable approach for stellar object classification.

---

# 🚀 Future Improvements

Potential future work:

* SHAP explainability analysis
* Ensemble modeling
* Deep learning experimentation
* Advanced astrophysical feature engineering
* Real-time astronomical classification dashboard

---

# 👨‍💻 Author

**Đào Minh Thuấn**

Data Analytics | Machine Learning | Astronomy Analytics
