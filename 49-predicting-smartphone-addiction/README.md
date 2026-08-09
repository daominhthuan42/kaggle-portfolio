# 📱 Smartphone Addiction Prediction ⚠️

## 📌 Overview

Smartphones have become an essential part of daily life, supporting
communication, entertainment, education, and work. However, excessive
smartphone usage has raised concerns about digital addiction and its
potential impact on mental well-being, sleep quality, academic
performance, and work productivity.

This project analyzes demographic characteristics, smartphone usage
patterns, lifestyle indicators, and behavioral factors to identify the
key signals associated with smartphone addiction.

Machine learning models are then developed to predict whether a user is
likely to exhibit signs of smartphone addiction, supporting early
identification and healthier digital-wellness strategies.

------------------------------------------------------------------------

## 📂 Dataset Information

**Dataset sizes:**

-   **Training dataset:** 691,369 records, 14 original columns
-   **Test dataset:** 296,302 records, 13 original columns
-   **Original dataset:** 7,500 records, 16 original columns

**Target variable:**

-   `addicted_label`: Smartphone addiction indicator
    -   `0` → Not Addicted
    -   `1` → Addicted

### 🔑 Key Features

**User Demographics:**

-   `age`
-   `gender`

**Smartphone Usage Behavior:**

-   `daily_screen_time_hours`
-   `social_media_hours`
-   `gaming_hours`
-   `work_study_hours`
-   `weekend_screen_time`

**User Interaction Activity:**

-   `notifications_per_day`
-   `app_opens_per_day`

**Health & Lifestyle Indicators:**

-   `sleep_hours`
-   `stress_level`

**Behavioral Impact:**

-   `academic_work_impact`

**Identifier / Non-Predictive Feature:**

-   `id`

The original dataset additionally contains `transaction_id`, `user_id`,
and `addiction_level`. These fields are removed before modeling because
they are not used as predictive inputs.

------------------------------------------------------------------------

## 🎯 Objectives

-   Perform comprehensive **Exploratory Data Analysis (EDA)**:

    -   Smartphone addiction distribution
    -   Numerical and categorical feature distributions
    -   Missing-value and outlier analysis
    -   Skewness, kurtosis, and distribution analysis
    -   Correlation analysis
    -   Statistical comparison between addicted and non-addicted users

-   Identify the major **behavioral and usage-related factors**
    associated with smartphone addiction.

-   Perform **Feature Engineering** to capture:

    -   Total and entertainment usage
    -   Productivity and entertainment ratios
    -   Weekend usage patterns
    -   Notification and app-opening density
    -   Sleep-related indicators
    -   Interaction effects between age, screen time, social media, and
        gaming

-   Train and optimize gradient boosting models:

    -   CatBoost
    -   LightGBM
    -   XGBoost

-   Evaluate model performance using:

    -   Stratified 5-Fold Cross-Validation
    -   Out-of-Fold (OOF) predictions
    -   ROC-AUC
    -   Precision-Recall analysis
    -   Confusion Matrix
    -   Feature importance

-   Build an **AUC-weighted ensemble model** using CatBoost, LightGBM,
    and XGBoost.

-   Translate model findings into practical recommendations for
    healthier smartphone usage and early intervention.

------------------------------------------------------------------------

## 🛠 Methodology & Tools

### **Data Cleaning & Validation**

-   Standardized column names and data types.
-   Removed identifier columns from model inputs.
-   Checked missing values across train, test, and original datasets.
-   Checked duplicate records.
-   Reviewed numerical outliers using statistical thresholds.
-   Reduced numerical memory usage by downcasting numeric types.

### **Missing Value Handling**

Missing values are intentionally present across most predictor variables
in the competition datasets.

-   Numerical features → **Median imputation**
-   Categorical features → **`"Unknown"`**

The missing-value pattern is highly consistent between the training and
test datasets, making missing-value handling an important preprocessing
step.

### **Exploratory Data Analysis**

-   Target distribution analysis
-   Numerical feature distributions
-   Boxplots and outlier analysis
-   Skewness and kurtosis analysis
-   Correlation analysis
-   Independent two-sample t-tests
-   Cohen's d effect-size analysis
-   Chi-square tests for categorical variables
-   Categorical addiction-rate comparisons
-   Q-Q plots and distribution diagnostics

### **Feature Engineering**

The project expands the base dataset to **34 modeling features**.

Important engineered features include:

-   `total_usage_hours`
-   `entertainment_hours`
-   `study_usage_ratio`
-   `entertainment_ratio`
-   `weekend_usage_diff`
-   `weekend_ratio`
-   `notification_density`
-   `app_open_density`
-   `opens_per_notification`
-   `sleep_deficit`
-   `screen_sleep_score`
-   `age_screen_interaction`
-   `weekend_social`
-   `social_gaming`
-   `activity_score`
-   `engagement_score`

Additional statistics derived from the original dataset are also used,
including category-level mean and count features.

### **Categorical Encoding**

A custom **TargetEncoder** is used for categorical variables with K-Fold
out-of-fold encoding to reduce target leakage during model development.

### **Modeling**

Three gradient boosting models are trained using **5-Fold Stratified
Cross-Validation**:

-   `XGBClassifier`
-   `LGBMClassifier`
-   `CatBoostClassifier`

Early stopping is used during model training, and feature importance is
collected across folds.

### **Ensemble Learning**

The final ensemble combines the three model predictions using weights
proportional to their OOF ROC-AUC scores.

------------------------------------------------------------------------

## 📊 Key Insights

### 🔴 Smartphone Addiction

The target distribution shows a moderate class imbalance, with
approximately **70% Addicted** and **30% Not Addicted** users.

This makes classification performance and probability-based evaluation
important when assessing model quality.

### 📱 Screen Time & Smartphone Usage

`daily_screen_time_hours` is one of the strongest predictors of
smartphone addiction.

-   Addicted users average nearly **9 hours/day** of daily screen time.
-   Non-addicted users average approximately **5 hours/day**.
-   The correlation between `addicted_label` and
    `daily_screen_time_hours` is approximately **0.58--0.61**.

`weekend_screen_time` is another strong behavioral indicator, with
addicted users spending considerably more time on their smartphones
during weekends.

### 📲 Social Media & Entertainment

`social_media_hours` strongly distinguishes addicted users from
non-addicted users.

-   Addicted users average approximately **2.92 hours/day**.
-   Non-addicted users average approximately **1.38 hours/day**.

The analysis also shows that `gaming_hours` is higher among addicted
users, but its practical effect is weaker than overall screen time and
social media usage.

### 🔔 Interaction & Secondary Behavior

`app_opens_per_day` and `notifications_per_day` are associated with
smartphone addiction, but their practical contribution is more modest
than screen-time-related variables.

`work_study_hours` is also higher among addicted users, although the
effect is relatively small.

### 😴 Lifestyle Indicators

`sleep_hours` differs slightly between addicted and non-addicted groups,
but the practical effect is limited.

Similarly, `stress_level` is statistically associated with addiction,
while the differences between stress groups remain relatively small in
practical terms.

### 👤 Demographic Factors

`age` shows statistical differences but almost no practical effect on
smartphone addiction.

`gender` has a statistically significant but modest relationship, with
male users showing a slightly higher addiction rate.

Overall, demographic characteristics are considerably weaker indicators
than direct smartphone usage behavior.

### 🔎 Strongest Behavioral Signals

The analysis consistently identifies:

1.  `daily_screen_time_hours`
2.  `weekend_screen_time`
3.  `social_media_hours`

as the strongest behavioral indicators of smartphone addiction.

The model feature-importance analysis also highlights
`daily_screen_time_hours`, `app_opens_per_day`, `notifications_per_day`,
`gaming_hours`, and several engineered usage features as important
predictive signals.

------------------------------------------------------------------------

## 🤖 Model Performance

The three gradient boosting models were evaluated using **5-Fold
Out-of-Fold predictions**.

  Model        OOF ROC-AUC
  ---------- -------------
  XGBoost      **0.96385**
  LightGBM     **0.96315**
  CatBoost     **0.95934**

### 🔗 AUC-Weighted Ensemble

The final ensemble uses OOF ROC-AUC-based weights:

  Model                    OOF ROC-AUC   Ensemble Weight
  ---------------------- ------------- -----------------
  XGBoost                  **0.96385**           0.33393
  LightGBM                 **0.96315**           0.33369
  CatBoost                 **0.95934**           0.33237
  **Blended Ensemble**     **0.96319**               ---

The blended model produces an OOF ROC-AUC of **0.96319**, providing
strong discrimination between users with lower and higher predicted
addiction risk.

The final predictions are exported to:

``` text
submission.csv
```

with the following columns:

``` text
id
addicted_label
```

------------------------------------------------------------------------

## 💡 Recommendations

-   **Prioritize behavioral indicators**

    Focus monitoring and intervention on `daily_screen_time_hours`,
    `weekend_screen_time`, and `social_media_hours`, as these are the
    strongest predictors of smartphone addiction.

-   **Implement early-warning mechanisms**

    Identify users with excessive daily or weekend screen time and
    provide timely reminders or usage-limit interventions to encourage
    healthier digital habits.

-   **Monitor secondary behavioral signals**

    Combine gaming time, work/study screen time, and app-opening
    frequency with the primary indicators to improve risk assessment.

-   **Avoid over-relying on demographic characteristics**

    Variables such as `age` and `gender`, together with weaker
    behavioral indicators such as notifications, sleep duration, and
    stress level, contribute less to distinguishing smartphone
    addiction.

-   **Focus interventions on prolonged screen exposure and social media
    engagement**

    Reducing excessive screen exposure and social-media engagement
    should be prioritized because these behaviors show the strongest
    relationship with addiction risk.

> **Note:** Statistical association and model feature importance do not
> prove causality. The findings should be interpreted as predictive
> relationships rather than evidence that a particular behavior directly
> causes smartphone addiction.

------------------------------------------------------------------------

## 🧰 Tech Stack

-   **Language:** Python
-   **Data Processing:** Pandas, NumPy
-   **Visualization:** Matplotlib, Seaborn
-   **Machine Learning:** Scikit-learn
-   **Gradient Boosting:** CatBoost, LightGBM, XGBoost
-   **Hyperparameter Optimization:** Optuna
-   **Statistical Analysis:** SciPy, Pingouin, Statsmodels,
    scikit-posthocs
-   **Evaluation:** ROC-AUC, Precision-Recall, Confusion Matrix, OOF
    Evaluation
-   **Validation:** Stratified 5-Fold Cross-Validation
-   **Logging:** Python Logging, Colorlog

------------------------------------------------------------------------

## 👤 Author

-   **Name:** Đào Minh Thuấn
-   **GitHub:** [daominhthuan42](https://github.com/daominhthuan42)
