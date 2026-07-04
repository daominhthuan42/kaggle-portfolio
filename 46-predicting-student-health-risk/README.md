# 🩺 Student Health Risk Prediction & Wellness Behavior Analysis

# 📑 Table of Contents

* [📌 Overview](#-overview)
* [🎯 Project Objectives](#-project-objectives)
* [📂 Dataset Overview](#-dataset-overview)
* [🧾 Feature Description](#-feature-description)
* [🛠️ Tech Stack](#️-tech-stack)
* [🔍 Exploratory Data Analysis (EDA)](#-exploratory-data-analysis-eda)
* [📊 Overall Health Behavior Insights](#-overall-health-behavior-insights)
* [🤖 Machine Learning Modeling](#-machine-learning-modeling)
* [📈 Model Performance](#-model-performance)
* [🧠 Top Feature Importance Insights](#-top-feature-importance-insights)
* [💡 Health Recommendations](#-health-recommendations)
* [✅ Conclusion](#-conclusion)
* [🚀 Future Improvements](#-future-improvements)
* [👨‍💻 Author](#-author)

---

# 📌 Overview

Student health and lifestyle behaviors play a major role in academic performance, mental well-being, and long-term quality of life. Modern health monitoring systems increasingly rely on behavioral and physiological data to identify individuals at risk and support preventive intervention.

This project focuses on predicting overall student health condition using:

* Exploratory Data Analysis (EDA)
* Statistical testing
* Data quality assessment
* Machine Learning modeling
* Health-oriented recommendations

The objective is to identify the key factors associated with student health risk and develop predictive models capable of supporting wellness monitoring systems.

---

# 🎯 Project Objectives

The primary goals of this project are:

* Analyze student lifestyle behaviors and health patterns
* Identify major factors affecting health conditions
* Detect potential health-risk indicators
* Build predictive machine learning models
* Generate actionable health recommendations
* Support data-driven wellness interventions

---

# 📂 Dataset Overview

## Dataset Information

| Dataset  |    Rows | Columns |
| -------- | ------: | ------: |
| Train    | 690,088 |      15 |
| Test     | 295,753 |      14 |
| Original |  50,000 |      16 |

The dataset contains:

* Physiological measurements
* Lifestyle behavior information
* Dietary patterns
* Physical activity indicators
* Stress and sleep characteristics
* Demographic information

### 🎯 Target Variable

```python
health_condition = Healthy / At-risk / Unhealthy
```

---

# 🧾 Feature Description

| Feature                   | Description                | Health Meaning                     |
| ------------------------- | -------------------------- | ---------------------------------- |
| `sleep_duration`          | Average sleep duration     | Measures sleep adequacy            |
| `heart_rate`              | Resting heart rate         | Indicates cardiovascular condition |
| `bmi`                     | Body Mass Index            | Measures weight-health balance     |
| `calorie_expenditure`     | Daily calories burned      | Reflects metabolic activity        |
| `step_count`              | Daily step count           | Represents physical movement       |
| `exercise_duration`       | Daily exercise duration    | Indicates exercise behavior        |
| `water_intake`            | Daily water consumption    | Measures hydration quality         |
| `diet_type`               | Dietary pattern            | Reflects nutritional habits        |
| `stress_level`            | Self-reported stress level | Indicates emotional condition      |
| `sleep_quality`           | Sleep quality rating       | Represents sleep effectiveness     |
| `physical_activity_level` | Activity category          | Measures lifestyle intensity       |
| `smoking_alcohol`         | Smoking/alcohol habit      | Indicates risk behavior            |
| `gender`                  | Student gender             | Demographic information            |
| `health_condition`        | Overall health status      | Target variable                    |

---

# 🛠️ Tech Stack

## Programming & Analysis

* Python
* Pandas
* NumPy
* CuPy

## Visualization

* Matplotlib
* Seaborn

## Statistical Analysis

* Scipy
* Statsmodels
* Pingouin
* Scikit-posthocs

## Machine Learning

* Scikit-learn
* Optuna

## Models

* CatBoost
* XGBoost
* LightGBM
* Ensemble Modeling

---

# 🔍 Exploratory Data Analysis (EDA)

## Dataset Quality Findings

### Missing Values

Major missing-value features:

| Feature               | Missing Rate |
| --------------------- | -----------: |
| `stress_level`        |         ~12% |
| `sleep_duration`      |         ~11% |
| `sleep_quality`       |        ~8.5% |
| `calorie_expenditure` |        ~7.7% |

Observations:

* Missing patterns between Train and Test are highly consistent
* Original dataset contains no missing values
* Missing data handling becomes an important preprocessing step

---

### Duplicate Analysis

Dataset quality appears strong:

* No duplicate records detected
* Every observation represents a unique student profile

---

### Outlier Analysis

Outliers mainly appear in:

* Calorie expenditure
* Water intake
* BMI
* Heart rate

Key findings:

* Most outliers remain within realistic human health ranges
* Outliers likely represent natural variation rather than data errors
* Train and Test datasets share similar distributions

---

# 📊 Overall Health Behavior Insights

| Feature                   | Key Insight                                                   |
| ------------------------- | ------------------------------------------------------------- |
| `sleep_duration`          | Students average around 7 hours of sleep daily                |
| `heart_rate`              | Resting heart rate centers near normal adult range            |
| `bmi`                     | Most students remain within healthy BMI ranges                |
| `exercise_duration`       | Physical activity varies considerably                         |
| `water_intake`            | Hydration patterns remain relatively stable                   |
| `stress_level`            | Medium stress level dominates the dataset                     |
| `sleep_quality`           | Poor and average sleep become more common in competition data |
| `physical_activity_level` | Moderate activity is most common                              |
| `smoking_alcohol`         | Risk behaviors remain relatively balanced                     |
| `diet_type`               | Dietary habits show moderate variation                        |

Overall behavioral patterns indicate that health outcomes are likely influenced by multiple interacting lifestyle factors rather than a single dominant variable.

---

# 🤖 Machine Learning Modeling

## Models Evaluated

| Model             | Purpose                        |
| ----------------- | ------------------------------ |
| CatBoost          | Native categorical handling    |
| XGBoost           | Gradient boosting optimization |
| LightGBM          | Efficient large-scale learning |
| Ensemble Blending | Improve prediction robustness  |

Model development includes:

* Missing value handling
* Category encoding
* Feature engineering
* Stratified K-Fold validation
* Hyperparameter optimization using Optuna

---

# 📈 Model Performance

## Evaluation Metric

Primary evaluation metric:

```python
Balanced Accuracy Score
```

Balanced Accuracy was selected because:

* Multi-class classification problem
* Reduces bias from class imbalance
* Provides fair evaluation across all health categories

---

# 🧠 Top Feature Importance Insights

Potential high-impact health indicators:

## Strong Healthy Signals

* Good sleep quality
* Longer sleep duration
* Higher physical activity
* Regular exercise
* Healthy hydration behavior

## Strong Risk Signals

* High stress levels
* Poor sleep quality
* Smoking and alcohol behavior
* Elevated BMI
* Sedentary lifestyle

Results indicate that health status is strongly driven by behavioral and lifestyle factors rather than demographic characteristics alone.

---

# 💡 Health Recommendations

## 1️⃣ Improve Sleep Habits

Encourage students to maintain consistent and sufficient sleep schedules.

## 2️⃣ Promote Physical Activity

Increase exercise participation and daily movement.

## 3️⃣ Reduce Stress Exposure

Provide mental health support and stress management programs.

## 4️⃣ Encourage Healthy Hydration

Increase awareness regarding healthy water consumption behavior.

## 5️⃣ Reduce Risk Behaviors

Support interventions targeting smoking and alcohol habits.

## 6️⃣ Build Personalized Wellness Programs

Develop data-driven health monitoring systems for early risk detection.

---

# ✅ Conclusion

This project demonstrates that student health conditions are influenced by multiple interconnected factors including:

* Sleep behavior
* Stress management
* Physical activity
* Nutrition patterns
* Lifestyle habits

Machine learning models can successfully identify at-risk student groups and support preventive healthcare strategies.

The findings highlight how data science can improve student wellness monitoring and enable early intervention systems.

---

# 🚀 Future Improvements

Potential future enhancements include:

* SHAP explainability analysis
* Advanced feature engineering
* Deep learning experimentation
* Streamlit dashboard deployment
* Real-time health monitoring system
* Personalized recommendation engine

---

# 👨‍💻 Author

**Đào Minh Thuấn**

* GitHub: https://github.com/daominhthuan42
* LinkedIn: https://www.linkedin.com/in/đào-minh-thuấn-528084286/

Data Analytics | Machine Learning | Health Analytics
