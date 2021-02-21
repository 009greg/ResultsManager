# Get a .CSV from SUIS DATA and process data to user-friendly format

import pandas
import sqlite3
# Append useful information so it can be transferred to database
# fixme Calculate decimal score even if start numbers arn't in the csv.


def importcsvfile_3P(path):

    df = pandas.read_csv(path, sep=';', names=['StartN', 'PrimaryScore', 'SightorMatch', 'FP', 'SS',
              'Radius', 'Time', 'IT', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
              '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'])
    df.to_csv('test.csv', sep=';')

    # Remove non useful information

    f=pandas.read_csv('test.csv', sep=';')
    keep_col = ['StartN','PrimaryScore','SightorMatch','FP','SS','Radius',
                'Time', 'IT']
    new_f = f[keep_col]
    new_f.to_csv("useful.csv", index=False)


def importcsvfile_50m(path):

    df = pandas.read_csv(path, sep=';', names=['StartN', 'PrimaryScore', 'SightorMatch', 'FP', 'SS',
              'Radius', 'Time', 'IT', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
              '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'])
    df.to_csv('sinclairformatraw.csv', sep=';')

    # Remove non useful information

    f=pandas.read_csv('sinclairformatraw.csv', sep=';')
    keep_col = ['StartN','PrimaryScore','SightorMatch','FP','SS','Radius',
                'Time', 'IT']
    new_f = f[keep_col]
    new_f.to_csv("sinclairformatprocessed.csv", index=False)

