class Case:
    """
    Object which is representing a Case entity.
    """

    def __init__(self, country: int, date: str, total_cases: int, new_cases: int, total_deaths: int, new_deaths: int,
                 reproduction_rate: float):
        self.country = country
        self.date = date
        self.total_cases = total_cases
        self.new_cases = new_cases
        self.total_deaths = total_deaths
        self.new_deaths = new_deaths
        self.reproduction_rate = reproduction_rate

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

    def to_tuple(self) -> tuple:
        return (self.country, self.date, self.total_cases, self.new_cases, self.total_deaths, self.new_deaths,
                self.reproduction_rate)
