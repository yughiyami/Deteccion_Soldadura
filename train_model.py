from roboflow import Roboflow
from ultralytics import YOLO
import os

def train_welding_model(api_key):
    """
    Downloads the dataset and trains the YOLOv8 model.
    """
    print("--- Iniciando proceso de entrenamiento ---")
    
    # 1. Descargar Dataset de Roboflow
    # Usamos el dataset 'welding-defect-detection' mencionado en el plan
    # Nota: El usuario debe proveer su API KEY válida.
    try:
        rf = Roboflow(api_key=api_key)
        # Reemplaza 'workspace' y 'project' con los correctos si cambian, 
        # pero este es uno de los links comunes para defectos de soldadura.
        # Basado en: https://universe.roboflow.com/final-year-project-kswbt/welding-defect-detection
        project = rf.workspace("piticha").project("welding-owyo4")
        dataset = project.version(2).download("yolov8")
        
        print(f"Dataset descargado en: {dataset.location}")
    except Exception as e:
        print(f"Error al descargar dataset: {e}")
        print("Asegúrate de que tu API Key sea correcta y tengas acceso a internet.")
        return

    # 2. Entrenar Modelo YOLOv8
    # Usamos 'yolov8n.pt' (nano) para entrenamiento rápido. 
    # Cambiar a 'yolov8s.pt' o 'yolov8m.pt' para mayor precisión si hay tiempo/GPU.
    print("Cargando modelo YOLOv8n (nano)...")
    model = YOLO('yolov8n.pt') 

    print("Comenzando entrenamiento...")
    # data.yaml se encuentra dentro de la carpeta descargada
    data_yaml_path = os.path.join(dataset.location, 'data.yaml')
    
    # Entrenamos por 50 épocas (ajustable)
    results = model.train(
        data=data_yaml_path,
        epochs=50,
        imgsz=640,
        plots=True
    )
    
    print("Entrenamiento finalizado.")
    print(f"Mejor modelo guardado en: {results.save_dir}")

if __name__ == "__main__":
    # Pedir API Key al usuario si no está en variable de entorno
    api_key = os.getenv("ROBOFLOW_API_KEY")
    if not api_key:
        api_key = input("Por favor ingresa tu Roboflow API Key: ")
    
    if api_key:
        train_welding_model(api_key)
    else:
        print("Se requiere una API Key para continuar.")
