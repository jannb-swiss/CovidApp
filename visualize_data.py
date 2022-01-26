import getopt
import sys
from datetime import datetime

import config
from db.database_connection import DatabaseConnection
from visualize.charts import Charts

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


def run_with_date_input(method_to_run):
    """
    Run a method with a date input from the user.

    Parameters:
    method_to_run -- method which is called with date input
    """
    date_text = input('Enter specific date (e.g. 2021-11-22): ')

    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        method_to_run(date_text)
    except ValueError:
        print("The entered date is not in the correct format, should be YYYY-MM-DD. Please try again!")


if __name__ == "__main__":
    try:
        charts = Charts(db)

        get_help()

        while True:
            action = input('Enter your option: ')

            match action:
                case '1':
                    run_with_date_input(charts.show_total_cases_by_continent)
                case '2':
                    charts.show_death_chart()
                case '3':
                    run_with_date_input(charts.show_total_vaccinations_by_continent)
                case 'exit':
                    sys.exit(0)
                case _:
                    print("Invalid action. Please try again!")

    except getopt.error as err:
        print(str(err))
        sys.exit(2)
