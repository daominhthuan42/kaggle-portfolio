/*
===============================================================================
Quality Checks
===============================================================================
Script Purpose:
    This script performs quality checks to validate the integrity, consistency, 
    and accuracy of the Gold Layer. These checks ensure:
    - Uniqueness of surrogate keys in dimension tables.
    - Referential integrity between fact and dimension tables.
    - Validation of relationships in the data model for analytical purposes.

Usage Notes:
    - Investigate and resolve any discrepancies found during the checks.
===============================================================================
*/

USE    [DataWarehouseForSales];
GO

-- ====================================================================
-- Checking 'gold.dim_customers'
-- ====================================================================
-- Check for Uniqueness of Customer Key in gold.dim_customers
-- Expectation: No results 
SELECT      cu.customer_key,
            COUNT(*)
FROM        [gold].[dim_customers] AS cu
GROUP BY    cu.customer_key
HAVING      COUNT(*) > 1 OR cu.customer_key IS NULL;
GO

-- ====================================================================
-- Checking 'gold.product_key'
-- ====================================================================
-- Check for Uniqueness of Product Key in gold.dim_products
-- Expectation: No results 
SELECT      pr.product_key,
            COUNT(*)
FROM        [gold].[dim_products] AS pr
GROUP BY    pr.product_key
HAVING      COUNT(*) > 1 OR pr.product_key IS NULL;
GO

-- ====================================================================
-- Checking 'gold.fact_sales'
-- ====================================================================
-- Check the data model connectivity between fact and dimensions
SELECT      * 
FROM        gold.fact_sales f
LEFT JOIN   gold.dim_customers c ON c.customer_key = f.customer_key
LEFT JOIN   gold.dim_products p ON p.product_key = f.product_key
WHERE       p.product_key IS NULL 
            OR c.customer_key IS NULL;
GO
