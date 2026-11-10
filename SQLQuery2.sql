
USE SmartBuildingEnergyDB;
GO

CREATE TABLE dbo.BuildingEnergy_Raw
(
    ingestion_id BIGINT IDENTITY(1,1) PRIMARY KEY,

    report_year NVARCHAR(50),
    property_id NVARCHAR(50),
    property_name NVARCHAR(500),
    primary_property_type NVARCHAR(200),
    year_built NVARCHAR(50),
    energy_star_score NVARCHAR(50),
    site_eui_kbtu_ft NVARCHAR(100),
    site_energy_use_kbtu NVARCHAR(100),
    electricity_use_grid_purchase_1 NVARCHAR(100),
    natural_gas_use_kbtu NVARCHAR(100),
    total_location_based_ghg NVARCHAR(100),
    borough NVARCHAR(100),
    latitude NVARCHAR(100),
    longitude NVARCHAR(100),
    estimated_data_flag NVARCHAR(50),

    ingestion_timestamp DATETIME2 DEFAULT SYSDATETIME()
);
GO

SELECT TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_NAME = 'BuildingEnergy_Raw';
GO



USE SmartBuildingEnergyDB;
GO

EXEC sp_help 'dbo.BuildingEnergy_Raw';
GO



USE SmartBuildingEnergyDB;
GO

SELECT
    COLUMN_NAME,
    DATA_TYPE,
    CHARACTER_MAXIMUM_LENGTH,
    IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dbo'
  AND TABLE_NAME = 'BuildingEnergy_Raw'
ORDER BY ORDINAL_POSITION;
GO


USE SmartBuildingEnergyDB;
GO

SELECT COUNT(*) AS ExistingRecords
FROM dbo.BuildingEnergy_Raw;
GO


select * from dbo.BuildingEnergy_Raw;



USE SmartBuildingEnergyDB;
GO

-- 1. Verify total imported records
SELECT COUNT(*) AS TotalRecords
FROM dbo.BuildingEnergy_Raw;
GO

-- 2. Verify reporting years
SELECT
    report_year,
    COUNT(*) AS TotalRecords
FROM dbo.BuildingEnergy_Raw
GROUP BY report_year
ORDER BY report_year;
GO

-- 3. Verify duplicate building-year groups
SELECT COUNT(*) AS DuplicateGroups
FROM (
    SELECT property_id, report_year
    FROM dbo.BuildingEnergy_Raw
    GROUP BY property_id, report_year
    HAVING COUNT(*) > 1
) AS D;
GO

-- 4. Preview imported records
SELECT TOP 10 *
FROM dbo.BuildingEnergy_Raw
ORDER BY ingestion_id;
GO
