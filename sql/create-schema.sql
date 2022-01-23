USE master
GO

IF NOT EXISTS(
        SELECT name
        FROM sys.databases
        WHERE name = N'CovidAppDB'
    )
CREATE DATABASE [CovidAppDB]
GO

USE CovidAppDB;
GO

DROP TABLE IF EXISTS[dbo].[Vaccinations]
DROP TABLE IF EXISTS[dbo].[Tests]
DROP TABLE IF EXISTS[dbo].[Cases]
DROP TABLE IF EXISTS[dbo].[Country]
DROP TABLE IF EXISTS[dbo].[Continent]
GO

CREATE TABLE dbo.Continent
(
    ContinentID   INT PRIMARY KEY IDENTITY (1,1) NOT NULL,
    ContinentName VARCHAR(100)                   NOT NULL UNIQUE,
)

CREATE TABLE dbo.Country
(
    CountryID   INT PRIMARY KEY IDENTITY (1,1) NOT NULL,
    ContinentID INT                            NOT NULL,
    IsoCode     VARCHAR(10)                    NOT NULL UNIQUE,
    Location    VARCHAR(50)                    NOT NULL,
    Population  INT                            NOT NULL,
    CONSTRAINT FK_Country_Continent FOREIGN KEY (ContinentID) REFERENCES Continent (ContinentID)
)

CREATE TABLE dbo.Cases
(
    CasesID          INT PRIMARY KEY IDENTITY (1,1) NOT NULL,
    CasesDate        DATE                           NOT NULL,
    TotalCases       INT                            NOT NULL,
    NewCases         INT                            NOT NULL,
    TotalDeaths      INT                            NOT NULL,
    NewDeaths        INT                            NOT NULL,
    ReproductionRate FLOAT                          NOT NULL,
    CountryID        INT                            NOT NULL,
    CONSTRAINT FK_Cases_Country FOREIGN KEY (CountryID) REFERENCES Country (CountryID),
)

CREATE TABLE dbo.Tests
(
    TestsID      INT PRIMARY KEY IDENTITY (1,1) NOT NULL,
    TestsDate    DATE                           NOT NULL,
    NewTests     INT                            NOT NULL,
    TotalTests   INT                            NOT NULL,
    PositiveRate FLOAT                          NOT NULL,
    CountryID    INT                            NOT NULL,
    CONSTRAINT FK_Tests_Country FOREIGN KEY (CountryID) REFERENCES Country (CountryID)
)

CREATE TABLE dbo.Vaccinations
(
    VaccinationsID        INT PRIMARY KEY IDENTITY (1,1) NOT NULL,
    VaccinationsDate      DATE                           NOT NULL,
    TotalVaccinations     BIGINT,
    PeopleVaccinated      BIGINT,
    PeopleFullyVaccinated BIGINT,
    NewVaccinations       BIGINT,
    CountryID             INT                            NOT NULL,
    CONSTRAINT FK_Vaccinations_Country FOREIGN KEY (CountryID) REFERENCES Country (CountryID),
);
GO

IF EXISTS(
        SELECT *
        FROM INFORMATION_SCHEMA.ROUTINES
        WHERE SPECIFIC_SCHEMA = N'dbo'
          AND SPECIFIC_NAME = N'createContinent'
          AND ROUTINE_TYPE = N'PROCEDURE'
    )
    DROP PROCEDURE dbo.createContinent
GO
CREATE PROCEDURE dbo.createContinent @name varchar(50),
                                     @new_identity int = null output
AS
BEGIN
    SET NOCOUNT ON;
    INSERT INTO Continent (ContinentName) VALUES (@name);
    SET @new_identity = SCOPE_IDENTITY();
END
GO

IF EXISTS(
        SELECT *
        FROM INFORMATION_SCHEMA.ROUTINES
        WHERE SPECIFIC_SCHEMA = N'dbo'
          AND SPECIFIC_NAME = N'createCountry'
          AND ROUTINE_TYPE = N'PROCEDURE'
    )
    DROP PROCEDURE dbo.createCountry
GO
CREATE PROCEDURE dbo.createCountry @continent INT,
                                   @iso_code VARCHAR(20),
                                   @name VARCHAR(50),
                                   @population INT,
                                   @new_identity INT = NULL OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    INSERT INTO Country (ContinentID, IsoCode, Location, Population) VALUES (@continent, @iso_code, @name, @population);
    SET @new_identity = SCOPE_IDENTITY();
END
GO

IF EXISTS(
        SELECT *
        FROM INFORMATION_SCHEMA.ROUTINES
        WHERE SPECIFIC_SCHEMA = N'dbo'
          AND SPECIFIC_NAME = N'createCases'
          AND ROUTINE_TYPE = N'PROCEDURE'
    )
    DROP PROCEDURE dbo.createCases
GO
CREATE PROCEDURE dbo.createCases @country INT,
                                 @date DATE,
                                 @total_cases INT,
                                 @new_cases INT,
                                 @total_deaths INT,
                                 @new_deaths INT,
                                 @reproduction_rate FLOAT
AS
BEGIN
    SET NOCOUNT ON;
    INSERT INTO Cases (CountryID,
                       CasesDate,
                       TotalCases,
                       NewCases,
                       TotalDeaths,
                       NewDeaths,
                       ReproductionRate)
    VALUES (@country,
            @date,
            @total_cases,
            @new_cases,
            @total_deaths,
            @new_deaths,
            @reproduction_rate);
END
GO

IF EXISTS(
        SELECT *
        FROM INFORMATION_SCHEMA.ROUTINES
        WHERE SPECIFIC_SCHEMA = N'dbo'
          AND SPECIFIC_NAME = N'createTests'
          AND ROUTINE_TYPE = N'PROCEDURE'
    )
    DROP PROCEDURE dbo.createTests
GO
CREATE PROCEDURE dbo.createTests @country INT,
                                 @date DATE,
                                 @new_tests INT,
                                 @total_tests INT,
                                 @positive_rate INT
AS
BEGIN
    SET NOCOUNT ON;
    INSERT INTO Tests (CountryID,
                       TestsDate,
                       NewTests,
                       TotalTests,
                       PositiveRate)
    VALUES (@country,
            @date,
            @new_tests,
            @total_tests,
            @positive_rate);
END
GO

IF EXISTS(
        SELECT *
        FROM INFORMATION_SCHEMA.ROUTINES
        WHERE SPECIFIC_SCHEMA = N'dbo'
          AND SPECIFIC_NAME = N'createVaccinations'
          AND ROUTINE_TYPE = N'PROCEDURE'
    )
    DROP PROCEDURE dbo.createVaccinations
GO
CREATE PROCEDURE dbo.createVaccinations @country int,
                                        @date date,
                                        @total_vaccinations int,
                                        @people_vaccinated int,
                                        @people_fully_vaccinated int,
                                        @new_vaccinations int
AS
BEGIN
    SET NOCOUNT ON;
    INSERT INTO Vaccinations (CountryID,
                              VaccinationsDate,
                              TotalVaccinations,
                              PeopleVaccinated,
                              PeopleFullyVaccinated,
                              NewVaccinations)
    VALUES (@country,
            @date,
            @total_vaccinations,
            @people_vaccinated,
            @people_fully_vaccinated,
            @new_vaccinations);
END
GO

CREATE OR ALTER VIEW V_ContinentCases
AS
SELECT CasesDate, continent.ContinentID, sum(TotalCases) as totalCases
FROM Cases cases
         JOIN Country country ON cases.CountryID = country.CountryID
         JOIN Continent continent ON continent.ContinentID = country.ContinentID
GROUP BY continent.ContinentID, CasesDate
GO

CREATE OR ALTER VIEW V_ContinentVaccinations
AS
SELECT VaccinationsDate, continent.ContinentID, sum(TotalVaccinations) as TotalVaccinations
FROM Vaccinations vaccinations
         JOIN Country country ON vaccinations.CountryID = country.CountryID
         JOIN Continent continent ON continent.ContinentID = country.ContinentID
GROUP BY continent.ContinentID, VaccinationsDate
GO