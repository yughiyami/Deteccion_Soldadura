from ultralytics import YOLO
import os
import yaml
import shutil
import cv2
import numpy as np
import xml.etree.ElementTree as ET
from glob import glob
from sklearn.model_selection import train_test_split
import kagglehub

# Paths
DATASET_DIR = "gc10_yolo_dataset"
IMAGES_DIR = os.path.join(DATASET_DIR, "images")
LABELS_DIR = os.path.join(DATASET_DIR, "labels")

# GC10-DET Classes
CLASS_MAP = {
    "1": 0, "2": 1, "3": 2, "4": 3, "5": 4, 
    "6": 5, "7": 6, "8": 7, "9": 8, "10": 9,
    "punching": 0, "weld_line": 1, "crescent_gap": 2, "water_spot": 3,
    "oil_spot": 4, "silk_spot": 5, "inclusion": 6, "rolled_pit": 7,
    "crease": 8, "waist_folding": 9
}
CLASS_NAMES = {
    0: "Punching", 1: "Weld_line", 2: "Crescent_gap", 3: "Water_spot", 
    4: "Oil_spot", 5: "Silk_spot", 6: "Inclusion", 7: "Rolled_pit", 
    8: "Crease", 9: "Waist_folding"
}

def train_model():
    """Trains the YOLOv8 model using the prepared dataset."""
    print("\n" + "="*50)
    print("STARTING MODEL TRAINING")
    print("="*50)
    
    # Load a model
    model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)

    # Train the model
    # Using reasonable defaults for a real run. User can adjust epochs if needed.
    results = model.train(
        data=os.path.join(DATASET_DIR, "data.yaml"), 
        epochs=50,      # Good balance for performance
        imgsz=640,      # Standard YOLO input size
        batch=16,       # Standard batch size
        patience=10,    # Early stopping
        plots=True,
        project="runs/detect",
        name="surface_defect_model",
        exist_ok=True   # Overwrite existing experiment
    )
    
    print("\n" + "="*50)
    print("TRAINING COMPLETE")
    print(f"Best model saved at: {results.save_dir}/weights/best.pt")
    print("="*50)
    
    # Export the model (Optional)
    try:
        print("Attempting ONNX export...")
        success = model.export(format="onnx")
        print(f"Model exported to ONNX: {success}")
    except Exception as e:
        print(f"Export failed (non-critical): {e}")

def prepare_dataset():
    """Downloads dataset via kagglehub and converts to YOLO format."""
    print("Downloading dataset from Kaggle...")
    try:
        path = kagglehub.dataset_download("zhangyunsheng/defects-class-and-location")
        print("Path to dataset files:", path)
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        return

    if os.path.exists(DATASET_DIR):
        print(f"Cleaning up existing dataset directory: {DATASET_DIR}")
        shutil.rmtree(DATASET_DIR)
    
    for split in ["train", "val"]:
        os.makedirs(os.path.join(IMAGES_DIR, split), exist_ok=True)
        os.makedirs(os.path.join(LABELS_DIR, split), exist_ok=True)

    # Search for XML files in the downloaded path
    xml_files = glob(os.path.join(path, "**", "*.xml"), recursive=True)
    
    if not xml_files:
        print("No XML files found in downloaded dataset!")
        return

    print(f"Found {len(xml_files)} XML files. Processing...")
    
    train_files, val_files = train_test_split(xml_files, test_size=0.2, random_state=42)
    
    processed_count = 0
    for split, files in [("train", train_files), ("val", val_files)]:
        for xml_file in files:
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()
                
                # Image info
                filename = root.find("filename").text
                
                # Find corresponding image
                base_dir = os.path.dirname(xml_file)
                basename = os.path.splitext(os.path.basename(xml_file))[0]
                
                # Look for image with same basename
                image_path = None
                for ext in ['.jpg', '.jpeg', '.png', '.bmp']:
                    potential_path = os.path.join(base_dir, basename + ext)
                    if os.path.exists(potential_path):
                        image_path = potential_path
                        break
                
                if not image_path:
                    # Try searching recursively if not in same dir
                    image_files = glob(os.path.join(path, "**", f"{basename}.*"), recursive=True)
                    for img_f in image_files:
                        if img_f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                            image_path = img_f
                            break
                
                if not image_path:
                    continue
                
                # Copy image
                shutil.copy(image_path, os.path.join(IMAGES_DIR, split, os.path.basename(image_path)))
                
                # Parse objects
                img = cv2.imread(image_path)
                if img is None: continue
                h, w = img.shape[:2]
                
                label_path = os.path.join(LABELS_DIR, split, f"{basename}.txt")
                
                has_valid_labels = False
                with open(label_path, "w") as f:
                    for obj in root.findall("object"):
                        cls_name = obj.find("name").text.lower().replace(" ", "_")
                        
                        cls_id = -1
                        # Try exact match or number match
                        if cls_name in CLASS_MAP:
                            cls_id = CLASS_MAP[cls_name]
                        else:
                            # Try to find partial match or mapped name
                            for k, v in CLASS_MAP.items():
                                if k in cls_name:
                                    cls_id = v
                                    break
                        
                        if cls_id == -1:
                            continue
                            
                        bndbox = obj.find("bndbox")
                        xmin = float(bndbox.find("xmin").text)
                        ymin = float(bndbox.find("ymin").text)
                        xmax = float(bndbox.find("xmax").text)
                        ymax = float(bndbox.find("ymax").text)
                        
                        # Normalize
                        x_center = ((xmin + xmax) / 2) / w
                        y_center = ((ymin + ymax) / 2) / h
                        width = (xmax - xmin) / w
                        height = (ymax - ymin) / h
                        
                        f.write(f"{cls_id} {x_center} {y_center} {width} {height}\n")
                        has_valid_labels = True
                
                if has_valid_labels:
                    processed_count += 1
                        
            except Exception as e:
                print(f"Error processing {xml_file}: {e}")

    print(f"Successfully processed {processed_count} images.")

    # Create data.yaml
    data = {
        'path': os.path.abspath(DATASET_DIR),
        'train': 'images/train',
        'val': 'images/val',
        'names': CLASS_NAMES
    }
    
    with open(os.path.join(DATASET_DIR, "data.yaml"), "w") as f:
        yaml.dump(data, f)
    
    # Start training
    train_model()

if __name__ == "__main__":
    prepare_dataset()
