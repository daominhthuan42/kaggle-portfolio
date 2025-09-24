# 🏢 IBM HR Analytics - Employee Attrition

## 📌 Overview

Employee attrition (turnover) is a critical challenge for organizations, impacting productivity, morale, and costs.
This project analyzes the **IBM HR Analytics Employee Attrition dataset** to explore factors leading to attrition and to build predictive models that help HR departments identify employees at risk of leaving.

Dataset link: [IBM HR Analytics Employee Attrition (Kaggle)](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset)

## 📂 Dataset Information

**Size:** 1,470 employees, 35+ features.
**Target variable:** `Attrition` (Yes / No).

### 🔑 Key Features

* **Demographics:** `Age`, `Gender`, `MaritalStatus`
* **Work Conditions:** `BusinessTravel`, `Department`, `DistanceFromHome`, `JobRole`, `OverTime`.
* **Satisfaction & Engagement:** `EnvironmentSatisfaction`, `JobSatisfaction`, `WorkLifeBalance`, `RelationshipSatisfaction`.
* **Career & Income:** `JobLevel`, `MonthlyIncome`, `PercentSalaryHike`, `StockOptionLevel`.
* **Experience:** `TotalWorkingYears`, `YearsAtCompany`, `YearsInCurrentRole`, `YearsSinceLastPromotion`, `YearsWithCurrManager`.
* **Training & Performance:** `TrainingTimesLastYear`, `PerformanceRating`, `JobInvolvement`.

## 🎯 Objectives

* Conduct **EDA** to identify key factors influencing attrition.
* Visualize distributions, correlations, and employee segments.
* Feature engineering: categorical encoding, normalization, removing non-informative features (`EmployeeCount`, `Over18`, `StandardHours`).
* Build ML models: Logistic Regression, Random Forest, Gradient Boosting, XGBoost.
* Evaluate performance using **Accuracy, Precision, Recall, F1-score, ROC-AUC**.
* Provide business recommendations to reduce attrition.

## 🛠 Methodology & Tools

* **Data Cleaning:** drop irrelevant/constant features, encode categoricals.
* **Visualization:** Matplotlib, Seaborn for churn analysis.
* **Feature Engineering:** creation of meaningful groups (e.g., age bands, tenure categories).
* **Modeling:** tree-based models and linear models with hyperparameter tuning.
* **Evaluation:** classification report, confusion matrix, ROC curves.

## 📊 Key Insights

* **OverTime** is one of the strongest predictors of attrition — employees working overtime leave more often.
* **MonthlyIncome**: lower income groups show higher attrition.
* **JobRole & Department**: certain roles (Sales, HR) have higher turnover rates.
* **DistanceFromHome**: employees living farther away are more likely to leave.
* **WorkLifeBalance & JobSatisfaction**: poor scores strongly correlate with attrition.

## 🚀 Next Steps

* Handle potential class imbalance with **SMOTE** or weighted classes.
* Apply **hyperparameter tuning** (Optuna/GridSearchCV) for best models.
* Explore explainability techniques (SHAP, LIME) for HR insights.
* Build dashboard for HR managers to monitor attrition risk.

## 👤 Author

* **Name:** Đào Minh Thuấn.
* **GitHub:** [daominhthuan42](https://github.com/daominhthuan42)
