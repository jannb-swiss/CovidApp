class Country:

    def __init__(self, continent_id: int, iso_code: str, location: str, population: int):
        self._continent_id = continent_id
        self._iso_code = iso_code
        self._location = location
        self._population = population

    @staticmethod
    def from_csv_row(continent_id: int, row: list):
        return Country(
            continent_id,
        )

    @staticmethod
    def from_json_item(continent_id: int, item: any):
        return Country(
            continent_id,

        )

    def to_tuple(self) -> tuple:
        return (
            self.continent_id,
            self.iso_code,
            self.location,
            self.population,
        )
