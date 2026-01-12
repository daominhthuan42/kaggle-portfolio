/*
Create Database and Schemas
====================================================================

Script Purpose:

    This script creates a new database named 'DataWarehouse' after checking if it already exists.
    If the database exists, it is dropped and recreated. Additionally, the script sets up three schemas
    within the database: 'bronze', 'silver', and 'gold'.

WARNING:

    Running this script will drop the entire 'DataWarehouseForSales' database if it exists.
    All data in the database will be permanently deleted. Proceed with caution
    and ensure you have proper backups before running this script.
*/

USE master;
GO

IF EXISTS (SELECT 1 FROM sys.databases WHERE name = 'DataWarehouseForSales')
BEGIN
	ALTER DATABASE [DataWarehouseForSales] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
	DROP DATABASE [DataWarehouseForSales];
END;
GO

/* Create Database "DataWarehouse" */
CREATE DATABASE [DataWarehouseForSales]
GO

USE [DataWarehouseForSales];
GO

-- CREATE SCHEMAS
CREATE SCHEMA bronze;
GO

CREATE SCHEMA silver;
GO

CREATE SCHEMA gold;
GO
