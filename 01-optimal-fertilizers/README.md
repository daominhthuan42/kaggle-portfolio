# 🌱 Predicting Optimal Fertilizers for Precision Agriculture 🌤

## 📌 Overview

This project focuses on **predicting the most suitable fertilizer** for different crops and soil conditions, aiming to promote **precision agriculture** that enhances crop yield while minimizing environmental impact.
Using a synthetic dataset that simulates diverse agricultural environments, the goal is to build a robust **multi-class classification model** to recommend the optimal fertilizer based on soil nutrients, temperature, humidity, and crop type.

Dataset link: [Predicting Optimal Fertilizers (Kaggle)](https://www.kaggle.com/competitions/playground-series-s5e6)

**Goals:**

* Predict the **optimal fertilizer** for a given set of environmental and soil parameters.
* Analyze soil, nutrient, and crop characteristics to uncover **key agricultural patterns**.
* Enhance fertilizer use efficiency and reduce waste through **data-driven insights**.

## 📂 Dataset Information

**Size:**

* Train: 750,000 records
* Test: 250,000 records
* Original Source: 100,000 records

**Target variable:**

* `Fertilizer_Name` → categorical (7 classes)

### 🔑 Key Features

| Feature           | Description                                     |
| ----------------- | ----------------------------------------------- |
| `Temperature`     | Average temperature (°C)                        |
| `Humidity`        | Relative humidity (%)                           |
| `Moisture`        | Soil moisture content (%)                       |
| `Soil_Type`       | Type of soil (Sandy, Loamy, Clayey, Red, Black) |
| `Crop_Type`       | Crop name (Paddy, Maize, Sugarcane, etc.)       |
| `Nitrogen`        | Nitrogen content (ppm)                          |
| `Phosphorous`     | Phosphorous content (ppm)                       |
| `Potassium`       | Potassium content (ppm)                         |
| `Fertilizer_Name` | Optimal fertilizer label (target)               |

**Files Provided:**

* `train.csv` — labeled training dataset
* `test.csv` — unlabeled test dataset
* `sample_submission.csv` — competition submission template

## 🎯 Objectives

* Conduct **comprehensive EDA** to understand feature distributions, relationships, and target patterns.
* Perform **data quality checks**: missing values, duplicates, outliers, and consistency across datasets.
* **Engineer features** such as nutrient ratios (N/P, N/K) and categorical encodings.
* Build and evaluate multiple ML models:

  * Random Forest
  * LightGBM
  * CatBoost
  * XGBoost
* Optimize models using **Optuna** and **GridSearchCV**.
* Evaluate with **MAP@3**, **Accuracy**, and **Confusion Matrix**.

## 🛠 Methodology & Tools

| Stage                   | Techniques & Tools                                                                                  |
| ----------------------- | --------------------------------------------------------------------------------------------------- |
| **Data Cleaning**       | Removal of duplicates, missing value checks (none detected), and type validation                    |
| **EDA & Visualization** | Histograms, boxplots, heatmaps, violin plots, statistical tests (ANOVA, Kruskal-Wallis, Chi-Square) |
| **Feature Engineering** | Scaling, encoding (OneHot/Categorical), and memory optimization                                     |
| **Model Training**      | Multi-class classification with ensemble algorithms                                                 |
| **Evaluation**          | Stratified K-Fold cross-validation, MAP@3 metric, feature importance                                |

**Libraries Used:**
`pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, `optuna`, `xgboost`, `catboost`, `statsmodels`, `pingouin`, `scikit_posthocs`, `shap`.

## 📊 Key Insights

### 🌾 Data Quality

* No **missing values**, **duplicates**, or **outliers** across all datasets.
* Train/Test distributions align closely with the Original dataset, ensuring **no data leakage**.

### 🧮 Numerical Features

* Six numeric variables show **stable distributions** with mean temperature ≈ 31.5°C, humidity ≈ 61%, and moisture ≈ 45%.
* **Skewness ≈ 0**, indicating symmetrical distributions — no transformation needed.
* No strong correlations among nutrients or environmental factors (|r| < 0.1).

### 🌍 Categorical Features

* 5 soil types and 11 crop types, all **well-balanced** across datasets.
* Top soil: *Sandy (20.9%)*; Top crop: *Paddy (11.4%)*.
* Suitable for One-Hot Encoding or CatBoost native categorical handling.

### 🌿 Target Variable

* 7 fertilizer classes: `28-28`, `17-17-17`, `10-26-26`, `DAP`, `20-20`, `14-35-14`, `Urea`.
* Balanced class distribution (~14% per class) → ideal for multi-class classification.

## 📈 Statistical Insights

* **Chi-Square tests** confirm strong dependency between soil/crop type and fertilizer selection.
* **ANOVA and Kruskal-Wallis tests** show that nitrogen, potassium, and moisture significantly differ by fertilizer class.
* **No multicollinearity** detected — independent features contribute uniquely.

## 🚀 Next Steps

* Apply **SHAP analysis** for interpretability and explainable AI in fertilizer prediction.
* Experiment with **stacked ensemble models** to enhance predictive accuracy.
* Incorporate **geographical and seasonal data** for real-world deployment.
* Build a **fertilizer recommendation system** for farmers via web app or API.


## 👤 Author

**Name:** Đào Minh Thuấn
**GitHub:** [daominhthuan42](https://github.com/daominhthuan42)
**Project Type:** EDA + Multi-class ML Model for Sustainable Agriculture
