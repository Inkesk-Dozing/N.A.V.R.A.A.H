# N.A.V.R.A.A.H: Navigation Assistant for Visually Restricted and Aided Humans

[cite_start]N.A.V.R.A.A.H is a wearable intelligent navigation assistant designed as a clip-on device (AI pin form factor) that continuously observes the environment to help users move safely and confidently[cite: 1, 6]. [cite_start]It is designed to enhance awareness and independence rather than replace existing aids like the white cane[cite: 8].

---

## 1. System Architecture
[cite_start]The device operates using a three-layer processing flow to ensure real-time feedback[cite: 10, 11]:

### **Input Layer**
* [cite_start]**Camera**: Captures live video frames for visual recognition[cite: 10].
* [cite_start]**Sensors**: Ultrasonic or Time-of-Flight (ToF) sensors measure precise distances to obstacles[cite: 10, 13].

### **Processing Layer**
* [cite_start]**Main Brain**: Raspberry Pi Zero 2 W running Linux[cite: 10, 13].
* [cite_start]**Computer Vision**: OpenCV processes images, while TensorFlow Lite runs object detection models[cite: 10, 17].
* [cite_start]**Logic**: Combines AI context with sensor data to make movement decisions[cite: 10, 20].

### **Output Layer**
* [cite_start]**Audio**: Spoken instructions via speaker or earphones[cite: 10, 13].
* [cite_start]**Haptics**: A vibration motor provides tactile alerts; intensity increases as objects get closer[cite: 10, 15].

---

## 2. Hardware Components
| Component | Description & Purpose |
| :--- | :--- |
| **Raspberry Pi Zero 2 W** | [cite_start]Executes Python code and AI models in a compact form factor[cite: 13]. |
| **Camera Module** | [cite_start]Provides visual feed for identifying objects like chairs, people, or walls[cite: 10, 13]. |
| **Distance Sensor** | [cite_start]HC-SR04 (Ultrasonic) or VL53L0X (ToF) for fast obstacle detection[cite: 13, 14]. |
| **Vibration Motor** | [cite_start]Provides immediate tactile warnings in loud environments[cite: 15]. |
| **Power System** | [cite_start]3.7V Li-ion battery with a TP4056 charging/protection module[cite: 14, 15]. |
| **Audio Driver** | [cite_start]Amplifies signals for clear voice-based navigation[cite: 14]. |



---

## 3. Software Stack
* [cite_start]**Operating System**: Raspberry Pi OS[cite: 17].
* [cite_start]**Language**: Python[cite: 17].
* [cite_start]**AI Model**: Pre-trained lightweight models (e.g., MobileNet SSD) for object labeling[cite: 17].
* [cite_start]**Text-to-Speech**: Offline tools like `pyttsx3` or `eSpeak` to ensure functionality without internet[cite: 8, 17].

---

## 4. Operational Logic & User Experience
[cite_start]The system follows a continuous sensing loop (10–20 times per second)[cite: 19]:
1. [cite_start]**Initialize**: Check hardware and load AI models[cite: 19].
2. [cite_start]**Detect**: Identify objects and calculate their distance[cite: 19].
3. **Decide**: 
    * [cite_start]If distance < 70 cm: Trigger danger alert[cite: 19].
    * [cite_start]If object is centered: Say "Stop"[cite: 19].
    * [cite_start]If object is on left: Say "Move slightly right"[cite: 10, 19].
4. [cite_start]**Feedback**: Deliver short, meaningful voice messages and vibrations[cite: 30, 31].



---

## 5. Implementation Roadmap
* [cite_start]**Phase 1 (Week 1-2)**: Pi setup, camera testing, and audio output[cite: 45].
* [cite_start]**Phase 2 (Week 3-4)**: Distance sensor integration and vibration alerts[cite: 45].
* [cite_start]**Phase 3 (Week 5-6)**: TensorFlow Lite object detection implementation[cite: 45].
* [cite_start]**Phase 4 (Week 7-8)**: Fusion of detection and distance for smart guidance[cite: 45].
* [cite_start]**Phase 5 (Week 9+)**: Caretaker-assisted milestone navigation (Phase 2)[cite: 23, 45].

---

## 6. Safety and Limitations
* [cite_start]**Safety**: Always test with sighted volunteers first; do not store user images to respect privacy[cite: 33].
* [cite_start]**Speed**: The Raspberry Pi Zero has hardware-limited AI inference speeds[cite: 35].
* [cite_start]**Environment**: Accuracy may drop in low-light conditions[cite: 35].
* [cite_start]**Ethics**: The device is a supplement to, not a replacement for, the white cane[cite: 33].