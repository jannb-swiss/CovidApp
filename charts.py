import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import datetime, timedelta

from db import DatabaseConnection


class Charts:

    def __init__(self, db: DatabaseConnection):
        self._db = db

    # get pie chart of the total cases by continent and of the given date
    def showPieOfTotalCasesByContinent(self, date: str = None):
        if date is None:
            date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
        # load continent labels
        labels = [country[1] for country in self._db.get_continents()]
        # load cases by continent
        sizes = [case[1] for case in self._db.get_continent_cases(date)]
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%')
        ax1.axis('equal')
        plt.show()

    def showLineTotalCases(self):
        cases = self._db.getTotalCases()
        vaccines = self._db.getTotalVaccinations()
        labels = [datetime.strptime(x[0], '%Y-%m-%d') for x in cases]
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

    def showCaseDeathChart(self):
        data = self._db.getTotalCases()

        date = [datetime.strptime(x[0], '%Y-%m-%d') for x in data]
        cases = [x[1] for x in data]
        deaths = [x[2] for x in data]

        fig, ax1 = plt.subplots()

        color = 'tab:red'
        ax1.set_xlabel('Datum')
        ax1.set_ylabel('Fälle', color=color)
        ax1.plot(date, cases, color=color)
        ax1.tick_params(axis='y', labelcolor=color)

        plt.gca().yaxis.set_major_formatter(ticker.EngFormatter())

        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

        color = 'tab:blue'
        ax2.set_ylabel('Gestorbene', color=color)  # we already handled the x-label with ax1
        ax2.plot(date, deaths, color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        plt.gcf().autofmt_xdate()
        plt.gca().yaxis.set_major_formatter(ticker.EngFormatter())
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.grid(True)

        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.show()
