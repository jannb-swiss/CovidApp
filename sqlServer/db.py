import pyodbc

from models.case import Case
from models.test import Test
from models.vaccination import Vaccination


class DatabaseConnection:
    conn = None
    cursor = None

    def __init__(self, server: str, db: str, user: str, password: str):
        connection_string: str = 'DRIVER={{SQL Server}};SERVER={0};DATABASE={1};UID={2};PWD={3};Trusted_Connection=yes;'
        self.conn = pyodbc.connect(connection_string.format(server, db, user, password))
        self.cursor = self.conn.cursor()

    # def __init__(self, driver: str, server: str, db: str, user: str, password: str):
    #     connection_string: str = 'DRIVER={0};SERVER={1};DATABASE={2};UID={3};PWD={4};'
    #     self.conn = pyodbc.connect(connection_string.format(driver, server, db, user, password))
    #     self.cursor = self.conn.cursor()

    def truncate_countries(self):
        self.cursor.execute("truncate table Country")
        self.cursor.commit()

    def truncate_continents(self):
        self.cursor.execute("truncate table Continent")
        self.cursor.commit()

    def truncate_cases(self):
        self.cursor.execute("truncate table Cases")
        self.cursor.commit()

    def truncate_tests(self):
        self.cursor.execute("truncate table Tests")
        self.cursor.commit()

    def truncate_vaccinations(self):
        self.cursor.execute("truncate table Vaccinations")
        self.cursor.commit()

    def get_continents(self):
        self.cursor.execute("select * from Continent order by ContinentID")
        return self.cursor.fetchall()

    def get_countries(self):
        self.cursor.execute("select * from Country")
        return self.cursor.fetchall()

    def insertContent(self, name: str) -> int:
        sql = """
        declare @out int;
        exec createContinent @name = ?, @new_identity = @out output;
        select @out AS the_output;
        """
        self.cursor.execute(sql, name)
        inserted_id: int = self.cursor.fetchall()
        self.commit()
        return inserted_id[0][0]

    def insertCountry(self, con_id: int, iso: str, name: str, population: int) -> int:
        sql = """
        declare @out int;
        exec createCountry @continent = ?, @iso_code = ?, @name = ?, @population = ?, @new_identity = @out output;
        select @out as the_output;
        """
        self.cursor.execute(sql, (con_id, iso, name, population))
        inserted_id: int = self.cursor.fetchall()
        self.commit()
        return inserted_id[0][0]

    def insertCase(self, case: Case):
        sql = "exec createCases @country = ?, @date = ?, @total_cases = ?, @new_cases = ?, @total_deaths = ?, @new_deaths = ?, @reproduction_rate = ?;"
        self.cursor.execute(sql, case.to_tuple())
        self.commit()

    def insertVaccinations(self, vaccination: Vaccination):
        sql = "exec createVaccinations @country = ?, @date = ?, @total_vaccinations = ?, @people_vaccinated = ?, @people_fully_vaccinated = ?, @new_vaccinations = ?;"
        self.cursor.execute(sql, vaccination.to_tuple())
        self.commit()

    def insertTests(self, test: Test):
        sql = "exec createTests @country = ?, @date = ?, @new_tests = ?, @total_tests = ?, @positive_rate = ?;"
        self.cursor.execute(sql, test.to_tuple())
        self.commit()

    def get_continent_cases(self, date: str):
        sql = """
        select con.ContinentID, sum(TotalCases) as totalCases from Cases cas
        join Country cou on cas.CountryID = cou.CountryID
        join Continent con on con.ContinentID = cou.ContinentID
        where CasesDate = ?
        group by con.ContinentID, CasesDate
        order by con.ContinentID
        """
        self.cursor.execute(sql, date)
        return self.cursor.fetchall()

    def getTotalCases(self):
        sql = "select CasesDate, sum(TotalCases), sum(TotalDeaths) from Cases group by CasesDate order by CasesDate"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def getTotalVaccinations(self):
        sql = "select VaccinationsDate, sum(cast(TotalVaccinations as bigint)) from Vaccinations group by VaccinationsDate order by VaccinationsDate"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def commit(self):
        self.cursor.commit()
