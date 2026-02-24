import pyttsx3
import config
from hardware.hardware_base import BaseFeedback

try:
    if not config.TEST_MODE:
        import RPi.GPIO as GPIO
    else:
        GPIO = None
except ImportError:
    GPIO = None

class FeedbackSystem(BaseFeedback):
    def __init__(self):
        # Initialize TTS
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', config.TTS_RATE)
        self.engine.setProperty('volume', config.TTS_VOLUME)
        
        # Initialize Vibration Motor Pin
        self.vibe_pin = config.VIBRATION_PIN
        self.buzzer_pin = config.BUZZER_PIN
        if not config.TEST_MODE and GPIO:
            GPIO.setup(self.vibe_pin, GPIO.OUT)
            GPIO.setup(self.buzzer_pin, GPIO.OUT)

    def alert(self, message=None, vibrate=False):
        if message:
            print(f"[AUDIO ALERT] {message}")
            self.engine.say(message)
            self.engine.runAndWait()
        
        if vibrate:
            print("[HAPTIC ALERT] Vibrating...")
            if not config.TEST_MODE and GPIO:
                GPIO.output(self.vibe_pin, True)
                GPIO.output(self.buzzer_pin, True)

    def stop(self):
        if not config.TEST_MODE and GPIO:
            GPIO.output(self.vibe_pin, False)
            GPIO.output(self.buzzer_pin, False)
