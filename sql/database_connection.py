import pyodbc

from models.case import Case
from models.test import Test
from models.vaccination import Vaccination


class DatabaseConnection:
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
        self.cursor.execute("DELETE FROM Country")
        self.cursor.commit()

    def delete_continents(self):
        self.cursor.execute("DELETE FROM Continent")
        self.cursor.commit()

    def delete_cases(self):
        self.cursor.execute("DELETE FROM Cases")
        self.cursor.commit()

    def delete_tests(self):
        self.cursor.execute("DELETE FROM Tests")
        self.cursor.commit()

    def delete_vaccinations(self):
        self.cursor.execute("DELETE FROM Vaccinations")
        self.cursor.commit()

    def get_continents(self):
        self.cursor.execute("SELECT * FROM Continent ORDER BY ContinentID")
        return self.cursor.fetchall()

    def get_continent_by_name(self, name: str):
        self.cursor.execute("SELECT * FROM Continent WHERE ContinentName = ?", name)
        return self.cursor.fetchone()

    def get_country_by_iso_code(self, iso_code: str):
        self.cursor.execute("SELECT * FROM Country WHERE IsoCode = ?", iso_code)
        return self.cursor.fetchone()

    def insert_content(self, name: str) -> int:
        sql = """
        declare @out int;
        exec createContinent @name = ?, @new_identity = @out output;
        select @out AS the_output;
        """
        self.cursor.execute(sql, name)
        inserted_id: int = self.cursor.fetchall()
        self.cursor.commit()
        return inserted_id[0][0]

    def insert_country(self, con_id: int, iso: str, name: str, population: int) -> int:
        sql = """
        declare @out int;
        exec createCountry @continent = ?, @iso_code = ?, @name = ?, @population = ?, @new_identity = @out output;
        select @out as the_output;
        """
        self.cursor.execute(sql, (con_id, iso, name, population))
        inserted_id: int = self.cursor.fetchall()
        self.cursor.commit()
        return inserted_id[0][0]

    def insert_case(self, case: Case):
        sql = "exec createCases @country = ?, @date = ?, @total_cases = ?, @new_cases = ?, @total_deaths = ?, @new_deaths = ?, @reproduction_rate = ?;"
        self.cursor.execute(sql, case.to_tuple())
        self.cursor.commit()

    def insert_vaccinations(self, vaccination: Vaccination):
        sql = "exec createVaccinations @country = ?, @date = ?, @total_vaccinations = ?, @people_vaccinated = ?, @people_fully_vaccinated = ?, @new_vaccinations = ?;"
        self.cursor.execute(sql, vaccination.to_tuple())
        self.cursor.commit()

    def insert_tests(self, test: Test):
        sql = "exec createTests @country = ?, @date = ?, @new_tests = ?, @total_tests = ?, @positive_rate = ?;"
        self.cursor.execute(sql, test.to_tuple())
        self.cursor.commit()

    def get_continent_cases(self, date: str):
        sql = "SELECT * FROM V_ContinentCases WHERE CasesDate = ? ORDER BY ContinentID"
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