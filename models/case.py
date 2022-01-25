class Case:
    """
    Object which is representing a Case entity.
    """

    def __init__(self, country: int, date: str, total_cases: int, new_cases: int, total_deaths: int, new_deaths: int,
                 reproduction_rate: float):
        self._country = country
        self._date = date
        self._total_cases = total_cases
        self._new_cases = new_cases
        self._total_deaths = total_deaths
        self._new_deaths = new_deaths
        self._reproduction_rate = reproduction_rate

    @staticmethod
    def from_csv_row(country: int, row: list):
        """
        Create a Case object based on CSV record.

        Parameters:
        country -- id of the country
        row     -- record of the CSV file
        """
        return Case(
            country,
            row[3],
            int(float(row[4] or 0)),
            int(float(row[5] or 0)),
            int(float(row[7] or 0)),
            int(float(row[8] or 0)),
            float(row[16] or 0)
        )

    @staticmethod
    def from_json_item(country: int, item: any):
        """
        Create a Case object based on JSON record.

        Parameters:
        country -- id of the country
        item    -- one object from the JSON object
        """
        return Case(
            country,
            item['date'],
            int(float(item['total_cases'] or 0)),
            int(float(item['new_cases'] or 0)),
            int(float(item['total_deaths'] or 0)),
            int(float(item['new_deaths'] or 0)),
            float(item['reproduction_rate'] or 0)
        )

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, country: int):
        pass

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date: str):
        self._date = date

    @property
    def total_cases(self):
        return self._total_cases

    @total_cases.setter
    def total_cases(self, total_cases: str):
        self._total_cases = total_cases

    @property
    def new_cases(self):
        return self._new_cases

    @new_cases.setter
    def new_cases(self, new_cases: str):
        self._new_cases = new_cases

    @property
    def total_deaths(self):
        return self._total_deaths

    @total_deaths.setter
    def total_deaths(self, total_deaths: str):
        self._total_deaths = total_deaths

    @property
    def new_deaths(self):
        return self._new_deaths

    @new_deaths.setter
    def new_deaths(self, new_deaths: str):
        self._new_deaths = new_deaths

    @property
    def reproduction_rate(self):
        return self._reproduction_rate

    @reproduction_rate.setter
    def reproduction_rate(self, reproduction_rate: str):
        self._reproduction_rate = reproduction_rate

    def to_tuple(self) -> tuple:
        return (
            self.country,
            self.date,
            self.total_cases,
            self.new_cases,
            self.total_deaths,
            self.new_deaths,
            self.reproduction_rate
        )
