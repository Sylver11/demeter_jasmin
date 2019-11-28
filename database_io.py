from db_utils import db_connect
from datetime import datetime
import json
ENVIRONMENT_SETTINGS_TABLE = 'env_settings'

def read_temperature_settings():
    con = db_connect()
    cursor = con.cursor()
    query = f"SELECT * FROM {ENVIRONMENT_SETTINGS_TABLE} WHERE ID = (SELECT Max(ID) FROM {ENVIRONMENT_SETTINGS_TABLE})"
    cursor.execute(query)
    _, min_temperature, max_temperature, _ = cursor.fetchone()
    return min_temperature, max_temperature

def read_light_settings():
    con = db_connect()
    cursor = con.cursor()
    query = f"SELECT * FROM light_settings WHERE ID = (SELECT Max(ID) FROM light_settings)"
    cursor.execute(query)
    _, start, stop, _ = cursor.fetchone()
    return start, stop

def write_temperature_settings_to_database(a,b):
    con = db_connect()
    cur = con.cursor()
    a = int(a.decode('utf-8'))
    b = int(b.decode('utf-8'))
   # env_settings = """
   # CREATE TABLE env_settings (
   # ID INTEGER PRIMARY KEY AUTOINCREMENT,
   # min_temp INT,
   # max_temp INT,
   # datetime TEXT )"""
   # cur.execute(env_settings)
    time = datetime.now().strftime("%B %d, %Y %I:%M%p")
    print(type(time))
    print(type(a))
    query = "INSERT INTO env_settings (min_temp, max_temp, datetime) VALUES (?,?,?);"
    cur.execute(query, (a, b, time))
    con.commit()
    print("temps settings have been written to the database")

def write_light_settings_to_database(a,b):
    con = db_connect()
    cur = con.cursor()     
   # light_settings = """
   # CREATE TABLE light_settings (
   # ID INTEGER PRIMARY KEY AUTOINCREMENT,
   # start CHAR(60),
   # stop CHAR(60),
   # datetime TEXT )"""
   # cur.execute(light_settings)
    time = datetime.now().strftime("%B %d, %Y %I:%M%p")
    print(type(a))
    query = "INSERT INTO light_settings (start, stop, datetime) VALUES (?,?,?);"
    cur.execute(query, (a, b, time))
    con.commit()
    print("light settings have been written to the database")

def write_environment_values_to_database(temperature, humidity, pressure, moisture):
    con = db_connect()
    cur = con.cursor()
   # environment_values = """
   # CREATE TABLE environment_values (
   # ID INTEGER PRIMARY KEY AUTOINCREMENT,
   # temperature SMALLINT,
   # humidity SMALLINT,
   # pressure SMALLINT,
   # moisture SMALLINT,
   # datetime TEXT )"""
   # cur.execute(environment_values)
    time = datetime.now().strftime("%B %d, %Y %I:%M%p")
    print("this is the data which is being wrtiiten to the database")
    print(time)
    query = "INSERT INTO environment_values (temperature, humidity, pressure, moisture, datetime) VALUES (?,?,?,?,DATETIME('now'));"
    cur.execute(query, (temperature, humidity, pressure, moisture))
    con.commit()
    print("environment values have been written to the database")

def read_environment_values_from_database():
    con = db_connect()
    cursor = con.cursor()
    query = f"SELECT * FROM environment_values WHERE ID = (SELECT Max(ID) FROM environment_values)"
    cursor.execute(query)
    _, temperature, humidity, pressure, moisture, _ = cursor.fetchone()
    return temperature, humidity, pressure, moisture

def read_environment_values_from_last_3_days():
    con = db_connect()
    cursor = con.cursor()
    query =  f"SELECT * FROM environment_values WHERE datetime BETWEEN DATETIME('now', '-3 day') AND DATETIME('now')"
    cursor.execute(query)
    records = cursor.fetchall()
    environment_records = []
    for row in records:
        environment_records.append({
                'datatime' : row[1],
                'temperature' : row[5]
                })
    environment_data = json.dumps({'environment_records':environment_records})
    
    return environment_data
    #    print("Id: ", row[0])
    #    print("temperature: ", row[1])
    #    print("humidity: ", row[2])
    #    print("pressure: ", row[3])
    #    print("moisture ", row[4])
    #    print("datetime: ", row[5])
    #    print("\n")
