# N.A.V.R.A.A.H
**Navigation Assistant for Visually Restricted And Aided Humans**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

N.A.V.R.A.A.H is an intelligent assistive navigation system designed to enhance mobility and safety for visually restricted individuals. By integrating computer vision, distance sensors, and audio feedback, this project aims to make navigation and spatial awareness more accessible, helping individuals navigate their environment safely and independently without relying on internet connectivity.

## 👥 Team & Contributions

**Faculty Mentor:** Gaurav Verma

| Team Member | Role |
|-------------|------|
| **Rishita** | Hardware integration and sensor setup |
| **Manas Bhasker** | Camera configuration and OpenCV processing |
| **Harsh Dev Jha** | Machine learning model integration |
| **Ishan Rawat** | Audio output and alert logic |
| **Krishyangi Dixit** | Testing, documentation, and presentation |

## ✨ Features

- **Object Detection**: Identifies common objects such as people, chairs, walls, and stairs using specific ML models.
- **Obstacle Avoidance**: Detects obstacles and measures their distance to the user.
- **Audio Guidance**: Provides real-time spoken navigation instructions (e.g., "Turn left", "Obstacle ahead").
- **Haptic Feedback**: Generates vibration alerts for immediate danger or proximity warnings.
- **Offline Functionality**: Designed to work entirely offline, ensuring reliability without internet access.
- **Compact Design**: A wearable system built on the Raspberry Pi Zero 2 W platform.

## �️ Hardware Components

- **Processing Unit**: Raspberry Pi Zero 2 W
- **Vision**: Camera Module
- **Sensors**: Ultrasonic Sensor / Laser ToF Sensor
- **Output**: Speaker / Earphones (Audio), Vibration Motor (Haptic)
- **Power**: Li-ion Battery with Charging & Protection Module
- **Storage**: MicroSD Card (16–32 GB)

## 💻 Software Requirements

- **Operating System**: Raspberry Pi OS
- **Language**: Python
- **Computer Vision**: OpenCV
- **Machine Learning**: TensorFlow Lite
- **Audio**: Text-to-Speech (Offline)

## 🚀 Getting Started

*(Instructions for setting up the hardware and software will be added here based on the repository contents)*

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/Inkesk-Dozing/N.A.V.R.A.A.H.git
    cd N.A.V.R.A.A.H
    ```

2.  **Install Dependencies**
    *(Example - ensure you have the required libraries installed on your Raspberry Pi)*
    ```bash
    pip install opencv-python tensorflow-lite generic-sensor-library
    ```

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) to get started.

---
*Submitted in partial fulfillment of the requirement of the degree of Bachelor of Technology in Computer and Software Engineering.*
