# 🚢 Titanic - Machine Learning from Disaster

## 📌 Overview

The **Titanic competition** is one of the most famous beginner challenges on Kaggle.
It uses real passenger data from the **RMS Titanic (1912)** tragedy to predict survival outcomes.

Competition link: [Titanic on Kaggle](https://www.kaggle.com/competitions/titanic)

This project applies a full **ML pipeline** (EDA → Preprocessing → Feature Engineering → Modeling → Evaluation → Submission).

## 📂 Dataset Information

**Training set:** 891 passengers (with labels).
**Test set:** 418 passengers (without labels).
**Target variable:**

* `Survived` → 1 = Survived, 0 = Did not survive.

### 🔑 Key Features

* **Pclass** → Ticket class (1 = 1st, 2 = 2nd, 3 = 3rd).
* **Sex** → Gender (male/female).
* **Age** → Passenger age in years.
* **SibSp** → Number of siblings/spouses aboard.
* **Parch** → Number of parents/children aboard.
* **Fare** → Ticket fare.
* **Embarked** → Port of embarkation (C = Cherbourg, Q = Queenstown, S = Southampton).
* **Cabin** → Cabin number (many missing values).
* **Name, Ticket, PassengerId** → Passenger identifiers.

## 🎯 Objectives

* Perform **EDA**: distributions, missing values, survival rates by feature.
* **Feature Engineering**: handle missing values, create `FamilySize`, extract titles from names, log-transform `Fare`.
* Train classification models: Logistic Regression, Random Forest, Gradient Boosting, XGBoost, LightGBM.
* Evaluate model performance with Accuracy, ROC-AUC, Confusion Matrix.
* Generate predictions for Kaggle submission.

## 🛠 Methodology & Tools

* **Data Cleaning:** missing value imputation (`Age`, `Embarked`, `Fare`), drop irrelevant features (`Ticket`, `Cabin`).
* **EDA & Visualization:** Matplotlib, Seaborn.
* **Feature Engineering:** categorical encoding, derived features (titles, family size).
* **Modeling:** Logistic Regression, Decision Tree, Random Forest, Gradient Boosting, XGBoost.
* **Evaluation:** Accuracy (for Kaggle), ROC-AUC, F1-score.

## 📊 Key Insights

* **Sex** is the strongest predictor: survival rate of females is significantly higher.
* **Pclass** is critical: 1st class passengers had much higher survival probability.
* 👨‍👩Passengers traveling with family (`FamilySize > 1`) had higher chances of survival.
* Higher **Fare** correlates with higher survival probability.
* **Embarked** also plays a role: passengers from Cherbourg had better survival rates.

## 🚀 Next Steps

* Improve feature engineering (cabin grouping, ticket family extraction).
* Perform **hyperparameter tuning** with Optuna.
* Use **stacking / ensemble models** for higher Kaggle scores.
* Deploy as a simple web app for Titanic survival prediction.

## 👤 Author

* **Name:** Đào Minh Thuấn
* **GitHub:** [daominhthuan42](https://github.com/daominhthuan42)
