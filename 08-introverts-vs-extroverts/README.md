# 🙈 Introverts vs Extroverts 🗣️

## 📌 Overview

This project is part of the **Kaggle Playground Series (S5E7)**.
The dataset was synthetically generated from a deep learning model trained on the **Extrovert vs. Introvert Behavior dataset**.

Competition link: [Playground Series - S5E7 (Kaggle)](https://www.kaggle.com/competitions/playground-series-s5e7)

**Goal:** Build a machine learning model to classify whether a person is an **Introvert** or **Extrovert** based on their habits and behaviors.

## 📂 Dataset Information

**Training set:** 18,524 samples, 9 columns (including target).
**Test set:** 6,175 samples, 8 columns (without target).
**Target variable:**

* `Personality`: Extrovert (1) or Introvert (0)

### 🔑 Key Features

| Feature                     | Type        | Description                                 |
| --------------------------- | ----------- | ------------------------------------------- |
| `Time_spent_Alone`          | Numerical   | Hours spent alone daily (0–11)              |
| `Stage_fear`                | Categorical | Presence of stage fright (Yes/No)           |
| `Social_event_attendance`   | Numerical   | Frequency of attending social events (0–10) |
| `Going_outside`             | Numerical   | Frequency of going outside (0–7)            |
| `Drained_after_socializing` | Categorical | Feeling drained after socializing (Yes/No)  |
| `Friends_circle_size`       | Numerical   | Number of close friends (0–15)              |
| `Post_frequency`            | Numerical   | Frequency of posting on social media (0–10) |

## 🎯 Objectives

* Perform **EDA**: distributions, missing values, imbalances, and feature correlations.
* **Feature Engineering**: encode categorical variables, handle missing values.
* Build classification models: Logistic Regression, Random Forest, XGBoost, LightGBM, SVM.
* Evaluate with **Accuracy, F1-score, ROC-AUC, Confusion Matrix**.
* Generate predictions for Kaggle submission.

## 🛠 Methodology & Tools

* **Data Cleaning:** handle missing values in categorical and numerical features.
* **EDA & Visualization:** Matplotlib, Seaborn.
* **Feature Engineering:** one-hot encoding, scaling, interaction terms.
* **Modeling:** Logistic Regression, Random Forest, Gradient Boosting (XGBoost/LightGBM), SVM.
* **Evaluation:** cross-validation, confusion matrix, ROC-AUC.

## 📊 Key Insights

* **Extroverts** show higher values in `Social_event_attendance`, `Friends_circle_size`, `Post_frequency`.
* **Introverts** tend to have higher `Time_spent_Alone` and often feel `Drained_after_socializing`.
* Features such as **Stage\_fear** and **Drained\_after\_socializing** provide strong discriminative power.
* Train/Test distribution is slightly skewed compared to the original dataset (more extroverted behaviors represented).

## 🚀 Next Steps

* Apply **class imbalance techniques** (SMOTE, class weights).
* Try ensemble models and hyperparameter tuning (Optuna).
* Explore explainability (SHAP, LIME) for behavioral insights.
* Deploy as a **web app** for personality prediction.

## 👤 Author

* **Name:** Đào Minh Thuấn.
* **GitHub:** [daominhthuan42](https://github.com/daominhthuan42)
