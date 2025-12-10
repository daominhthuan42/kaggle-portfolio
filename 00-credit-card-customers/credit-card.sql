DROP DATABASE IF EXISTS [03_Credit_Score_DB]
CREATE DATABASE [03_Credit_Score_DB]
ON
(
	NAME = 'Credit_Score_DB',
	FILENAME = 'C:\01_Data\02-kaggle-portfolio\00-credit-card-customers\Credit_Score_DB.mdf',
	SIZE = 10MB,
	MAXSIZE = 100MB,
	FILEGROWTH = 5MB)
LOG ON
(
	NAME = 'Credit_Score_DB_LOG',
	FILENAME = 'C:\01_Data\02-kaggle-portfolio\00-credit-card-customers\Credit_Score_DB_LOG.ldf',
	SIZE = 5MB,
	MAXSIZE = 50MB,
	FILEGROWTH = 5MB
)

USE [03_Credit_Score_DB]
GO

DROP TABLE IF EXISTS BankChurners
CREATE TABLE BankChurners (
    CLIENTNUM BIGINT NOT NULL,
    Attrition_Flag VARCHAR(30),
    Customer_Age INT,
    Gender VARCHAR(10),
    Dependent_count INT,
    Education_Level VARCHAR(50),
    Marital_Status VARCHAR(50),
    Income_Category VARCHAR(50),
    Card_Category VARCHAR(20),
    Months_on_book INT,
    Total_Relationship_Count INT,
    Months_Inactive_12_mon INT,
    Contacts_Count_12_mon INT,
    Credit_Limit FLOAT,
    Total_Revolving_Bal FLOAT,
    Avg_Open_To_Buy FLOAT,
    Total_Trans_Amt FLOAT,
    Total_Trans_Ct FLOAT,
    Total_Ct_Chng_Q4_Q1 FLOAT,
    Total_Amt_Chng_Q4_Q1 FLOAT,
    Avg_Utilization_Ratio FLOAT,
	CONSTRAINT CK_BankChurners_Gender CHECK(Gender IN ('M', 'F'))
);

ALTER TABLE dbo.BankChurners
ADD CONSTRAINT UQ_Clientnum UNIQUE (CLIENTNUM);

TRUNCATE TABLE dbo.BankChurners;
