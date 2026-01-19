/*
===============================================================================
DDL Script: Create Silver Tables
===============================================================================
Script Purpose:
    This script creates cleansed and conformed data tables in the 'silver' schema.
    If the tables already exist, they will be dropped and recreated.

    The Silver layer stores data that has been:
        - Cleaned (trimmed, standardized, normalized)
        - Deduplicated (latest records per business key)
        - Conformed across source systems (CRM and ERP)

    These tables represent the "current state" of entities and are designed
    to be reliable inputs for analytical, reporting, and downstream processing
    in the Gold layer.

Execution Notes:
    - This script is intended for development and test environments.
    - All existing data in the Silver tables will be permanently deleted.
    - No primary keys or foreign keys are enforced at this layer.
    - Audit columns (dwh_create_date) are used to track load time into DWH.

Source Systems:
    - CRM
    - ERP

Target Schema:
    - silver
===============================================================================
*/

USE [DataWarehouseForSales];
GO

IF OBJECT_ID('silver.crm_cust_info', 'U') IS NOT NULL
    DROP TABLE silver.crm_cust_info;
GO

CREATE TABLE silver.crm_cust_info(
    cst_id              INT                 NULL,
    cst_key             NVARCHAR(50)        NULL,
    cst_firstname       NVARCHAR(50)        NULL,
    cst_lastname        NVARCHAR(50)        NULL,
    cst_marital_status  NVARCHAR(50)        NULL,
    cst_gndr            NVARCHAR(50)        NULL,
    cst_create_date     DATE                NULL,
    dwh_create_date     DATE                CONSTRAINT DF_CRMCustInfo_DWHCreateDate DEFAULT GETDATE()
);
GO

IF OBJECT_ID('silver.crm_prd_info', 'U') IS NOT NULL
    DROP TABLE silver.crm_prd_info;
GO

CREATE TABLE silver.crm_prd_info(
    prd_id              INT                 NULL,
    prd_cat_id          NVARCHAR(100)       NULL,
    prd_key             NVARCHAR(100)       NULL,
    prd_nm              NVARCHAR(100)       NULL,
    prd_cost            INT                 NULL,
    prd_line            NVARCHAR(50)        NULL,
    prd_start_dt        DATE                NULL,
    prd_end_dt          DATE                NULL,
    dwh_create_date     DATE                CONSTRAINT DF_CRMPrdInfo_DWHCreateDate DEFAULT GETDATE()
);
GO

IF OBJECT_ID('silver.crm_sales_details', 'U') IS NOT NULL
    DROP TABLE silver.crm_sales_details;
GO

CREATE TABLE silver.crm_sales_details(
    sls_ord_num         NVARCHAR(50)        NULL,
    sls_prd_key         NVARCHAR(50)        NULL,
    sls_cust_id         INT                 NULL,
    sls_order_dt        DATE                NULL,
    sls_ship_dt         DATE                NULL,
    sls_due_dt          DATE                NULL,
    sls_sales           INT                 NULL,
    sls_quantity        INT                 NULL,
    sls_price           INT                 NULL,
    dwh_create_date     DATE                CONSTRAINT DF_CRMSalesDetails_DWHCreateDate DEFAULT GETDATE()
);
GO

IF OBJECT_ID('silver.erp_cust_az12', 'U') IS NOT NULL
    DROP TABLE silver.erp_cust_az12;
GO

CREATE TABLE silver.erp_cust_az12(
    cid                 NVARCHAR(50)        NULL,
    bdate               DATE                NULL,
    gen                 NVARCHAR(50)        NULL,
    dwh_create_date     DATE                CONSTRAINT DF_ERPCustAZ12_DWHCreateDate DEFAULT GETDATE()
);
GO

IF OBJECT_ID('silver.erp_loc_a101', 'U') IS NOT NULL
    DROP TABLE silver.erp_loc_a101;
GO

CREATE TABLE silver.erp_loc_a101(
    cid                 NVARCHAR(50)        NULL,
    cntry               NVARCHAR(50)        NULL,
    dwh_create_date     DATE                CONSTRAINT DF_ERPLocA101_DWHCreateDate DEFAULT GETDATE()
);
GO

IF OBJECT_ID('silver.erp_px_cat_g1v2', 'U') IS NOT NULL
    DROP TABLE silver.erp_px_cat_g1v2;
GO

CREATE TABLE silver.erp_px_cat_g1v2(
    id                  NVARCHAR(50)        NULL,
    cat                 NVARCHAR(50)        NULL,
    subcat              NVARCHAR(50)        NULL,
    maintenance         NVARCHAR(50)        NULL,
    dwh_create_date     DATE                CONSTRAINT DF_ERPPxCatG1V2_DWHCreateDate DEFAULT GETDATE()
);
GO
