from datetime import datetime, timedelta

import sqlite3
from sqlite3 import Error
from urllib.error import URLError

import pandas as pd
import os
import json
import logging

logger = logging.getLogger()

handler = logging.FileHandler('airquality.log')
format = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S')
handler.setFormatter(format)

logger.addHandler(handler)


def cls():
    os.system('cls' if os.name=='nt' else 'clear')


def create_connection(db_file):
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        return connection

    except Error as e:
        logger.error(e)


def get_date():
    print("please enter...")
    year = str(input("...year > "))
    month = str(input("...month > "))
    if len(month) == 1:
        month = "0" + month
    day = str(input("...day > "))
    if len(day) == 1:
        day = "0" + day
    cls()
    return {'year': year, 'month': month, 'day': day}


def get_temperature(year, month, day):
    connection = create_connection("airquality.db")
    cursor = connection.cursor()

    start = f"{year}-{month}-{day}T00:00:00"
    end =  f"{year}-{month}-{day}T23:59:59"

    try:
        cursor.execute(
            'SELECT MAX(temperature), MIN(temperature), ROUND(Avg(temperature),1) FROM dht_sensor WHERE timestamp between ? AND ?', (start, end))
        
        temperature_values = cursor.fetchone()
        
        return {'max': temperature_values[0],'min': temperature_values[1], 'avg': temperature_values[2]}

    except Error as err:
        logger.error(err)

        return None


def get_particle(year, month, day):
    connection = create_connection("airquality.db")
    cursor = connection.cursor()

    start = f"{year}-{month}-{day}T00:00:00"
    end =  f"{year}-{month}-{day}T23:59:59"
    try:
        cursor.execute(
            'SELECT MAX(P1), MIN(P1), ROUND(Avg(P1),1) FROM sds_sensor WHERE timestamp between ? AND ?', (start, end))

        temperature_values = cursor.fetchone()

        return {'max': temperature_values[0],'min': temperature_values[1], 'avg': temperature_values[2]}

    except Error as err:
        logger.error(err)

        return None

def import_data(date, connection):
    sds_url = f'http://archive.sensor.community/{date}/{date}_sds011_sensor_3659.csv'

    dht_url = f'http://archive.sensor.community/{date}/{date}_dht22_sensor_3660.csv'

    success = None

    try:
        sds_dataframe = pd.read_csv(sds_url, sep=";")

        sds_dataframe.dropna(how='all', axis=1, inplace=True)

        sds_dataframe.to_sql("sds_sensor", connection, if_exists="append")

        dht_dataframe = pd.read_csv(dht_url, sep=";")

        dht_dataframe.dropna(how='all', axis=1, inplace=True)

        dht_dataframe.to_sql("dht_sensor", connection, if_exists="append")

        success = date
    
    except Error as e:
        logger.error(e)

    except URLError as url_error:
        logging.error(
            f"could not read data for {date}: {url_error}")

    except:
        logger.warning(f"could not read data for {date}")

    finally:
        return success


def auto_import():
    print("loading data. . .\n\n\n")

    try:
        with open("config.json", "r") as config_file:
            config = json.load(config_file)
            delta = datetime.now()-datetime.strptime(config["latest"],"%Y-%m-%d")
            period = int(delta.days)

    except json.JSONDecodeError as decodeError:
        logging.error(f"an decode error occured while reading config file: {decodeError}")

    except Exception as ex:
        logging.exception(f"failed to load config: {ex}")

    loaded_days = []

    if(period>=2):     
        connection = create_connection("airquality.db")
        for amount_days in range(period):
            requested_date = datetime.now()-timedelta(days=amount_days)
            formated_date = requested_date.strftime("%Y-%m-%d")

            tmp = import_data(formated_date, connection)

            if tmp != None:
                loaded_days.append(tmp)

            printProgressBar(amount_days, delta.days, prefix = 'Progress:', suffix = 'Complete', length = 50)

    #save latest date to json file
    try:
        if(len(loaded_days)>0):
            with open("config.json", "w") as config_file:
                json.dump({"latest": loaded_days[0]}, config_file)

    except Exception as ex:
        logging.exception(f"failed to save latest day: {ex}")

    print("\n")
    cls()

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)

    if iteration == total: 
        print("\n")


def menu():
    while True:
        cls()
        print("+----------------+------------------+----------+")
        print("| AirQuality menue                             |")
        print("+----------------+------------------+----------+")
        print("| 1: temperature | 2: particle size | 0: exit  |")
        print("+----------------+------------------+----------+\n")

        option = input("Enter number > ")
        
        print("")
        
        if option == "0":
            break
        
        elif option == "1":
            cls()
            
            requested_date = get_date()
            
            temp = get_temperature(requested_date['year'], requested_date['month'], requested_date['day'])
            
            print(f"Temperature values for {requested_date['day']}-{requested_date['month']}-{requested_date['year']}:")
            print(f"+ maximal temperature:\t{temp['max']}")
            print(f"+ minimal temperature:\t{temp['min']}")
            print(f"+ average temperature:\t{temp['avg']}")
        
        elif option == "2":
            cls()
            
            requested_date = get_date()
            
            temp = get_particle(requested_date['year'], requested_date['month'], requested_date['day'])
            
            print(f"Particle (P1) values for {requested_date['day']}-{requested_date['month']}-{requested_date['year']}:")
            print(f"+ maximal amount:\t{temp['max']}")
            print(f"+ minimal amount:\t{temp['min']}")
            print(f"+ average amount:\t{temp['avg']}")
        
        elif option == "import":
            cls()
            
            print("Import day by date:\n")
            
            requested_date = get_date()
            
            connection = create_connection("airquality.db")
            
            import_data(f"{requested_date['year']}-{requested_date['month']}-{requested_date['day']}", connection)
        
        else:
            print("error: please enter a valid menue number")
        
        input("\n\npress enter to continue")


if __name__ == '__main__':
    auto_import()
    menu()