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
