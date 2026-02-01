# 🚖 Mobility Analytics Platform

### Data Lakehouse & Analytics Project

Welcome to the **Mobility Analytics Platform** repository!
This project demonstrates an end-to-end **Data Lakehouse and Analytics solution** built using Apache Spark and Delta Lake following the Medallion Architecture.

Designed as a portfolio project, it highlights modern best practices in **Data Engineering, Data Modeling, and Analytics Engineering**.

---

## 🏗️ Data Architecture

The data architecture follows the Medallion Architecture with **Bronze**, **Silver**, and **Gold** layers:

```
CSV Files → Bronze → Silver → Gold → BI / Analytics
```

### Layers Overview

1. **Bronze Layer**

   * Stores raw CSV data as-is
   * Ingested using Spark Structured Streaming
   * Ensures data traceability and fault tolerance

2. **Silver Layer**

   * Performs data cleansing and standardization
   * Handles schema alignment and deduplication
   * Prepares curated datasets

3. **Gold Layer**

   * Builds analytics-ready Star Schema
   * Contains fact and dimension tables
   * Optimized for reporting and BI tools

---

## 📖 Project Overview

This project covers the complete lifecycle of building a modern analytics platform:

1. **Data Architecture**

   * Design of a Lakehouse system using Medallion Architecture

2. **ETL / ELT Pipelines**

   * Ingestion, transformation, and enrichment using PySpark

3. **Data Modeling**

   * Development of fact and dimension tables
   * Star schema design

4. **Analytics & Reporting**

   * Creation of business-ready datasets
   * Support for BI and dashboarding tools

🎯 This repository is ideal for showcasing skills in:

* Data Engineering
* Analytics Engineering
* Apache Spark
* Delta Lake
* ETL Pipeline Development
* Data Modeling
* Lakehouse Architecture

---

## 🛠️ Important Links & Tools

All tools used in this project are free and open-source:

* **[Apache Spark](https://spark.apache.org/):** Distributed data processing engine
* **[Delta Lake](https://delta.io/):** Reliable Lakehouse storage layer
* **[Databricks Bundles](https://docs.databricks.com/en/dev-tools/bundles/index.html):** Deployment framework
* **[Python](https://www.python.org/):** Main programming language
* **[GitHub](https://github.com/):** Version control and collaboration
* **[DrawIO](https://www.drawio.com/):** Architecture and data modeling diagrams

---

## 🚀 Project Requirements

### Building the Data Lakehouse (Data Engineering)

#### Objective

Develop a scalable Lakehouse platform for mobility data to support analytical reporting and business intelligence.

#### Specifications

* **Data Sources**

  * CSV files for customers, drivers, trips, vehicles, locations, and payments

* **Data Quality**

  * Handle missing values and duplicates
  * Standardize data formats

* **Integration**

  * Consolidate multiple datasets into a unified star schema

* **Processing Mode**

  * Incremental ingestion using Structured Streaming
  * Batch-style processing with streaming guarantees

* **Documentation**

  * Provide clear documentation for architecture and data models

---

### BI: Analytics & Reporting (Data Analysis)

#### Objective

Enable analytical insights into:

* **Customer Behavior**
* **Trip Patterns**
* **Revenue Performance**
* **Geographical Distribution**
* **Vehicle Utilization**

These insights support operational and strategic decision-making.

---

## 📊 Data Model

### Dimension Tables

* `dim_customer`
* `dim_vehicle`
* `dim_locations`
* `dim_driver`

### Fact Table

* `fact_trips`

All Gold tables include ETL metadata (`etl_created_at`) for auditing and lineage tracking.

---

## 📂 Repository Structure

```
36_mobility_analytics_platform/
│
├── docs/                                 # Project documentation and architecture details
│   ├── data_architecture.drawio          # Draw.io file shows the project's architecture
│   ├── data_catalog.md                   # Catalog of datasets, including field descriptions and metadata
│   ├── data_flow.png                     # Draw.io file for the data flow diagram
│   ├── naming-conventions.md             # Consistent naming guidelines for tables, columns, and files
|
├── fixtures/                             # Raw CSV datasets
│   ├── customers/
│   ├── drivers/
│   ├── locations/
│   ├── trips/
│   └── vehicles/
│
├── logs/                                 # log file
│
├── resources/                            # Databricks job & pipeline configs
│
├── src/                                  # ETL source code
│   ├── bronze_ingestion.py
│   ├── silver_transformation.py
│   ├── gold_transformation.py
│   ├── main.py
│   ├── io_config.py
│   └── utils/
│
├── scratch/                              # Exploratory notebooks
│
├── tests/                                # Unit tests
│
├── databricks.yml                        # Databricks bundle configuration
│
├── README.md                             # Project documentation
└── .gitignore
```

---

## ▶️ How to Run

### Run Locally

#### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3. Run Pipeline

```bash
python src/main.py
```

---

### Run on Databricks

1. Configure Databricks CLI
2. Update `databricks.yml`
3. Deploy bundle

```bash
databricks bundle deploy
databricks bundle run
```

---

## 📈 Logging & Monitoring

* Centralized logging via `logger.py`
* Delta Lake checkpoints for fault tolerance
* ETL metadata columns for auditability
* Structured logs for pipeline debugging

---

## 🧪 Testing

Run unit tests:

```bash
pytest tests/
```

---

## 🔮 Future Improvements

* Implement SCD Type 2 for dimensions
* Add automated data quality framework
* Integrate CI/CD pipelines
* Build BI dashboards (Power BI / Tableau / Looker)
* Add data lineage and governance tools

---

## 👤 Author

**Thuấn**
Data Engineer / Analytics Engineer

This project is developed for learning, portfolio, and professional development purposes.

---

## 🛡️ License

This project is for educational and portfolio use.
You are free to use and modify it with proper attribution.
