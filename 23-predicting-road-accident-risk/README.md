# 🚦 Predicting Road Accident Risk 🚗💥

## 📌 Overview

Road crashes are driven by a mix of **infrastructure**, **environment**, and **time-of-day** factors.
This project is based on the **Kaggle Playground Series – S5E10**, which challenges participants to predict a **continuous accident risk score** for road segments.

Competition link: [Playground S5E10 – Predicting Road Accident Risk](https://www.kaggle.com/competitions/playground-series-s5e10)
Notebook reference: *Accident Risk – Comprehensive EDA & ML Pipeline*. ([Kaggle][1])

**Goal:**

* Explore which features most influence **accident risk**.
* Build robust **regression models** to predict a risk score ∈ [0, 1].
* Provide insights for **road-safety planning** and **preventive measures**.

## 📂 Dataset Information

**Training set:** 517,754 rows, 14 columns (incl. target).
**Test set:** 172,585 rows, 13 columns (same structure, no target).
**Identifier:** `id` (dropped before modeling).
**Target variable:**

* `accident_risk` → Continuous likelihood score in **[0, 1]**.

### 🔑 Key Features (from competition data)

* **Numeric**

  * `curvature` — road curvature intensity.

* **Categorical / Binary**

  * `num_lanes`, `speed_limit`, `num_reported_accidents`
  * `road_type`, `lighting`, `weather`, `time_of_day`
  * `road_signs_present`, `public_road`, `holiday`, `school_season`

> Notes from EDA:
>
> * `curvature` shows a **moderate positive correlation (~0.54)** with `accident_risk` (higher curvature → higher risk).
> * No missing values observed; categorical fields are consistent across train/test.

### 🧪 Engineered Features (used in notebook)

* `high_risk_condition` (e.g., **high speed** + **foggy/rainy**).
* `expected_light_condition` (mismatch between time-of-day and lighting).
* `holiday_public_risk` (public holidays on public roads).
* `school_rush_hour_risk` (school season + morning/afternoon peaks).
* `is_holiday_night` (holiday & night combo).

## 🎯 Objectives

* **EDA:** distributions, target behavior, correlation checks.
* **Feature Engineering:** risk heuristics & interaction flags above.
* **Modeling (regression):**

  * Linear: **Ridge**, **Lasso**
  * Gradient boosting: **CatBoost**, **LightGBM**, **XGBoost**
  * **VotingRegressor** ensemble
* **Validation & Metrics:** 5-Fold CV with **RMSE** (Root Mean Squared Error). ([Kaggle][2])

## 🛠 Methodology & Tools

* **Data Cleaning:** drop `id`; set categorical dtypes; type optimizations.
* **Preprocessing:**

  * `ColumnTransformer` → `StandardScaler` for `curvature`, `OneHotEncoder` for categoricals (handle_unknown="ignore").
* **CV & Training:** `KFold(n_splits=5, shuffle=True, random_state=42)`.
* **Ensembling:** Weighted **VotingRegressor** combining CatBoost, XGB, LGBM, Ridge, Lasso.
* **Interpretability:** SHAP for global/local feature attributions (notebook section).

## 📊 Key Insights

* **Curvature** is a meaningful driver of risk (≈0.54 correlation).
* **Adverse conditions** (fog/rain) at **high speed** raise risk notably.
* **Lighting mismatches** (e.g., *morning* with *dim/night* lighting) associate with higher risk.
* **Holiday & night** and **school-season rush hours** present elevated risk patterns.

## 🧾 Model Performance (from notebook)

* **VotingRegressor (5-Fold CV)** → **RMSE ≈ 0.056**
  → Small error on a [0, 1] target, predictions align closely with actuals; slight underestimation for very high-risk cases.

## 🚀 Next Steps

* Swap Voting → **StackingRegressor** for learned meta-weights.
* Calibrate predictions (e.g., isotonic) for top-risk ranges.
* SHAP-driven feature pruning & interaction exploration.
* Package as a **risk-scoring service** (batch & real-time).

## 👤 Author

* **Name:** Đào Minh Thuấn
* **GitHub:** [daominhthuan42](https://github.com/daominhthuan42)
