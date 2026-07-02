import cv2
import numpy as np
import os
import time
import collections
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
        self.last_boxes = [] # Store boxes for debug visualization

        # Accessibility Priorities (Ordered by importance for a blind user)
        # Higher number = announced first. 0 = still announced, just lower priority.
        self.ACCESSIBILITY_PRIORITIES = {
            # Critical navigation hazards — always speak first
            "stairs": 10, "traffic light": 10, "stop sign": 10, "wall": 9,
            "door": 9, "window": 9, "pillar": 9, "column": 9, "fence": 9,
            # Vehicles & people
            "vehicle": 8, "car": 8, "motorcycle": 8, "bicycle": 8, "bus": 8, "truck": 8,
            "person": 7, "man": 7, "woman": 7,
            # Wearable clothing & accessories (important for recognising who/what is near)
            "clothing": 6, "jacket": 6, "shirt": 6, "trousers": 6, "dress": 6,
            "hat": 5, "glasses": 5, "sunglasses": 5, "shoe": 5, "boot": 5,
            "tie": 4, "glove": 4, "scarf": 4, "belt": 4,
            # Common indoor furniture & surfaces
            "desk": 6, "table": 6, "chair": 6, "couch": 6, "sofa": 6, "bed": 6,
            "coffee table": 6, "stool": 5, "shelf": 5, "bookcase": 5,
            # Tech & everyday items
            "laptop": 6, "monitor": 6, "phone": 6, "mobile phone": 6, "tablet": 5,
            "keyboard": 5, "mouse": 5, "television": 5, "printer": 4,
            "headphones": 4, "camera": 4, "remote control": 4,
            # Drinkware & food
            "mug": 4, "cup": 4, "bottle": 4, "bowl": 3, "plate": 3,
            # Office/study items
            "book": 4, "pen": 3, "whiteboard": 4,
            # Personal items
            "backpack": 5, "handbag": 5, "watch": 5,
            "money": 4, "coin": 4,
            # Appliances
            "refrigerator": 4, "microwave oven": 4, "oven": 4, "sink": 4,
        }

        # How many of the last 5 frames an object must appear in to be 'stable'
        # Large static surfaces need fewer confirmations; small items need more
        self.STABILITY_REQUIREMENTS = {
            # Environmental surfaces — always present, confirm quickly
            "wall": 2, "stairs": 2, "door": 2, "window": 2, "pillar": 2,
            "fence": 2, "floor": 2, "ceiling": 2,
            # People & clothing — confirm with 2 frames
            "person": 2, "man": 2, "woman": 2,
            "clothing": 2, "jacket": 2, "shirt": 2, "trousers": 2, "dress": 2,
            # Small items — require 3 frames to avoid false positives
            "glasses": 3, "sunglasses": 3, "coin": 3, "money": 3, "watch": 3,
            # Default for everything else: 3
        }
        
        # Label Mapping: OIV7 raw label -> clean natural-language name
        self.LABEL_MAP = {
            # People
            "human face": "person", "human body": "person",
            "human head": "person", "man": "person", "woman": "person",
            "boy": "person", "girl": "person",
            # Clothing & wearables — keep distinct so user knows what they see
            "top, t-shirt, sweatshirt": "clothing", "dress": "dress",
            "shorts": "clothing", "skirt": "clothing", "swimwear": "clothing",
            "footwear": "shoe", "boot": "boot", "high heels": "shoe",
            "sunglasses": "sunglasses", "glasses": "glasses",
            "hat": "hat", "fedora": "hat", "baseball cap": "hat",
            "jacket": "jacket", "coat": "jacket",
            "trousers": "trousers", "jeans": "trousers",
            "tie": "tie", "scarf": "scarf", "glove": "glove", "belt": "belt",
            # Solid surfaces / structural elements
            "wall": "wall", "pillar": "pillar", "column": "pillar",
            "fence": "fence", "door": "door", "window": "window",
            # Tech devices
            "mobile phone": "phone", "corded phone": "phone", "telephone": "phone",
            "computer mouse": "mouse", "computer keyboard": "keyboard",
            "computer monitor": "monitor", "tablet computer": "tablet",
            # Furniture
            "kitchen & dining room table": "table", "coffee table": "table",
            "couch": "sofa", "sofa bed": "sofa", "studio couch": "sofa",
            # Currency
            "bill": "money", "coin": "money",
            # Vehicles
            "land vehicle": "vehicle",
        }
        
        # Scene Memory (Object -> Last timestamp announced)
        self.scene_memory = {}
        self.COOLDOWN = 5.0  # Default cooldown in seconds
        # Environmental objects are announced less often; clothing more often
        self.COOLDOWN_MAP = {
            "wall": 15.0, "floor": 20.0, "ceiling": 20.0, "pillar": 10.0,
            "stairs": 8.0, "door": 8.0, "window": 8.0,
            "person": 5.0, "glasses": 5.0, "sunglasses": 5.0,
            "clothing": 5.0, "jacket": 5.0, "shirt": 5.0,
        }
        
        # Temporal Smoothing (Consistency Buffer — last 5 frames)
        self.detection_history = collections.deque(maxlen=5)
        
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
        
        if frame is None:
            return []
            
        results = []
        self.last_boxes = [] # Clear previous debug boxes

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
                    label_raw = self.labels[int(classes[i])] if self.labels else f"id_{int(classes[i])}"
                    label = self.LABEL_MAP.get(label_raw.lower(), label_raw)
                    # For TFLite default to center position if no bbox
                    results.append((label, 0.5))
        
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
                    # 0.28 is the sweet-spot for YOLOv8-OIV7 on a laptop camera:
                    # — high enough to block pure noise, low enough to catch walls,
                    #   clothing, glasses, and environmental surfaces reliably.
                    threshold = 0.28 if is_v8 else config.CONFIDENCE_THRESHOLD
                    
                    mask = confidences > threshold
                    valid_indices = np.where(mask)[0]
                    
                    if len(valid_indices) > 0:
                        boxes = []
                        confs = []
                        class_ids = []
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
                                label_raw = self.labels[class_ids[i]]
                                label = self.LABEL_MAP.get(label_raw.lower(), label_raw)
                                
                                
                                # Store for debugging
                                if config.DEBUG_VISION:
                                    self.last_boxes.append({
                                        'box': boxes[i],
                                        'label': f"{label} ({int(confs[i]*100)}%)",
                                        'color': (0, 255, 0) # Green
                                    })
                                
                                # Store for Spatial Logic: (Name, X-Center)
                                cx_normalized = (boxes[i][0] + boxes[i][2]/2) / scale
                                results.append((label, cx_normalized))
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
                        label_raw = self.caffe_labels[idx]
                        label = self.LABEL_MAP.get(label_raw.lower(), label_raw)
                        # Default to center position
                        results.append((label, 0.5))
        
        # 4. Haar Cascade: Supplement YOLO — catches faces YOLO OIV7 may miss.
        # Run alongside YOLO (not instead of it). Only add if person not already found.
        existing_labels = {r[0].lower() for r in results}
        if "person" not in existing_labels:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(60, 60))
            for (x, y, w, h) in faces:
                cx_normalized = (x + w / 2) / frame.shape[1]
                results.append(("person", cx_normalized))
            
        # Temporal Smoothing: Only objects seen in required frames are "Stable"
        self.detection_history.append(results)
        
        # Count frames where object appeared (not total bounding boxes)
        counts = collections.Counter()
        for frame_res in self.detection_history:
            unique_objs_in_frame = set([item[0] for item in frame_res])
            counts.update(unique_objs_in_frame)
        
        stable_results = []
        # Keep the most recent spatial position for each detected object
        latest_positions = {item[0]: item[1] for item in results}
        
        for obj_name, count in counts.items():
            if obj_name not in latest_positions:
                continue
            # Decide how many of the last 5 frames we need to see it in
            if config.TEST_MODE:
                # In test mode: instant confirmation (1 frame)
                required = 1
            else:
                required = self.STABILITY_REQUIREMENTS.get(obj_name.lower(), 3)
                required = min(required, len(self.detection_history))
            
            if count >= required:
                # Directional awareness: divide frame into left / ahead / right
                cx = latest_positions[obj_name]
                if cx < 0.33:
                    pos_text = "on your left"
                elif cx > 0.66:
                    pos_text = "on your right"
                else:
                    pos_text = "directly ahead"
                full_label = f"{obj_name} {pos_text}"
                stable_results.append((obj_name, full_label))

        # 2. Apply per-object cooldown via Scene Memory
        now = time.time()
        filtered_objs = []
        for base_obj, full_label in stable_results:
            cooldown = self.COOLDOWN_MAP.get(base_obj.lower(), self.COOLDOWN)
            last_seen = self.scene_memory.get(full_label, 0)
            if now - last_seen > cooldown:
                filtered_objs.append((base_obj, full_label))
                self.scene_memory[full_label] = now
        
        # 3. Sort by accessibility priority (highest first)
        filtered_objs.sort(
            key=lambda x: (self.ACCESSIBILITY_PRIORITIES.get(x[0].lower(), 1), x[1]),
            reverse=True
        )
        return [item[1] for item in filtered_objs]

    def show_frame(self, frame):
        """Draws stored debug boxes and shows the window if DEBUG_VISION is enabled."""
        if not config.DEBUG_VISION or frame is None:
            return
            
        debug_frame = frame.copy()
        for item in self.last_boxes:
            x, y, w, h = item['box']
            cv2.rectangle(debug_frame, (x, y), (x + w, y + h), item['color'], 2)
            cv2.putText(debug_frame, item['label'], (x, y - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, item['color'], 2)
        
        cv2.imshow("N.A.V.R.A.A.H - Debug Vision", debug_frame)
        cv2.waitKey(1)

    def release(self):
        if self.cap:
            self.cap.release()
