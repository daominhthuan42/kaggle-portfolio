# 🌆 Delhi Air Quality 😷

## 📌 Overview

This project analyzes **daily air pollution levels in Delhi**, one of the most polluted cities in the world.
The dataset contains measurements of **major pollutants** such as PM2.5, PM10, NO₂, SO₂, CO, and Ozone, along with **temporal features** like year, month, holidays, and weekday.

Dataset link: [Delhi Air Quality (Kaggle)](https://www.kaggle.com/datasets/kunshbhatia/delhi-air-quality-dataset)

**Goal:**

* Predict the **Air Quality Index (AQI)**.
* Identify key pollutants affecting AQI.
* Analyze **seasonal and temporal pollution trends**.
* Support **policy-making and mitigation strategies**.

## 📂 Dataset Information

**Size:** 1,461 daily records (2021–2024).
**Target variable:** `AQI` (Air Quality Index).

### 🔑 Key Features

* **Temporal:** `Date`, `Month`, `Year`, `Days` (weekday), `Holidays_Count`.
* **Pollutants:** `PM2.5`, `PM10`, `NO2`, `SO2`, `CO`, `Ozone`.
* **Target:** `AQI`.

## 🎯 Objectives

* Perform **EDA**: distributions, pollutant trends, correlation with AQI.
* **Feature Engineering**: add seasonal flags, weekday/weekend, handle outliers.
* Train regression models to predict AQI:

  * Linear Regression.
  * Random Forest.
  * XGBoost / LightGBM.
* Evaluate with **RMSE, MAE, R²**.

## 🛠 Methodology & Tools

* **Data Cleaning:** outlier handling, type conversions.
* **Visualization:** Seaborn, Matplotlib for pollution trends.
* **Modeling:** Linear, tree-based, and boosting regressors.
* **Evaluation:** Cross-validation, error metrics.

## 📊 Key Insights

* **PM2.5 & PM10** values far exceed WHO safe thresholds → strong drivers of AQI.
* **Seasonal spikes** observed in winter months (linked to stubble burning & weather).
* **NO₂ and CO** levels suggest traffic & industrial contribution.
* **Weekday vs Weekend:** some variation due to work/traffic patterns.
* **Holidays** slightly affect pollution (lower traffic = marginally lower AQI).

## 👤 Author

* **Name:** Đào Minh Thuấn.
* **GitHub:** [daominhthuan42](https://github.com/daominhthuan42)
