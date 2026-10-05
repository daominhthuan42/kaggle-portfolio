/*
=============================================================
Create or Recreate Retail Analytics Database
=============================================================
Script Purpose:
    This script creates a new database named '01_RetailAnalytics'
    with dedicated data and log files after checking whether the
    database already exists.

    If the database does not exist, it is created with the specified
    data file and transaction log file configuration.

    If the database already exists, it is set to SINGLE_USER mode,
    all active connections are rolled back, and the database is
    dropped to allow a clean recreation.

WARNING:
    Running this script will drop the entire '01_RetailAnalytics'
    database if it already exists.

    All data, tables, views, stored procedures, and other database
    objects will be permanently deleted.

    Proceed with caution and ensure you have proper backups before
    running this script.
*/

USE master;
GO

IF EXISTS (SELECT 1 FROM sys.databases WHERE name ='01_RetailAnalytics')
BEGIN	
    PRINT 'Database [01_RetailAnalytics] already exists.';
	ALTER DATABASE [01_RetailAnalytics] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
	DROP DATABASE [01_RetailAnalytics];
END

CREATE DATABASE [01_RetailAnalytics]
ON
(
	NAME = 'RetailAnalytics_data',
	FILENAME = 'D:\02_DATA\00_kaggle-portfolio\48-retail-analytics\datasets\RetailAnalytics.mdf',
	SIZE = 10MB,
	MAXSIZE = 100MB,
	FILEGROWTH = 5MB)
LOG ON
(
	NAME = 'RetailAnalytics_log',
	FILENAME = 'D:\02_DATA\00_kaggle-portfolio\48-retail-analytics\datasets\RetailAnalytics.ldf',
	SIZE = 512MB,
	MAXSIZE = 5GB,
	FILEGROWTH = 256MB
)
PRINT 'Database [01_RetailAnalytics] created successfully.';
GO
