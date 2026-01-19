/*
===============================================================================
Stored Procedure: Load Silver Layer (Bronze -> Silver)
===============================================================================
Script Purpose:
    This stored procedure performs the ETL (Extract, Transform, Load) process to 
    populate the 'silver' schema tables from the 'bronze' schema.
    Actions Performed:
        - Truncates Silver tables.
        - Inserts transformed and cleansed data from Bronze into Silver tables.
        
Parameters:
    None. 
      This stored procedure does not accept any parameters or return any values.

Usage Example:
    EXEC Silver.load_silver;
===============================================================================
*/

USE [DataWarehouseForSales];
GO

CREATE OR ALTER PROCEDURE [silver].[usp_load_silver]
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE
    @run_id             UNIQUEIDENTIFIER = NEWID(),
    @step_name          NVARCHAR(100),
    @target_object      NVARCHAR(100),
    @start_time         DATETIME,
    @end_time           DATETIME,
    @batch_start_time   DATETIME,
    @batch_end_time     DATETIME,
    @row_count          INT,
    @duration           INT;

    BEGIN TRY
        /* ===================== BATCH START ===================== */
        SET @batch_start_time = GETDATE();
        RAISERROR('[INFO] Starting Load Silver Layer', 0, 1) WITH NOWAIT;
        RAISERROR('================================================', 0, 1) WITH NOWAIT;

        /* LOAD CRM TABLES */
        RAISERROR('[INFO] Load CRM Tables', 0, 1) WITH NOWAIT;
        RAISERROR('================================================', 0, 1) WITH NOWAIT;
        /* ===================== crm_cust_info ===================== */
        SET @step_name     = 'Load crm_cust_info';
        SET @target_object = 'silver.crm_cust_info';
        SET @start_time    = GETDATE();
        INSERT INTO [dbo].[etl_pipeline_audit](run_id, layer_name, step_name, source_system, target_object, start_time, end_time,
                                               duration_sec, row_count, status, message)
        VALUES (@run_id, 'Silver', @step_name, 'CRM', @target_object, @start_time, @start_time, 0, 0, 'STARTED', 'Step started');
        RAISERROR('[INFO] Truncating [silver].[crm_cust_info]', 0, 1) WITH NOWAIT;
        TRUNCATE TABLE [silver].[crm_cust_info];
        RAISERROR('[INFO] Insert -> [silver].[crm_cust_info]', 0, 1) WITH NOWAIT;
        INSERT INTO [silver].[crm_cust_info] (cst_id, cst_key, cst_firstname, cst_lastname, 
                                              cst_marital_status, cst_gndr, cst_create_date)
        SELECT      cst_id,
                    cst_key,
                    NULLIF(TRIM(cst_firstname), '') AS cst_firstname,
                    NULLIF(TRIM(cst_lastname), '')  AS cst_lastname,
                    CASE
                        WHEN UPPER(TRIM(cst_marital_status)) = 'S' THEN 'Single'
                        WHEN UPPER(TRIM(cst_marital_status)) = 'M' THEN 'Married'
                        ELSE 'N/A'
                    END AS cst_marital_status, -- Normalize marital status values to readable format
                    CASE
                        WHEN UPPER(TRIM(cst_gndr)) = 'F' THEN 'Female'
                        WHEN UPPER(TRIM(cst_gndr)) = 'M' THEN 'Male'
                        ELSE 'N/A'
                    END AS cst_gndr, -- Normalize gender values to readable format
                    cst_create_date
        FROM (
                    SELECT  *,
                            ROW_NUMBER() OVER (PARTITION BY c.cst_id ORDER BY c.cst_create_date DESC) AS flag_last
                    FROM    bronze.crm_cust_info AS c
                    WHERE    c.cst_id IS NOT NULL
        ) AS t
        WHERE       t.flag_last = 1 -- Select the most recent record per customer
        ORDER BY    cst_id ASC;

        SET @row_count = @@ROWCOUNT;
        SET @end_time  = GETDATE();
        SET @duration  = DATEDIFF(SECOND, @start_time, @end_time);
        UPDATE  [dbo].[etl_pipeline_audit]
        SET     end_time        = @end_time,
                duration_sec    = @duration,
                row_count       = @row_count,
                status          = 'SUCCESS',
                message         = 'Load completed successfully'
        WHERE   run_id = @run_id
                AND step_name = @step_name;
        RAISERROR('[INFO] Rows Inserted: %d', 0, 1, @row_count) WITH NOWAIT;
        RAISERROR('[INFO] Duration: %d seconds', 0, 1, @duration) WITH NOWAIT;
        RAISERROR('================================================', 0, 1) WITH NOWAIT;

        /* ===================== crm_prd_info ===================== */
        SET @step_name     = 'Load crm_prd_info';
        SET @target_object = 'silver.crm_prd_info';
        SET @start_time    = GETDATE();
        INSERT INTO [dbo].[etl_pipeline_audit](run_id, layer_name, step_name, source_system, target_object, start_time, end_time,
                                               duration_sec, row_count, status, message)
        VALUES (@run_id, 'Silver', @step_name, 'CRM', @target_object, @start_time, @start_time, 0, 0, 'STARTED', 'Step started');
        RAISERROR('[INFO] Truncating [silver].[crm_prd_info]', 0, 1) WITH NOWAIT;
        TRUNCATE TABLE [silver].[crm_prd_info];
        RAISERROR('[INFO] Insert -> [silver].[crm_prd_info]', 0, 1) WITH NOWAIT;
        INSERT INTO [silver].[crm_prd_info]([prd_id], [prd_cat_id], [prd_key], [prd_nm], [prd_cost], [prd_line], 
                                             [prd_start_dt], [prd_end_dt])
        SELECT      prd.prd_id AS prd_id,
                    REPLACE(SUBSTRING(TRIM(prd.prd_key), 1, 5), '-', '_') AS prd_cat_id, -- Extract category ID
                    SUBSTRING(TRIM(prd.prd_key), 7, LEN(prd.prd_key)) AS prd_key,        -- Extract product key
                    prd.prd_nm AS prd_nm,
                    COALESCE(prd.prd_cost, 0) AS prd_cost,
                    CASE
                        WHEN UPPER(TRIM(prd.prd_line)) = 'R' THEN 'Road'
                        WHEN UPPER(TRIM(prd.prd_line)) = 'S' THEN 'Other Sales'
                        WHEN UPPER(TRIM(prd.prd_line)) = 'M' THEN 'Mountain'
                        WHEN UPPER(TRIM(prd.prd_line)) = 'T' THEN 'Touring'
                        ELSE 'N/A' -- -- Map product line codes to descriptive values
                    END AS prd_line,
                    CAST(prd.prd_start_dt AS DATE) AS prd_start_dt,
                    CAST(DATEADD(DAY, -1, LEAD(CAST(prd.prd_start_dt AS DATE)) OVER (PARTITION BY prd.prd_key ORDER BY prd.prd_start_dt)) AS DATE) AS prd_end_dt
        FROM        bronze.crm_prd_info AS prd
        ORDER BY    prd_id ASC;

        SET @row_count = @@ROWCOUNT;
        SET @end_time  = GETDATE();
        SET @duration  = DATEDIFF(SECOND, @start_time, @end_time);
        UPDATE  [dbo].[etl_pipeline_audit]
        SET     end_time        = @end_time,
                duration_sec    = @duration,
                row_count       = @row_count,
                status          = 'SUCCESS',
                message         = 'Load completed successfully'
        WHERE   run_id = @run_id
                AND step_name = @step_name;
        RAISERROR('[INFO] Rows Inserted: %d', 0, 1, @row_count) WITH NOWAIT;
        RAISERROR('[INFO] Duration: %d seconds', 0, 1, @duration) WITH NOWAIT;
        RAISERROR('================================================', 0, 1) WITH NOWAIT;

        /* ===================== crm_sales_details ===================== */
        SET @step_name     = 'Load crm_sales_details';
        SET @target_object = 'silver.crm_sales_details';
        SET @start_time    = GETDATE();
        INSERT INTO [dbo].[etl_pipeline_audit](run_id, layer_name, step_name, source_system, target_object, start_time, end_time,
                                               duration_sec, row_count, status, message)
        VALUES (@run_id, 'Silver', @step_name, 'CRM', @target_object, @start_time, @start_time, 0, 0, 'STARTED', 'Step started');
        RAISERROR('[INFO] Truncating [silver].[crm_sales_details]', 0, 1) WITH NOWAIT;
        TRUNCATE TABLE [silver].[crm_sales_details];
        RAISERROR('[INFO] Insert -> [silver].[crm_sales_details]', 0, 1) WITH NOWAIT;
        INSERT INTO [silver].[crm_sales_details]([sls_ord_num], [sls_prd_key], [sls_cust_id], [sls_order_dt], [sls_ship_dt], [sls_due_dt],
                                                 [sls_sales], [sls_quantity], [sls_price])
        SELECT  s.sls_ord_num AS sls_ord_num,
                s.sls_prd_key AS sls_prd_key,
                s.sls_cust_id AS sls_cust_id,
                CASE
                    WHEN s.sls_order_dt = 0 OR LEN(s.sls_order_dt) != 8 THEN NULL
                    ELSE CAST(CAST(s.sls_order_dt AS VARCHAR) AS DATE)
                END AS sls_order_dt,
                CASE
                    WHEN s.sls_ship_dt = 0 OR LEN(s.sls_ship_dt) != 8 THEN NULL
                    ELSE CAST(CAST(s.sls_ship_dt AS VARCHAR) AS DATE)
                END AS sls_ship_dt,
                CASE
                    WHEN s.sls_due_dt = 0 OR LEN(s.sls_due_dt) != 8 THEN NULL
                    ELSE CAST(CAST(s.sls_due_dt AS VARCHAR) AS DATE)
                END AS sls_due_dt,
                CASE
                    WHEN s.sls_sales IS NULL OR s.sls_sales <= 0 OR s.sls_sales != s.sls_quantity * ABS(s.sls_price) THEN s.sls_quantity * ABS(s.sls_price)
                    ELSE s.sls_sales
                END AS sls_sales, -- Recalculate sales if original value is missing or incorrect
                s.sls_quantity AS sls_quantity,
                CASE
                    WHEN s.sls_price IS NULL OR s.sls_price <= 0 THEN ABS(s.sls_sales) / NULLIF(s.sls_quantity, 0)
                    ELSE s.sls_price
                END AS sls_price -- Derive price if original value is invalid.
        FROM    [bronze].[crm_sales_details] AS s;

        SET @row_count = @@ROWCOUNT;
        SET @end_time  = GETDATE();
        SET @duration  = DATEDIFF(SECOND, @start_time, @end_time);
        UPDATE  [dbo].[etl_pipeline_audit]
        SET     end_time        = @end_time,
                duration_sec    = @duration,
                row_count       = @row_count,
                status          = 'SUCCESS',
                message         = 'Load completed successfully'
        WHERE   run_id = @run_id
                AND step_name = @step_name;
        RAISERROR('[INFO] Rows Inserted: %d', 0, 1, @row_count) WITH NOWAIT;
        RAISERROR('[INFO] Duration: %d seconds', 0, 1, @duration) WITH NOWAIT;
        RAISERROR('================================================', 0, 1) WITH NOWAIT;

        /* LOAD ERP TABLES */
        RAISERROR('[INFO] Load ERP Tables', 0, 1) WITH NOWAIT;
        RAISERROR('================================================', 0, 1) WITH NOWAIT;
        /* ===================== erp_cust_az12 ===================== */
        SET @step_name     = 'Load erp_cust_az12';
        SET @target_object = 'silver.erp_cust_az12';
        SET @start_time    = GETDATE();
        INSERT INTO [dbo].[etl_pipeline_audit](run_id, layer_name, step_name, source_system, target_object, start_time, end_time,
                                               duration_sec, row_count, status, message)
        VALUES (@run_id, 'Silver', @step_name, 'ERP', @target_object, @start_time, @start_time, 0, 0, 'STARTED', 'Step started');
        RAISERROR('[INFO] Truncating [silver].[erp_cust_az12]', 0, 1) WITH NOWAIT;
        TRUNCATE TABLE [silver].[erp_cust_az12];
        RAISERROR('[INFO] Insert -> [silver].[erp_cust_az12]', 0, 1) WITH NOWAIT;
        INSERT INTO [silver].[erp_cust_az12]([cid], [bdate], [gen])
        SELECT  CASE
                    WHEN TRIM(az.cid) LIKE 'NAS%' THEN SUBSTRING(TRIM(az.cid), 4, LEN(az.cid))
                    ELSE TRIM(az.cid)
                END AS cid,
                CASE
                    WHEN az.bdate > GETDATE() THEN NULL
                    ELSE az.bdate
                END AS bdate,
                CASE
                    WHEN TRIM(az.gen) IN ('F', 'FEMALE') THEN 'Female'
                    WHEN TRIM(az.gen) IN ('M', 'MALE') THEN 'Male'
                    ELSE 'N/A'
                END AS gen -- Normalize marital status values to readable format                
        FROM    [bronze].[erp_cust_az12] as az;

        SET @row_count = @@ROWCOUNT;
        SET @end_time  = GETDATE();
        SET @duration  = DATEDIFF(SECOND, @start_time, @end_time);
        UPDATE  [dbo].[etl_pipeline_audit]
        SET     end_time        = @end_time,
                duration_sec    = @duration,
                row_count       = @row_count,
                status          = 'SUCCESS',
                message         = 'Load completed successfully'
        WHERE   run_id = @run_id
                AND step_name = @step_name;
        RAISERROR('[INFO] Rows Inserted: %d', 0, 1, @row_count) WITH NOWAIT;
        RAISERROR('[INFO] Duration: %d seconds', 0, 1, @duration) WITH NOWAIT;
        RAISERROR('================================================', 0, 1) WITH NOWAIT;

        /* ===================== erp_loc_a101 ===================== */
        SET @step_name     = 'Load erp_loc_a101';
        SET @target_object = 'silver.erp_loc_a101';
        SET @start_time    = GETDATE();
        INSERT INTO [dbo].[etl_pipeline_audit](run_id, layer_name, step_name, source_system, target_object, start_time, end_time,
                                               duration_sec, row_count, status, message)
        VALUES (@run_id, 'Silver', @step_name, 'ERP', @target_object, @start_time, @start_time, 0, 0, 'STARTED', 'Step started');
        RAISERROR('[INFO] Truncating [silver].[erp_loc_a101]', 0, 1) WITH NOWAIT;
        TRUNCATE TABLE [silver].[erp_loc_a101];
        RAISERROR('[INFO] Insert -> [silver].[erp_loc_a101]', 0, 1) WITH NOWAIT;
        INSERT INTO [silver].[erp_loc_a101]([cid], [cntry])
        SELECT  REPLACE(TRIM(a1.cid), '-', '') AS cid,
                CASE
                    WHEN TRIM(a1.cntry) IN ('US', 'USA') THEN 'United States'
                    WHEN TRIM(a1.cntry) = 'DE' THEN 'Germany'
                    WHEN TRIM(a1.cntry) = '' OR a1.cntry IS NULL THEN 'N/A'
                    ELSE TRIM(a1.cntry)
                END AS cntry
        FROM    [bronze].[erp_loc_a101] AS a1;

        SET @row_count = @@ROWCOUNT;
        SET @end_time  = GETDATE();
        SET @duration  = DATEDIFF(SECOND, @start_time, @end_time);
        UPDATE  [dbo].[etl_pipeline_audit]
        SET     end_time        = @end_time,
                duration_sec    = @duration,
                row_count       = @row_count,
                status          = 'SUCCESS',
                message         = 'Load completed successfully'
        WHERE   run_id = @run_id
                AND step_name = @step_name;
        RAISERROR('[INFO] Rows Inserted: %d', 0, 1, @row_count) WITH NOWAIT;
        RAISERROR('[INFO] Duration: %d seconds', 0, 1, @duration) WITH NOWAIT;
        RAISERROR('================================================', 0, 1) WITH NOWAIT;

        /* ===================== erp_px_cat_g1v2 ===================== */
        SET @step_name     = 'Load erp_px_cat_g1v2';
        SET @target_object = 'silver.erp_px_cat_g1v2';
        SET @start_time    = GETDATE();
        INSERT INTO [dbo].[etl_pipeline_audit](run_id, layer_name, step_name, source_system, target_object, start_time, end_time,
                                               duration_sec, row_count, status, message)
        VALUES (@run_id, 'Silver', @step_name, 'ERP', @target_object, @start_time, @start_time, 0, 0, 'STARTED', 'Step started');
        RAISERROR('[INFO] Truncating [silver].[erp_px_cat_g1v2]', 0, 1) WITH NOWAIT;
        TRUNCATE TABLE [silver].[erp_px_cat_g1v2];
        RAISERROR('[INFO] Insert -> [silver].[erp_px_cat_g1v2]', 0, 1) WITH NOWAIT;
        INSERT INTO [silver].[erp_px_cat_g1v2]([id], [cat], [subcat], [maintenance])
        SELECT  TRIM(px.id) AS id,
                TRIM(px.cat) AS cat,
                TRIM(px.subcat) AS subcat,
                TRIM(px.maintenance) AS maintenance
        FROM    [bronze].[erp_px_cat_g1v2] AS px;

        SET @row_count = @@ROWCOUNT;
        SET @end_time  = GETDATE();
        SET @duration  = DATEDIFF(SECOND, @start_time, @end_time);
        UPDATE  [dbo].[etl_pipeline_audit]
        SET     end_time        = @end_time,
                duration_sec    = @duration,
                row_count       = @row_count,
                status          = 'SUCCESS',
                message         = 'Load completed successfully'
        WHERE   run_id = @run_id
                AND step_name = @step_name;
        RAISERROR('[INFO] Rows Inserted: %d', 0, 1, @row_count) WITH NOWAIT;
        RAISERROR('[INFO] Duration: %d seconds', 0, 1, @duration) WITH NOWAIT;
        RAISERROR('================================================', 0, 1) WITH NOWAIT;
    END TRY
    BEGIN CATCH
        /* ERROR HANDLING: Capture and rethrow detailed error information */
        DECLARE 
            @ErrNumber   INT = ERROR_NUMBER(),
            @ErrSeverity INT = ERROR_SEVERITY(),
            @ErrState    INT = ERROR_STATE(),
            @ErrLine     INT = ERROR_LINE(),
            @ErrProc     NVARCHAR(200) = ISNULL(ERROR_PROCEDURE(), 'N/A'),
            @ErrMsg      NVARCHAR(4000) = ERROR_MESSAGE();

        /* Insert error log */
        INSERT INTO [dbo].[etl_error_log](run_id, layer_name, table_name, error_number, error_severity, error_state,
                                          error_line, error_procedure, error_message)
        VALUES (@run_id, 'Silver', @target_object, @ErrNumber, @ErrSeverity, @ErrState, @ErrLine, @ErrProc, @ErrMsg);

        /* Update audit status to FAILED */
        SET @duration  = DATEDIFF(SECOND, @start_time, @end_time);
        UPDATE  [dbo].[etl_pipeline_audit]
        SET     end_time        = GETDATE(),
                duration_sec    = @duration,
                status          = 'FAILED',
                message         = @ErrMsg
        WHERE   run_id = @run_id
                AND step_name = @step_name;

        RAISERROR('================================================', 0, 1) WITH NOWAIT;
        RAISERROR('[ERROR] Silver Load FAILED', 0, 1) WITH NOWAIT;
        RAISERROR(@ErrMsg, @ErrSeverity, @ErrState);
        RAISERROR('================================================', 0, 1) WITH NOWAIT;
    END CATCH
END;
GO

EXEC [silver].[usp_load_silver];
GO

SELECT * FROM [silver].[crm_cust_info];
SELECT * FROM [silver].[crm_prd_info];
SELECT * FROM [silver].[crm_sales_details];
SELECT * FROM [silver].[erp_cust_az12];
SELECT * FROM [silver].[erp_loc_a101];
SELECT * FROM [silver].[erp_px_cat_g1v2];
SELECT * FROM [dbo].[etl_pipeline_audit];
SELECT * FROM [dbo].[etl_error_log];
GO
