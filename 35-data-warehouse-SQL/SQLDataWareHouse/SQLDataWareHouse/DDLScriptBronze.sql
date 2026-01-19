/*
===============================================================================
DDL Script: Create Bronze Tables
===============================================================================
Script Purpose:
    This script creates raw data tables in the 'bronze' schema.
    If the tables already exist, they will be dropped and recreated.

    The Bronze layer stores data exactly as received from source systems
    (CRM and ERP) without applying any transformations, constraints,
    or business rules.

    These tables are designed for data ingestion, traceability,
    and debugging purposes only.
    
Execution Notes:
    - This script is intended for development and test environments.
    - All existing data in the Bronze tables will be permanently deleted.
    - No primary keys, foreign keys, or constraints are enforced by design.

Source Systems:
    - CRM
    - ERP

Target Schema:
    - bronze
===============================================================================
*/

USE [DataWarehouseForSales];
GO

IF OBJECT_ID('bronze.crm_cust_info', 'U') IS NOT NULL
    DROP TABLE bronze.crm_cust_info;
GO

CREATE TABLE bronze.crm_cust_info(
    cst_id              INT                 NULL,
    cst_key             NVARCHAR(50)        NULL,
    cst_firstname       NVARCHAR(50)        NULL,
    cst_lastname        NVARCHAR(50)        NULL,
    cst_marital_status  NVARCHAR(50)        NULL,
    cst_gndr            NVARCHAR(50)        NULL,
    cst_create_date     DATE                NULL
);
GO

IF OBJECT_ID('bronze.crm_prd_info', 'U') IS NOT NULL
    DROP TABLE bronze.crm_prd_info;
GO

CREATE TABLE bronze.crm_prd_info(
    prd_id              INT                 NULL,
    prd_key             NVARCHAR(100)       NULL,
    prd_nm              NVARCHAR(100)       NULL,
    prd_cost            INT                 NULL,
    prd_line            NVARCHAR(10)        NULL,
    prd_start_dt        DATE                NULL,
    prd_end_dt          DATE                NULL
);
GO

IF OBJECT_ID('bronze.crm_sales_details', 'U') IS NOT NULL
    DROP TABLE bronze.crm_sales_details;
GO

CREATE TABLE bronze.crm_sales_details(
    sls_ord_num         NVARCHAR(50)        NULL,
    sls_prd_key         NVARCHAR(50)        NULL,
    sls_cust_id         INT                 NULL,
    sls_order_dt        INT                 NULL,
    sls_ship_dt         INT                 NULL,
    sls_due_dt          INT                 NULL,
    sls_sales           INT                 NULL,
    sls_quantity        INT                 NULL,
    sls_price           INT                 NULL
);
GO

IF OBJECT_ID('bronze.erp_cust_az12', 'U') IS NOT NULL
    DROP TABLE bronze.erp_cust_az12;
GO

CREATE TABLE bronze.erp_cust_az12(
    cid                 NVARCHAR(50)        NULL,
    bdate               DATE                NULL,
    gen                 NVARCHAR(50)        NULL
);
GO

IF OBJECT_ID('bronze.erp_loc_a101', 'U') IS NOT NULL
    DROP TABLE bronze.erp_loc_a101;
GO

CREATE TABLE bronze.erp_loc_a101(
    cid                 NVARCHAR(50)        NULL,
    cntry               NVARCHAR(50)        NULL
);
GO

IF OBJECT_ID('bronze.erp_px_cat_g1v2', 'U') IS NOT NULL
    DROP TABLE bronze.erp_px_cat_g1v2;
GO

CREATE TABLE bronze.erp_px_cat_g1v2(
    id                  NVARCHAR(50)        NULL,
    cat                 NVARCHAR(50)        NULL,
    subcat              NVARCHAR(50)        NULL,
    maintenance         NVARCHAR(50)        NULL
);
GO

IF OBJECT_ID('dbo.etl_pipeline_audit', 'U') IS NOT NULL
    DROP TABLE dbo.etl_pipeline_audit;
GO

CREATE TABLE dbo.etl_pipeline_audit (
    audit_id            INT                 IDENTITY NOT NULL,
    run_id              UNIQUEIDENTIFIER    NOT NULL,
    layer_name          NVARCHAR(20)        NOT NULL,   -- Bronze / Silver / Gold
    step_name           NVARCHAR(100)       NOT NULL,  -- table / transform name
    source_system       NVARCHAR(50)        NOT NULL,
    target_object       NVARCHAR(100)       NOT NULL,
    start_time          DATETIME            NOT NULL,
    end_time            DATETIME            NOT NULL,
    duration_sec        INT                 NOT NULL,
    row_count           INT                 NOT NULL,
    status              NVARCHAR(20)        NOT NULL,   -- STARTED / SUCCESS / WARN / FAILED
    message             NVARCHAR(1000)      NOT NULL,
    created_at          DATETIME            CONSTRAINT DF_EtlPipelineAudit_CreatedAt DEFAULT GETDATE(),
    CONSTRAINT PK_EtlPipelineAudit_AuditId  PRIMARY KEY(audit_id),
    CONSTRAINT CK_EtlPipelineAudit_LayerName CHECK(layer_name IN ('Bronze', 'Silver', 'Gold')),
    CONSTRAINT CK_EtlPipelineAudit_SourceSystem CHECK(source_system IN ('ERP', 'CRM')),
    CONSTRAINT CK_EtlPipelineAudit_Status CHECK(status IN ('STARTED', 'SUCCESS', 'WARN', 'FAILED')),
    CONSTRAINT CK_EtlPipelineAudit_DurationSec CHECK(duration_sec >= 0),
    CONSTRAINT CK_EtlPipelineAudit_RowCount CHECK(row_count >= 0)
);
GO

IF OBJECT_ID('dbo.etl_error_log', 'U') IS NOT NULL
    DROP TABLE dbo.etl_error_log;
GO

CREATE TABLE dbo.etl_error_log (
    error_id            INT                 IDENTITY(1,1) NOT NULL,
    run_id              UNIQUEIDENTIFIER    NOT NULL,
    layer_name          NVARCHAR(20)        NOT NULL,   -- Bronze / Silver / Gold
    table_name          NVARCHAR(100)       NOT NULL,
    error_number        INT                 NOT NULL,
    error_severity      INT                 NOT NULL,
    error_state         INT                 NOT NULL,
    error_line          INT                 NOT NULL,
    error_procedure     NVARCHAR(200)       NOT NULL,
    error_message       NVARCHAR(4000)      NOT NULL,
    created_at          DATETIME            CONSTRAINT DF_EtlErrorLog_CreatedAt DEFAULT GETDATE(),
    CONSTRAINT PK_EtlErrorLog_ErrorId  PRIMARY KEY(error_id),
    CONSTRAINT CK_EtlErrorLog_LayerName CHECK(layer_name IN ('Bronze', 'Silver', 'Gold')),
);
GO
