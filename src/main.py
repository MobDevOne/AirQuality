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

def show_temperature(year, month, day):
    connection = create_connection("airquality.db")
    cursor = connection.cursor()
    try:
        cursor.execute(f'SELECT MAX(temperature) as "maximal temperature", MIN(temperature) as "minimal temperature", ROUND(Avg(temperature),1) as "average temperature" FROM dht_sensor WHERE timestamp between "{year}-{month}-{day}T00:00:00" AND "{year}-{month}-{day}T23:59:59"')
    
        for row in cursor.fetchall():
            print(row)
    except Error as err:
        print(err)

def show_particle(year, month, day):
    connection = create_connection("airquality.db")
    cursor = connection.cursor()
    try:
        cursor.execute(f'SELECT MAX(P1) as "maximal particle size", MIN(P1) as "minimal particle size", ROUND(Avg(P1),0) as "average particle size" FROM sds_sensor WHERE timestamp between "{year}-{month}-{day}T00:00:00" AND "{year}-{month}-{day}T23:59:59"')
        
        for row in cursor.fetchall():
            print(row)
    except Error as err:
        print(err)

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
   #import_data(400) 
    year = str(input("Geben Sie das Jahr ein: "))
    month = str(input("Geben Sie den Monat ein: "))
    day = str(input("Geben Sie den Tag ein: "))
    
    show_temperature(year, month, day)
    show_particle(year, month, day)

    
