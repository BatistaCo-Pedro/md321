import RPi.GPIO as GPIO

class MotionSensor():
      def __init__(self):
           self.PIN = 16
           GPIO.setmode(GPIO.BOARD) #Die GPIO Boardkonfiguration benutzen.
           GPIO.setup(self.PIN, GPIO.IN)  #Der Pin der Deklarierten Variable wird als Input gesetzt.
           
      def read(self): 
            if(GPIO.input(self.PIN) == 0): # Wenn der Sensor Input = 0 ist
                  return False
            elif(GPIO.input(self.PIN) == 1): # Wenn der Sensor Input = 1 ist
                  return True
