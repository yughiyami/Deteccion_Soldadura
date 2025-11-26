# Detector de Defectos de Soldadura SMAW con IA

Este proyecto utiliza **YOLOv8** para la detección de defectos en soldadura y **Streamlit** para la interfaz de usuario.

## Requisitos Previos

1.  Python 3.8 o superior.
2.  Una cuenta en [Roboflow](https://roboflow.com) para obtener tu API Key (gratuita).

## Instalación

1.  Clona o descarga este repositorio.
2.  Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Paso 1: Entrenamiento del Modelo

Para que el sistema sea un "experto", necesita entrenarse con datos de soldadura.

1.  Ejecuta el script de entrenamiento:
    ```bash
    python train_model.py
    ```
2.  Ingresa tu **Roboflow API Key** cuando se te solicite.
3.  El script descargará el dataset y comenzará a entrenar.
4.  Al finalizar, te indicará dónde se guardó el modelo (usualmente en `runs/detect/train/weights/best.pt`).

> **Nota**: Si no tienes GPU, este paso puede ser lento. Puedes usar Google Colab para entrenar y luego descargar el archivo `best.pt`.

## Paso 2: Ejecutar la Aplicación

1.  Inicia la interfaz gráfica:
    ```bash
    streamlit run app.py
    ```
2.  Se abrirá una pestaña en tu navegador.
3.  En la barra lateral, ingresa la ruta a tu modelo entrenado (ej. `runs/detect/train/weights/best.pt`). Si aún no has entrenado, puedes usar `yolov8n.pt` para probar (aunque no detectará defectos específicos de soldadura hasta que se entrene).
4.  Sube imágenes o videos para probar la detección.

## Datasets Soportados

El script está configurado para usar el dataset: `final-year-project-kswbt/welding-defect-detection` de Roboflow, que contiene clases como:
- Porosity
- Crack
- Undercut
- etc.
