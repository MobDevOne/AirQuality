from datetime import datetime, timedelta

import sqlite3
from sqlite3 import Error

import pandas as pd


def create_connection(db_file):
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        return connection

    except Error as e:
        print(e)

def show_data():
    connection = create_connection("airquality.db")
    cursor = connection.cursor()

    cursor.execute('SELECT  MAX(temperature) AS "Max Temp", MIN(temperature) AS "Min Temp", Avg(temperature) AS "Avg Temp" FROM dht_sensor WHERE timestamp like "2022-03-10T*"')
    
    for row in cursor.fetchall():
        print(row)

def show_day():
    connection = create_connection("airquality.db")
    cursor = connection.cursor()

    cursor.execute('SELECT timestamp FROM dht_sensor')
    
    for row in cursor.fetchall():
        print(row)

def import_data(period = 1):
    connection = create_connection("airquality.db")

    for days in range(period):
        requested_date = datetime.now()-timedelta(days= days)

        formated_date = requested_date.strftime("%Y-%m-%d")

        sds_url = f'http://archive.sensor.community/{formated_date}/{formated_date}_sds011_sensor_3659.csv'
        
        dht_url = f'http://archive.sensor.community/{formated_date}/{formated_date}_dht22_sensor_3660.csv'

        try:
            sds_dataframe = pd.read_csv(sds_url, sep=";")

            sds_dataframe.dropna(how='all', axis=1, inplace=True)

            sds_dataframe.to_sql("sds_sensor", connection, if_exists="append")
        except:
            print(f"could not read data for {formated_date}")

        try:
            dht_dataframe = pd.read_csv(dht_url, sep=";")
            dht_dataframe.dropna(how='all', axis=1, inplace=True)

            dht_dataframe.to_sql("dht_sensor", connection, if_exists="append")
        except:
            print(f"could not read data for {formated_date}")

if __name__ == '__main__':
    import_data(15) 
    show_data()
    #show_day()
    