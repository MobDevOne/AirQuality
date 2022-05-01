from datetime import datetime, timedelta

import sqlite3
from sqlite3 import Error
from urllib.error import URLError

import pandas as pd
import json

from requests import request


def create_connection(db_file):
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        return connection

    except Error as e:
        print(e)


def get_temperature(date):
    connection = create_connection("airquality.db")
    cursor = connection.cursor()
    try:
        dates = (f"{date}T00:00:00", f"{date}T23:59:59")
        cursor.execute(
            f'SELECT MAX(temperature) as "maximal temperature", MIN(temperature) as "minimal temperature", ROUND(Avg(temperature),1) as "average temperature" FROM dht_sensor WHERE timestamp between ? AND ?', dates)

        temperature_values = cursor.fetchone()
        return {'max': temperature_values[0], 'min': temperature_values[1], 'avg': temperature_values[2]}
    except Error as err:
        print(err)


def get_humidity(date):
    connection = create_connection("airquality.db")
    cursor = connection.cursor()
    try:
        dates = (f"{date}T00:00:00", f"{date}T23:59:59")
        cursor.execute(
            f'SELECT MAX(humidity) as "maximal humidity", MIN(humidity) as "minimal humidity", ROUND(Avg(humidity),1) as "average humidity" FROM dht_sensor WHERE timestamp between ? AND ?', dates)

        humidity_values = cursor.fetchone()
        return {'max': humidity_values[0], 'min': humidity_values[1], 'avg': humidity_values[2]}
    except Error as err:
        print(err)


def get_particle1(date):
    connection = create_connection("airquality.db")
    cursor = connection.cursor()
    try:
        dates = (f"{date}T00:00:00", f"{date}T23:59:59")
        cursor.execute(
            f'SELECT MAX(P1) as "maximal particle size", MIN(P1) as "minimal particle size", ROUND(Avg(P1),0) as "average particle size" FROM sds_sensor WHERE timestamp between ? AND ?', dates)

        particle_values = cursor.fetchone()
        return {'max': particle_values[0], 'min': particle_values[1], 'avg': particle_values[2]}
    except Error as err:
        print(err)


def get_particle2(date):
    connection = create_connection("airquality.db")
    cursor = connection.cursor()
    try:
        dates = (f"{date}T00:00:00", f"{date}T23:59:59")
        cursor.execute(
            f'SELECT MAX(P2) as "maximal particle size", MIN(P2) as "minimal particle size", ROUND(Avg(P2),0) as "average particle size" FROM sds_sensor WHERE timestamp between ? AND ?', dates)

        particle_values = cursor.fetchone()
        return {'max': particle_values[0], 'min': particle_values[1], 'avg': particle_values[2]}
    except Error as err:
        print(err)


def import_data(date, connection):
    sds_url = f'http://archive.sensor.community/{date}/{date}_sds011_sensor_3659.csv'

    dht_url = f'http://archive.sensor.community/{date}/{date}_dht22_sensor_3660.csv'

    successfull_added = None

    try:
        #reading SDS data
        sds_dataframe = pd.read_csv(sds_url, sep=";")

        sds_dataframe.dropna(how='all', axis=1, inplace=True)

        sds_dataframe.to_sql("sds_sensor", connection, if_exists="append")

        #reading DHT data
        dht_dataframe = pd.read_csv(dht_url, sep=";")

        dht_dataframe.dropna(how='all', axis=1, inplace=True)

        dht_dataframe.to_sql("dht_sensor", connection, if_exists="append")

        successfull_added = date

    except Error as e:
        print(e)

    except URLError as url_error:
        print(f"could not read data for {date}: {url_error}")

    except:
        print(f"could not read data for {date}")

    finally:
        return successfull_added


def auto_load():
    print("loading data. . .\n")

    #reading config json
    try:
        with open("config.json", "r") as config_file:
            config = json.load(config_file)
            delta = datetime.now() - datetime.strptime(config["latest"], "%Y-%m-%d")
            period = int(delta.days)

    except json.JSONDecodeError as decodeError:
        print(
            f"an decode error occured while reading config file: {decodeError}")

    except Exception as ex:
        print(f"failed to load config: {ex}")


    loaded_dates = []
    failed_dates = []

    if(period > 1):
        connection = create_connection("airquality.db")

        for amount_days in range(period):
            requested_date = datetime.now() - timedelta(days=amount_days)
            formated_date = requested_date.strftime("%Y-%m-%d")

            successfull_loaded_date = import_data(formated_date, connection)

            if successfull_loaded_date != None:
                loaded_dates.append(successfull_loaded_date)

                if successfull_loaded_date in config["not_found"]:
                    config["not_found"].remove(successfull_loaded_date)
            else:
                failed_dates.append(formated_date)

        if(len(loaded_dates) > 0):
            print(f"successfully loaded {len(loaded_dates)} days.")

        #save latest date and failed dates to json file
        config.update({"latest": loaded_dates[0]})

        temp = list(dict.fromkeys(config["not_found"] + failed_dates))
        config.update({"not_found": temp})

        try:
            if(len(loaded_dates) > 0):
                with open("config.json", "w") as config_file:
                    json.dump(config, config_file, indent=4, sort_keys=True)

        except Exception as ex:
            print(f"failed to save latest day: {ex}")
    else:
            print("everything up to date.\n")

def read_date():
    print("please enter...")
    year = str(input("+ year: "))
    month = str(input("+ month: "))
    day = str(input("+ day: "))

    #formating months and days if necessary 
    if len(month) == 1:
          month = "0" + month
    if len(day) == 1:
        day = "0" + day

    return f"{year}-{month}-{day}"

if __name__ == '__main__':
    auto_load()
    
    request_date = read_date()

    while(True):
        print("\n1 temperature | 2 humidity | 3 particles | 0 exit")
        mode = int(input("enter number to get values for: "))

        if (mode == 1):
            temp_data = get_temperature(request_date)
            print(f'Temperature values for {request_date}:')
            print(f"+ maximal temperature:\t{temp_data['max']} °C")
            print(f"+ minimal temperature:\t{temp_data['min']} °C")
            print(f"+ average temperature:\t{temp_data['avg']} °C")
        
        elif (mode == 2):    
            humid_data = get_humidity(request_date)
            print(f'Humidity values for {request_date}:')
            print(f"+ maximal amount:\t{humid_data['max']} %")
            print(f"+ minimal amount:\t{humid_data['min']} %")
            print(f"+ average amount:\t{humid_data['avg']} %")
        
        elif (mode == 3):
            part1_data = get_particle1(request_date)
            print(f'Particle (P1) values for {request_date}:')
            print(f"+ maximal amount:\t{part1_data['max']} nm")
            print(f"+ minimal amount:\t{part1_data['min']} nm")
            print(f"+ average amount:\t{part1_data['avg']} nm\n")
            
            part2_data = get_particle2(request_date)
            print(f'Particle (P2) values for {request_date}:')
            print(f"+ maximal amount:\t{part2_data['max']} nm")
            print(f"+ minimal amount:\t{part2_data['min']} nm")
            print(f"+ average amount:\t{part2_data['avg']} nm")
        
        elif (mode == 0):
            break
        else:
            print("not a valid input.")
        
