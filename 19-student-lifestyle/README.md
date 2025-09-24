# 🎓 Student Lifestyle & Stress Prediction 📚

## 📌 Overview

This project explores the **lifestyle patterns of university students** and their relationship with **stress levels and academic performance**.
The dataset provides insights into how students allocate their time to **studying, sleeping, socializing, extracurriculars, and physical activities**, along with GPA and self-reported stress levels.

Dataset link: [Student Lifestyle Dataset (Kaggle)](https://www.kaggle.com/datasets/steve1215rogg/student-lifestyle-dataset)

**Goals:**

* Explore lifestyle habits and their impact on **stress and GPA**.
* Build predictive models to estimate **Stress Level** based on lifestyle features.
* Provide insights for students, educators, and policymakers to promote balanced living.

## 📂 Dataset Information

**Size:** 2,000 records, 8 features.
**Target variable:**

* `Stress_Level` → categorical (Low / Medium / High).

### 🔑 Key Features

| Feature                           | Description                               |
| --------------------------------- | ----------------------------------------- |
| `Student_ID`                      | Unique student identifier                 |
| `Study_Hours_Per_Day`             | Hours spent studying daily                |
| `Extracurricular_Hours_Per_Day`   | Hours spent on extracurricular activities |
| `Sleep_Hours_Per_Day`             | Average daily sleep hours                 |
| `Social_Hours_Per_Day`            | Hours of social interaction               |
| `Physical_Activity_Hours_Per_Day` | Hours spent on physical activities        |
| `GPA`                             | Grade Point Average (0–4 scale)           |
| `Stress_Level`                    | Reported stress level (target)            |

## 🎯 Objectives

* Perform **EDA**: analyze lifestyle distributions and correlations with stress & GPA.
* **Feature Engineering**: derive balanced lifestyle scores, normalize continuous features.
* Train ML models:

  * Logistic Regression.
  * Random Forest.
  * Gradient Boosting (XGBoost/LightGBM).
* Evaluate with **Accuracy, F1-score, Confusion Matrix**.

## 🛠 Methodology & Tools

* **Data Cleaning:** check missing/duplicate values (dataset is clean).
* **EDA & Visualization:** histograms, boxplots, correlation heatmaps.
* **Modeling:** classification models to predict Stress Level.
* **Evaluation:** cross-validation with standard classification metrics.

## 📊 Key Insights

* Students study on average **7.5 hours/day**, suggesting heavy academic workloads.
* **Sleep hours (7–8h/day)** appear healthy, but students sleeping <6h tend to show **higher stress**.
* Physical activity varies widely (0–13h/day), strongly linked to stress and GPA balance.
* Social hours differentiate **introverted vs extroverted** students, influencing stress coping.
* GPA distribution is stable (mean \~3.1), limiting its predictive power compared to lifestyle variables.

## 🚀 Next Steps

* Test **ensemble models** (LightGBM, CatBoost) for better prediction.
* Investigate **multi-class classification with imbalance handling**.
* Provide **policy recommendations** for universities.

## 👤 Author

* **Name:** Đào Minh Thuấn.
* **GitHub:** [daominhthuan42](https://github.com/daominhthuan42)
