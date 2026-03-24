import pyttsx3
import config
import threading
import queue
import time
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
        # Initialize Threaded TTS
        self.speech_queue = queue.Queue(maxsize=2)
        self.stop_requested = False
        self.worker_thread = threading.Thread(target=self._speech_worker, daemon=True)
        self.worker_thread.start()
        
        # Initialize Vibration Motor Pin
        self.vibe_pin = config.VIBRATION_PIN
        self.buzzer_pin = config.BUZZER_PIN
        if not config.TEST_MODE and GPIO:
            GPIO.setup(self.vibe_pin, GPIO.OUT)
            GPIO.setup(self.buzzer_pin, GPIO.OUT)

    def _speech_worker(self):
        """Background thread that processes the speech queue."""
        # Note: pyttsx3 engine must be in the same thread as runAndWait on some platforms
        engine = pyttsx3.init()
        engine.setProperty('rate', config.TTS_RATE)
        engine.setProperty('volume', config.TTS_VOLUME)
        
        while not self.stop_requested:
            try:
                message = self.speech_queue.get(timeout=0.1)
                if message:
                    engine.say(message)
                    engine.runAndWait()
                self.speech_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"TTS Worker Error: {e}")
                time.sleep(1)

    def alert(self, message=None, vibrate=False):
        if message:
            # message can be a list of detections or a single string
            if isinstance(message, list):
                if not message: return
                if len(message) == 1:
                    full_msg = f"I see a {message[0]}"
                else:
                    items = ", and a ".join([", ".join(message[:-1]), message[-1]])
                    full_msg = f"I see a {items}"
                message = full_msg

            print(f"[AUDIO QUEUED] {message}")
            try:
                self.speech_queue.put_nowait(message)
            except queue.Full:
                try:
                    self.speech_queue.get_nowait() # Remove old stale message
                except queue.Empty:
                    pass
                try:
                    self.speech_queue.put_nowait(message)
                except queue.Full:
                    pass
        
        if vibrate:
            # Vibrate handles INSTANTLY regardless of speech
            print("[HAPTIC ALERT] Vibrating...")
            if not config.TEST_MODE and GPIO:
                GPIO.output(self.vibe_pin, True)
                GPIO.output(self.buzzer_pin, True)

    def stop(self):
        """Standard stop for haptics."""
        if not config.TEST_MODE and GPIO:
            GPIO.output(self.vibe_pin, False)
            GPIO.output(self.buzzer_pin, False)

    def shutdown(self):
        """Stops the speech thread and releases resources."""
        self.stop()
        self.stop_requested = True
        # Put an empty task to unblock the queue.get()
        self.speech_queue.put(None)
        if hasattr(self, 'worker_thread'):
            self.worker_thread.join(timeout=1.0)
        print("Feedback system shutdown complete.")
