import logging
from datetime import datetime, timedelta

from urllib.error import URLError
from numpy import uint
import sqlalchemy

import mariadb
import pandas as pd
from pandas.io.sql import DatabaseError


logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


class AirQuality:
    def __init__(self, particle_sensor_id, humidity_sensor_id):
        self.sds_id = particle_sensor_id
        self.dht_id = humidity_sensor_id

    def connect_database(self):
        conn = None
        try:
            conn = mariadb.connect(
                user="example-user",
                password="my_cool_secret",
                host="127.0.0.1",
                port=3306,
                database="AirQuality"
            )
            logging.info("Successfully conected to database.")
        except mariadb.Error as mariadb_error:
            logging.error(
                f"Error connecting to MariaDB Platform: {mariadb_error}")

        return conn

    def import_data(self, period: uint = 1):
        engine = sqlalchemy.create_engine(
            "mariadb+mariadbconnector://example-user:my_cool_secret@127.0.0.1:3306")

        for days_counter in range(period):
            now = datetime.now()-timedelta(days=days_counter)
            date = now.strftime("%Y-%m-%d")

            sds_url = f'http://archive.sensor.community/{date}/{date}_sds011_sensor_{self.sds_id}.csv'

            dht_url = f'http://archive.sensor.community/{date}/{date}_dht22_sensor_{self.dht_id}.csv'

            logging.debug(f"Importing data for {date}")
            try:
                sds_df = pd.read_csv(sds_url, sep=';')

                sds_df.dropna(how='all', axis=1, inplace=True)
                sds_df.to_sql("tabelle", engine, if_exists="append")
                #sds_df.to_sql("sds_sensor", engine.raw_connection, if_exists="append")
            except DatabaseError as db_error:
                logging.error(f"a database error occoured: {db_error}")
            except URLError as url_error:
                logging.error(
                    f"could not read sds data for {date}: {url_error}")
            except Exception as ex:
                logging.exception(f"something went wrong: {ex}")

            try:
                dht_df = pd.read_csv(dht_url, sep=';')

                dht_df.dropna(how='all', axis=1, inplace=True)

                #sds_df.to_sql("dht_sensor", engine.raw_connection, if_exists="append")
            except DatabaseError as db_error:
                logging.error(f"a database error occoured: {db_error}")
            except URLError as url_error:
                logging.error(
                    f"could not read dht data for {date}: {url_error}")
            except Exception as ex:
                logging.exception(f"something went wrong: {ex}")


if __name__ == "__main__":
    location = AirQuality(3659, 3660)
    location.import_data(5)
