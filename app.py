from flask import Flask, render_template, Response, request, session, jsonify
#from camera_pi import Camera
#import serial
import time
#import re
from time import sleep
from datetime import datetime
import struct
import json
import transform
import database_io
import gviz_api
app = Flask(__name__)


#@app.route('/_scheduled_Update')
#def scheduled_Update():
#    getENVdata()
#    return ''
#
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/environment/')
def lights():
    # start, stop= transform.wght_settings_views()
    min_temperature, max_temperature, start, stop = transform.update_env_settings()
    # start = struct.unpack('<H',start)
    env_settings = {
        'start': int(start),
        'stop': int(stop),
        'min_temperature':int(min_temperature),
        'max_temperature':int(max_temperature)
    }
    return render_template('environment.html', env_settings=env_settings)

@app.route('/charts/')
def data():
    return render_template('charts.html')



@app.route('/temperature/')
def temperature():
    return render_template('temperature.html')


@app.route('/feed')
def ENVdata():
    temperature, humidity, pressure, moisture, datetime = transform.update_environment_values_views()
    return jsonify(temperature=temperature, humidity=humidity, pressure=pressure, moisture=moisture, datetime=datetime)

# @app.route('/_display-light')
# def display_light_settings():
#     start, stop = transform.display_light_settings_views()
#     return Response(start, stop)

@app.route('/_temp')
def add_numbers():
    a = bytes(request.args.get('temp', 0, type=str), 'utf-8')
    b = bytes(request.args.get('hum', 0, type=str), 'utf-8')
    database_io.write_temperature_settings_to_database(a, b)
    return Response()

@app.route('/_light')
def set_light_time():
    #capture start stop time and write to the database. 
    a = bytes(request.args.get('start', 0, type=str), 'utf-8')
    b = bytes(request.args.get('stop', 0, type=str), 'utf-8')
   # print(a)
   # print(b)
    database_io.write_light_settings_to_database(a,b)
    return Response()


@app.route('/temps', methods=["GET", "POST"])
def httpTemps():
    min_temperature, max_temperature, start, stop = transform.update_env_settings()
    now = datetime.now()
    print(now)
    current_time = now.strftime("%H")
    print(current_time)
    lights = 0
    if (int(current_time) >= int(start) and int(current_time) < int(stop)):
        lights = 1
        print("lights are being switched on")
    else:
        lights = 0
        print("lights are being switched off")
    content = request.get_json()
   # print(content)
    temperature = content['environment'][0]
    print(temperature)
    humidity = content['environment'][1]
    print(humidity)
    pressure = content['environment'][2]
    print(pressure)
    moisture = content['environment'][3]
    print(moisture)
    if (temperature == ""):
        print("not writing data to database because values are invalid")
    else:
        database_io.write_environment_values_to_database(temperature, humidity, pressure, moisture)
   # print(lights)
    return jsonify(min_temperature=min_temperature,max_temperature= max_temperature,lights=lights)


@app.route('/chart01')
def chart01(): 
    environment_data =  database_io.read_environment_temp_values_from_last_3_days()
    data_table = json.dumps(environment_data)
    return data_table


@app.route('/chart02')
def chart02(): 
    environment_data =  database_io.read_environment_all_values_from_last_1_days()
    data_table = json.dumps(environment_data)
    return data_table


@app.route('/chart03')
def chart03(): 
    environment_data =  database_io.read_environment_all_values_from_last_3_days()
    data_table = json.dumps(environment_data)
    return data_table

@app.route('/chart04')
def chart04(): 
    environment_data =  database_io.read_environment_all_values_from_last_7_days()
    data_table = json.dumps(environment_data)
    return data_table




def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', port =4003, debug=True, threaded=True)
