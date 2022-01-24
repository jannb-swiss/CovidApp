from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from db.database_connection import DatabaseConnection


class Charts:
    """
    Chart object for creating the different matplotlib charts based on the use case. To be able to access the data,
    the object needs a reference to the DatabaseConnection.
    """

    def __init__(self, db: DatabaseConnection):
        self._db = db

    @staticmethod
    def create_pie_chart(title, date_text, sizes, labels):
        """
        Common methode to create a pie chart width data and label

        Parameters:
        title     -- the title to be shown
        date_text -- the selected date string
        sizes     -- the data sizes for the chart
        labels    -- the labels for the chart
        """
        if not sizes:
            print("No data found for date [{}]".format(date_text))
            return

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%')

        ax1.axis('equal')
        plt.title(title, bbox={'facecolor': '0.9', 'pad': 5}, y=1.05)
        plt.show()

    def show_total_cases_by_continent(self, date_text: str):
        """
        Creates a matplotlib pie chart to show all the cases for a specific date.

        Parameters:
        date_text -- the date for showing the cases (e.g. 2022-01-22)
        """
        labels = [continent[1] for continent in self._db.get_continents()]
        sizes = [case[2] for case in self._db.get_continent_cases(date_text)]

        title = "Total Cases by Continent - {}".format(date_text)
        self.create_pie_chart(title, date_text, sizes, labels)

    def show_total_vaccinations_by_continent(self, date_text: str):
        """
        Creates a matplotlib pie chart to show all the vaccinations for a specific date.

        Parameters:
        date_text -- the date for showing the cases (e.g. 2022-01-22)
        """
        labels = [continent[1] for continent in self._db.get_continents()]
        sizes = [case[2] for case in self._db.get_continent_vaccinations(date_text)]

        title = "Total Vaccinations by Continent - {}".format(date_text)
        self.create_pie_chart(title, date_text, sizes, labels)

    def show_death_chart(self):
        """
        Creates a matplotlib pie chart to show all the cases and deaths.
        """
        data = self._db.get_total_cases()

        dates = [datetime.strptime(str(row[0]), '%Y-%m-%d') for row in data]
        cases = [row[1] for row in data]
        deaths = [row[2] for row in data]

        fig, ax1 = plt.subplots()

        color = 'tab:green'
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Cases', color=color)
        ax1.plot(dates, cases, color=color)
        ax1.tick_params(axis='y', labelcolor=color)

        plt.gca().yaxis.set_major_formatter(ticker.EngFormatter())

        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

        color = 'tab:blue'
        ax2.set_ylabel('Deceased', color=color)
        ax2.plot(dates, deaths, color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        plt.gcf().autofmt_xdate()
        plt.gca().yaxis.set_major_formatter(ticker.EngFormatter())
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.grid(True)

        plt.title("Total Cases & Deaths", bbox={'facecolor': '0.9', 'pad': 5}, y=1.08)

        fig.tight_layout()
        plt.show()
