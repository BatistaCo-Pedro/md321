import time
import RPi.GPIO as GPIO

class DistanceSensor(): 
    def __init__(self):
        GPIO.setmode(GPIO.BOARD) # Setze die GPIO Boardkonfiguration ein.

        self.TRIG = 36    # Variablendeklaration 
        self.ECHO = 32    # Variablendeklaration

        GPIO.setup(self.TRIG,GPIO.OUT) # Variable TRIG als Output festlegen.
        GPIO.setup( self.ECHO,GPIO.IN)  # Variable ECHO als Input festlegen.

        GPIO.output(self.TRIG, False)
        time.sleep(2) # 2 Sekunden Wartezeit.
        
    def read(self):
        GPIO.output(self.TRIG, True)  # Sendet ein Ultraschallsignal
        time.sleep(0.00001)    
        GPIO.output(self.TRIG, False) # Beendet das senden des Ultraschallsignals

        while GPIO.input( self.ECHO)==0:
            self.pulse_start = time.time()

        while GPIO.input( self.ECHO)==1:
            self.pulse_end = time.time()

        pulse_duration = self.pulse_end - self.pulse_start # Berechnung für die Dauer Des Pulses

        distance = pulse_duration * 17150  # Berechnung zur Bestimmung der Entfernung.

        distance = round(distance, 2)
        
        return distance