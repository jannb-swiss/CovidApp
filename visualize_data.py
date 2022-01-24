import getopt
import sys
from datetime import datetime

import config
from visualize.charts import Charts
from db.database_connection import DatabaseConnection

db = DatabaseConnection(
    config.db_credentials['driver'],
    config.db_credentials['host'],
    config.db_credentials['database'],
    config.db_credentials['user'],
    config.db_credentials['password']
)


def get_help():
    print("################################################")
    print('# exit: Stop the application                   #')
    print('# 1: Show total cases by continent             #')
    print('# 2: Show total cases and deaths               #')
    print('# 3: Show total vaccinations by continent      #')
    print("################################################")


if __name__ == "__main__":
    try:
        charts = Charts(db)

        get_help()
        action = None

        while True:
            action = input('Enter your option: ')

            if action == '1':
                date_text = input('Enter specific date (e.g. 2021-11-22): ')

                try:
                    datetime.strptime(date_text, '%Y-%m-%d')
                    charts.show_total_cases_by_continent(date_text)
                except ValueError:
                    print("The entered date is not in the correct format, should be YYYY-MM-DD. Please try again!")

            if action == '2':
                charts.show_death_chart()

            if action == '3':
                date_text = input('Enter specific date (e.g. 2021-06-06): ')

                try:
                    datetime.strptime(date_text, '%Y-%m-%d')
                    charts.show_total_vaccinations_by_continent(date_text)
                except ValueError:
                    print("The entered date is not in the correct format, should be YYYY-MM-DD. Please try again!")

            elif action == 'exit':
                sys.exit(0)

    except getopt.error as err:
        print(str(err))
        sys.exit(2)
