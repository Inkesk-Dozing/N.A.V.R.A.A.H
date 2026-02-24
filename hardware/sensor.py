import time
import random
from hardware.hardware_base import BaseSensor
import config

try:
    if not config.TEST_MODE:
        import RPi.GPIO as GPIO
    else:
        GPIO = None
except ImportError:
    GPIO = None

class UltrasonicSensor(BaseSensor):
    def __init__(self, trig=config.TRIG_PIN, echo=config.ECHO_PIN):
        self.trig = trig
        self.echo = echo
        if not config.TEST_MODE and GPIO:
            GPIO.setup(self.trig, GPIO.OUT)
            GPIO.setup(self.echo, GPIO.IN)

    def read(self):
        if config.TEST_MODE or not GPIO:
            # Simulate distance: 20cm to 200cm
            return round(random.uniform(20.0, 200.0), 2)
        
        GPIO.output(self.trig, True)
        time.sleep(0.00001)
        GPIO.output(self.trig, False)

        pulse_start = time.time()
        timeout = pulse_start + 0.1 # 100ms timeout
        
        while GPIO.input(self.echo) == 0:
            pulse_start = time.time()
            if pulse_start > timeout: return 999

        while GPIO.input(self.echo) == 1:
            pulse_end = time.time()
            if pulse_end > timeout: return 999

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        return round(distance, 2)
