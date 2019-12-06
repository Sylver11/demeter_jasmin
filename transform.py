"""All communication with io
goes through here.
"""

import database_io

def update_env_settings():
    min_temperature, max_temperature = database_io.read_temperature_settings() 
    start, stop = database_io.read_light_settings()
    return min_temperature, max_temperature, start, stop 

def display_light_settings_views():
    start, stop = database_io.read_light_settings()
    return start, stop


def update_environment_values_views():
    temperature, humidity, pressure, moisture, datetime = database_io.read_environment_values_from_database()
    return temperature, humidity, pressure, moisture, datetime 



