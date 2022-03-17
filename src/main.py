import logging
import time
from datetime import datetime, timedelta

import sqlite3
from sqlite3 import Error

import pandas as pd

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

def create_connection(db_file):
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        logging.info(f"Successfully connected to {db_file}.")
        return connection

    except Error as e:
        logging.error(e)

def show_data(sensor):
    connection = create_connection("airquality.db")
    cursor = connection.cursor()

    cursor.execute(f'''SELECT * FROM {sensor}''')
    
    for row in cursor.fetchall():
        print(row)

def import_data(period = 1):
    connection = create_connection("airquality.db")
    logging.debug(f"import stated at {time.strftime('%X')}")
    for days in range(period):
        requested_date = datetime.now()-timedelta(days= days)

        formated_date = requested_date.strftime("%Y-%m-%d")

        sds_url = f'http://archive.sensor.community/{formated_date}/{formated_date}_sds011_sensor_3659.csv'
        
        dht_url = f'http://archive.sensor.community/{formated_date}/{formated_date}_dht22_sensor_3660.csv'

        try:
            sds_dataframe = pd.read_csv(sds_url, sep=";")

            sds_dataframe.dropna(how='all', axis=1, inplace=True)

            sds_dataframe.to_sql("sds_sensor", connection, if_exists="append")
        except Exception as e:
            logging.error(f"could not import data for {formated_date}: {e}")

        try:
            dht_dataframe = pd.read_csv(dht_url, sep=";")

            dht_dataframe.dropna(how='all', axis=1, inplace=True)

            dht_dataframe.to_sql("dht_sensor", connection, if_exists="append")
        except Exception as e:
            logging.error(f"could not import data for {formated_date}: {e}")

    logging.debug(f"import finished at {time.strftime('%X')}")

if __name__ == '__main__':
    import_data(5)
    #show_data("dht_sensor")
    #show_data("sds_sensor")
    