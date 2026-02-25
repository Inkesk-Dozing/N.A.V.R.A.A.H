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
            # Only log/alert distance if mock alerts are enabled OR real sensor is present
            if not config.TEST_MODE or config.ENABLE_MOCK_ALERTS:
                logger.info(f"Distance: {distance} cm")
                if distance < config.DANGER_DISTANCE:
                    logger.warning("!!! DANGER: OBSTACLE CLOSE !!!")
                    feedback.alert(config.MSG_DANGER, vibrate=True)
                elif distance < config.WARNING_DISTANCE:
                    feedback.alert(config.MSG_OBSTACLE_AHEAD)
                else:
                    feedback.stop()
            
            # 2. Vision Check (Real-time Camera)
            frame = vision.get_frame()
            if frame is not None:
                objects = vision.detect(frame)
                if objects:
                    obj_msg = f"In front: {', '.join(objects)}"
                    logger.info(obj_msg)
                    feedback.alert(obj_msg)
            
            time.sleep(config.LOOP_DELAY)
            
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        feedback.stop()
        vision.release()
        try:
            import RPi.GPIO as GPIO
            GPIO.cleanup()
        except:
            pass

if __name__ == "__main__":
    main()
