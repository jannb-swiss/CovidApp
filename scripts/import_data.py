#!/usr/bin/python
import csv
import getopt
import json
import os
import sys

import config
from models.case import Case
from models.test import Test
from models.vaccination import Vaccination
from sql.database_connection import DatabaseConnection

verbose: bool = True
csv_data_folder_path = "./data/csv"
json_data_folder_path = "./data/json"

db = DatabaseConnection(
    config.db_credentials['driver'],
    config.db_credentials['host'],
    config.db_credentials['database'],
    config.db_credentials['user'],
    config.db_credentials['password'],
)


def cleanup_database():
    db.delete_vaccinations()
    if verbose:
        print('Database table [Vaccinations] cleaned')

    db.delete_tests()
    if verbose:
        print('Database table [Tests] cleaned')

    db.delete_cases()
    if verbose:
        print('Database table [Cases] cleaned')

    db.delete_countries()
    if verbose:
        print('Database table [Country] cleaned')

    db.delete_continents()
    if verbose:
        print('Database table [Continent] cleaned')


def insert_continent_if_not_existing(name: str) -> int:
    continent = db.get_continent_by_name(name)
    if continent:
        return continent[0]
    else:
        if verbose:
            print('Found new continent {}'.format(name))
        return db.insert_content(name)


def insert_country_if_not_existing(iso_code: str, location: str, population: str, continent_id) -> int:
    country = db.get_country_by_iso_code(iso_code)
    if country:
        return country[0]
    else:
        if verbose:
            print('found new country {}'.format(location))
        return db.insert_country(continent_id, iso_code, location, int(float(population or 0)))


def import_all_files():
    for root, dirs, files in os.walk(csv_data_folder_path):
        if verbose:
            print("Found {} CSV files to import".format(len(files)))

        for file in files:
            file_path: str = csv_data_folder_path + "/" + file
            import_csv_file(file_path)

    for root, dirs, files in os.walk(json_data_folder_path):
        if verbose:
            print("Found {} JSON files to import".format(len(files)))

        for file in files:
            file_path: str = json_data_folder_path + "/" + file
            import_json_file(file_path)


def import_csv_file(file_path: str):
    if verbose:
        print('Loading CSV file [{}|'.format(file_path))

    with open(file_path, newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='|')

        next(reader)

        for index, row in enumerate(reader):
            if verbose:
                print('{}, {}'.format(row[2], row[3]))

            if row[1] == "":
                continue

            continent_id: id = insert_continent_if_not_existing(row[1])
            country_id: id = insert_country_if_not_existing(row[0], row[2], row[44], continent_id)

            db.insert_case(Case.from_csv_row(country_id, row))
            db.insert_tests(Test.from_csv_row(country_id, row))
            db.insert_vaccinations(Vaccination.from_csv_row(country_id, row))


def import_json_file(file_path: str):
    if verbose:
        print('Loading JSON file [{}|'.format(file_path))

    with open(file_path) as json_file:
        json_data = json.load(json_file)

        for item in json_data:
            if verbose:
                print('{}, {}'.format(item['location'], item['date']))

            if item['continent'] == "":
                continue

            continent_id: id = insert_continent_if_not_existing(item['location'])
            country_id: id = insert_country_if_not_existing(item['iso_code'], item['location'], item['population'],
                                                            continent_id)

            db.insert_case(Case.from_json_item(country_id, item))
            db.insert_tests(Test.from_json_item(country_id, item))
            db.insert_vaccinations(Vaccination.from_json_item(country_id, item))


if __name__ == "__main__":
    try:
        cleanup_database()
        import_all_files()

    except getopt.error as err:
        print(str(err))
        sys.exit(2)
