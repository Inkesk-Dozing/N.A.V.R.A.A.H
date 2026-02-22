"""
N.A.V.R.A.A.H - Configuration Settings
=====================================
This file contains all configurable settings for the navigation assistant.
Edit these values to customize the behavior without changing the core code.

Author: N.A.V.R.A.A.H Team
Version: 0.0.1
"""

# =============================================================================
# GPIO Pin Configuration
# =============================================================================
# Ultrasonic Sensor (HC-SR04)
TRIG_PIN = 23  # Trigger pin
ECHO_PIN = 24  # Echo pin

# Output devices
BUZZER_PIN = 18      # Buzzer pin for audio alert
VIBRATION_PIN = 25   # Vibration motor pin

# =============================================================================
# Distance Settings (in centimeters)
# =============================================================================
DANGER_DISTANCE = 70          # Distance to trigger danger alert (from project-details)
WARNING_DISTANCE = 100        # Distance to trigger warning alert
SAFE_DISTANCE = 150           # Distance considered saf
# =============================================================================
# Camera Settings
# =============================================================================
CAMERA_RESOLUTION = (640, 480)  # (width, height)
CAMERA_FRAMERATE = 30            # Frames per second
CAMERA_WARMUP_TIME = 2           # Seconds to wait for camera to warm up

# =============================================================================
# Audio Settings (Text-to-Speech)
# =============================================================================
TTS_RATE = 150           # Speech rate (words per minute)
TTS_VOLUME = 1.0         # Volume (0.0 to 1.0)
TTS_VOICE_ID = None      # None for default, or specify voice ID

# Audio messages
MSG_OBSTACLE_AHEAD = "Obstacle ahead"
MSG_STOP = "Stop"
MSG_MOVE_RIGHT = "Move slightly right"
MSG_MOVE_LEFT = "Move slightly left"
MSG_CLEAR = "Path clear"
MSG_DISTANCE_FORMAT = "{distance} centimeters"

# =============================================================================
# Vibration/Buzzer Settings
# =============================================================================
VIBRATION_DURATION = 0.5     # Duration of vibration in seconds
BUZZER_DURATION = 0.5       # Duration of buzzer in seconds

# =============================================================================
# Main Loop Settings
# =============================================================================
LOOP_DELAY = 0.05           # Delay between cycles (seconds) - ~20 times/sec
                            # Set to 0.05 for ~20fps, 0.1 for ~10fps

# =============================================================================
# Logging Settings
# =============================================================================
LOG_LEVEL = "INFO"           # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# =============================================================================
# Safety Settings
# =============================================================================
ENABLE_SAFE_MODE = True     # Enable additional safety checks
TEST_MODE = False            # If True, don't activate hardware (for testing)
