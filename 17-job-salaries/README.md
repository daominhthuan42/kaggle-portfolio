# 💰 Data Science Job Salaries 💼

## 📌 Overview

This project analyzes **global salary data for Data Science roles** across multiple years, job titles, company sizes, and working arrangements.

Dataset link: [Data Science Job Salaries (Kaggle)](https://www.kaggle.com/datasets/ruchi798/data-science-job-salaries)

**Goals:**

* Predict salaries (`salary_in_usd`) based on job, experience, and company attributes.
* Identify key factors influencing compensation.
* Provide insights for job seekers and HR professionals to make informed decisions.

## 📂 Dataset Information

**Size:** 607 records, 12 features.
**Target variable:**

* `salary_in_usd` → Salary standardized to USD.

### 🔑 Key Features

| Feature              | Description                                  |
| -------------------- | -------------------------------------------- |
| `work_year`          | Year of observation (2020–2022)              |
| `experience_level`   | Level (Entry, Junior, Senior, Executive)     |
| `employment_type`    | FT (Full-time), PT, Contract, Freelance      |
| `job_title`          | Job role (e.g., Data Scientist, ML Engineer) |
| `salary`             | Salary amount in original currency           |
| `salary_currency`    | Currency of reported salary                  |
| `salary_in_usd`      | Converted salary in USD (**target**)         |
| `employee_residence` | Country of employee                          |
| `remote_ratio`       | 0 = on-site, 50 = hybrid, 100 = fully remote |
| `company_location`   | Country of company                           |
| `company_size`       | Company size: S, M, L                        |

## 🎯 Objectives

* Perform **EDA**: analyze distributions, salary trends, remote work effects.
* **Feature Engineering**: encode categorical vars, normalize target, derive region-based features.
* Train regression models: Linear Regression, Random Forest, XGBoost, LightGBM.
* Evaluate with **R², RMSE, MAE**.
* Provide career and HR insights.

## 🛠 Methodology & Tools

* **EDA & Visualization:** Seaborn, Matplotlib.
* **Feature Engineering:** log-transform salary, encode categoricals, group rare job titles.
* **Modeling:** Linear Regression, Random Forest, XGBoost, LightGBM.
* **Evaluation:** Cross-validation, error metrics (RMSE, MAE, R²).

## 📊 Key Insights

* **Senior (SE) professionals** dominate the dataset (\~46%).
* **Remote jobs** (remote\_ratio = 100) are common and often offer competitive salaries.
* US Salaries in the **US** are significantly higher than other regions.
* **Company size** impacts salaries: large (L) > medium (M) > small (S).
* Popular roles: **Data Scientist, ML Engineer, Data Analyst** with wide salary ranges.

## 🚀 Next Steps

* Hyperparameter tuning with Optuna.
* Try **stacking/ensembling models** for improved performance.
* Provide **career recommendations** based on job role and region.

## 👤 Author

* **Name:** Đào Minh Thuấn.
* **GitHub:** [daominhthuan42](https://github.com/daominhthuan42)
