import sqlite3
from sqlite3 import Cursor, Error

def create_connection(db_file):
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        return connection

    except Error as e:
        print(e)
  
def create_table(connection, statement):
    try:
        cursor = connection.cursor()
        cursor.execute(statement)
    except Error as e:
        print(e)

if __name__ == '__main__':
    create_connection("pythonsqlite.db")