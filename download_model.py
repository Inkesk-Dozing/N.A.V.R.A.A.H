import urllib.request
import os
import time

# Using MobileNet SSD Caffe model (OpenCV friendly)
prototxt_url = "https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/master/deploy.prototxt"
model_url = "https://github.com/chuanqi305/MobileNet-SSD/raw/master/mobilenet_iter_73000.caffemodel"
prototxt_path = os.path.join("models", "deploy.prototxt")
model_path = os.path.join("models", "mobilenet_ssd.caffemodel")

# Using YOLOv8n-OIV7 ONNX (Open Images V7 - 600+ classes including Watch)
oiv7_url = "https://github.com/CVHub520/X-AnyLabeling/releases/download/v2.3.7/yolov8n-oiv7.onnx"
oiv7_path = os.path.join("models", "yolov8n-oiv7.onnx")

if not os.path.exists("models"):
    os.makedirs("models")

def download_with_retry(url, path, max_retries=5):
    for i in range(max_retries):
        try:
            print(f"Attempt {i+1}: Downloading model from {url}...")
            urllib.request.urlretrieve(url, path)
            print(f"Successfully downloaded to {path}")
            return True
        except Exception as e:
            print(f"Attempt {i+1} failed: {e}")
            time.sleep(5)
    return False

print("--- Downloading Caffe Model ---")
download_with_retry(prototxt_url, prototxt_path)
download_with_retry(model_url, model_path)

print("--- Downloading YOLOv8n-OIV7 Model ---")
if download_with_retry(oiv7_url, oiv7_path):
    print(f"YOLOv8n-OIV7 ready: {oiv7_path}")

print("Finished downloads.")
