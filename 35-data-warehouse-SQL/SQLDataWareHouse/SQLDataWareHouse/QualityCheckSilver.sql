/*
===============================================================================
Quality Checks
===============================================================================
Script Purpose:
    This script performs various quality checks for data consistency, accuracy, 
    and standardization across the 'silver' layer. It includes checks for:
    - Null or duplicate primary keys.
    - Unwanted spaces in string fields.
    - Data standardization and consistency.
    - Invalid date ranges and orders.
    - Data consistency between related fields.

Usage Notes:
    - Run these checks after data loading Silver Layer.
    - Investigate and resolve any discrepancies found during the checks.
===============================================================================
*/
USE [DataWarehouseForSales];
GO

-- ====================================================================
-- Checking 'silver.crm_cust_info'
-- ====================================================================
-- Check for NULLs or Duplicates in Primary Key
-- Expectation: No Results
SELECT      cus.cst_id,
            COUNT(*) AS TotalCustomer
FROM        [silver].[crm_cust_info] AS cus
GROUP BY    cus.cst_id
HAVING      COUNT(*) > 1 OR cus.cst_id IS NULL;
GO

-- Check for Unwanted Spaces
-- Expectation: No Results
SELECT      *
FROM        [silver].[crm_cust_info] AS cu
WHERE       cu.cst_key != TRIM(cu.cst_key)
            OR cu.cst_firstname != TRIM(cu.cst_firstname)
            OR cu.cst_lastname != TRIM(cu.cst_lastname)
            OR cu.cst_marital_status != TRIM(cu.cst_marital_status)
            OR cu.cst_gndr != TRIM(cu.cst_gndr);
GO

-- Data Standardization & Consistency
SELECT      DISTINCT cu.cst_marital_status 
FROM        [silver].[crm_cust_info] AS cu


-- ====================================================================
-- Checking 'silver.crm_prd_info'
-- ====================================================================
-- Check for NULLs or Duplicates in Primary Key
-- Expectation: No Results
SELECT      prd.prd_id,
            COUNT(*) AS TotalProduct
FROM        [silver].[crm_prd_info] AS prd
GROUP BY    prd.prd_id
HAVING      COUNT(*) > 1 OR prd.prd_id IS NULL;
GO

-- Check for Unwanted Spaces
-- Expectation: No Results
SELECT        *
FROM        [silver].[crm_prd_info] AS prd
WHERE       CAST(prd.prd_id AS VARCHAR) != TRIM(CAST(prd.prd_id AS VARCHAR))
            OR prd.prd_cat_id != TRIM(prd.prd_cat_id)
            OR prd.prd_key != TRIM(prd.prd_key)
            OR prd.prd_nm != TRIM(prd.prd_nm)
            OR CAST(prd.prd_cost AS VARCHAR) != TRIM(CAST(prd.prd_cost AS VARCHAR))
            OR prd.prd_line != TRIM(prd.prd_line)
            OR CAST(prd.prd_start_dt AS VARCHAR) != TRIM(CAST(prd.prd_start_dt AS VARCHAR))
            OR CAST(prd.prd_end_dt AS VARCHAR) != TRIM(CAST(prd.prd_end_dt AS VARCHAR));
GO

-- Check for NULLs or Negative Values in Cost
-- Expectation: No Results
SELECT      *
FROM        [silver].[crm_prd_info] AS prd
WHERE       prd.prd_cost < 0
            OR prd.prd_cost IS NULL;
GO

-- Data Standardization & Consistency
SELECT      DISTINCT prd.prd_line
FROM        [silver].[crm_prd_info] AS prd
GO

-- Check for Invalid Date Orders (Start Date > End Date)
-- Expectation: No Results
SELECT      *
FROM        [silver].[crm_prd_info] AS prd
WHERE       prd.prd_start_dt > prd.prd_end_dt;
GO

-- ====================================================================
-- Checking 'silver.crm_sales_details'
-- ====================================================================
-- Check for Invalid Dates
-- Expectation: No Invalid Dates
SELECT      *
FROM        [silver].[crm_sales_details] AS s
WHERE       s.sls_due_dt IS NULL
            OR LEN(s.sls_due_dt) != 10
            OR s.sls_due_dt > '2050-01-01'
            OR s.sls_due_dt < '1900-01-01';
GO

-- Check for Invalid Date Orders (Order Date > Shipping/Due Dates)
-- Expectation: No Results
SELECT      *
FROM        [silver].[crm_sales_details] AS s
WHERE       s.sls_order_dt > s.sls_ship_dt
            OR s.sls_order_dt > s.sls_due_dt;
GO

-- Check Data Consistency: Sales = Quantity * Price
-- Expectation: No Results
SELECT      *
FROM        [silver].[crm_sales_details] AS s
WHERE       s.sls_sales != (s.sls_quantity * s.sls_price)
            OR s.sls_sales IS NULL
            OR s.sls_quantity IS NULL
            OR s.sls_price IS NULL
            OR s.sls_sales <= 0
            OR s.sls_quantity <= 0
            OR s.sls_price <= 0;
GO

-- ====================================================================
-- Checking 'silver.erp_cust_az12'
-- ====================================================================
-- Identify Out-of-Range Dates
-- Expectation: Birthdates between 1924-01-01 and Today
SELECT      *
FROM        [silver].[erp_cust_az12] AS cu
WHERE       cu.bdate < '1924-01-01'
            AND cu.bdate > GETDATE();
GO

-- Data Standardization & Consistency
SELECT      DISTINCT cu.gen
FROM        [silver].[erp_cust_az12] AS cu
GO

-- ====================================================================
-- Checking 'silver.erp_loc_a101'
-- ====================================================================
-- Data Standardization & Consistency
SELECT      DISTINCT loc.cntry
FROM        [silver].[erp_loc_a101] AS loc
ORDER BY    loc.cntry;
GO

-- ====================================================================
-- Checking 'silver.erp_px_cat_g1v2'
-- ====================================================================
-- Check for Unwanted Spaces
-- Expectation: No Results
SELECT      *
FROM        [silver].[erp_px_cat_g1v2] AS px
WHERE       px.id != TRIM(px.id)
            OR px.cat != TRIM(px.cat)
            OR px.subcat != TRIM(px.subcat)
            OR px.maintenance != TRIM(px.maintenance);
GO

-- Data Standardization & Consistency
SELECT      DISTINCT px.maintenance 
FROM        [silver].[erp_px_cat_g1v2] AS px
GO
