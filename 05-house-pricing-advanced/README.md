# 🏠 House Prices - Advanced Regression Techniques

## 📌 Overview

This project is based on the **Kaggle Competition: House Prices - Advanced Regression Techniques**.
With **79 explanatory variables** describing almost every aspect of residential homes in Ames, Iowa, the challenge is to predict the **final sale price** of each home.

Competition link: [House Prices (Kaggle)](https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques)

## 📂 Dataset Information

**Training set:** 1,460 samples, 81 features (including `SalePrice`).
**Test set:** 1,459 samples, 80 features (excluding target).
**Target variable:**

* `SalePrice`: property’s sale price in dollars.

### 🔑 Key Features

* **Property & Lot:** `MSSubClass`, `LotFrontage`, `LotArea`, `LotShape`, `LandContour`.
* **Location:** `Neighborhood`, `Condition1`, `Condition2`.
* **Dwelling:** `BldgType`, `HouseStyle`, `OverallQual`, `OverallCond`, `YearBuilt`, `YearRemodAdd`.
* **Exterior:** `RoofStyle`, `Exterior1st`, `Exterior2nd`, `MasVnrType`, `ExterQual`.
* **Basement:** `BsmtQual`, `BsmtCond`, `BsmtExposure`, `TotalBsmtSF`.
* **Utilities & Systems:** `Heating`, `CentralAir`, `Electrical`.
* **Interior:** `GrLivArea`, `BedroomAbvGr`, `KitchenQual`, `TotRmsAbvGrd`.
* **Bathrooms:** `FullBath`, `HalfBath`, `BsmtFullBath`, `BsmtHalfBath`.
* **Garage:** `GarageType`, `GarageCars`, `GarageArea`.
* **Extra:** `Fireplaces`, `Fence`, `PoolArea`, `MiscVal`.
* **Sale:** `MoSold`, `YrSold`, `SaleType`, `SaleCondition`.

## 🎯 Objectives

* Perform **Exploratory Data Analysis (EDA)** to understand key drivers of house prices.
* Apply **feature engineering**: handle missing values, encode categoricals, create new features.
* Train regression models: Linear Regression, Random Forest, Gradient Boosting, XGBoost, LightGBM, SVR.
* Evaluate model performance with **RMSE (Root Mean Squared Error)**.
* Submit predictions to Kaggle competition.

## 🛠 Methodology & Tools

* **Data Preprocessing:** missing value imputation, outlier treatment, scaling.
* **Visualization:** Matplotlib, Seaborn.
* **Feature Engineering:** log transformation, polynomial features, categorical encoding.
* **Modeling:**

  * Linear Regression.
  * Random Forest.
  * Gradient Boosting (XGBoost, LightGBM).
  * Support Vector Regression (SVR).
* **Evaluation:** Cross-validation, Kaggle leaderboard RMSE.

## 📊 Key Insights

* **Overall Quality (`OverallQual`)** strongly correlates with `SalePrice`.
* **Living Area (`GrLivArea`)** is one of the most important predictors.
* **Neighborhood** has a significant influence on housing prices.
* Features like **GarageCars**, **TotalBsmtSF**, **YearBuilt** are highly relevant.
* Handling missing data (e.g., `LotFrontage`, `Alley`, `PoolQC`) is crucial for model performance.

## 🚀 Next Steps

* Feature selection & dimensionality reduction (PCA, feature importance).
* Advanced hyperparameter tuning with **Optuna / GridSearchCV**.
* Model ensembling & stacking to improve Kaggle leaderboard score.
* Build a Streamlit dashboard for interactive house price predictions.

## 👤 Author

* **Name:** Đào Minh Thuấn
* **GitHub:** [daominhthuan42](https://github.com/daominhthuan42)
