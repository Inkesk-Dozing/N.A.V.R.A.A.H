''import RPi.GPIO as GPIO
import time
import cv2
import numpy as np
from tflite_runtime.interpreter import Interpreter
import pyttsx3
from picamera import PiCamera
from picamera.array import PiRGBArray

# GPIO pin setup
TRIG = 23  # Ultrasonic sensor trigger pin
ECHO = 24  # Ultrasonic sensor echo pin
BUZZER = 18  # Buzzer pin
VIBRATION = 25  # Vibration motor pin

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.setup(VIBRATION, GPIO.OUT)

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech

# Load TFLite model and labels
MODEL_PATH = 'ssd_mobilenet_v1_1_metadata_1.tflite'  # Download and place in directory
LABELS_PATH = 'labels.txt'  # COCO labels or custom

interpreter = Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load labels
with open(LABELS_PATH, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

# Initialize camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
raw_capture = PiRGBArray(camera, size=(640, 480))

def get_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance

def detect_objects(frame):
    # Preprocess frame
    input_shape = input_details[0]['shape']
    frame_resized = cv2.resize(frame, (input_shape[1], input_shape[2]))
    input_data = np.expand_dims(frame_resized, axis=0).astype(np.uint8)

    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    boxes = interpreter.get_tensor(output_details[0]['index'])[0]
    classes = interpreter.get_tensor(output_details[1]['index'])[0]
    scores = interpreter.get_tensor(output_details[2]['index'])[0]

    detected_objects = []
    for i in range(len(scores)):
        if scores[i] > 0.5:  # Confidence threshold
            class_id = int(classes[i])
            label = labels[class_id] if class_id < len(labels) else 'Unknown'
            detected_objects.append(label)
    return detected_objects

def speak(text):
    engine.say(text)
    engine.runAndWait()

try:
    time.sleep(2)  # Camera warm-up
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        image = frame.array

        # Object detection
        objects = detect_objects(image)
        if objects:
            unique_objects = list(set(objects))
            message = "Detected: " + ", ".join(unique_objects)
            print(message)
            speak(message)

        # Distance measurement
        dist = get_distance()
        print(f"Distance: {dist} cm")

        if dist < 50:
            GPIO.output(BUZZER, True)
            GPIO.output(VIBRATION, True)
            speak("Obstacle ahead")
            time.sleep(0.5)
            GPIO.output(BUZZER, False)
            GPIO.output(VIBRATION, False)
        else:
            GPIO.output(BUZZER, False)
            GPIO.output(VIBRATION, False)

        raw_capture.truncate(0)
        time.sleep(1)  # Delay between cycles

except KeyboardInterrupt:
    print("Stopped by user")
    GPIO.cleanup()
    camera.close()
