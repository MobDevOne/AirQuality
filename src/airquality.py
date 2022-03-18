import logging
from datetime import datetime, timedelta

import pandas as pd
from pandas import errors
import mariadb

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


class AirQuality:
    def __init__(self, particle_sensor_id, humidity_sensor_id):
        self.sds_id = particle_sensor_id
        self.dht_id = humidity_sensor_id
        self._sds_df = None
        self._dht_df = None

    def connect_database(self):
        conn = None
        try:
            conn = mariadb.connect(
                user = "example-user",
                password = "my_cool_secret",
                host = "127.0.0.1",
                port = 3306,
                database = "AirQuality"
            )
            logging.info("Successfully conected to database.")

            return conn
        except mariadb.Error as error:
            logging.error(f"Error connecting to MariaDB Platform: {error}")
            return conn

    def import_data(self, days=1):
        connection = self.connect_database()
        for day in range(days):
            now = datetime.now()-timedelta(days=day)
            date = now.strftime("%Y-%m-%d")

            sds_url = f'http://archive.sensor.community/{date}/{date}_sds011_sensor_{self.sds_id}.csv'

            dht_url = f'http://archive.sensor.community/{date}/{date}_dht22_sensor_{self.dht_id}.csv'

            logging.debug(f"Importing data for {date}")

            try:
                self._sds_df = pd.read_csv(sds_url, sep=';')
                self._sds_df.dropna(how='all', axis=1, inplace=True)
                self._sds_df.to_sql("sds_sensor", connection, if_exists="append")
                
            except errors.ParserError as e:
                logging.warning(f"could not read sds data for {date}: {e}")

            try:
                self._dht_df = pd.read_csv(dht_url, sep=';')
                self._dht_df.dropna(how='all', axis=1, inplace=True)
                self._sds_df.to_sql("dht_sensor", connection, if_exists="append")
            except errors.ParserError as e:
                logging.warning(f"could not read dht data for {date}: {e}")

    def get_particle_dataframe(self):
        return self._sds_df

    def get_humidity_dataframe(self):
        return self._sds_df



if __name__ == "__main__":
    location = AirQuality(3659, 3660)
    location.import_data(3)
