# N.A.V.R.A.A.H: Navigation Assistant for Visually Restricted and Aided Humans

**N.A.V.R.A.A.H** is a wearable intelligent navigation assistant designed as a clip-on device (AI pin form factor) that continuously observes the environment to help users move safely and confidently. It is designed to solve the "last-meter" navigation challenges by providing real-time situational awareness.

---

## 🎯 Project Vision & Goals
*   **Environmental Context**: Unlike traditional white canes, N.A.V.R.A.A.H identifies *what* an obstacle is (e.g., a chair vs. a person).
*   **Proactive Guidance**: Provides directional instructions to help users navigate around obstacles.
*   **Offline Reliability**: All processing occurs locally on the Raspberry Pi Zero 2 W, ensuring it works without an internet connection.
*   **Independence**: Enhances user independence and safety in both familiar and dynamic environments.

---

## 🏗️ System Architecture
The device operates using a three-layer processing flow to ensure real-time feedback:

### **Input Layer**
*   **Camera**: Captures live video frames for visual recognition.
*   **Sensors**: Ultrasonic (HC-SR04) or Time-of-Flight (ToF) sensors measure precise distances to obstacles.

### **Processing Layer**
*   **Main Brain**: Raspberry Pi Zero 2 W running Raspberry Pi OS.
*   **Computer Vision**: OpenCV processes images, while TensorFlow Lite runs lightweight object detection models (e.g., SSD MobileNet).
*   **Logic**: A modular Python-based loop that fuses sensor data with AI context.

### **Output Layer**
*   **Audio Alerts**: Spoken instructions and distance information via `pyttsx3`.
*   **Haptic Feedback**: A vibration motor provides immediate tactile alerts for immediate danger (distance < 50cm).

---

## 🛠️ Hardware Specifications
| Component | Description & Purpose |
| :--- | :--- |
| **Raspberry Pi Zero 2 W** | Executes Python code and AI models in a compact form factor. |
| **RPi Camera Module** | Provides visual feed for identifying objects. |
| **HC-SR04 / VL53L0X** | Distance sensors for fast obstacle proximity detection. |
| **Vibration Motor** | Provides immediate tactile warnings for high-risk obstacles. |
| **Power System** | 3.7V Li-ion battery with a TP4056 charging/protection module. |
| **Audio Alert System** | Buzzer and Audio Amplifier/Earphones for voice guidance. |

---

## 💻 Software Stack
*   **Operating System**: Raspberry Pi OS
*   **Language**: Python 3.x
*   **Vision/AI**: OpenCV & TensorFlow Lite (TFLite)
*   **Audio**: Offline Text-to-Speech (TTS) via `pyttsx3`

---

## 🚦 Operational Logic
The system follows a continuous sensing loop:
1.  **Initialize**: Load hardware drivers and TFLite models.
2.  **Sense**: Measure distance using the ultrasonic sensor.
3.  **Analyze**: Capture camera frame and detect objects if an obstacle is approaching.
4.  **Decide**: 
    *   **Danger (< 50cm)**: Trigger full vibration + "Stop! Obstacle very close".
    *   **Warning (< 100cm)**: Voice alert "Obstacle ahead" + specific object labels (e.g., "Detected: chair").
5.  **Feedback**: Deliver synchronized audio and haptic alerts.

---

## 🗺️ Implementation Roadmap
*   **Phase 1**: Pi setup, camera testing, and audio output. (Completed)
*   **Phase 2**: Distance sensor integration and vibration alerts. (Completed)
*   **Phase 3**: TensorFlow Lite object detection implementation. (Completed)
*   **Phase 4**: Fusion of detection and distance for smart guidance. (Completed)
*   **Phase 5**: Caretaker-assisted milestone navigation and field testing. (Upcoming)

---

## ⚠️ Safety and Limitations
*   **Auxiliary Aid**: This device is a supplement to, not a replacement for, the white cane.
*   **Environmental Factors**: Accuracy may drop in low-light conditions or extremely crowded environments.
*   **Privacy**: The system processes all video locally and does not store images to respect user and public privacy.
*   **Hardware Limits**: AI inference speed is optimized for the Raspberry Pi Zero 2 W but may have slight latency compared to high-end hardware.