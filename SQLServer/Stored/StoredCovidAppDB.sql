USE CovidAppDB;

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
