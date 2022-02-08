import logging
import pandas as pd
from datetime import datetime, timedelta

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

class AirQuality:
    def __init__(self, particle_sensor_id, humidity_sensor_id):
        self.sds_id = particle_sensor_id
        self.dht_id = humidity_sensor_id

    def import_data(self, days=1):
        self._dht_df = self._get_dht_data(days)
        #self._sds_df = self._get_sds_data(days)

    def get_particle_dataframe(self):
        return self._sds_df
    
    def get_humidity_dataframe(self):
        return self._sds_df

    def _get_sds_data(self, days):
        data = []
        for day in range(days):
            now = datetime.now()-timedelta(days=day) # current date - days
            date = now.strftime("%Y-%m-%d") 
            logging.debug(f"Importing data for {date}")

            try:
                SDS_URL = f'http://archive.sensor.community/{date}/{date}_sds011_sensor_{self.sds_id}.csv'
               
                sds_df = pd.read_csv(SDS_URL, sep=';')
                sds_df.dropna(how='all', axis=1, inplace=True)
                data.append(sds_df)
                print("hello")
                #TODO: INSERT INTO sds_data (timestamp, P1, P2) VALUES()

            except:
                logging.warning(f"could not read data for {date}")
        
        return pd.concat(data, axis=0)
            

    def _get_dht_data(self, days=1):
        data =[]
        for day in range(days):
            now = datetime.now()-timedelta(days=day) # current date - days
            date = now.strftime("%Y-%m-%d") 
            logging.debug(f"Importing data for {date}")

            try:
                DHT_URL = f'http://archive.sensor.community/{date}/{date}_dht22_sensor_{self.dht_id}.csv'

                dht_df = pd.read_csv(DHT_URL, sep=';')
                dht_df.dropna(how='all', axis=1, inplace=True)
                data.append(dht_df)

            except:
                logging.warning(f"could not read data for {date}")
            
        return pd.concat(data, axis=0)

if __name__ == "__main__":
    aq = AirQuality(3659, 3660)
    aq.import_data(4)
    #print(aq.get_particle_dataframe())

