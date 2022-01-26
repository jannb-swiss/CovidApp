class Vaccination:
    """
    Object which is representing a Vaccination entity.
    """

    def __init__(self, country: int, date: str, total_vaccinations: int, people_vaccinated: int,
                 people_fully_vaccinated: int, new_vaccinations: int):
        self.country = country
        self.date = date
        self.total_vaccinations = total_vaccinations
        self.people_vaccinated = people_vaccinated
        self.people_fully_vaccinated = people_fully_vaccinated
        self.new_vaccinations = new_vaccinations

    @staticmethod
    def from_csv_row(country: int, row: list):
        """
        Create a Vaccination object based on CSV record.

        Parameters:
        country -- id of the country
        row     -- record of the CSV file
        """
        return Vaccination(
            country,
            row[3],
            int(float(row[34] or 0)),
            int(float(row[35] or 0)),
            int(float(row[36] or 0)),
            int(float(row[37] or 0)),
        )

    @staticmethod
    def from_json_item(country: int, item: any):
        """
        Create a Vaccination object based on JSON record.

        Parameters:
        country -- id of the country
        item    -- one object from the JSON object
        """
        return Vaccination(
            country,
            item['date'],
            int(float(item['total_vaccinations'] or 0)),
            int(float(item['people_vaccinated'] or 0)),
            int(float(item['people_fully_vaccinated'] or 0)),
            int(float(item['new_vaccinations'] or 0)),
        )

    def to_tuple(self) -> tuple:
        return (self.country, self.date, self.total_vaccinations, self.people_vaccinated, self.people_fully_vaccinated,
                self.new_vaccinations)
