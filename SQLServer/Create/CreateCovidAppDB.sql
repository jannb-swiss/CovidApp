use master;
go


if(DB_ID(N'CovidAppDB') IS NOT NULL)
    begin
        alter database CovidAppDB set offline with rollback immediate
        drop database CovidAppDB;
    end
go

create database CovidAppDB;
go

use CovidAppDB;
go

if(OBJECT_ID(N'Continent') IS NOT NULL)
    begin
        drop table Continent;
    end
go

create table Continent (
   ContinentID		int	primary key	identity(1,1)	not null,
   ContinentName	varchar(100)	not null,
   constraint U_name unique(ContinentName)
)

if(OBJECT_ID(N'Country') IS NOT NULL)
    begin
        drop table Country;
    end
go

create table Country
(
    CountryID			int primary key identity(1,1)	not null,
    ContinentID			int				not null,
    IsoCode	            varchar(10)		not null,
    Location	        varchar(50)		not null,
    Population          int             not null,
    constraint FK_Country_Continent foreign key (ContinentID) references Continent(ContinentID),
    constraint U_iso_code unique (IsoCode)
)

if(OBJECT_ID(N'Cases') IS NOT NULL)
    begin
        drop table Cases;
    end
go

create table Cases
(
    CasesID					int primary key identity(1,1)	not null,
    CasesDate				date	not null,
    TotalCases			    int		not null,
    NewCases			    int		not null,
    TotalDeaths		        int		not null,
	NewDeaths		        int		not null,
    ReproductionRate	float	not null,
    CountryID				int		not null,
    constraint FK_Cases_Country foreign  key (CountryID) references Country(CountryID),
)

if(OBJECT_ID(N'Tests') IS NOT NULL)
    begin
        drop table Tests;
    end
go

create table Tests
(
    TestsID				int	primary key	identity(1,1)	not null,
    TestsDate			date	not null,
    NewTests		    int		not null,
    TotalTests		    int		not null,
    PositiveRate	    float	not null,
    CountryID			int		not null,
    constraint FK_Tests_Country foreign key (CountryID) references Country(CountryID)
)

if(OBJECT_ID(N'Vaccinations') IS NOT NULL)
    begin
        drop table Vaccinations;
    end
go

create table Vaccinations
(
    VaccinationsID						int primary key	identity(1,1)	not null,
    VaccinationsDate					date	not null,
    TotalVaccinations					bigint,
    PeopleVaccinated					bigint,
    PeopleFullyVaccinated				bigint,
    NewVaccinations					    bigint,
    CountryID							int		not null,
    constraint FK_Vaccinations_Country foreign key (CountryID) references Country(CountryID),
);