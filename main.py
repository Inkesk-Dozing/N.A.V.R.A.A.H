import time
import logging
import config
from hardware.sensor import UltrasonicSensor
from hardware.vision import VisionSystem
from hardware.feedback import FeedbackSystem

# Setup Logging
logging.basicConfig(level=config.LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("Initializing N.A.V.R.A.A.H...")
    
    # Initialize Hardware
    sensor = UltrasonicSensor()
    vision = VisionSystem()
    feedback = FeedbackSystem()
    
    if config.TEST_MODE:
        logger.info("RUNNING IN TEST MODE (MOCKED HARDWARE)")
    
    try:
        while True:
            # 1. Distance Check
            distance = sensor.read()
            logger.info(f"Distance: {distance} cm")
            
            # 2. Logic & Alerts
            if distance < config.DANGER_DISTANCE:
                logger.warning("!!! DANGER: OBSTACLE CLOSE !!!")
                feedback.alert(config.MSG_DANGER, vibrate=True)
            elif distance < config.WARNING_DISTANCE:
                logger.info("Warning: Obstacle approaching")
                feedback.alert(config.MSG_OBSTACLE_AHEAD)
            else:
                feedback.stop()
            
            # 3. Vision Check (Periodic)
            frame = vision.get_frame()
            objects = vision.detect(frame)
            if objects:
                obj_msg = f"Detected: {', '.join(objects)}"
                logger.info(obj_msg)
                feedback.alert(obj_msg)
            
            time.sleep(config.LOOP_DELAY)
            
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        feedback.stop()
        # On RPi we would do GPIO.cleanup() here if we imported it
        try:
            import RPi.GPIO as GPIO
            GPIO.cleanup()
        except:
            pass

if __name__ == "__main__":
    main()
