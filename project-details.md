# N.A.V.R.A.A.H 🕶️🔊
**Navigation Assistant for Visually Restricted And Aided Humans**

### 🌟 Project Vision
[cite_start]N.A.V.R.A.A.H is an IoT-based intelligent assistive system designed to solve the "last-meter" navigation challenges faced by visually impaired individuals[cite: 60, 104]. [cite_start]Unlike traditional white canes, this wearable provides environmental context, object identification, and proactive directional guidance[cite: 103, 105].

---

## 🎯 The Scope & Need
### Why N.A.V.R.A.A.H?
* [cite_start]**Problem:** Conventional aids are reactive and provide no information about *what* an obstacle is (e.g., a chair vs. a person)[cite: 103, 115].
* [cite_start]**Solution:** An affordable, portable device that uses AI and sensors to give users real-time situational awareness without needing the internet[cite: 111, 117].
* [cite_start]**Goal:** Enhance user independence and safety in both familiar and dynamic environments[cite: 112].

### Core Functionality
- [cite_start]**Real-time Object Detection:** Identifies people, stairs, and furniture[cite: 121, 143].
- [cite_start]**Distance Measurement:** High-precision proximity sensing via Ultrasonic/ToF sensors[cite: 135, 144].
- [cite_start]**Dual-Mode Feedback:** Spoken instructions for context and haptic (vibration) alerts for immediate danger[cite: 126, 131].
- [cite_start]**Offline Reliability:** All processing occurs locally on the Raspberry Pi Zero 2 W[cite: 106, 130].

---

## 🛠️ Technical Specifications

### Hardware List (Procurement Status: In Progress)
* [cite_start]**Compute:** Raspberry Pi Zero 2 W [cite: 135]
* [cite_start]**Vision:** RPi Camera Module [cite: 135]
- [cite_start]**Sensing:** HC-SR04 Ultrasonic Sensor or VL53L0X ToF [cite: 135]
- [cite_start]**Alerts:** Vibration Motor + Audio Amplifier/Earphones [cite: 135]
- [cite_start]**Power:** 3.7V Li-ion Battery with TP4056 Protection Module [cite: 135]

### Software Stack
- [cite_start]**OS:** Raspberry Pi OS [cite: 140]
- [cite_start]**Logic:** Python 3.x [cite: 140]
- [cite_start]**Vision/AI:** OpenCV & TensorFlow Lite [cite: 140]
- [cite_start]**Audio:** Offline Text-to-Speech (TTS) [cite: 140]

---

## 💻 Primary Implementation (`main.py`)

```python
# Simplified Logic for Team-A Prototype
import cv2
import pyttsx3
import RPi.GPIO as GPIO
from tflite_runtime.interpreter import Interpreter

# Initialize GPIO (Assigned to Rishita)
GPIO.setmode(GPIO.BCM)
TRIG, ECHO, MOTOR = 23, 24, 18
GPIO.setup([TRIG, MOTOR], GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Initialize Audio (Assigned to Ishan)
engine = pyttsx3.init()

# ML Model Loading (Assigned to Harsh)
interpreter = Interpreter(model_path="models/detect.tflite")
interpreter.allocate_tensors()

try:
    cap = cv2.VideoCapture(0) # Assigned to Manas
    while True:
        ret, frame = cap.read()
        # Logic: Combine Sensor Distance + AI Detection here
        # If distance < threshold: Trigger Vibration + Voice Alert
        pass
finally:
    GPIO.cleanup()
```
