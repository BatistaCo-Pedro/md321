import RPi.GPIO as GPIO
import dht11

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()

class AirSensor(): 
    def __init__(self):
        self.instance = dht11.DHT11(pin = 7)
        self.result = self.instance.read()
        
    def read(self):
        self.result = self.instance.read()
        
        while not self.result.is_valid():
            self.result = self.instance.read()
            
        return self.result