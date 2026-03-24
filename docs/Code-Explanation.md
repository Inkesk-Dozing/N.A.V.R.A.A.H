# N.A.V.R.A.A.H: Beginner-Friendly Project Explanation

Welcome to the N.A.V.R.A.A.H project explanation! "NAVRAAH" stands for **Navigation Assistant for Visually Restricted And Aided Humans**. If you are looking at our project and wondering how it works without diving into the complex code, this document is for you.

## 1. The Core Problem
For visually impaired individuals, navigating the world independently is incredibly challenging. Traditional white canes can detect obstacles on the ground (like steps or curbs) but cannot detect things at head-height (like low hanging branches) or tell the user *what* the obstacle is (e.g., distinguishing between a person and a parked car).

## 2. What is NAVRAAH?
NAVRAAH is a smart, wearable assistant. Think of it as a set of "digital eyes" that a visually impaired person can wear. It uses a tiny computer (a Raspberry Pi), a camera, and physical sensors to look at the world, understand what is in front of the user, and speak to them through an earpiece to guide them safely.

## 3. How Does It Work?
The system relies on two main "senses":

### A. The "Touch/Proximity" Sense (Ultrasonic Sensor)
We use an Ultrasonic Sensor (similar to how bats use echolocation) to measure exactly how far away objects are. 
- If an object is extremely close (e.g., less than 50 cm), it triggers an **immediate physical vibration** (Haptic Feedback) and a voice warning: *"Stop! Obstacle very close."* This instinctual vibration allows for instant reaction, faster than processing speech.

### B. The "Sight" Sense (Computer Vision Camera)
While the sensor tells you *how far* something is, the camera tells you *what* it is. 
We use a lightweight Artificial Intelligence model (Edge AI) that runs directly on the device. It looks at the camera feed and identifies objects. 

**Intelligent Prioritization:**
Not all objects are equally important. If the camera sees a "car", a "person", and a "potted plant", the user needs to know about the moving car or the person first. 
We wrote a strict **Priority Logic System**:
- Priority 1 (Crucial): Cars, Stairs, Traffic Lights.
- Priority 2 (Important): People, Bicycles, Chairs.
- Priority 3 (Informational): Backpacks, Laptops.

The system sorts everything it sees by these priorities and only tells the user about the most dangerous/important items first.

**Directional Awareness & Scene Memory:**
Instead of just shouting "Person!", the math in our code splits the camera frame into three zones. It tells the user: *"Person on your left."* 
Furthermore, to avoid annoying the user by repeating "Person on your left" every second, we built a **Scene Memory Caching System**. If the system warns you about a person, it "remembers" that it told you and stays quiet about that specific person for a few seconds to prevent audio fatigue.

## 4. The Engineering: Text-to-Speech Queue
One major challenge in assistive tech is "Audio Lag." If the camera sees 10 objects rapidly, standard text-to-speech engines will queue them all up. By the time it announces the 10th object, the user might have already walked past it!

To fix this, we engineered a **Multithreaded Audio Queue with a Drop-Stale mechanic**. We limit our audio queue to strictly 2 messages. If the queue is full and a *new* object appears, the code instantly deletes the oldest, stale message and inserts the new one. This ensures the user is **always** hearing real-time, current information about their environment, rather than a backlog of history.

## 5. Why is this project impactful?
NAVRAAH doesn't rely on the cloud or internet connection—everything runs entirely offline on the device ("Edge Deployment"). By combining physical distance sensors for instant reaction, with intelligent, prioritized AI vision for context, NAVRAAH offers a comprehensive, affordable, and practical step forward in assistive mobility technology.
