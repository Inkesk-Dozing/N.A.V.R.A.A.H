import cv2
import numpy as np
import os
import config

# Try to import TFLite runtime, fallback to tensorflow if needed
try:
    from tflite_runtime.interpreter import Interpreter
except ImportError:
    try:
        from tensorflow.lite.python.interpreter import Interpreter
    except ImportError:
        Interpreter = None

class VisionSystem:
    def __init__(self):
        self.model_path = config.MODEL_PATH
        self.labels_path = config.LABELS_PATH
        self.interpreter = None
        self.labels = []
        
        if os.path.exists(self.model_path) and Interpreter:
            self.interpreter = Interpreter(model_path=self.model_path)
            self.interpreter.allocate_tensors()
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
        else:
            print(f"Warning: Model not found at {self.model_path}. Vision will be in Mock Mode.")

        if os.path.exists(self.labels_path):
            with open(self.labels_path, 'r') as f:
                self.labels = [line.strip() for line in f.readlines()]

    def get_frame(self):
        # In a real RPi, we might use picamera. 
        # For this implementation, we use standard OpenCV cap which works on both.
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        return frame if ret else None

    def detect(self, frame):
        if frame is None: return []
        if self.interpreter is None:
            # Mock detection: randomly detect "person" or "chair" if in TEST_MODE
            if config.TEST_MODE:
                return ["person"] if np.random.rand() > 0.7 else []
            return []

        # Real TFLite Logic
        input_shape = self.input_details[0]['shape']
        frame_resized = cv2.resize(frame, (input_shape[2], input_shape[1]))
        input_data = np.expand_dims(frame_resized, axis=0).astype(np.uint8)

        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()

        classes = self.interpreter.get_tensor(self.output_details[1]['index'])[0]
        scores = self.interpreter.get_tensor(self.output_details[2]['index'])[0]

        detected = []
        for i in range(len(scores)):
            if scores[i] > config.CONFIDENCE_THRESHOLD:
                label = self.labels[int(classes[i])] if self.labels else f"id_{int(classes[i])}"
                detected.append(label)
        return list(set(detected))
