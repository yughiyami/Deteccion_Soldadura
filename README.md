# Sistema de Gestión de Calidad de Soldadura con IA

Este proyecto implementa un sistema integral para la detección y gestión de defectos en soldadura utilizando Inteligencia Artificial (YOLOv8). El sistema cubre desde la inspección de la superficie del material base hasta el análisis post-soldadura, generando reportes técnicos detallados.

## 🚀 Características Principales

*   **Flujo de Trabajo Guiado**: Proceso paso a paso (Datos -> Inspección -> Validación -> Reporte).
*   **Doble Inspección con IA**:
    1.  **Modelo de Superficie**: Detecta contaminación previa (óxido, aceite, manchas).
    2.  **Modelo de Soldadura**: Detecta defectos en el cordón (porosidad, grietas, socavado, etc.).
*   **Generación de Fichas Técnicas**: Automáticamente genera fichas de Trazabilidad, Geometría, Defectología y Dimensionalidad.
*   **Despliegue Flexible**: Dockerizado y listo para desplegar en local o VPS.

## 🛠️ Tecnologías

*   **Python 3.11**
*   **Streamlit**: Interfaz de usuario web.
*   **Ultralytics YOLOv8**: Modelos de detección de objetos.
*   **OpenCV & Pillow**: Procesamiento de imágenes.
*   **Pandas**: Manejo de datos y reportes.

## 📊 Reporte Técnico de Modelos IA

A continuación se presentan las métricas de rendimiento de los modelos entrenados e integrados en el sistema.

### 1. Modelo de Defectos de Superficie (GC10-DET)
Este modelo analiza la chapa metálica antes de soldar para asegurar que la superficie esté limpia.

*   **Dataset**: GC10-DET (Public Dataset)
*   **Clases Detectadas**:
    *   Punching (Perforación)
    *   Weld_line (Línea de soldadura)
    *   Crescent_gap (Hueco creciente)
    *   Water_spot (Mancha de agua)
    *   Oil_spot (Mancha de aceite)
    *   Silk_spot (Mancha de seda)
    *   Inclusion (Inclusión)
    *   Rolled_pit (Picadura laminada)
    *   Crease (Pliegue)
    *   Waist_folding (Plegado de cintura)

**Métricas de Entrenamiento (Última Época):**

| Métrica | Valor | Descripción |
| :--- | :--- | :--- |
| **Precisión (Precision)** | **0.715** | % de detecciones correctas sobre el total de detecciones. |
| **Exhaustividad (Recall)** | **0.604** | % de defectos reales que fueron detectados. |
| **mAP@50** | **0.639** | Precisión media con umbral de IoU del 50%. |
| **mAP@50-95** | **0.330** | Precisión media promediada sobre varios umbrales (más estricto). |

---

### 2. Modelo de Defectos de Soldadura (Welding Defect)
Este modelo analiza el cordón de soldadura final para identificar fallos críticos.

*   **Dataset**: Welding Defect Detection (Roboflow)
*   **Clases Detectadas**:
    *   Bad Welding (Soldadura Defectuosa / Irregular)
    *   Crack (Grieta)
    *   Excess Reinforcement (Exceso de Refuerzo)
    *   Good Welding (Soldadura Correcta)
    *   Porosity (Porosidad)
    *   Spatters (Salpicaduras)
    *   Undercut (Socavado)

**Métricas de Entrenamiento (Última Época):**

| Métrica | Valor | Descripción |
| :--- | :--- | :--- |
| **Precisión (Precision)** | **0.694** | % de detecciones correctas sobre el total de detecciones. |
| **Exhaustividad (Recall)** | **0.620** | % de defectos reales que fueron detectados. |
| **mAP@50** | **0.665** | Precisión media con umbral de IoU del 50%. |
| **mAP@50-95** | **0.389** | Precisión media promediada sobre varios umbrales. |

> **Nota sobre Detección**: El modelo puede clasificar áreas con múltiples poros pequeños como "Bad Welding" en lugar de "Porosity" individual. El sistema mapea automáticamente "Bad Welding" a "Cordón Irregular" en el reporte.

## 📦 Instalación y Despliegue

### Requisitos Previos
*   Docker y Docker Compose instalados.

### Pasos para Ejecutar

1.  **Clonar el repositorio**:
    ```bash
    git clone https://github.com/yughiyami/Deteccion_Soldadura.git
    cd Deteccion_Soldadura
    ```

2.  **Construir y Levantar Contenedor**:
    ```bash
    docker-compose up --build
    ```

3.  **Acceder a la Aplicación**:
    Abrir navegador en `http://localhost:8501`.

### Estructura del Proyecto

*   `app.py`: Aplicación principal (Streamlit).
*   `fichas_config.py`: Configuración de campos para los reportes.
*   `train_surface_model.py`: Script para entrenar el modelo de superficie.
*   `train_model.py`: Script para entrenar el modelo de soldadura.
*   `models/`: Carpeta que contiene los pesos entrenados (`.pt`).
*   `Dockerfile` & `docker-compose.yml`: Configuración de contenedores.

## 🤝 Contribución
Proyecto desarrollado para la mejora del aseguramiento de calidad en procesos de soldadura mediante visión artificial.
