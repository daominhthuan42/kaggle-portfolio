# Sales Forecasting Project

## **Overview**
This project focuses on forecasting sales for a retailer using historical sales data. The goal is to predict the number of products sold (num_sold) for future dates, enabling better inventory management and business decision-making.

## **Data Description**
The dataset consists of historical sales data from different countries, stores, and product types. The key components are:

### **1. Training Data (`train.csv`)**  
Contains historical sales records used to train the forecasting model. Key columns include:
- `id`: Unique identifier for each record.
- `date`: The date when sales were recorded.
- `country`: The country where sales occurred (e.g., Canada, Finland, Italy, Kenya, Norway, Singapore).
- `store`: The store type (e.g., Discount Stickers, Stickers for Less, Premium Sticker Mart).
- `product`: The product type (e.g., Holographic Goose, Kaggle, Kaggle Tiers, Kerneler, Kerneler Dark Mode).
- `num_sold`: The number of units sold (target variable).

### **2. Test Data (`test.csv`)**  
Contains future sales records without the `num_sold` column. The goal is to predict the values for this column.

### **3. Sample Submission (`sample_submission.csv`)**  
Provides the expected submission format with columns `id` and `num_sold`. Predictions will replace the `num_sold` column.

### **4. Supplementary Data**  
- Includes various factors affecting sales trends:
  - Day-of-week sales ratios.
  - GDP per capita adjustments.
  - Store weights for disaggregating forecasts.

## **Objective**
The primary objective of this project is to build an accurate forecasting model that predicts `num_sold` for the test dataset. This involves:

### **1. Understanding Sales Patterns**
- Analyzing historical sales data to identify trends in:
  - Seasonality (e.g., weekends).
  - Store types and country-specific variations.
  - Product demand changes over time.

### **2. Building a Forecasting Model**
The model uses advanced data processing techniques such as:
- **Missing data imputation**: Handling missing values in historical data.
- **Aggregation and disaggregation**: Modeling total sales and individual store/product sales using weighted distributions.
- **Ratio-based adjustments**: Incorporating GDP per capita, day-of-week effects, and store-specific influences.

### **3. Providing Actionable Insights**
The final model will help businesses:
- Optimize inventory management by predicting future demand.
- Allocate resources effectively across different regions and stores.
- Make data-driven strategic decisions to maximize sales and profitability.

## **Technologies and Libraries Used**
The project utilizes several data science and visualization libraries:
- **Programming Language:** Python
- **Libraries:** Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn, Statsmodels
- **Visualization Tools:** Matplotlib, Seaborn, Plotly

### **Fetching External Data (World Bank API)**
```python
# Fetch GDP per capita for a specific country and year
url = f'https://api.worldbank.org/v2/country/{alpha3}/indicator/NY.GDP.PCAP.CD?date={year}&format=json'
```

## **Project Workflow**
1. **Data Preprocessing**
   - Handling missing values and imputing missing sales records.
   - Normalizing and transforming data for better model performance.
   - Feature engineering based on sales trends and external factors.

2. **Exploratory Data Analysis (EDA)**
   - Visualizing historical sales trends.
   - Analyzing seasonality and holiday effects.
   - Identifying correlations between store types, countries, and products.

3. **Model Development**
   - Using time series forecasting techniques.
   - Aggregating total sales and disaggregating forecasts.
   - Adjusting predictions using GDP per capita and other external factors.

4. **Evaluation and Optimization**
   - Fine-tuning hyperparameters to improve accuracy.
   - Ensuring robust validation and testing of predictions.

5. **Submission Generation**
   - Formatting predictions according to the `sample_submission.csv` format.
   - Saving the final submission file:
   ```python
   sample_df.to_csv("submission.csv", index=False)
   print("Submission file created.")
   ```

## **Conclusion**
This project aims to improve sales forecasting accuracy, enabling businesses to make informed decisions regarding inventory and resource allocation. By leveraging historical data and advanced forecasting techniques, we enhance predictability and efficiency in retail sales management.

