from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time
import threading
from air_sensor import AirSensor
from distance_sensor import DistanceSensor
from light_sensor import LightSensor
from motion_sensor import MotionSensor
from sound_sensor import SoundSensor

import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, reason_code, properties):
    print(f'Connected to MQTT Broker with result {reason_code}')

def on_message(client, userdata, msg: object):
    print(msg.topic + ' ' + str(msg.payload))

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect('pedropi', 1883, 60)

# read data using pin 14
lightSensor = LightSensor()
airSensor = AirSensor()
distanceSensor = DistanceSensor()
motionSensor = MotionSensor()
soundSensor = SoundSensor()

class Server(BaseHTTPRequestHandler):
    def sendJSON(self, object: object, code: int = 200):
            self.send_response(code)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            self.wfile.write(json.dumps(object).encode())
    
    def do_GET(self):
        if(self.path == '/air'):
            airResult = airSensor.read()
            self.sendJSON({
                'temperature' : airResult.temperature,
                'humidity': airResult.humidity
            })
        
        if(self.path == '/distance'):
            self.sendJSON({
                'distance': distanceSensor.read()
            })
            
        if(self.path == '/light'):
            self.sendJSON({
                'light': lightSensor.read()
            })
            
        if(self.path == '/motion'):
            self.sendJSON({
                'moving' : motionSensor.read()
            })
            
        if(self.path == '/sound'):
            self.sendJSON({
                'sound': soundSensor.read()
            })
            
        if self.path == '/metrics':
            airResult = airSensor.read()
            response = f'\
# HELP light measured light intensity in lux\n\
# TYPE light gauge\n\
light {lightSensor.read()}\n\
# HELP air_temperature measured temperature in celcius\n\
# TYPE air_temperature gauge\n\
air_temperature {airResult.temperature}\n\
# HELP air_humidity measured humidity in percent\n\
# TYPE air_humidity gauge\n\
air_humidity {airResult.humidity}'
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(response.encode())
                        
                        
def read_distance_sensor(sleep: float):
    while True:
        distance = distanceSensor.read()
        mqtt_client.publish('pedropi/distance', distance, qos=2)
        time.sleep(sleep)
                                

def main():
    webserver = HTTPServer(('0.0.0.0', 8080), Server)
    print('Web Server starting...')
    
    distanceSensorThread = threading.Thread(target=read_distance_sensor, args=(0.5,), daemon=True)
    distanceSensorThread.start()

    try:
        mqtt_client.loop_start()
        mqtt_client.publish('pedropi/up', 'true', qos=2)
        webserver.serve_forever()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()