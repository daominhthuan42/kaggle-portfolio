# Data Catalog for Gold Layer

## Overview

The Gold Layer represents the curated, business-ready data model designed to support analytical, reporting, and decision-making use cases.  
It follows a dimensional modeling approach, consisting of **dimension tables** and **fact tables** related to trips, customers, drivers, vehicles, locations, and payments.

This layer ensures consistent definitions, historical tracking, and high data quality for downstream consumers.

---

## 1. **gold.dim_customers**

- **Purpose:** Stores master data related to customers, including personal and geographic information, to support customer-centric analytics.

- **Columns:**

| Column Name            | Data Type  | Description                                                                 |
|------------------------|-----------|-----------------------------------------------------------------------------|
| customer_id            | INT       | Unique identifier assigned to each customer.                                |
| full_name              | STRING    | Full name of the customer.                                                   |
| email                  | STRING    | Email address used for customer communication and identification.           |
| city                   | STRING    | City where the customer is primarily located.                               |
| signup_date            | DATE      | Date when the customer registered on the platform.                          |
| last_updated_timestamp | TIMESTAMP | Timestamp of the most recent update to the customer record.                 |
| ingested_at            | TIMESTAMP | Timestamp indicating when the record was ingested into the data platform.   |

---

## 2. **gold.dim_drivers**

- **Purpose:** Contains information about drivers operating on the platform, including identification, performance, and location attributes.

- **Columns:**

| Column Name            | Data Type  | Description                                                                 |
|------------------------|-----------|-----------------------------------------------------------------------------|
| driver_id              | INT       | Unique identifier for each driver.                                          |
| vehicle_id             | INT       | Identifier of the vehicle assigned to the driver.                           |
| full_name              | STRING    | Full name of the driver.                                                     |
| driver_rating          | DOUBLE    | Average customer rating for the driver.                                     |
| city                   | STRING    | Primary operating city of the driver.                                       |
| last_updated_timestamp | TIMESTAMP | Timestamp of the latest driver record update.                               |
| ingested_at            | TIMESTAMP | Timestamp when the record was ingested into the platform.                   |

---

## 3. **gold.dim_locations**

- **Purpose:** Stores geographic and spatial reference data used for trip origin and destination analysis.

- **Columns:**

| Column Name            | Data Type  | Description                                                                 |
|------------------------|-----------|-----------------------------------------------------------------------------|
| location_id            | INT       | Unique identifier for each location.                                        |
| city                   | STRING    | City name of the location.                                                   |
| state                  | STRING    | State or province of the location.                                          |
| country                | STRING    | Country where the location is situated.                                     |
| latitude               | DOUBLE    | Geographic latitude coordinate.                                             |
| longitude              | DOUBLE    | Geographic longitude coordinate.                                            |
| last_updated_timestamp | TIMESTAMP | Timestamp of the most recent update to location data.                        |
| ingested_at            | TIMESTAMP | Timestamp when the record was ingested into the platform.                   |

---

## 4. **gold.dim_payments**

- **Purpose:** Stores reference and transactional metadata related to customer payments for completed trips.

- **Columns:**

| Column Name            | Data Type  | Description                                                                 |
|------------------------|-----------|-----------------------------------------------------------------------------|
| payment_id             | INT       | Unique identifier for each payment transaction.                             |
| trip_id                | INT       | Identifier of the associated trip.                                          |
| customer_id            | INT       | Identifier of the customer who made the payment.                            |
| payment_channel        | STRING    | Payment method or channel used (e.g., Card, Wallet, Cash).                  |
| amount                 | DOUBLE    | Total payment amount for the trip.                                          |
| transaction_time       | TIMESTAMP | Timestamp when the payment was processed.                                   |
| last_updated_timestamp | TIMESTAMP | Timestamp of the latest update to the payment record.                        |
| ingested_at            | TIMESTAMP | Timestamp when the record was ingested into the platform.                   |

---

## 5. **gold.dim_vehicles**

- **Purpose:** Maintains detailed information about vehicles used on the platform, supporting fleet and performance analysis.

- **Columns:**

| Column Name            | Data Type  | Description                                                                 |
|------------------------|-----------|-----------------------------------------------------------------------------|
| vehicle_id             | INT       | Unique identifier for each vehicle.                                         |
| model                  | STRING    | Vehicle model name.                                                         |
| make                   | STRING    | Manufacturer or brand of the vehicle.                                       |
| year                   | INT       | Manufacturing year of the vehicle.                                          |
| vehicle_type           | STRING    | Type or category of the vehicle (e.g., Sedan, SUV, Bike).                   |
| last_updated_timestamp | TIMESTAMP | Timestamp of the most recent vehicle record update.                          |
| ingested_at            | TIMESTAMP | Timestamp when the record was ingested into the platform.                   |

---

## 6. **gold.fact_trips**

- **Purpose:** Stores transactional trip-level data, representing completed, cancelled, and ongoing rides.  
  This table serves as the central fact table for operational and financial analytics.

- **Columns:**

| Column Name            | Data Type  | Description                                                                 |
|------------------------|-----------|-----------------------------------------------------------------------------|
| trip_id                | INT       | Unique identifier for each trip.                                            |
| driver_id              | INT       | Identifier of the driver assigned to the trip.                              |
| customer_id            | INT       | Identifier of the customer who requested the trip.                          |
| vehicle_id             | INT       | Identifier of the vehicle used for the trip.                                |
| trip_start_time        | TIMESTAMP | Timestamp when the trip started.                                            |
| trip_end_time          | TIMESTAMP | Timestamp when the trip ended.                                              |
| start_location         | STRING    | Starting location of the trip.                                              |
| end_location           | STRING    | Destination location of the trip.                                           |
| distance_km            | DOUBLE    | Total distance traveled during the trip (in kilometers).                   |
| fare_amount            | DOUBLE    | Total fare charged for the trip.                                            |
| payment_method         | STRING    | Payment method used for the trip.                                           |
| trip_status            | STRING    | Current or final status of the trip (e.g., Completed, Cancelled).           |
| last_updated_timestamp | TIMESTAMP | Timestamp of the latest update to the trip record.                          |
| ingested_at            | TIMESTAMP | Timestamp when the record was ingested into the platform.                   |

---

## Notes

- All tables follow CDC-based ingestion and maintain `last_updated_timestamp` for change tracking.
- The `ingested_at` column is used for data lineage, auditing, and pipeline monitoring.
- Dimension tables provide descriptive context for analytical queries on `fact_trips`.
- This Gold Layer model is optimized for BI reporting, dashboarding, and advanced analytics.
