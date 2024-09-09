from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from air_sensor import AirSensor
from distance_sensor import DistanceSensor
from light_sensor import LightSensor
from motion_sensor import MotionSensor
from sound_sensor import SoundSensor

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
                        
def main():
    webserver = HTTPServer(('0.0.0.0', 8080), Server)
    print('Web Server starting...')

    try:
        webserver.serve_forever()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()