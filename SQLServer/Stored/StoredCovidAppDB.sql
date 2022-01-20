use CovidAppDB;

if(OBJECT_ID(N'createContinent') IS NOT NULL)
    begin
        drop procedure createContinent;
    end
go

create procedure createContinent
    @name varchar(50),
    @new_identity int = null output
as begin
    set nocount on;
    insert into Continent (ContinentName) values (@name);
    set @new_identity = SCOPE_IDENTITY();
end
go

if(OBJECT_ID(N'createCountry') IS NOT NULL)
    begin
        drop procedure createCountry;
    end
go

create procedure createCountry
    @continent int,
    @iso_code varchar(20),
    @name varchar(50),
    @population int,
    @new_identity int = null output
as begin
    set nocount on;
    insert into Country (CountryID, IsoCode, Location, Population) values (@continent, @iso_code, @name, @population);
    set @new_identity = SCOPE_IDENTITY();
end
go

if(OBJECT_ID(N'createCases') IS NOT NULL)
    begin
        drop procedure createCases;
    end
go

create procedure createCases
    @country int,
    @date date,
    @total_cases int,
    @new_cases int,
    @total_deaths int,
    @new_deaths int,
    @reproduction_rate float
as begin
    set nocount on;
    insert into Cases (
        CountryID,
        CasesDate,
        TotalCases,
        NewCases,
        TotalDeaths,
		NewDeaths,
        ReproductionRate
    ) values (
         @country,
         @date,
         @total_cases,
         @new_cases,
         @total_deaths,
         @new_deaths,
         @reproduction_rate
     );
end
go

if(OBJECT_ID(N'createTests') IS NOT NULL)
    begin
        drop procedure createTests;
    end
go

create procedure createTests
    @country int,
    @date date,
    @new_tests int,
    @total_tests int,
    @positive_rate int
as begin
    set nocount on;
    insert into Tests (
        CountryID,
        TestsDate,
        NewTests,
        TotalTests,
        PositiveRate
    ) values (
         @country,
         @date,
         @new_tests,
         @total_tests,
         @positive_rate
     );
end
go

if(OBJECT_ID(N'createVaccinations') IS NOT NULL)
    begin
        drop procedure createVaccinations;
    end
go

create procedure createVaccinations
    @country int,
    @date date,
    @total_vaccinations int,
    @people_vaccinated int,
    @people_fully_vaccinated int,
    @new_vaccinations int
as begin
    set nocount on;
    insert into Vaccinations (
        CountryID,
        VaccinationsDate,
        TotalVaccinations,
        PeopleVaccinated,
        PeopleFullyVaccinated,
        NewVaccinations
    ) values (
         @country,
         @date,
         @total_vaccinations,
         @people_vaccinated,
         @people_fully_vaccinated,
         @new_vaccinations
     );
end
go