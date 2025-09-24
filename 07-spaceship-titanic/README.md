# 🚀 Spaceship Titanic - Kaggle Competition

## 📌 Overview

In the year **2912**, the interstellar passenger liner **Spaceship Titanic** collided with a spacetime anomaly. Many passengers were mysteriously **transported to another dimension**.

Competition link: [Spaceship Titanic (Kaggle)](https://www.kaggle.com/competitions/spaceship-titanic)

**Goal:** Build a machine learning model to predict whether a passenger was **transported or not** (`Transported` = True/False).

## 📂 Dataset Information

**Training set:** 8,693 passengers (with labels).
**Test set:** 4,277 passengers (without labels).
**Target variable:**

* `Transported`: True if transported to another dimension, False otherwise.

### 🔑 Key Features

* **PassengerId** → Unique ID (group/family encoded as `gggg_pp`).
* **HomePlanet** → Origin planet (Earth, Europa, Mars).
* **CryoSleep** → Passenger in suspended animation (True/False).
* **Cabin** → Cabin assignment (Deck/Num/Side).
* **Destination** → Planet of destination (TRAPPIST-1e, 55 Cancri e, PSO J318.5-22).
* **Age** → Passenger age.
* **VIP** → VIP service purchased (True/False).
* **RoomService, FoodCourt, ShoppingMall, Spa, VRDeck** → Expenditure on ship amenities.
* **Name** → Passenger name (not predictive, often dropped).

## 🎯 Objectives

* Perform **EDA**: explore distributions, missing values, correlations.
* **Feature Engineering**: split cabin into `Deck`, `Number`, `Side`; encode categoricals.
* Train models: Logistic Regression, Random Forest, Gradient Boosting, XGBoost, LightGBM.
* Evaluate performance with Accuracy, F1-score, ROC-AUC.
* Generate predictions for Kaggle submission.

## 🛠 Methodology & Tools

* **Data Preprocessing:** handle missing values, encode categorical features, scale numerical data.
* **Visualization:** Matplotlib, Seaborn.
* **Feature Engineering:** derived features (e.g., family grouping, log-transformed spending).
* **Modeling:** ensemble methods (Random Forest, XGBoost, LightGBM).
* **Evaluation:** cross-validation, confusion matrix, accuracy (for leaderboard).

## 📊 Key Insights

* **HomePlanet** and **Destination** strongly influence survival (transportation) rates.
* **CryoSleep** correlates heavily with transportation (most cryosleep passengers were transported).
* **Spending on amenities** (Spa, FoodCourt, VRDeck) shows patterns related to transport likelihood.
* **Group travel** (same PassengerId group) impacts predictions: family/friends often share the same fate.

## 🚀 Next Steps

* Handle class imbalance if needed (SMOTE, class weights).
* Hyperparameter tuning with Optuna.
* Model ensembling & stacking for better Kaggle score.
* Build interactive dashboard for predictions.

## 👤 Author

* **Name:** Đào Minh Thuấn.
* **GitHub:** [daominhthuan42](https://github.com/daominhthuan42)
