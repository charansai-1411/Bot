from ultralytics import YOLO
from PIL import Image

# load model once
model = YOLO("yolov8n.pt")

def detect_disease(image_path):
    results = model(image_path)

    names = model.names
    boxes = results[0].boxes

    if boxes is None or len(boxes) == 0:
        return "No disease detected"

    cls_id = int(boxes.cls[0])
    disease = names[cls_id]

    return disease