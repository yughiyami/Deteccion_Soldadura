from ultralytics import YOLO
from PIL import Image
import numpy as np

def debug_inference():
    # Load model
    model_path = "models/welding_model.pt"
    try:
        model = YOLO(model_path)
        print(f"Model loaded: {model_path}")
        print(f"Model classes: {model.names}")
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # Load image
    img_path = "debug_image.png"
    try:
        # Load as RGB
        image = Image.open(img_path).convert("RGB")
        print(f"Image loaded: {img_path}, Size: {image.size}")
    except Exception as e:
        print(f"Error loading image: {e}")
        return

    # Run inference with low confidence to see everything
    print("\n--- Running Inference (conf=0.1) ---")
    results = model.predict(image, conf=0.1)
    
    # Print results
    for r in results:
        boxes = r.boxes
        if len(boxes) == 0:
            print("No detections found.")
        else:
            print(f"Found {len(boxes)} detections:")
            for box in boxes:
                cls_id = int(box.cls[0])
                cls_name = model.names[cls_id]
                conf = float(box.conf[0])
                print(f"- Class: {cls_name} (ID: {cls_id}), Confidence: {conf:.4f}")

if __name__ == "__main__":
    debug_inference()
