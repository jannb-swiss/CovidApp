#!/usr/bin/python
import csv
import getopt
import json
import os
import sys

import config
from db.database_connection import DatabaseConnection
from models.case import Case
from models.test import Test
from models.vaccination import Vaccination

verbose: bool = False
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
    """
    Deletes all the existing data from the database
    """
    print("Start to cleanup all data from database")

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

    print("Cleanup of database is completed")


def insert_continent_if_not_existing(name: str) -> int:
    """
    Inserts a continent record if it's not already existing.

    Parameters:
    name -- the name of the continent (e.g. Europe)
    """

    continent = db.get_continent_by_name(name)
    if continent:
        return continent[0]
    else:
        if verbose:
            print('Found new continent {}'.format(name))
        return db.insert_continent(name)


def insert_country_if_not_existing(iso_code: str, location: str, population: str, continent_id) -> int:
    """
    Inserts a country record if it's not already existing.

    Parameters:
    iso_code     -- the iso code of the country (e.g. ARG)
    location     -- the location name of the country (e.g. Argentina)
    population   -- the population of the country
    continent_id -- the id of the corresponding continent
    """

    country = db.get_country_by_iso_code(iso_code)
    if country:
        return country[0]
    else:
        if verbose:
            print('found new country {}'.format(location))
        return db.insert_country(continent_id, iso_code, location, int(float(population or 0)))


def import_all_files():
    """
    Imports all the CSV and JSON files which are stored in the ./data/ folder.
    """
    print("Start importing all files")

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

    print("Import of files is done")


def import_csv_file(file_path: str):
    """Importing all the data of a specific CSV file.

    Parameters:
    file_path -- path to the file (e.g. ./data/csv/Covid19_FRA.csv)
    """

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

            db.insert_cases(Case.from_csv_row(country_id, row))
            db.insert_tests(Test.from_csv_row(country_id, row))
            db.insert_vaccinations(Vaccination.from_csv_row(country_id, row))


def import_json_file(file_path: str):
    """
    Importing all the data of a specific JSON file.

    Parameters:
    file_path -- path to the file (e.g. ./data/json/Covid_ARG.json)
    """

    if verbose:
        print('Loading JSON file [{}|'.format(file_path))

    with open(file_path) as json_file:
        json_data = json.load(json_file)

        for item in json_data:
            if verbose:
                print('{}, {}'.format(item['location'], item['date']))

            if item['continent'] == "":
                continue

            continent_id: id = insert_continent_if_not_existing(item['continent'])
            country_id: id = insert_country_if_not_existing(item['iso_code'], item['location'], item['population'],
                                                            continent_id)

            db.insert_cases(Case.from_json_item(country_id, item))
            db.insert_tests(Test.from_json_item(country_id, item))
            db.insert_vaccinations(Vaccination.from_json_item(country_id, item))


if __name__ == "__main__":
    try:
        arguments, values = getopt.getopt(sys.argv[1:], "v", ["verbose"])

        for argument, value in arguments:
            if argument in ("-v", "--verbose"):
                verbose = True
            else:
                print("invalid parameter `" + argument + "`")
                sys.exit(2)

        cleanup_database()
        import_all_files()

    except getopt.error as err:
        print(str(err))
        sys.exit(2)
