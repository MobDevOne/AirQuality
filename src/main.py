#um das Datum zu berechnen und zu importieren
from datetime import datetime, timedelta

import sqlite3
from sqlite3 import Error
from numpy import append

#um die csv dateien zu laden und abzuspeichern
import pandas as pd


def create_connection(db_file):
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        return connection

    except Error as e:
        print(e)

#daten werden für einen Zeitraum (period) importiert
#wenn kein Argument übergeben wird, ist der default bei 1(Tag)
def import_data(period = 1):
    #erst legen wir uns eine Datenbank an und speichern die connection
    connection = create_connection("airquality.db")

    #die Schleife zählt die Anzahl der Tage hoch für den Zeitraum, erst 1, dann 2 usw.
    for days in range(period):
        #vom heutigen Datum aus, wird dann die Anzahl an Tagen bei jedem Durchlauf abgezogen.
        #Beim ersten Durchlauf heute - 0 Tage, also heute,
        #beim zweiten heute - 1 Tag, also gestern
        requested_date = datetime.now()-timedelta(days= days)
        #Das Datum muss in ein passendes Format gebracht werden
        formated_date = requested_date.strftime("%Y-%m-%d")

        #Die CSV-Dateien befinden sich auf bestimmten Pfaden auf der Webseite
        # Als Beispiel für den SDS Sensor: tauscht man also Datum aus, bekommt man 
        # die Daten für einen anderen Tag (weswegen das Format wichtig ist
        # und bei einer anderen ID entsprechend die Daten für einen anderen Sensor
        # http://archive.sensor.community/2022-03-01/2022-03-01_sds011_sensor_3359.csv

        #Nach jedem durchlauf, wird ein neues Datum berechnet und das fügen wir 
        #in diesen String hinein
        sds_url = f'http://archive.sensor.community/{formated_date}/{formated_date}_sds011_sensor_3659.csv'
        
        #das gleiche beim dht Sensor
        dht_url = f'http://archive.sensor.community/{formated_date}/{formated_date}_dht22_sensor_3660.csv'

        #jetzt versuchen wir die Daten zu importieren. 
        #Falls beim entsprechenden Datum keine Daten verfügbar sind,
        #würde das Ganze abstürzen. Um das zu verhindern, packen wir das
        #in ein try except Konstrukt rein.
        try:
            #ein Dataframe ist ein pandas Objekt, könnt ihr euch wie eine Tabelle vorstellen
            #in diesen CSV Dateien sind die Datensätze mit einem Semikolon getrennt, deswegen
            #geben wir das unten bei sep an. Wären die mit Komma getrennt, entsprechend ein Komma
            sds_dataframe = pd.read_csv(sds_url, sep=";")
            #Damit wir eine saubere Tabelle haben, droppen wir die leeren Spalten
            sds_dataframe.dropna(how='all', axis=1, inplace=True)

            #dieser Befehl legt mittels der Daten nun automatisch eine Tabelle "sds_sensor" an
            #falls die Tabelle existiert, fügt er nur Daten hinzu
            sds_dataframe.to_sql("sds_sensor", connection, if_exists="append")
            print(sds_dataframe)
        except:
            print(f"could not read data for {formated_date}")

        #das gleiche noch mal für den dht
        try:
            dht_dataframe = pd.read_csv(dht_url, sep=";")
            dht_dataframe.dropna(how='all', axis=1, inplace=True)

            dht_dataframe.to_sql("dht_sensor", connection, if_exists="append")
        except:
            print(f"could not read data for {formated_date}")
        #WICHTIG!!! Durch diese Methode gibt keinen direkten Primary Key
        #wir haben für jeden Datensatz einen eigenen Index vom Typ Integer

#Mit dieser Funktion könnt ihr alle Daten für einen Sensor ausgeben
def show_data(sensor):
    connection = create_connection("airquality.db")
    cursor = connection.cursor()

    cursor.execute(f'''SELECT * FROM {sensor}''')
    
    for row in cursor.fetchall():
        print(row)

if __name__ == '__main__':
    import_data(5)
    show_data("dht_sensor")
    show_data("sds_sensor")
    