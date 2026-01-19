/*
===============================================================================
Database      : DataWarehouseForSales
Schema        : bronze
===============================================================================
Script Purpose:
    This script performs post-load validation and sanity checks on Bronze
    tables after data ingestion from source systems.

    The objective is to ensure that data has been loaded correctly and meets
    minimum quality expectations before downstream Silver transformations.

    The checks include:
        - Verifying that Bronze tables are not empty after load.
        - Validating expected column counts using system metadata.
        - Detecting accidental header rows inserted as data.
        - Logging row counts and issuing warnings for abnormal conditions.

    All checks are informational or warning-based and do not stop execution,
    but provide visibility into potential data quality issues at the Bronze
    layer.

Parameters:
    None.
    This script does not accept any parameters or return any values.

Usage Example:
    EXEC bronze.usp_load_bronze;
    -- Then run this script for validation
===============================================================================
*/

USE [DataWarehouseForSales];
GO

/* Check that the file is not empty (row count > 0). */
IF NOT EXISTS (SELECT 1 FROM bronze.crm_cust_info)
BEGIN
    RAISERROR('[WARN] Bronze table is empty after load', 0, 1) WITH NOWAIT;
END
GO

/* Check column number */
SELECT  COUNT(*) AS column_count
FROM    sys.columns
WHERE   object_id = OBJECT_ID('bronze.crm_cust_info');
GO

SELECT  COUNT(*) AS column_count
FROM    sys.columns
WHERE   object_id = OBJECT_ID('[bronze].[erp_px_cat_g1v2]');
GO

/* Check NULL header row */
IF EXISTS (
    SELECT  1
    FROM    bronze.crm_cust_info
    WHERE   cst_id = 1
)
BEGIN
    RAISERROR('[WARN] Header row detected in Bronze table', 0, 1) WITH NOWAIT;
END
GO

/* Volume & sanity checks */
DECLARE @row_count INT;
SELECT @row_count = COUNT(*) FROM bronze.crm_cust_info;
RAISERROR('[INFO] Bronze row count: %d', 0, 1, @row_count) WITH NOWAIT;

IF @row_count = 0
BEGIN
    RAISERROR('[WARN] No data loaded into Bronze table', 0, 1) WITH NOWAIT;
END
GO
