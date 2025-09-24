# ✈️ Airlines Flights Price Prediction 💸

## 📌 Overview

This project analyzes the **Airlines Flights Dataset**, which contains ticket listings across major Indian airlines.
The dataset includes details such as **airline, source/destination cities, departure & arrival time slots, number of stops, class, flight duration, days left until departure, and price**.

Dataset link: [Airlines Flights Data (Kaggle)](https://www.kaggle.com/datasets/rohitgrewal/airlines-flights-data)

**Goal:**

* Explore pricing trends in Indian airlines.
* Predict flight ticket prices based on travel and booking attributes.
* Provide actionable insights for **travelers, travel agencies, and airlines**.

## 📂 Dataset Information

**Size:** 300,153 records, 12 features (including target `price`).
**Target variable:**

* `price` → Ticket price in INR.

### 🔑 Key Features

| Feature            | Description                                     |
| ------------------ | ----------------------------------------------- |
| `airline`          | Airline name (SpiceJet, Vistara, AirAsia, etc.) |
| `flight`           | Flight identifier (e.g., SG-8709)               |
| `source_city`      | Departure city                                  |
| `departure_time`   | Time slot of departure (Morning, Evening, etc.) |
| `stops`            | Number of stops (non-stop, 1 stop, etc.)        |
| `arrival_time`     | Time slot of arrival                            |
| `destination_city` | Arrival city                                    |
| `class`            | Travel class (Economy/Business)                 |
| `duration`         | Flight duration (hours)                         |
| `days_left`        | Days left until departure                       |
| `price`            | Ticket price (target variable)                  |

## 🎯 Objectives

* Perform **EDA** to analyze pricing by airline, class, route, time, and days left.
* **Feature Engineering**: encode categoricals, handle skewed distributions, derive booking-related insights.
* Build regression models: Linear Regression, Random Forest, XGBoost, LightGBM.
* Evaluate with **RMSE, MAE, R²**.
* Provide insights for airfare optimization.

## 🛠 Methodology & Tools

* **Data Cleaning:** remove irrelevant features (`flight`, `index`), handle outliers in `price`.
* **EDA & Visualization:** Matplotlib, Seaborn for trends & distributions.
* **Feature Engineering:** categorical encoding, duration bucketing, weekend/weekday flag.
* **Modeling:** Linear Regression, Random Forest, Gradient Boosting, LightGBM.
* **Evaluation:** RMSE, MAE, cross-validation.

## 📊 Key Insights

* **Economy class dominates** the dataset (\~70%), but **Business tickets** skew prices upwards.
* **Days left until departure** strongly impacts price → earlier bookings are cheaper.
* **Longer duration & more stops** usually increase ticket prices.
* Popular routes (Delhi–Mumbai, Bangalore–Delhi) show **higher price variance**.
* **Airline differences:** some airlines (e.g., Vistara, Air India) consistently have higher fares.

## 🚀 Next Steps

* Hyperparameter tuning (Optuna) for boosting models.
* Ensemble approaches (Stacking, Blending).
* Build a **flight price prediction API**.

## 👤 Author

* **Name:** Đào Minh Thuấn.
* **GitHub:** [daominhthuan42](https://github.com/daominhthuan42)
