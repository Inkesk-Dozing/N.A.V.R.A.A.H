# N.A.V.R.A.A.H: Technical Deep Dive & Educational Guide

Welcome! This document explains how the **N.A.V.R.A.A.H** project works from the ground up. If you have no background in Computer Vision or Machine Learning, this guide is for you.

---

## 1. The Core Architecture: "Eyes, Brain, and Mouth"
We can think of this project as an artificial being with three main parts:
*   **The Eyes (The Camera)**: Constantly takes pictures and feeds them to the system.
*   **The Brain (The AI Model)**: Analyzes the pictures to figure out what is in them.
*   **The Mouth (Text-to-Speech)**: Tells the user what the brain found.

---

## 2. Component 1: The Eyes (OpenCV)
**What it is**: OpenCV (Open Source Computer Vision Library) is the industry standard for handling images and video.

**How it works**:
Instead of seeing a "video," the computer sees a series of fast-moving still pictures called **"Frames."**
1.  The camera captures a frame.
2.  We use OpenCV to "clean" the frame (resize it, fix colors).
3.  OpenCV then hands that frame to the AI Brain.

---

## 3. Component 2: The Brain (Machine Learning & YOLOv8)
This is where the "magic" happens.

### What is a "Model"?
Think of an AI Model like a **huge book of experiences.** Millions of pictures of "Watches" were shown to a computer, and it learned the patterns (the circles, the straps). When our system sees a new watch, it compares it to that "book" to see if it matches.

### Why YOLOv8?
**YOLO** stands for "You Only Look Once." 
*   **Traditional AI**: Scans a picture bit by bit, which is very slow.
*   **YOLO**: Looks at the *entire* picture in one go. It is incredibly fast, allowing us to detect objects in "Real-Time" (many times every second).

### What is Open Images V7?
The "Dataset." This is the specific collection of 612 objects our AI was trained on. Because we used this dataset, the AI knows what a "Stair" or a "Traffic Light" is, whereas the original prototype only knew "Faces."

---

## 4. Component 3: The Translator (ONNX vs. TensorFlow)
You might have heard of **TensorFlow** (Google's AI engine). 
*   **The Problem**: TensorFlow is "heavy" and hard to set up on some Windows computers.
*   **The Solution (ONNX)**: **Open Neural Network Exchange.** 
Think of ONNX as a **Universal Translator.** We took a model built in a high-tech lab (in TensorFlow/PT) and "translated" it into ONNX format. This makes it light, fast, and able to run natively on your laptop without needing complex software.

---

## 5. Component 4: Advanced Tuning (The "Secret Sauce")
When we first ran the AI, it was confused. We fixed it with two advanced techniques:

### A. Letterboxing (Protecting the Shape)
Cameras are usually "Wide Screen" (Rectangle). But AI Brains prefer "Square" images.
*   **Old Way (Squashing)**: If you force a rectangle into a square, a round "Watch" becomes a tall, thin oval. The AI says "I don't know what that oval is!"
*   **New Way (Letterboxing)**: We add black bars to the top and bottom. The watch stays round. The AI says "Aha! That's a Watch!"

### B. Non-Maximum Suppression (NMS)
AI is often "unsure" and might draw 5 different boxes around one person, guessing "Person, Man, Human, Head, Body." 
**NMS** acts like a **Judge.** It looks at all overlapping guesses and says, "These are all the same thing. I'll combine them into the single most certain answer." This stops the system from shouting five things for one object.

---

## 6. Component 5: The Safety Net (Ultrasonic Sensors)
AI can be fooled by shadows or photos. That’s why we have **Ultrasonic Sensors.**
*   **How it works**: It sends out a high-pitched sound wave (like a bat).
*   **The Math**: It measures how long the sound takes to bounce back.
*   **The Result**: It knows *exactly* how many centimeters away an obstacle is. This is the primary safety layer—if you are 50cm from a wall, the AI doesn't matter; the sensor will trigger a "Stop!" alert.

---

## 7. Component 6: The Voice (TTS)
We use a **TTS (Text-to-Speech) engine.**
1.  The AI gives us a list: `['Stairs', 'Door']`.
2.  We turn that into a sentence: `"In front: Stairs, Door"`.
3.  The computer speaks it through the speakers.

---

## Summary of our Work
1.  **Stage 1: The Upgrade**: Switched from 1 object (Face) to 600+ objects (YOLOv8-OIV7).
2.  **Stage 2: Stability**: Implemented Letterboxing and NMS so the AI doesn't get "confused" by shapes or multiple objects.
3.  **Stage 3: Accessibility**: Added priority logic so "Stairs" are mentioned before "Glasses."
4.  **Stage 4: Cleanup**: Organized the code to be professional and modular.

**You now have a state-of-the-art navigation assistant!**
