# N.A.V.R.A.A.H Project Details
**Navigation Assistant for Visually Restricted and Aided Humans**

N.A.V.R.A.A.H is a wearable intelligent navigation assistant designed as a clip-on device (AI pin form factor) that continuously observes the environment to help users move safely and confidently. It specializes in "last-meter" navigation by providing real-time situational awareness.

---

## 🎯 Project Vision & Goals

* **Environmental Context**: Unlike traditional white canes, N.A.V.R.A.A.H identifies *what* an obstacle is (e.g., stairs vs. a chair).
* **Proactive Guidance**: Provides directional instructions to help users navigate around obstacles.
* **Offline Reliability**: All processing occurs locally, ensuring safety without internet dependency.
* **Independence**: Enhances safety in dynamic environments like busy streets or unfamiliar buildings.

---

## 🏗️ System Architecture

### **Input Layer**
* **Camera**: High-speed frame capture for real-time visual recognition.
* **Sensors**: Ultrasonic distance monitoring (HC-SR04) for secondary safety.

### **Processing Layer**
* **AI Brain**: Modernized **YOLOv8** engine optimized for 600+ object recognition.
* **Universal Translation**: Integration via **ONNX** for high-performance execution on standard hardware.
* **Decision Logic**: Real-time fusion of AI vision context and ultrasonic distance data.

### **Output Layer**
* **Audio Alerts**: Priority-based voice feedback (Safety-critical objects announced first).
* **Haptic Feedback**: Immediate vibration alerts for obstacles within 50cm.

---

## 🛠️ Hardware Specifications

| Component | Purpose |
| :--- | :--- |
| **Microprocessor** | Raspberry Pi Zero 2 W / PC Emulation |
| **Vision Module** | High Definition Camera (USB/CSI) |
| **Proximity Sensors**| Ultrasonic / ToF (Distance Measurement) |
| **Vibration Motor** | Immediate Haptic Danger Alerts |
| **Audio Output** | Text-to-Speech (TTS) via speakers/headphones |

---

## 💻 Software Stack & AI Features

* **YOLOv8 Engine**: Capable of detecting 600+ objects including Stairs, Traffic Lights, and Currency.
* **Stability Suite**: Includes **Letterboxing** (shape preservation) and **Non-Maximum Suppression** (combining overlapping detections).
* **Programming**: Python 3.x using OpenCV DNN and NumPy.
* **Offline TTS**: Local voice generation for instant feedback.

---

## 🚦 Operational Logic

1. **Capture**: Continuously frame-grab from the vision module.
2. **Analyze**: AI Brain identifies objects using 600+ class library.
3. **Prioritize**: Sort detections by safety criticalness (e.g., Stairs > Faces).
4. **Sense**: Simultaneously monitor proximity via ultrasonic sensor.
5. **Alert**: Deliver immediate haptic vibration for danger and spoken alerts for recognized objects.

---

## ⚠️ Safety and Limitations
* **Auxiliary Aid**: Designed to supplement, not replace, traditional mobility aids like white canes.
* **Privacy**: All processing is performed locally; no images or personal data are stored or uploaded.
* **Inference Speed**: Optimized for low-latency feedback in dynamic environments.