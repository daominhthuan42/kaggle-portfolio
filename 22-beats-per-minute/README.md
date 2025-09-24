# 🎶 Predicting the Beats-per-Minute (BPM) of Songs ⏱️

## 📌 Overview

Music tempo, measured in **Beats-per-Minute (BPM)**, plays a vital role in shaping how listeners perceive the **mood, genre, and energy** of a track.
This project is based on the **Kaggle Playground Series - S5E9**, which challenges participants to predict BPM from audio-extracted features.

Competition link: [Playground S5E9 - Predicting the BPM of Songs](https://www.kaggle.com/competitions/playground-series-s5e9)
Dataset source: [BPM Prediction Challenge](https://www.kaggle.com/datasets/gauravduttakiit/bpm-prediction-challenge)

**Goal:**

* Explore audio features that influence song tempo.
* Build regression models to predict BPM.
* Provide insights for **music recommendation systems and playlist curation**.

## 📂 Dataset Information

**Training set:** 524,164 records.
**Test set:** 174,722 records.
**Original dataset:** 14,633 samples.

**Target variable:**

* `BeatsPerMinute` → Numeric value of track tempo.

### 🔑 Key Features

| Feature                     | Description                             |
| --------------------------- | --------------------------------------- |
| `RhythmScore`               | Rhythmic complexity/clarity             |
| `AudioLoudness`             | Sound intensity in decibels             |
| `VocalContent`              | Degree of vocal presence                |
| `AcousticQuality`           | How acoustic/natural the recording is   |
| `InstrumentalScore`         | Instrumental vs vocal emphasis          |
| `LivePerformanceLikelihood` | Probability of being a live performance |
| `MoodScore`                 | Encoded emotional tone of the track     |
| `TrackDurationMs`           | Duration of the song in milliseconds    |
| `Energy`                    | Indicator of song intensity             |

## 🎯 Objectives

* Perform **EDA**: analyze feature distributions, correlations, and tempo patterns.
* **Feature Engineering**: scaling, transformation, derived audio insights.
* Train and compare regression models:

  * Linear Regression.
  * Random Forest.
  * Gradient Boosting (XGBoost, LightGBM).
* Evaluate using **RMSE** and cross-validation.

## 🛠 Methodology & Tools

* **Data Cleaning:** drop ID column, type optimization for efficiency.
* **EDA & Visualization:** histograms, scatter plots, correlation heatmaps.
* **Modeling:** baseline linear models → advanced tree-based regressors.
* **Evaluation:** Root Mean Squared Error (RMSE), model comparison.

## 📊 Key Insights

* **BPM distribution** spans from <60 BPM (slow ballads) to >200 BPM (dance/electronic).
* **Loudness & Energy** positively correlate with BPM.
* Tracks with **low vocal content** often show more extreme BPM values.
* **Acoustic vs electronic balance** influences tempo predictability.
* Typical track durations cluster around 3–5 minutes, aligning with standard song structures.

## 🚀 Next Steps

* Hyperparameter tuning with Optuna.
* Ensemble stacking for improved prediction.
* Deploy BPM predictor as a **music analytics API**.

## 👤 Author

* **Name:** Đào Minh Thuấn.
* **GitHub:** [daominhthuan42](https://github.com/daominhthuan42)
