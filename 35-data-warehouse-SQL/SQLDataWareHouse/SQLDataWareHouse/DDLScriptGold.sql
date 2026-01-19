/*
===============================================================================
DDL Script: Create Gold Views
===============================================================================
Script Purpose:
    This script creates views for the Gold layer in the data warehouse. 
    The Gold layer represents the final dimension and fact tables (Star Schema)

    Each view performs transformations and combines data from the Silver layer 
    to produce a clean, enriched, and business-ready dataset.

Usage:
    - These views can be queried directly for analytics and reporting.
===============================================================================
*/

USE [DataWarehouseForSales];
GO

IF OBJECT_ID('gold.dim_customers', 'V') IS NOT NULL
    DROP VIEW gold.dim_customers;
GO

CREATE OR ALTER VIEW gold.dim_customers AS
SELECT      ROW_NUMBER() OVER (ORDER BY cust.cst_id) AS customer_key,
            cust.cst_id AS customer_id,
            cust.cst_key AS customer_number,
            cust.cst_firstname AS first_name,
            cust.cst_lastname AS last_name,
            cust.cst_marital_status AS marital_status,
            CASE
                WHEN cust.cst_gndr != 'N/A' THEN cust.cst_gndr -- CRM is the primary source for gender
                ELSE COALESCE(cu.gen, 'N/A') -- Fallback to ERP data
            END AS gender,
            cu.bdate AS birthdate,
            loc.cntry AS country
FROM        [silver].[crm_cust_info] AS cust
LEFT JOIN   [silver].[erp_cust_az12] AS cu ON cu.cid = cust.cst_key
LEFT JOIN   [silver].[erp_loc_a101] AS loc ON loc.cid = cu.cid;
GO

IF OBJECT_ID('gold.dim_products', 'V') IS NOT NULL
    DROP VIEW gold.dim_products;
GO

CREATE OR ALTER VIEW gold.dim_products AS
SELECT      ROW_NUMBER() OVER (ORDER BY prd.prd_start_dt, prd.prd_key) AS product_key, -- Surrogate key
            prd.prd_id AS product_id,
            prd.prd_key AS product_number,
            prd.prd_cat_id AS category_id,
            px.cat AS category,
            px.subcat AS subcategory,
            px.maintenance AS maintenance,
            prd.prd_cost AS cost,
            prd.prd_line AS product_line,
            prd.prd_start_dt AS start_date
FROM        [silver].[crm_prd_info] AS prd
LEFT JOIN   [silver].[erp_px_cat_g1v2] AS px ON px.id = prd.prd_cat_id
WHERE       prd.prd_end_dt IS NULL;
GO

IF OBJECT_ID('gold.fact_sales', 'V') IS NOT NULL
    DROP VIEW gold.fact_sales;
GO

CREATE OR ALTER VIEW gold.fact_sales AS
SELECT      sd.sls_ord_num AS order_number,
            pr.product_key AS product_key,
            cu.customer_key AS customer_key,
            sd.sls_order_dt AS order_date,
            sd.sls_ship_dt AS shipping_date,
            sd.sls_due_dt AS due_date,
            sd.sls_sales AS sales_amount,
            sd.sls_quantity AS quantity,
            sd.sls_price AS price
FROM        [silver].[crm_sales_details] AS sd
LEFT JOIN   [gold].[dim_products] AS pr ON pr.product_number = sd.sls_prd_key
LEFT JOIN   [gold].[dim_customers] AS cu ON cu.customer_id = sd.sls_cust_id;
GO

SELECT * FROM [gold].[dim_customers];
GO

SELECT * FROM [gold].[dim_products];
GO

SELECT * FROM [gold].[fact_sales];
GO
