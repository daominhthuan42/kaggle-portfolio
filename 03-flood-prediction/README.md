# 🌪️ Flood Prediction Analysis 🌩️

## 📌 Overview

In a world increasingly affected by climate change and extreme weather events, predicting flood risks has become crucial for disaster preparedness and urban planning.
This project analyzes the **Flood Prediction dataset** and builds machine learning models to predict the probability of flood occurrence based on environmental, infrastructural, and socio-economic factors.

Competition link: [Playground Series - S4E5 (Kaggle)](https://www.kaggle.com/competitions/playground-series-s4e5)
Full dataset: [Flood Prediction Dataset (Kaggle)](https://www.kaggle.com/competitions/playground-series-s4e5/data)

## 📂 Dataset Information

**Training set:** 1,117,957 samples, 22 columns.
**Test set:** 745,305 samples, 21 columns.
**Original dataset:** Synthetic data generated using data simulation techniques.

**Target variable:**

* `FloodProbability`: Probability of flood occurrence (0 → 1).

### 🔑 Key Features

* **Environmental Factors:** `MonsoonIntensity`, `TopographyDrainage`, `ClimateChange`, `Landslides`, `Watersheds`, `Siltation`.
* **Infrastructure:** `DamsQuality`, `DrainageSystems`, `DeterioratingInfrastructure`, `RiverManagement`.
* **Human Impact:** `Urbanization`, `Deforestation`, `AgriculturalPractices`, `Encroachments`.
* **Governance:** `PoliticalFactors`, `IneffectiveDisasterPreparedness`, `InadequatePlanning`.
* **Risk Factors:** `CoastalVulnerability`, `PopulationScore`, `WetlandLoss`.
* **ID column:** unique identifier in training data (not predictive).

## 🎯 Objectives

* Perform **EDA**: distributions, correlations, outliers analysis.
* **Feature Engineering**: interaction features, risk indices, nonlinear transformations.
* Train ML models: CatBoost Regressor with hyperparameter optimization.
* Evaluate with **R² Score (Coefficient of Determination)**.
* Generate Kaggle submissions and provide actionable insights.

## 🛠 Methodology & Tools

* **Data Cleaning:** memory optimization, duplicate detection, outlier analysis.
* **Visualization:** Matplotlib, Seaborn (distribution analysis, correlation heatmaps).
* **Feature Engineering:** interaction features, grouped risk indices, power transformations.
* **Modeling:** CatBoost Regressor with Optuna hyperparameter tuning.
* **Evaluation:** cross-validation, residual analysis, SHAP feature importance.

## 📊 Key Insights

* **Feature Distributions** are approximately symmetric with low skewness (0.42-0.46), indicating well-balanced synthetic data.
* **Weak Individual Correlations** with target variable suggest complex non-linear relationships requiring ensemble methods.
* **InfrastructureRisk, NaturalRisk, GovernanceRisk** are the most influential factors based on SHAP analysis.
* **Feature Engineering** significantly improved model performance through interaction terms and risk indices.
* **CatBoost Model** achieved **R² = 0.8512** on validation set, demonstrating strong predictive capability.

## 🚀 Next Steps

* Apply **ensemble methods** combining multiple algorithms (CatBoostRegressor).
* Hyperparameter tuning with **Optuna** for optimal performance.
* Add **temporal features** and **geospatial analysis** if available.
* Implement **model interpretability** tools for better understanding.

## 👤 Author

* **Name:** Đào Minh Thuấn.
* **GitHub:** [daominhthuan42](https://github.com/daominhthuan42)
