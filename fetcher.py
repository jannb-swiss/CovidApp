#!/usr/bin/python


import codecs
import csv
import getopt
import glob
import sys
from contextlib import closing

import requests
import pandas as pd
import config
from db import DatabaseConnection
from models.case import Case
from models.test import Test
from models.vaccination import Vaccination

# config


url = 'https://raw.githubusercontent.com/jannb-swiss/CovidApp/main/CSV/Covid19_FRA.csv'
# dj = pd.concat(map(pd.read_json, glob.glob('json/*.json')))
# df = pd.concat(map(pd.read_csv, glob.glob('CSV/*.csv')))
# dn = pd.concat((dj, df))

# db connection
db = DatabaseConnection(
    # config.db_credentials['driver'],
    config.db_credentials['host'],
    config.db_credentials['database'],
    config.db_credentials['user'],
    config.db_credentials['password']
)

def rebuildDatabase(verbose: bool = False):
    if verbose:
        print('loading continent and country data')

    # load initial continent / country data
    continents: list = db.get_continents()
    countries: list = db.get_countries()

    if verbose:
        print('found {} continents and {} countries'.format(len(continents), len(countries)))

    if verbose:
        print('clearing database')

    db.truncate_cases()
    db.truncate_tests()
    db.truncate_vaccinations()

    row_count: int = 0

    # load csv
    with closing(requests.get(url, stream=True)) as r:

        if verbose:
            print('loading csv rows')

        # read csv
        reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'), delimiter=',')

        # skip header row
        next(reader)

        # iterate through all csv rows
        for index, row in enumerate(reader):

            row_count += 1

            if verbose:
                print('[{}] {}, {}'.format(index, row[2], row[3]))

            # skip row if continent is empty (non country data, eg world, europe, etc)
            if row[1] == "":
                continue

            # insert continent if not present already
            if not any(continent[1] == row[1] for continent in continents):
                if verbose:
                    print('found new continent {}'.format(row[1]))
                ContinentID: int = db.insertContent(row[1])
                continents.append([ContinentID, row[1]])

            # get the continent id for the current row
            continent_id: int = [c for c in continents if c[1] == row[1]][0][0]

            if not any(country[2] == row[0] for country in countries):
                if verbose:
                    print('found new country {}'.format(row[2]))
                CountryID: int = db.insertCountry(continent_id, row[0], row[2], int(float(row[44] or 0)))
                countries.append([CountryID, continent_id, row[0], row[2], row[44]])

            # get the country id for the current row
            country_id: int = [c for c in countries if c[2] == row[0]][0][0]

            # insert case
            db.insertCase(Case.from_row(country_id, row))

            # create test
            db.insertTests(Test.from_row(country_id, row))

            # create vaccination
            db.insertVaccinations(Vaccination.from_row(country_id, row))

    if verbose:
        print('script finished, found {} rows'.format(row_count))


if __name__ == "__main__":
    try:
        # if no params available, start in silent mode
        rebuildDatabase(verbose=True)

    except getopt.error as err:
        print(str(err))
        sys.exit(2)
