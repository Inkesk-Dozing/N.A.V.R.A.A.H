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

## 📚 Documentation & Research
For an in-depth understanding of the system, please refer to the following reports in the `docs/` folder:
- [**Beginner-Friendly Code Explanation**](docs/Code-Explanation.md): A simplified, non-technical overview of how the sensory hardware and priority software work together to solve real-world problems.
- [**Academic Research Paper**](docs/Research-Paper/NAVRAAH_Research_Paper.md): A formal IEEE-format paper detailing the edge computational models, spatial awareness algorithms, and offline feasibility.
- [**Technical Deep Dive**](docs/Technical_Deep_Dive.md): A comprehensive guide to the AI, Computer Vision, and Machine Learning concepts used in this project.
- [**Final Project Status**](docs/Final_Project_Status.md): A summary of the major upgrades and current capabilities.

## ✨ Features

- **Advanced Object Detection**: Identifies **600+ objects** (Stairs, Doors, Traffic Lights, Watches, etc.) using a modernized **YOLOv8-OIV7** engine.
- **Priority Alerts**: Intelligent logic that prioritizes safety-critical items (like stairs) in audio announcements.
- **Obstacle Avoidance**: Ultrasonic monitoring for precise distance measurements.
- **Audio & Haptic Guidance**: Real-time spoken alerts and vibration warnings for immediate danger.
- **Optimized for Windows**: Enhanced with Non-Maximum Suppression (NMS) and Letterboxing for high-stability detection.

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
