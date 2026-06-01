# 🏢 HR Attrition Prediction & Workforce Retention Analysis

# 📑 Table of Contents

* [📌 Overview](#-overview)
* [🎯 Project Objectives](#-project-objectives)
* [📂 Dataset Overview](#-dataset-overview)
* [🧾 Feature Description](#-feature-description)
* [🛠️ Tech Stack](#️-tech-stack)
* [🔍 Exploratory Data Analysis (EDA)](#-exploratory-data-analysis-eda)
* [📊 Overall Business Picture](#-overall-business-picture)
* [🤖 Machine Learning Modeling](#-machine-learning-modeling)
* [📈 Model Performance](#-model-performance)
* [🧠 Top Feature Importance Insights](#-top-feature-importance-insights)
* [💼 HR Business Recommendations](#-hr-business-recommendations)
* [✅ Conclusion](#-conclusion)
* [🚀 Future Improvements](#-future-improvements)
* [👨‍💻 Author](#-author)


## 📌 Overview

Employee attrition is one of the most critical challenges organizations face in maintaining workforce stability and operational efficiency. High employee turnover increases recruitment costs, reduces productivity, weakens team morale, and disrupts business continuity.

This project focuses on analyzing employee attrition behavior using:

* Exploratory Data Analysis (EDA)
* Statistical testing
* Machine Learning modeling
* Business-oriented HR recommendations

The objective is to identify the key drivers of employee turnover and provide actionable retention strategies for organizations.

# 🎯 Project Objectives

The primary goals of this project are:

* Analyze employee attrition behavior
* Identify factors influencing workforce turnover
* Build predictive machine learning models
* Improve HR decision-making through data-driven insights
* Provide actionable retention recommendations

# 📂 Dataset Overview

## Dataset Information

| Dataset |   Rows | Columns |
| ------- | -----: | ------: |
| Train   | 59,598 |      24 |
| Test    | 14,900 |      24 |

The dataset contains:

* Employee demographics
* Compensation information
* Workplace satisfaction metrics
* Career development indicators
* Organizational reputation features
* Workplace flexibility variables

### 🎯 Target Variable

```python
Attrition = Stayed / Left
```

# 🧾 Feature Description

| Feature                    | Description                               | Business Meaning                                               |
| -------------------------- | ----------------------------------------- | -------------------------------------------------------------- |
| `Age`                      | Employee age                              | Helps identify attrition trends across career stages.          |
| `Gender`                   | Employee gender                           | Used to analyze demographic retention behavior.                |
| `Years_at_Company`         | Years employed at the company             | Measures organizational attachment and tenure stability.       |
| `Job_Role`                 | Employee functional role                  | Helps detect turnover patterns across departments.             |
| `Monthly_Income`           | Employee monthly salary                   | Represents compensation and financial satisfaction.            |
| `WorkLife_Balance`         | Employee work-life balance level          | Strong indicator of employee well-being and burnout risk.      |
| `Job_Satisfaction`         | Employee satisfaction score               | Measures workplace engagement and emotional attachment.        |
| `Performance_Rating`       | Employee performance evaluation           | Helps analyze relationships between performance and attrition. |
| `Number_of_Promotions`     | Number of promotions received             | Indicates career growth and advancement opportunities.         |
| `Overtime`                 | Overtime working status                   | Represents workload pressure and burnout exposure.             |
| `Distance_from_Home`       | Employee commuting distance               | Reflects commuting burden and convenience.                     |
| `Education_Level`          | Highest education qualification           | Helps analyze retention across education groups.               |
| `Marital_Status`           | Employee marital status                   | Used to evaluate personal stability and retention patterns.    |
| `Number_of_Dependents`     | Number of employee dependents             | Indicates financial responsibility and stability.              |
| `Job_Level`                | Employee seniority level                  | Represents career stage and organizational hierarchy.          |
| `Company_Size`             | Organization size category                | Helps compare retention behavior across company scales.        |
| `Company_Tenure`           | Company operational tenure                | Reflects organizational maturity and workforce stability.      |
| `Remote_Work`              | Remote work arrangement                   | Measures workplace flexibility impact on retention.            |
| `Leadership_Opportunities` | Leadership development opportunities      | Indicates long-term career growth support.                     |
| `Innovation_Opportunities` | Innovation and creativity opportunities   | Measures organizational innovation culture.                    |
| `Company_Reputation`       | Employee perception of company reputation | Represents employer branding and organizational image.         |
| `Employee_Recognition`     | Employee recognition level                | Measures workplace appreciation and acknowledgment.            |
| `Attrition`                | Employee attrition status                 | Target variable used for prediction modeling.                  |

# 🛠️ Tech Stack

## Programming & Analysis

* Python
* Pandas
* NumPy

## Visualization

* Matplotlib
* Seaborn

## Machine Learning

* Scikit-learn
* Optuna

## Models

* Logistic Regression
* Ridge Classifier
* LinearSVC
* Ensemble Blending

# 🔍 Exploratory Data Analysis (EDA)

## Attrition Distribution

The dataset is relatively balanced:

* Stayed: ~52%
* Left: ~48%

This balanced distribution improves modeling stability and reduces the need for aggressive resampling techniques.

# 📊 Overall Business Picture

| Feature                    | Key Insight                                                                                          |
| -------------------------- | ---------------------------------------------------------------------------------------------------- |
| `WorkLife_Balance`         | Employees with poor work-life balance show significantly higher attrition risk.                      |
| `Overtime`                 | Overtime strongly increases employee turnover probability.                                           |
| `Job_Level`                | Entry-level employees are much more likely to leave, while senior employees show stronger retention. |
| `Remote_Work`              | Remote work significantly improves employee retention.                                               |
| `Number_of_Promotions`     | More promotions strongly correlate with lower attrition.                                             |
| `Leadership_Opportunities` | Leadership opportunities positively impact retention behavior.                                       |
| `Innovation_Opportunities` | Innovation opportunities slightly improve retention stability.                                       |
| `Company_Reputation`       | Poor company reputation is strongly associated with higher attrition.                                |
| `Marital_Status`           | Single employees exhibit higher turnover risk compared to married employees.                         |
| `Education_Level`          | Employees with PhD-level education demonstrate stronger retention patterns.                          |
| `Number_of_Dependents`     | Employees with larger family responsibilities tend to stay longer.                                   |
| `Employee_Recognition`     | Employee recognition shows minimal practical impact on attrition.                                    |
| `Gender`                   | No major business impact detected across gender groups.                                              |
| `Company_Size`             | Small companies show slightly higher attrition patterns.                                             |
| `Job_Satisfaction`         | Higher job satisfaction improves retention likelihood.                                               |
| `Monthly_Income`           | Higher compensation contributes moderately to employee retention.                                    |
| `Years_at_Company`         | Longer-tenure employees generally show stronger organizational attachment.                           |

# 🤖 Machine Learning Modeling

## Models Evaluated

| Model               | Purpose                                |
| ------------------- | -------------------------------------- |
| Logistic Regression | Interpretable baseline classifier      |
| Ridge Classifier    | Regularized linear classifier          |
| LinearSVC           | High-dimensional linear classification |
| Ensemble Blending   | Improve prediction stability           |

# 📈 Model Performance

## Baseline ROC-AUC Results

| Model               | ROC-AUC |
| ------------------- | ------: |
| AdaBoostClassifier  |   ~0.85 |
| LinearSVC           |   ~0.85 |
| Logistic Regression |   ~0.85 |
| RidgeClassifier     |   ~0.85 |
| CatBoostClassifier  |   ~0.85 |

Interestingly, simpler linear models outperformed many complex ensemble models, suggesting that attrition patterns are largely linearly separable and strongly driven by structured organizational behavior.

# 🧠 Top Feature Importance Insights

LinearSVC coefficients identified several major retention and attrition signals.

## Strong Retention Signals

* Senior Job Level
* Remote Work
* Excellent Work-Life Balance
* Higher Promotions
* PhD Education Level

## Strong Attrition Signals

* Entry-Level Employees
* Single Employees
* Poor Work-Life Balance
* Lack of Promotions
* Overtime Work

The model findings strongly aligned with the EDA and statistical analysis results, improving business interpretability and model trustworthiness.

# 💼 HR Business Recommendations

## 1️⃣ Improve Work-Life Balance

Reduce excessive overtime and strengthen employee well-being initiatives.

## 2️⃣ Expand Flexible Work Policies

Remote and hybrid work arrangements significantly improve retention.

## 3️⃣ Focus on Entry-Level Retention

Develop onboarding, mentoring, and career progression programs for junior employees.

## 4️⃣ Strengthen Internal Promotion Pathways

Career advancement opportunities strongly reduce attrition risk.

## 5️⃣ Improve Organizational Reputation

Enhance employer branding and workplace culture initiatives.

## 6️⃣ Support High-Risk Employee Groups

Single employees and overtime-heavy employees should receive targeted engagement support.

# ✅ Conclusion

This project demonstrates that employee attrition is heavily influenced by:

* Work-life balance
* Career growth opportunities
* Workplace flexibility
* Organizational reputation
* Employee seniority

The machine learning models successfully identified high-risk employee groups and generated interpretable business insights that can help HR departments proactively reduce turnover risk and improve workforce stability.

Overall, the project highlights how machine learning and business analytics can support strategic HR decision-making and organizational retention planning.

# 🚀 Future Improvements

Potential future enhancements include:

* XGBoost / LightGBM implementation
* SHAP explainability analysis
* Threshold optimization
* Streamlit dashboard deployment
* Real-time HR monitoring system

# 👨‍💻 Author

**Đào Minh Thuấn**

* GitHub: [Thuan Dao Git Hub](https://github.com/daominhthuan42)
* LinkedIn: [Thuan Dao Linkedlin](https://www.linkedin.com/in/%C4%91%C3%A0o-minh-thu%E1%BA%A5n-528084286/?skipRedirect=true)

Data Analytics | Machine Learning | Business Intelligence
