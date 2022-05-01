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

def show_temperature(date):
    connection = create_connection("airquality.db")
    cursor = connection.cursor()
    try:
        cursor.execute(f'SELECT MAX(temperature) as "maximal temperature", MIN(temperature) as "minimal temperature", ROUND(Avg(temperature),1) as "average temperature" FROM dht_sensor WHERE timestamp between "{date["year"]}-{date["month"]}-{date["day"]}T00:00:00" AND "{date["year"]}-{date["month"]}-{date["day"]}T23:59:59"')
    
        temperature_values = cursor.fetchone()
        return {'max': temperature_values[0],'min': temperature_values[1], 'avg': temperature_values[2]}
    except Error as err:
        print(err)

def show_humidity(date):
    connection = create_connection("airquality.db")
    cursor = connection.cursor()
    try:
        cursor.execute(f'SELECT MAX(humidity) as "maximal humidity", MIN(humidity) as "minimal humidity", ROUND(Avg(humidity),1) as "average humidity" FROM dht_sensor WHERE timestamp between "{date["year"]}-{date["month"]}-{date["day"]}T00:00:00" AND "{date["year"]}-{date["month"]}-{date["day"]}T23:59:59"')
    
        humidity_values = cursor.fetchone()
        return {'max': humidity_values[0],'min':humidity_values[1], 'avg': humidity_values[2]}
    except Error as err:
        print(err)

def show_particle1(date):
    connection = create_connection("airquality.db")
    cursor = connection.cursor()
    try:
        cursor.execute(f'SELECT MAX(P1) as "maximal particle size", MIN(P1) as "minimal particle size", ROUND(Avg(P1),0) as "average particle size" FROM sds_sensor WHERE timestamp between "{date["year"]}-{date["month"]}-{date["day"]}T00:00:00" AND "{date["year"]}-{date["month"]}-{date["day"]}T23:59:59"')
        
        particle_values = cursor.fetchone()
        return {'max': particle_values[0],'min': particle_values[1], 'avg': particle_values[2]}
    except Error as err:
        print(err)

def show_particle2(date):
    connection = create_connection("airquality.db")
    cursor = connection.cursor()
    try:
        cursor.execute(f'SELECT MAX(P2) as "maximal particle size", MIN(P2) as "minimal particle size", ROUND(Avg(P2),0) as "average particle size" FROM sds_sensor WHERE timestamp between "{date["year"]}-{date["month"]}-{date["day"]}T00:00:00" AND "{date["year"]}-{date["month"]}-{date["day"]}T23:59:59"')
        
        particle_values = cursor.fetchone()
        return {'max': particle_values[0],'min': particle_values[1], 'avg': particle_values[2]}
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
    #import_data(21) 
    request_date = {
        "year": str(input("Geben Sie das Jahr ein: ")),
        "month": str(input("Geben Sie den Monat ein: ")),
        "day": str(input("Geben Sie den Tag ein: "))
    }
    if len(request_date["month"]) == 1:
          request_date["month"] = "0" + request_date["month"]
    if len(request_date["day"]) == 1:
        request_date["day"] = "0" + request_date["day"]
    
    print("1 für Temperatur | 2 für Luftfeuchtigkeit | 3 für für Feinstaub")
    print("Welcher Wertetyp? ")
    mode = int(input())
    if (mode == 1):
        temp_data = show_temperature(request_date)
        print(f'Particle (P1) values for {request_date["day"]}-{request_date["month"]}-{request_date["year"]}:')
        print(f"+ maximal temperature:\t{temp_data['max']} °C")
        print(f"+ minimal temperature:\t{temp_data['min']} °C")
        print(f"+ average temperature:\t{temp_data['avg']} °C")
    elif (mode == 2):    
        humid_data = show_humidity(request_date)
        print(f'Particle (P1) values for {request_date["day"]}-{request_date["month"]}-{request_date["year"]}:')
        print(f"+ maximal amount:\t{humid_data['max']} %")
        print(f"+ minimal amount:\t{humid_data['min']} %")
        print(f"+ average amount:\t{humid_data['avg']} %")
    elif (mode == 3):
        part1_data = show_particle1(request_date)
        print(f'Particle (P1) values for {request_date["day"]}-{request_date["month"]}-{request_date["year"]}:')
        print(f"+ maximal amount:\t{part1_data['max']} nm")
        print(f"+ minimal amount:\t{part1_data['min']} nm")
        print(f"+ average amount:\t{part1_data['avg']} nm\n")
        part2_data = show_particle1(request_date)
        print(f'Particle (P1) values for {request_date["day"]}-{request_date["month"]}-{request_date["year"]}:')
        print(f"+ maximal amount:\t{part2_data['max']} nm")
        print(f"+ minimal amount:\t{part2_data['min']} nm")
        print(f"+ average amount:\t{part2_data['avg']} nm")
    
    else:
        print("Keine gültige Eingabe.")
    

    
