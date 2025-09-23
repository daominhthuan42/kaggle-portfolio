# 📚 Student Habits vs Academic Performance

## 📌 Overview

This project analyzes the **Student Habits vs Academic Performance** dataset from Kaggle.
The dataset simulates **1,000 students’ daily habits** (study time, sleep, social media, diet, mental health, etc.) and compares them with their **academic exam scores**.

👉 Dataset link: [Student Habits vs Academic Performance (Kaggle)](https://www.kaggle.com/datasets/jayaantanaath/student-habits-vs-academic-performance)

The aim of this project is to:

* Explore lifestyle factors that affect academic outcomes
* Build regression models to predict exam scores
* Provide insights for students, parents, and educators

## 📂 Dataset Information

**Size:** 1,000 records, 15+ features
**Target variable:** `exam_score`

### 🔑 Key Features

* **Student Info:** `student_id`, `Age`, `gender`, `parental_education_level`
* **Academic Performance:** `attendance_percentage`, `study_hours_per_day`
* **Well-being & Lifestyle:** `sleep_hours`, `exercise_frequency`, `mental_health_rating`
* **Digital Habits:** `social_media_hours`, `netflix_hours`, `internet_quality`
* **Diet & Daily Routine:** `diet_quality`
* **Other Factors:** `part_time_job`, `extracurricular_participation`

## 🎯 Objectives

* Perform **EDA**: distributions, correlations, insights into lifestyle habits
* Study the impact of **study hours, sleep, and social media use** on exam scores
* Build regression models (Linear Regression, XGBoost) to predict exam scores
* Evaluate with metrics like **R²** and **RMSE**
* Provide recommendations for improving student performance

## 🛠 Methodology & Tools

* **Data Cleaning:** handle missing values (e.g., `parental_education_level`)
* **EDA:** visualizations of numerical & categorical features
* **Feature Engineering:** encoding categorical variables, scaling numerical ones
* **Modeling:** Linear Regression, XGBoost, tuned hyperparameters
* **Evaluation:** Cross-validation, metrics (R², RMSE)

## 📊 Key Insights

* Students with **higher study hours** and **better attendance** tend to score higher
* **Excessive social media and Netflix use** negatively impacts performance
* **Healthy sleep (6–8 hours)** correlates positively with higher exam scores
* **Active lifestyle (exercise, extracurriculars)** shows positive influence
* **Poor diet quality & low mental health** are associated with lower scores

## 🚀 Next Steps

* Try additional models (Random Forest, LightGBM)
* Explore feature interactions (sleep + study hours, social media + mental health)
* Build clustering models to segment students into **performance profiles**
* Create a dashboard for educators and students

## 👤 Author

* **Name:** Đào Minh Thuấn
* **GitHub:** [daominhthuan42](https://github.com/daominhthuan42)
