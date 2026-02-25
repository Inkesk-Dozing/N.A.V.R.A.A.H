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
        self.cap = None
        
        # Load Hair Cascade for fallback (Face Detection)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        if config.ENABLE_REAL_CAMERA:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                print("Warning: Could not open camera.")
                self.cap = None

        if os.path.exists(self.model_path) and Interpreter:
            self.interpreter = Interpreter(model_path=self.model_path)
            self.interpreter.allocate_tensors()
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            print(f"Loaded TFLite model from {self.model_path}")
        else:
            # Silence the fallback warning if YOLO/Caffe exists
            pass

        # Load Caffe Model as fallback/primary for PC (VOC - 20 classes)
        self.caffe_net = None
        if os.path.exists(config.CAFFE_PROTOTXT) and os.path.exists(config.CAFFE_MODEL):
            self.caffe_net = cv2.dnn.readNetFromCaffe(config.CAFFE_PROTOTXT, config.CAFFE_MODEL)
            self.caffe_labels = ["background", "aeroplane", "bicycle", "bird", "boat",
                                "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                                "dog", "horse", "motorbike", "person", "pottedplant", 
                                "sheep", "sofa", "train", "tvmonitor"]

        # Load YOLOv3-tiny or YOLOv8-OIV7 Model (COCO/OpenImages)
        self.yolo_net = None
        if os.path.exists(config.YOLO_MODEL):
            self.yolo_net = cv2.dnn.readNet(config.YOLO_MODEL)
            # YOLO output layer names
            self.layer_names = self.yolo_net.getLayerNames()
            self.output_layers = [self.layer_names[i - 1] for i in self.yolo_net.getUnconnectedOutLayers()]
            print(f"Loaded YOLO model from {config.YOLO_MODEL}")

        if not self.interpreter and not self.yolo_net and not self.caffe_net:
            print("Warning: No AI models loaded. Falling back to Haar Cascade only.")

        if os.path.exists(self.labels_path):
            with open(self.labels_path, 'r') as f:
                self.labels = [line.strip() for line in f.readlines()]

    def get_frame(self):
        if self.cap:
            ret, frame = self.cap.read()
            return frame if ret else None
        return None

    def detect(self, frame, mock_objects=None):
        if mock_objects:
            return mock_objects
        
        if frame is None: return []
        
        results = []

        # 1. Try TFLite Model
        if self.interpreter is not None:
            input_shape = self.input_details[0]['shape']
            frame_resized = cv2.resize(frame, (input_shape[2], input_shape[1]))
            input_data = np.expand_dims(frame_resized, axis=0).astype(np.uint8)

            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
            self.interpreter.invoke()

            classes = self.interpreter.get_tensor(self.output_details[1]['index'])[0]
            scores = self.interpreter.get_tensor(self.output_details[2]['index'])[0]

            for i in range(len(scores)):
                if scores[i] > config.CONFIDENCE_THRESHOLD:
                    label = self.labels[int(classes[i])] if self.labels else f"id_{int(classes[i])}"
                    results.append(label)
        
        # 2. Try YOLO Model (COCO/OpenImages)
        elif self.yolo_net is not None:
            # YOLOv8 expects 640x640, YOLOv3-tiny 416x416
            is_v8 = "v8" in config.YOLO_MODEL.lower()
            size = (640, 640) if is_v8 else (416, 416)
            # --- Better Preprocessing: Letterboxing to maintain Aspect Ratio ---
            (h, w) = frame.shape[:2]
            max_side = max(h, w)
            padded_frame = np.zeros((max_side, max_side, 3), dtype=np.uint8)
            padded_frame[0:h, 0:w] = frame
            
            # YOLO usually needs swapRB=True for RGB
            blob = cv2.dnn.blobFromImage(padded_frame, 1/255.0, size, (0,0,0), swapRB=True, crop=False)
            self.yolo_net.setInput(blob)
            outs = self.yolo_net.forward(self.output_layers)
            
            for out in outs:
                if len(out.shape) == 3:
                    if out.shape[2] > out.shape[1]:
                        out = out[0].transpose()
                    else:
                        out = out[0]
                elif len(out.shape) == 4:
                    out = out.reshape(-1, out.shape[-1])
                
                # Fast NumPy filtering
                if out.shape[1] > 4:
                    scores = out[:, 4:]
                    confidences = np.max(scores, axis=1)
                    threshold = 0.35 if is_v8 else config.CONFIDENCE_THRESHOLD
                    
                    mask = confidences > threshold
                    valid_indices = np.where(mask)[0]
                    
                    if len(valid_indices) > 0:
                        boxes = []
                        confs = []
                        class_ids = []
                        # Scale boxes back to original coordinate system (using padded max_side)
                        scale = max_side
                        
                        for idx in valid_indices:
                            s = scores[idx]
                            c_id = np.argmax(s)
                            conf = s[c_id]
                            
                            cx, cy, bw, bh = out[idx][:4]
                            x = int((cx - bw/2) * scale)
                            y = int((cy - bh/2) * scale)
                            width = int(bw * scale)
                            height = int(bh * scale)
                            
                            boxes.append([x, y, width, height])
                            confs.append(float(conf))
                            class_ids.append(int(c_id))
                        
                        indices = cv2.dnn.NMSBoxes(boxes, confs, threshold, 0.45)
                        if len(indices) > 0:
                            for i in indices.flatten():
                                label = self.labels[class_ids[i]]
                                results.append(label)
                else:
                    # Fallback for other formats
                    for detection in out:
                        if len(detection) >= 5:
                            pass

        # 3. Try Caffe Model (VOC classes)
        elif self.caffe_net is not None:
            (h, w) = frame.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
            self.caffe_net.setInput(blob)
            detections = self.caffe_net.forward()

            for i in range(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > config.CONFIDENCE_THRESHOLD:
                    idx = int(detections[0, 0, i, 1])
                    if idx < len(self.caffe_labels):
                        results.append(self.caffe_labels[idx])
        
        # 4. Fallback: Face Detection (Haar Cascade)
        # This ensures the camera "sees" things even without the AI models
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        if len(faces) > 0:
            results.append("person")
            
        return list(set(results))

    def release(self):
        if self.cap:
            self.cap.release()
