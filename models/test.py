class Test:
    """
    Object which is representing a Test entity.
    """

    def __init__(self, country: int, date: str, new_tests: int, total_tests: int, positive_rate: float):
        self.country = country
        self.date = date
        self.new_tests = new_tests
        self.total_tests = total_tests
        self.positive_rate = positive_rate

    @staticmethod
    def from_csv_row(country: int, row: list):
        """
        Create a Test object based on CSV record.

        Parameters:
        country -- id of the country
        row     -- record of the CSV file
        """
        return Test(
            country,
            row[3],
            int(float(row[25] or 0)),
            int(float(row[26] or 0)),
            float(row[31] or 0),
        )

    @staticmethod
    def from_json_item(country: int, item: any):
        """
        Create a Test object based on JSON record.

        Parameters:
        country -- id of the country
        item    -- one object from the JSON object
        """
        return Test(
            country,
            item['date'],
            int(float(item['new_tests'] or 0)),
            int(float(item['total_tests'] or 0)),
            float(item['positive_rate'] or 0),
        )

    def to_tuple(self) -> tuple:
        return self.country, self.date, self.new_tests, self.total_tests, self.positive_rate
