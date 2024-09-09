import RPi.GPIO as GPIO

class SoundSensor():
    def __init__(self):
        self.PIN = 18
        
        GPIO.setmode(GPIO.BOARD)
        # sound_pin wird als Eingang festgelegt
        GPIO.setup(self.PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
    def read(self):
        if(GPIO.input(self.PIN) == GPIO.LOW):
            return True
        return False