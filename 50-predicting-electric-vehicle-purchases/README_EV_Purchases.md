# 🚗 Predicting Electric Vehicle Purchases ⚡

> An end-to-end machine learning project for exploring consumer EV adoption patterns and predicting whether a consumer is likely to purchase an electric vehicle.

---

## 📂 Overview

### Background

The adoption of **electric vehicles (EVs)** is becoming increasingly important as consumers and governments move toward more sustainable transportation.

EV purchase decisions can be associated with several dimensions, including:

- 💰 Financial capacity and income
- 🚗 Daily commuting needs and vehicle ownership
- 🔌 Charging infrastructure and home-charging availability
- 🌱 Environmental concerns
- 💵 Purchase subsidies
- 🛣️ Range anxiety

This project analyzes these factors and develops machine learning models to predict the target variable `Will_Buy_EV`.

### Goal of the Project

The project combines **exploratory data analysis (EDA)**, statistical analysis, feature engineering, hyperparameter tuning, and **5-Fold Out-of-Fold (OOF) evaluation** to:

- Understand EV adoption patterns across consumer groups
- Identify important predictive signals
- Examine relationships between financial, behavioral, charging, environmental, and policy-related variables
- Build classification models for EV purchase prediction
- Generate a final ensemble submission

---

## 🎯 Target Variable

| Feature | Description |
|---|---|
| `Will_Buy_EV` | Whether the consumer will purchase an electric vehicle (`Yes` / `No`) |

---

## 📊 Dataset

The project works with three datasets:

| Dataset | Rows | Columns | Description |
|---|---:|---:|---|
| Train | 668,665 | 15 | Competition training data including `Will_Buy_EV` |
| Test | 286,571 | 14 | Competition test data without the target |
| Original | 10,000 | 15 | Original EV adoption dataset |

The Train and Test datasets contain a combined **955,236 observations**, substantially larger than the original 10,000-row dataset.

### Dataset Features

#### 👤 Buyer Demographics

- `Age` — Age of the buyer
- `Gender` — Gender of the buyer

#### 💰 Financial & Geographic Characteristics

- `Annual_Income_USD` — Annual income in USD
- `City_Type` — Type of city where the buyer lives

#### 🚗 Driving & Vehicle Ownership

- `Daily_Commute_km` — Average daily commuting distance
- `Number_of_Cars_Owned` — Number of cars currently owned
- `Current_Car_Type` — Type of vehicle currently owned

#### 🔌 Charging Infrastructure

- `Charging_Stations_Near_Home` — Charging stations available near home
- `Charging_Stations_Near_Work` — Charging stations available near the workplace
- `Home_Charging_Possible` — Whether home charging is possible

#### 🌱 Environmental & Policy Factors

- `Environmental_Concern_Level` — Level of environmental concern
- `Subsidy_Available` — Whether an EV purchase subsidy is available

#### 🛣️ EV Adoption Barrier

- `Range_Anxiety_Level` — Level of concern about EV driving range

---

## 🔎 Exploratory Data Analysis

The EDA covers:

- Dataset structure and memory usage
- Numerical descriptive statistics
- Categorical feature distributions
- Target class distribution
- Train/Test/Original distribution comparison
- Missing-value analysis
- Duplicate-value analysis
- Outlier detection
- Skewness analysis
- Numerical feature distributions
- Categorical feature relationships with the target
- Statistical significance and effect-size analysis
- Correlation analysis

### Key EDA Findings

#### Numerical Features

- `Age` is centered around approximately **47 years**.
- Train and Test have very similar income distributions, with average annual income around **$84.8K**.
- `Daily_Commute_km` averages about **32.2 km** in Train/Test, while the Original dataset has a noticeably higher average of about **41.1 km**.
- `Charging_Stations_Near_Home` averages approximately **5 stations**.
- `Charging_Stations_Near_Work` averages approximately **7.2 stations**.
- Train and Test numerical distributions are generally well aligned.

#### Categorical Features

- `Gender` contains three categories, with Male representing approximately 55% of Train/Test.
- `City_Type` is dominated by Urban consumers in Train/Test.
- `Current_Car_Type` is dominated by Sedan.
- Approximately 69% of Train/Test observations have `Home_Charging_Possible = Yes`.
- Approximately 63% of Train/Test observations have `Subsidy_Available = Yes`.
- `Environmental_Concern_Level` contains five ordered levels.
- `Range_Anxiety_Level` is strongly concentrated in the `Low` category, around 90% in Train/Test.
- `Number_of_Cars_Owned` contains four values, with 2 cars being the most common category.

---

## 🧹 Data Quality

### Missing Values

Train and Test contain no missing predictor values.

The Original dataset contains:

| Feature | Missing | Missing % |
|---|---:|---:|
| `Environmental_Concern_Level` | 184 | 1.84% |
| `Daily_Commute_km` | 181 | 1.81% |
| `Annual_Income_USD` | 178 | 1.78% |
| **Total** | **543** | — |

For the modeling pipeline, missing `Environmental_Concern_Level` values are represented as a separate `"Missing"` category rather than being replaced by the mode.

### Duplicate Values

No duplicate rows were detected in:

- Train
- Test
- Original

### Outliers

The IQR-based analysis identified outliers mainly in:

- `Annual_Income_USD`
- `Daily_Commute_km`

The presence of statistical outliers was inspected rather than automatically removing observations.

---

## 🧠 Feature Engineering

The modeling pipeline starts with **13 base predictors** and creates **5 engineered features**, resulting in **18 final features**.

### Engineered Features

| Feature | Description |
|---|---|
| `Total_Charging_Stations` | Sum of charging stations near home and work |
| `Charging_Station_Difference` | Difference between workplace and home charging stations |
| `Commute_per_Charging_Station` | Daily commute relative to total charging infrastructure |
| `Range_Anxiety_Commute` | Interaction between range anxiety and daily commute |
| `Home_Charging_Score` | Combines home charging availability with nearby home charging stations |

### Ordinal Encoding

`Range_Anxiety_Level` is converted to an ordinal score for interaction modeling:

```text
Low    → 1
Medium → 2
High   → 3
```

### Categorical Features

The final categorical feature set contains 8 variables:

```text
Gender
City_Type
Current_Car_Type
Home_Charging_Possible
Subsidy_Available
Environmental_Concern_Level
Range_Anxiety_Level
Number_of_Cars_Owned
```

`Number_of_Cars_Owned` is treated categorically because it has only four discrete values.

`Environmental_Concern_Level` and `Range_Anxiety_Level` are ordinal variables and their ordering is preserved during analysis/modeling.

---

## 💾 Memory Optimization

Because the competition data contains more than 955K observations, memory efficiency is considered during preprocessing.

The project:

- Downcasts numerical columns where appropriate
- Converts low-cardinality variables to `category`
- Removes identifier columns before model training
- Keeps Test IDs separately for submission generation

The preprocessing pipeline reduces the competition training data from roughly **93.5 MB** initially to about **18.6 MB** after feature processing and dtype optimization.

---

## 🤖 Machine Learning

Three gradient-boosting models are evaluated:

- **CatBoost**
- **LightGBM**
- **XGBoost**

### Hyperparameter Optimization

Hyperparameters are tuned using **Optuna** with 5-fold stratified validation.

The tuning process evaluates model configurations using **ROC-AUC**.

### Out-of-Fold Evaluation

Each model is evaluated using **5-Fold Out-of-Fold predictions**.

This provides a consistent validation framework before generating Test predictions.

---

## 📈 Model Performance

| Model | OOF ROC-AUC |
|---|---:|
| XGBoost | **0.94068** |
| CatBoost | **0.94040** |
| LightGBM | **0.93417** |
| AUC-Weighted Ensemble | **0.94009** |

The final ensemble uses OOF ROC-AUC-based weights:

| Model | OOF ROC-AUC | Ensemble Weight |
|---|---:|---:|
| XGBoost | 0.94068 | 0.33414 |
| LightGBM | 0.93417 | 0.33182 |
| CatBoost | 0.94040 | 0.33404 |
| **Blended Ensemble** | **0.94009** | — |

The final predictions are exported to:

```text
submission.csv
```

with:

```text
id
Will_Buy_EV
```

---

## 🔍 Feature Importance

Feature-importance analysis across CatBoost, LightGBM, and XGBoost shows recurring importance for several variables.

### Important Predictive Signals

- `Subsidy_Available`
- `Environmental_Concern_Level`
- `Annual_Income_USD`
- `Range_Anxiety_Level`

The relative importance of individual variables differs between models.

Charging-related variables such as:

- `Charging_Stations_Near_Home`
- `Charging_Stations_Near_Work`
- `Home_Charging_Possible`

also contribute to the model, although their individual importance is generally lower than the strongest signals above.

> **Note:** Feature importance describes contribution to model predictions. It does not establish causality.

---

## 💡 Business Insights

### 💵 Affordability & Income

`Annual_Income_USD` is an important predictive signal. This suggests that affordability-related factors should be considered when analyzing EV purchase behavior.

Potential areas for further analysis include:

- Pricing
- Financing options
- Incentives
- Income-based customer segmentation

### 🌱 Environmental Concern

`Environmental_Concern_Level` shows a strong relationship with EV purchase behavior in the analysis and remains important across the evaluated models.

This supports further investigation into environmental attitudes as a component of EV adoption behavior.

### 💰 Subsidy Availability

`Subsidy_Available` is consistently important across the evaluated models.

Government incentives can therefore be analyzed as an important contextual variable when studying EV purchase behavior.

### 🛣️ Range Anxiety

`Range_Anxiety_Level` is another meaningful predictive signal.

The engineered `Range_Anxiety_Commute` feature combines range anxiety with daily commuting distance to capture their interaction.

### 🔌 Charging Infrastructure

Charging infrastructure variables capture the practicality of EV ownership, particularly around home and workplace locations.

However, the relatively lower individual model importance of some charging-station variables indicates that charging infrastructure alone does not fully explain purchase predictions in this dataset.

### 👥 Customer Segmentation

The combination of:

- Income
- Environmental concern
- Subsidy availability
- Range anxiety

can be used as a basis for further customer-segmentation analysis.

---

## 🛠️ Tech Stack

### Programming

- Python
- Pandas
- NumPy

### Visualization

- Matplotlib
- Seaborn

### Statistics

- SciPy
- Statsmodels
- Pingouin
- Scikit-posthocs

### Machine Learning

- CatBoost
- LightGBM
- XGBoost
- Scikit-learn

### Optimization

- Optuna

### Environment

- Jupyter Notebook
- Kaggle Notebook
- Git / GitHub

---

## 📁 Project Structure

```text
50-predicting-electric-vehicle-purchases/
│
├── config/
│   └── config.yaml
│
├── dataset/
│   ├── train.csv
│   ├── test.csv
│   └── EV_Adoption_and_Range_Anxiety_Dataset.csv
│
├── models/
│   ├── benchmark.py
│   ├── oof.py
│   ├── catboost_tuning.py
│   ├── lgbm_tunning.py
│   └── xgboost_tuning.py
│
├── preprocessing/
│   └── validation.py
│
├── utils/
│   ├── logger.py
│   ├── config_loader.py
│   ├── utils.py
│   └── stats_utils.py
│
├── visualization/
│   └── visualization_plots.py
│
├── notebook/
│   └── electric.ipynb
│
├── submission.csv
└── README.md
```

---

## 🚀 Workflow

```text
Dataset
   │
   ▼
Data Loading
   │
   ▼
Data Validation
   ├── Missing Values
   ├── Duplicates
   ├── Outliers
   └── Skewness
   │
   ▼
Exploratory Data Analysis
   │
   ▼
Statistical Analysis
   │
   ▼
Memory Optimization
   │
   ▼
Feature Engineering
   │
   ▼
18 Final Features
   │
   ├──────────────┬──────────────┐
   ▼              ▼              ▼
CatBoost       LightGBM       XGBoost
   │              │              │
   └──────────────┴──────────────┘
                  │
                  ▼
           5-Fold OOF Evaluation
                  │
                  ▼
          AUC-Weighted Ensemble
                  │
                  ▼
            Test Prediction
                  │
                  ▼
            submission.csv
```

---

## 📌 Reproducibility

The project uses a centralized YAML configuration and a fixed random seed.

```yaml
random_state: 42
```

The notebook also clones the project source from GitHub and uses sparse checkout to retrieve only the EV project directory in the Kaggle environment.

Statistical dependencies used by the notebook include:

```text
statsmodels
scikit_posthocs
pingouin==0.5.5
pandas==3.0.0
```

---

## 📚 Key Takeaways

- The competition Train and Test datasets are highly consistent in their overall numerical and categorical distributions.
- The Original dataset differs more noticeably in `Daily_Commute_km` and `Range_Anxiety_Level`.
- Train/Test contain no missing predictor values, while the Original dataset contains 543 missing values across three variables.
- Memory optimization is important because the competition datasets contain more than 955K combined observations.
- Feature engineering expands the base feature set from 13 to 18 predictors.
- `Subsidy_Available`, `Environmental_Concern_Level`, `Annual_Income_USD`, and `Range_Anxiety_Level` repeatedly appear as important predictive signals.
- CatBoost, LightGBM, and XGBoost are evaluated using 5-Fold OOF ROC-AUC.
- The final pipeline produces an AUC-weighted ensemble submission.

---

## 👨‍💻 Author

**Dao Minh Thuan**
