from http.server import BaseHTTPRequestHandler, HTTPServer

import RPi.GPIO as GPIO
import dht11

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# read data using pin 14
instance = dht11.DHT11(pin = 4)

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        result = instance.read()

        while not result.is_valid():  # read until valid values
            result = instance.read()

        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()

        self.wfile.write(f'Temp: {result.temperature}\nHumi: {result.humidity}'.encode())

def main():
    webserver = HTTPServer(('0.0.0.0', 8080), Server)
    print('Web Server starting...')

    try:
        webserver.serve_forever()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()