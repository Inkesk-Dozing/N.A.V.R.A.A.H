"""
N.A.V.R.A.A.H - Configuration Settings
=====================================
Centralized configuration for the Navigation Assistant.
"""
import os
import platform

# Detect environment
IS_WINDOWS = platform.system() == "Windows"
TEST_MODE = False  # Toggle this to False to enable real hardware access
ENABLE_REAL_CAMERA = True  # Use the laptop camera
ENABLE_MOCK_ALERTS = True # Keep distance/mock alerts active for testing

# =============================================================================
# GPIO Pin Configuration (BCM)
# =============================================================================
TRIG_PIN = 23
ECHO_PIN = 24
VIBRATION_PIN = 25
BUZZER_PIN = 18

# =============================================================================
# Distance Settings (cm)
# =============================================================================
DANGER_DISTANCE = 50          # Immediate danger (Vibration + Voice)
WARNING_DISTANCE = 100        # Warning (Voice only)
SAFE_DISTANCE = 150           # Safe zone

# =============================================================================
# Camera and AI Settings
# =============================================================================
CAMERA_RESOLUTION = (640, 480)
CAMERA_FRAMERATE = 30
MODEL_PATH = os.path.join("models", "detect.tflite")
LABELS_PATH = os.path.join("models", "labels_oiv7.txt")
CAFFE_PROTOTXT = os.path.join("models", "deploy.prototxt")
CAFFE_MODEL = os.path.join("models", "mobilenet_ssd.caffemodel")
YOLO_MODEL = os.path.join("models", "yolov8n-oiv7.onnx")
CONFIDENCE_THRESHOLD = 0.5

# =============================================================================
# Audio Settings (TTS)
# =============================================================================
TTS_RATE = 150
TTS_VOLUME = 1.0

# Messages
MSG_OBSTACLE_AHEAD = "Obstacle ahead"
MSG_CLEAR = "Path clear"
MSG_DANGER = "Stop! Obstacle very close"

# =============================================================================
# System Settings
# =============================================================================
LOG_LEVEL = "INFO"
LOOP_DELAY = 0.1  # Seconds between loops
