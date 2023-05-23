'''
Convert openFDA medical device data from JSON to SQL via Pandas.

Data flow is JSON -> Pandas -> write pandas rows to SQL.

There are 2 openFDA device data files, so some operations
below are performed twice.
'''

import csv
import flatten_json
import json
import os
import pandas as pd

import settings
from openfda_json_cleaner import OpenFdaJsonCleaner

device_data_dir = 'device-data'
outfile = f'{device_data_dir}/usfda_medical_devices.csv'


def get_file_size(file_path):
    byte_size = os.path.getsize(file_path)
    megabytes = byte_size / 1024 / 1024
    return megabytes

def combine_device_jsons(json1, json2):
    return json1['results'] + json2['results']

def sql_stringify_columns(columns):
    # Turn a list of dict keys into SQL-friendly column names
    columns = str(columns)
    columns = columns[11:-2] # Delete prepended dict info and [(...)] at start/end
    columns = columns.replace('\'','') # Delete single quotes
    return columns

def sql_stringify_values(values):
    # Turn a list of dict keys into a SQL-friendly value string
    values = str(values)
    values = values[13:-2] # Delete prepended dict info and [(...)] at start/end
    values = values.replace('{}', '\'\'') # Replace braces with empty string
    values = values.replace('[]', '\'\'') # Replace brackets with empty string
    return values

def add_device_to_sql_db(db, device):
    sql_columns = sql_stringify_columns(device.keys())
    device_values = sql_stringify_values(device.values())
    try:
        sql_command = f'''
            INSERT INTO devices ({sql_columns})
            VALUES ({device_values})
            '''
        print(f"Performing SQL insertion with the following command:\t{sql_command}")
        sql_insert = db.cursor().execute(sql_command)
        print(dir(sql_insert))
        print(f"Result of SQL insertion: {sql_insert}")
        print(f"Saving SQL database changes...")
        db_commit = db.commit()
        print(f"Database save ended with the following result: {db_commit}")
    except Exception as e:
        print(e)


def main():
    device_file1 = device_data_dir + '/device-registrationlisting-0001-of-0002.json'
    device_file2 = device_data_dir + '/device-registrationlisting-0002-of-0002.json'

    # Open openFDA JSON files
    file_size1 = get_file_size(device_file1)
    print(f"Opening '{device_file1}' ({file_size1} MB)...")
    devices1 = json.load(open(device_file1))
    file_size2 = get_file_size(device_file2)
    print(f"Opening '{device_file2}' ({file_size2} MB)...")
    devices2 = json.load(open(device_file2))

    # Combine JSON files into one
    print(f"Combining openFDA JSON files...")
    devices = combine_device_jsons(devices1, devices2)

    # Parse JSON into device_list
    device_list = []
    print("Converting JSON to CSV...")
    #devices = devices[0:10000] # Limited index for testing only
    for device in devices:
        print("\tParsing line of JSON:", device)
        flattened_data = OpenFdaJsonCleaner.clean(device)
        print("Flattened data: ", flattened_data)
        device_list.append(flattened_data)

    # Convert device list to dataframe
    device_df = pd.DataFrame(device_list)

    # Preview device data
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_rows', 999)
    pd.set_option('display.max_columns', 999)
    print(device_df.head(3))

    # Save dataframe to CSV
    print(f'Saving data to CSV: `{outfile}`')
    device_df.to_csv(outfile)


if __name__ == "__main__":
    main()

