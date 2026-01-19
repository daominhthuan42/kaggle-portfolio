/*
===============================================================================
Stored Procedure: usp_load_bronze (Source -> Bronze)
Database        : DataWarehouseForSales
Schema          : bronze
===============================================================================
Script Purpose:
    This stored procedure loads raw data from external CSV files into the
    'bronze' schema of the Data Warehouse.

    It performs the following actions:
        - Truncates Bronze tables prior to loading.
        - Uses the BULK INSERT command to ingest data from source CSV files.

Parameters:
    None.
    This stored procedure does not accept any parameters or return any values.

Usage Example:
    EXEC bronze.usp_load_bronze;
===============================================================================
*/

USE [DataWarehouseForSales];
GO

CREATE OR ALTER PROCEDURE [bronze].[usp_load_bronze]
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
        RAISERROR('[INFO] Starting Load Bronze Layer', 0, 1) WITH NOWAIT;
        RAISERROR('================================================', 0, 1) WITH NOWAIT;

        /* LOAD CRM TABLES */
        RAISERROR('[INFO] Load CRM Tables', 0, 1) WITH NOWAIT;
        RAISERROR('================================================', 0, 1) WITH NOWAIT;

        /* ===================== crm_cust_info ===================== */
        SET @step_name     = 'Load crm_cust_info';
        SET @target_object = 'bronze.crm_cust_info';
        SET @start_time    = GETDATE();
        INSERT INTO [dbo].[etl_pipeline_audit](run_id, layer_name, step_name, source_system, target_object, start_time, end_time,
                                               duration_sec, row_count, status, message)
        VALUES (@run_id, 'Bronze', @step_name, 'CRM', @target_object, @start_time, @start_time, 0, 0, 'STARTED', 'Step started');

        RAISERROR('[INFO] Truncating [bronze].[crm_cust_info]', 0, 1) WITH NOWAIT;
        TRUNCATE TABLE [bronze].[crm_cust_info];
        RAISERROR('[INFO] Bulk Insert -> [bronze].[crm_cust_info]', 0, 1) WITH NOWAIT;
        BULK INSERT [bronze].[crm_cust_info]
        FROM 'C:\01_Data\02-kaggle-portfolio\35-data-warehouse-SQL\00-datasets\source_crm\cust_info.csv'
        WITH (
            FIRSTROW        = 2,          /* Skip CSV header                */
            FIELDTERMINATOR = ',',        /* Column delimiter               */
            ROWTERMINATOR   = '0x0D0A',   /* CRLF (Windows line ending)     */
            CODEPAGE        = '65001',    /* UTF-8 encoding                 */
            TABLOCK                       /* Optimize bulk load performance */
        )
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
        SET @target_object = 'bronze.crm_prd_info';
        SET @start_time    = GETDATE();
        INSERT INTO [dbo].[etl_pipeline_audit](run_id, layer_name, step_name, source_system, target_object, start_time, end_time,
                                               duration_sec, row_count, status, message)
        VALUES (@run_id, 'Bronze', @step_name, 'CRM', @target_object, @start_time, @start_time, 0, 0, 'STARTED', 'Step started');

        SET @start_time = GETDATE();
        RAISERROR('[INFO] Truncating [bronze].[crm_prd_info]', 0, 1) WITH NOWAIT;
        TRUNCATE TABLE [bronze].[crm_prd_info];
        RAISERROR('[INFO] Bulk Insert -> [bronze].[crm_prd_info]', 0, 1) WITH NOWAIT;
        BULK INSERT [bronze].[crm_prd_info]
        FROM 'C:\01_Data\02-kaggle-portfolio\35-data-warehouse-SQL\00-datasets\source_crm\prd_info.csv'
        WITH (
            FIRSTROW        = 2,          /* Skip CSV header                */
            FIELDTERMINATOR = ',',        /* Column delimiter               */
            ROWTERMINATOR   = '0x0D0A',   /* CRLF (Windows line ending)     */
            CODEPAGE        = '65001',    /* UTF-8 encoding                 */
            TABLOCK                       /* Optimize bulk load performance */
        )
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
        SET @target_object = 'bronze.crm_sales_details';
        SET @start_time    = GETDATE();
        INSERT INTO [dbo].[etl_pipeline_audit](run_id, layer_name, step_name, source_system, target_object, start_time, end_time,
                                               duration_sec, row_count, status, message)
        VALUES (@run_id, 'Bronze', @step_name, 'CRM', @target_object, @start_time, @start_time, 0, 0, 'STARTED', 'Step started');

        SET @start_time = GETDATE();
        RAISERROR('[INFO] Truncating [bronze].[crm_sales_details]', 0, 1) WITH NOWAIT;
        TRUNCATE TABLE [bronze].[crm_sales_details];
        RAISERROR('[INFO] Bulk Insert -> [bronze].[crm_sales_details]', 0, 1) WITH NOWAIT;
        BULK INSERT [bronze].[crm_sales_details]
        FROM 'C:\01_Data\02-kaggle-portfolio\35-data-warehouse-SQL\00-datasets\source_crm\sales_details.csv'
        WITH (
            FIRSTROW        = 2,          /* Skip CSV header                */
            FIELDTERMINATOR = ',',        /* Column delimiter               */
            ROWTERMINATOR   = '0x0D0A',   /* CRLF (Windows line ending)     */
            CODEPAGE        = '65001',    /* UTF-8 encoding                 */
            TABLOCK                       /* Optimize bulk load performance */
        )
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
        SET @target_object = 'bronze.erp_cust_az12';
        SET @start_time    = GETDATE();
        INSERT INTO [dbo].[etl_pipeline_audit](run_id, layer_name, step_name, source_system, target_object, start_time, end_time,
                                               duration_sec, row_count, status, message)
        VALUES (@run_id, 'Bronze', @step_name, 'ERP', @target_object, @start_time, @start_time, 0, 0, 'STARTED', 'Step started');

        RAISERROR('[INFO] Truncating [bronze].[erp_cust_az12]', 0, 1) WITH NOWAIT;
        TRUNCATE TABLE [bronze].[erp_cust_az12];
        RAISERROR('[INFO] Bulk Insert -> [bronze].[erp_cust_az12]', 0, 1) WITH NOWAIT;
        BULK INSERT [bronze].[erp_cust_az12]
        FROM 'C:\01_Data\02-kaggle-portfolio\35-data-warehouse-SQL\00-datasets\source_erp\CUST_AZ12.csv'
        WITH (
            FIRSTROW        = 2,          /* Skip CSV header                */
            FIELDTERMINATOR = ',',        /* Column delimiter               */
            ROWTERMINATOR   = '0x0D0A',   /* CRLF (Windows line ending)     */
            CODEPAGE        = '65001',    /* UTF-8 encoding                 */
            TABLOCK                       /* Optimize bulk load performance */
        )
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
        SET @target_object = 'bronze.erp_loc_a101';
        SET @start_time    = GETDATE();
        INSERT INTO [dbo].[etl_pipeline_audit](run_id, layer_name, step_name, source_system, target_object, start_time, end_time,
                                               duration_sec, row_count, status, message)
        VALUES (@run_id, 'Bronze', @step_name, 'ERP', @target_object, @start_time, @start_time, 0, 0, 'STARTED', 'Step started');

        RAISERROR('[INFO] Truncating [bronze].[erp_loc_a101]', 0, 1) WITH NOWAIT;
        TRUNCATE TABLE [bronze].[erp_loc_a101];
        RAISERROR('[INFO] Bulk Insert -> [bronze].[erp_loc_a101]', 0, 1) WITH NOWAIT;
        BULK INSERT [bronze].[erp_loc_a101]
        FROM 'C:\01_Data\02-kaggle-portfolio\35-data-warehouse-SQL\00-datasets\source_erp\LOC_A101.csv'
        WITH (
            FIRSTROW        = 2,          /* Skip CSV header                */
            FIELDTERMINATOR = ',',        /* Column delimiter               */
            ROWTERMINATOR   = '0x0D0A',   /* CRLF (Windows line ending)     */
            CODEPAGE        = '65001',    /* UTF-8 encoding                 */
            TABLOCK                       /* Optimize bulk load performance */
        )
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
        SET @target_object = 'bronze.erp_px_cat_g1v2';
        SET @start_time    = GETDATE();
        INSERT INTO [dbo].[etl_pipeline_audit](run_id, layer_name, step_name, source_system, target_object, start_time, end_time,
                                               duration_sec, row_count, status, message)
        VALUES (@run_id, 'Bronze', @step_name, 'ERP', @target_object, @start_time, @start_time, 0, 0, 'STARTED', 'Step started');

        RAISERROR('[INFO] Truncating [bronze].[erp_px_cat_g1v2]', 0, 1) WITH NOWAIT;
        TRUNCATE TABLE [bronze].[erp_px_cat_g1v2];
        RAISERROR('[INFO] Bulk Insert -> [bronze].[erp_px_cat_g1v2]', 0, 1) WITH NOWAIT;
        BULK INSERT [bronze].[erp_px_cat_g1v2]
        FROM 'C:\01_Data\02-kaggle-portfolio\35-data-warehouse-SQL\00-datasets\source_erp\PX_CAT_G1V2.csv'
        WITH (
            FIRSTROW        = 2,          /* Skip CSV header                */
            FIELDTERMINATOR = ',',        /* Column delimiter               */
            ROWTERMINATOR   = '0x0D0A',   /* CRLF (Windows line ending)     */
            CODEPAGE        = '65001',    /* UTF-8 encoding                 */
            TABLOCK                       /* Optimize bulk load performance */
        )
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

        SET @batch_end_time = GETDATE();
        SET @duration  = DATEDIFF(SECOND, @batch_start_time, @batch_end_time);
        RAISERROR('================================================', 0, 1) WITH NOWAIT;
        RAISERROR('[INFO] Loading Bronze Layer is Completed', 0, 1) WITH NOWAIT;
        RAISERROR('[INFO] Total Load Duration: %d seconds', 0, 1, @duration) WITH NOWAIT;
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
        VALUES (@run_id, 'Bronze', @target_object, @ErrNumber, @ErrSeverity, @ErrState, @ErrLine, @ErrProc, @ErrMsg);

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
        RAISERROR('[ERROR] Bronze Load FAILED', 0, 1) WITH NOWAIT;
        RAISERROR(@ErrMsg, @ErrSeverity, @ErrState);
        RAISERROR('================================================', 0, 1) WITH NOWAIT;
    END CATCH
END;
GO

EXEC [bronze].[usp_load_bronze];
GO
