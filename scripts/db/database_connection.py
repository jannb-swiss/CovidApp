import pyodbc

from models.case import Case
from models.test import Test
from models.vaccination import Vaccination


class DatabaseConnection:
    """
    Database connection object to manage the access and the queries.
    """

    conn = None
    cursor = None

    def __init__(self, driver: str, server: str, db: str, user: str, password: str):
        if driver == '{SQL Server}':
            connection_string: str = 'DRIVER={0};SERVER={1};DATABASE={2};UID={3};PWD={4};Trusted_Connection=yes;'
        else:
            connection_string: str = 'DRIVER={0};SERVER={1};DATABASE={2};UID={3};PWD={4};'
        self.conn = pyodbc.connect(connection_string.format(driver, server, db, user, password))
        self.cursor = self.conn.cursor()

    def delete_countries(self):
        """
        Deletes all data records from the Table Country.
        """
        self.cursor.execute("DELETE FROM Country")
        self.cursor.commit()

    def delete_continents(self):
        """
        Deletes all data records from the Table Continent.
        """
        self.cursor.execute("DELETE FROM Continent")
        self.cursor.commit()

    def delete_cases(self):
        """
        Deletes all data records from the Table Cases.
        """
        self.cursor.execute("DELETE FROM Cases")
        self.cursor.commit()

    def delete_tests(self):
        """
        Deletes all data records from the Table Tests.
        """
        self.cursor.execute("DELETE FROM Tests")
        self.cursor.commit()

    def delete_vaccinations(self):
        """
        Deletes all data records from the Table Vaccinations.
        """
        self.cursor.execute("DELETE FROM Vaccinations")
        self.cursor.commit()

    def get_continents(self):
        """
        Loads all continents ordered by ContinentID.
        """
        self.cursor.execute("SELECT * FROM Continent ORDER BY ContinentID")
        return self.cursor.fetchall()

    def get_continent_by_name(self, name: str):
        """
        Load continent by name.

        Parameters:
        name -- the name of the continent (e.g. Europe)
        """
        self.cursor.execute("SELECT * FROM Continent WHERE ContinentName = ?", name)
        return self.cursor.fetchone()

    def get_country_by_iso_code(self, iso_code: str):
        """
        Load one specific country by iso code.

        Parameters:
        iso_code -- the iso code of the country (e.g. ARG)
        """
        self.cursor.execute("SELECT * FROM Country WHERE IsoCode = ?", iso_code)
        return self.cursor.fetchone()

    def insert_continent(self, name: str) -> int:
        """
        Creates a new continent record with the previous created procedure.

        Parameters:
        name -- the name of the continent (e.g. Europe)
        """
        sql = """
        declare @out int;
        exec createContinent @name = ?, @new_identity = @out output;
        select @out AS the_output;
        """
        self.cursor.execute(sql, name)
        inserted_id: int = self.cursor.fetchall()
        self.cursor.commit()
        return inserted_id[0][0]

    def insert_country(self, continent_id: int, iso_code: str, name: str, population: int) -> int:
        """
        Creates a new country record with the previous created procedure.

        Parameters:
        continent_id -- the id of the continent (e.g. 15)
        iso_code     -- the iso code of the country (e.g. ARG)
        name         -- the name of the country (e.g. Argentina)
        population   -- the population of the country (20000)
        """
        sql = """
        declare @out int;
        exec createCountry @continent = ?, @iso_code = ?, @name = ?, @population = ?, @new_identity = @out output;
        select @out as the_output;
        """
        self.cursor.execute(sql, (continent_id, iso_code, name, population))
        inserted_id: int = self.cursor.fetchall()
        self.cursor.commit()
        return inserted_id[0][0]

    def insert_cases(self, case: Case):
        """
        Creates a new cases record with the previous created procedure.

        Parameters:
        case -- case object with all the necessary information
        """
        sql = "exec createCases @country = ?, @date = ?, @total_cases = ?, @new_cases = ?, @total_deaths = ?, @new_deaths = ?, @reproduction_rate = ?;"
        self.cursor.execute(sql, case.to_tuple())
        self.cursor.commit()

    def insert_vaccinations(self, vaccination: Vaccination):
        """
        Creates a new vaccinations record with the previous created procedure.

        Parameters:
        vaccination -- vaccination object with all the necessary information
        """
        sql = "exec createVaccinations @country = ?, @date = ?, @total_vaccinations = ?, @people_vaccinated = ?, @people_fully_vaccinated = ?, @new_vaccinations = ?;"
        self.cursor.execute(sql, vaccination.to_tuple())
        self.cursor.commit()

    def insert_tests(self, test: Test):
        """
        Creates a new test record with the previous created procedure.

        Parameters:
        test -- test object with all the necessary information
        """
        sql = "exec createTests @country = ?, @date = ?, @new_tests = ?, @total_tests = ?, @positive_rate = ?;"
        self.cursor.execute(sql, test.to_tuple())
        self.cursor.commit()

    def get_continent_cases(self, date: str):
        """
        Loads all the cases for all continents for a specific date ordered by the continent id.

        Parameters:
        date -- the date which should be loaded (e.g. 2022-01-22)
        """
        sql = "SELECT * FROM V_ContinentCases WHERE CasesDate = ? ORDER BY ContinentID"
        self.cursor.execute(sql, date)
        return self.cursor.fetchall()

    def get_continent_vaccinations(self, date: str):
        """
        Loads all the vaccinations for all continents for a specific date ordered by the continent id.

        Parameters:
        date -- the date which should be loaded (e.g. 2022-01-22)
        """
        sql = "SELECT * FROM V_ContinentTotalVaccinations WHERE VaccinationsDate = ? ORDER BY ContinentID"
        self.cursor.execute(sql, date)
        return self.cursor.fetchall()

    def get_total_cases(self):
        sql = "SELECT CasesDate, sum(TotalCases), sum(TotalDeaths) FROM Cases GROUP BY CasesDate ORDER BY CasesDate"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_total_vaccinations(self):
        sql = "SELECT VaccinationsDate, sum(cast(TotalVaccinations AS bigint)) FROM Vaccinations GROUP BY VaccinationsDate ORDER BY VaccinationsDate"
        self.cursor.execute(sql)
        return self.cursor.fetchall()
