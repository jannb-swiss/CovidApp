from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from sql.database_connection import DatabaseConnection


class Charts:

    def __init__(self, db: DatabaseConnection):
        self._db = db

    def show_total_cases_by_continent(self, date_text: str):
        labels = [continent[1] for continent in self._db.get_continents()]
        sizes = [case[1] for case in self._db.get_continent_cases(date_text)]

        if not sizes:
            print("No data found for date [{}]".format(date_text))
            return

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%')

        ax1.axis('equal')
        plt.title("Total Cases by Continent", bbox={'facecolor': '0.9', 'pad': 5})
        plt.show()

    def show_death_chart(self):
        data = self._db.get_total_cases()

        dates = [datetime.strptime(str(x[0]), '%Y-%m-%d') for x in data]
        cases = [x[1] for x in data]
        deaths = [x[2] for x in data]

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

    def show_total_cases(self):
        cases = self._db.get_total_cases()
        vaccines = self._db.get_total_vaccinations()
        labels = [datetime.strptime(str(x[0]), '%Y-%m-%d') for x in cases]
        plt.plot(labels, [x[1] for x in cases])
        plt.plot(labels, [x[2] for x in cases])
        plt.plot(labels, [x[1] for x in vaccines])
        plt.title('total worldwide cases')
        plt.gcf().autofmt_xdate()
        plt.gca().yaxis.set_major_formatter(ticker.EngFormatter())
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.grid(True)
        plt.show()
