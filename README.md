# N.A.V.R.A.A.H
### Navigation Assistant Via Real-time Awareness and Audio Help

> A Python project that helps visually impaired people navigate the world around them using a camera and a speaker.

---

## 🧠 What Does This Project Do? (The Big Idea)

Imagine you are blind. You cannot see walls, people, doors, or objects in front of you. This project acts like a pair of **AI-powered eyes with a voice**.

It uses:
- 📷 **A Camera** — to see the world in real time
- 🧠 **An AI Model** — to figure out *what* is in the frame and *where* it is (left, ahead, or right)
- 🔊 **A Speaker** — to say things like *"I see a person on your left and a wall directly ahead"*
- 📳 **A Vibration Motor** — to buzz when something is dangerously close (this runs on a Raspberry Pi with physical hardware)
- 📡 **An Ultrasonic Sensor** — like the reverse sensor in a car, it measures how far away the nearest object is in centimetres

On a **Windows laptop**, you can run and test it using just the built-in camera and speakers — no special hardware needed.

---

## 📁 Project Structure — What Each File Does

```
N.A.V.R.A.A.H/
│
├── main.py              ← The entry point. Run this to start the assistant.
├── config.py            ← All settings in one place (thresholds, pins, flags).
├── test_mocks.py        ← Automated tests to verify everything works.
├── download_model.py    ← Downloads the AI model files automatically.
├── requirements.txt     ← List of Python libraries this project needs.
│
├── hardware/            ← The "organs" of the assistant (each is a Python class)
│   ├── hardware_base.py ← A base class that sensor/vision/feedback all inherit from.
│   ├── sensor.py        ← Reads distance from the ultrasonic sensor (or fakes it).
│   ├── vision.py        ← Reads the camera, runs the AI, returns what it sees.
│   └── feedback.py      ← Says things out loud and controls vibration.
│
└── models/              ← The AI brain files (downloaded, not written by hand)
    ├── yolov8n-oiv7.onnx   ← Main AI model — can recognise 600+ types of objects
    ├── labels_oiv7.txt     ← List of all 600+ object names the AI knows
    └── ...                 ← Backup models (Caffe, TFLite) used if YOLO is missing
```

---

## 🧩 How the Code Is Organised (OOP Explained Simply)

The project uses **classes** — think of each class as a worker with a specific job.

### `UltrasonicSensor` (in `hardware/sensor.py`)
- **Job:** Measure distance to the nearest object.
- **On a Raspberry Pi:** Sends a sound pulse and times how long it takes to come back (like a bat).
- **On Windows:** Returns a random number between 20–200 cm to simulate a sensor (this is called "mocking").

### `VisionSystem` (in `hardware/vision.py`)
- **Job:** Look at the camera feed, run the AI, and return a list like:
  `["person directly ahead", "wall on your left", "clothing on your right"]`
- Uses a pre-trained AI model (YOLOv8) that has already learned what thousands of objects look like.
- Applies several intelligence layers (explained below).

### `FeedbackSystem` (in `hardware/feedback.py`)
- **Job:** Turn the detected object list into spoken words, and trigger vibration.
- Takes `["person directly ahead", "door on your left"]` and says:
  *"I see a person directly ahead and a door on your left"*
- Speech runs in a **separate background thread** so vibration is never delayed by talking.

---

## 🤖 How the AI Vision Works (Step by Step)

When `vision.detect(frame)` is called with one camera image, here is exactly what happens inside:

### Step 1 — Run YOLOv8 (the main AI)
- The camera image is resized to 640×640 pixels and fed into the AI model.
- The AI outputs bounding boxes: rectangles around objects it found, with a confidence score (0.0 to 1.0).
- Only detections above **0.28 confidence** are kept. (Below this is considered unreliable noise.)
- Each detected object's raw AI label (like `"Top, T-shirt, Sweatshirt"`) is translated to a plain name (like `"clothing"`) using a dictionary called `LABEL_MAP`.

### Step 2 — Supplement with Face Detection (Haar Cascade)
- A simpler, faster algorithm specifically for detecting faces is also run.
- If the main AI missed a person, this catches them.
- **Only runs if "person" was not already found** — no double counting.

### Step 3 — Temporal Smoothing (Anti-Flicker)
- A single frame is not trusted immediately.
- The system keeps a history of the **last 5 frames**.
- An object must appear in a minimum number of frames to be confirmed as "really there":
  - **Walls, doors, stairs** → 2 out of 5 frames (they are always present, confirm fast)
  - **People, clothing** → 2 out of 5 frames (important, should not be delayed)
  - **Small items like glasses, coins** → 3 out of 5 frames (prevent false positives)
- This stops the AI from saying random objects that appeared for just one blurry frame.

### Step 4 — Directional Awareness (Left / Ahead / Right)
- Every detected object has a bounding box. The centre X coordinate of that box tells us where it is in the frame.
- The frame is divided into 3 zones:
  ```
  |--- Left ---|--- Ahead ---|--- Right ---|
  0           33%           66%          100%
  ```
- So `"person"` at 20% → `"person on your left"`

### Step 5 — Priority Sorting
- Not everything is equally important for a blind person.
- Objects are sorted by an `ACCESSIBILITY_PRIORITIES` score:
  - `stairs`, `traffic light`, `wall` → Priority 9–10 (spoken first)
  - `person`, `vehicle` → Priority 7–8
  - `clothing`, `glasses` → Priority 5–6
  - `book`, `pen` → Priority 3–4

### Step 6 — Scene Memory (Anti-Repetition)
- If an object was already announced, it is not announced again for a while (cooldown):
  - `wall` → 15 seconds (it is still there, no need to repeat)
  - `stairs`, `door` → 8 seconds
  - `person`, `clothing` → 5 seconds
- This prevents the assistant from being annoying by repeating itself every second.

---

## ⚙️ Settings You Can Change (`config.py`)

| Setting | What it does | Default |
|---|---|---|
| `TEST_MODE` | `True` = use fake sensor data (for laptop testing), `False` = use real hardware | `False` |
| `ENABLE_REAL_CAMERA` | `True` = use your laptop/Pi camera | `True` |
| `DEBUG_VISION` | `True` = draw coloured boxes on screen around detected objects | `True` |
| `DANGER_DISTANCE` | Distance in cm where vibration triggers immediately | `50` |
| `WARNING_DISTANCE` | Distance in cm for a voice warning only | `100` |
| `CONFIDENCE_THRESHOLD` | How certain the AI must be (0.0–1.0) — used by Caffe/TFLite fallback models | `0.5` |
| `LOOP_DELAY` | Seconds between each detection loop (lower = faster but more CPU) | `0.1` |

---

## 🚀 How to Run It (On Your Laptop)

### First Time Setup
```powershell
# 1. Create a virtual environment (an isolated Python box for this project)
python -m venv .venv

# 2. Activate it
.\.venv\Scripts\activate

# 3. Install all required libraries
pip install -r requirements.txt

# 4. Download the AI model
python download_model.py
```

### Run the Tests (Recommended First)
```powershell
python test_mocks.py
```
You should see `OK` at the end. The live camera test will open your webcam for ~8 seconds and print everything it detects.

### Run the Full Assistant
```powershell
python main.py
```
Point your laptop camera at the room — it will start announcing what it sees.

**Press `Ctrl + C`** to stop it cleanly.

---

## 🧪 What Do the Tests Check? (`test_mocks.py`)

| Test Name | What it checks |
|---|---|
| `test_sensor_mock` | Sensor returns a sensible distance number |
| `test_vision_pipeline` | Vision system returns a list even when camera is off |
| `test_mock_passthrough` | Fake object injection works (for simulating specific scenes) |
| `test_feedback_system` | TTS and vibration run without crashing |
| `test_live_camera_realtime` | Opens real camera for 8 seconds and prints everything seen |

---

## 🔌 On a Raspberry Pi (Real Hardware)

On the actual device worn by a visually impaired person:
- The **ultrasonic sensor** (HC-SR04) is wired to GPIO pins 23 (trigger) and 24 (echo).
- A **vibration motor** is on GPIO pin 25.
- A **buzzer** is on GPIO pin 18.
- The **Pi Camera** is connected via the ribbon cable port.
- Set `TEST_MODE = False` in `config.py` to enable all real hardware.

---

## 📦 AI Models Explained Simply

| File | What it is | Size |
|---|---|---|
| `yolov8n-oiv7.onnx` | **Main AI** — knows 600+ objects (OIV7 dataset). Used on Windows/Pi. | 14 MB |
| `mobilenet_ssd.caffemodel` | **Backup AI** — knows 20 objects. Used if YOLO fails. | 23 MB |
| `detect.tflite` | **Lightweight AI** — designed for Raspberry Pi. | 4 MB |
| `labels_oiv7.txt` | Text file listing all 600+ object names in order. | 6 KB |

The system tries them in order: **YOLO → TFLite → Caffe → Haar Cascade (face only)**.

---

## 💡 Glossary (Plain English Definitions)

| Term | Meaning |
|---|---|
| **AI Model** | A file containing millions of learned patterns from training on labelled images. |
| **ONNX** | A universal file format for AI models — works across frameworks. |
| **Bounding Box** | A rectangle the AI draws around a detected object. |
| **Confidence Score** | How sure the AI is (0 = not sure at all, 1.0 = 100% certain). |
| **Thread** | A second task running alongside the main program simultaneously. |
| **GPIO** | General Purpose Input/Output — the physical pins on a Raspberry Pi. |
| **Mock** | Fake data used in tests so you don't need real hardware to test logic. |
| **OIV7** | Open Images V7 — a dataset of 9 million labelled images used to train the AI. |
| **Haar Cascade** | An older, simpler face-detection algorithm built into OpenCV. |
| **Scene Memory** | A dictionary tracking when each object was last announced, to avoid repetition. |

---

*Built for accessibility. Made in Python.*
