# Gestión de Fichas Técnicas

Este documento explica la lógica de negocio detrás de la generación y gestión de las fichas técnicas dentro de la aplicación.

## Estructura de Datos (`fichas_config.py`)

El sistema maneja 4 tipos de fichas técnicas, definidas en el archivo de configuración. Cada ficha se compone de dos tipos de campos:

1.  **Manuales**: Datos ingresados por el inspector u operario *antes* o *después* del proceso.
2.  **Automáticos**: Datos inferidos por los modelos de IA o calculados mediante algoritmos de visión computacional.

### 1. Ficha de Trazabilidad
Registra el contexto del trabajo. Es fundamental para el seguimiento de calidad.
*   **Manual**: Soldador, Máquina, WPS, Materiales, Parámetros eléctricos (V, A), Gas.
*   **Automático**: ID único del cordón (UUID), Imagen de evidencia, Aprobación final.

### 2. Ficha de Geometría
Evalúa las dimensiones físicas del cordón.
*   **Manual**: Distancia cámara-pieza (para calibración), Tipo de junta.
*   **Automático**:
    *   *Ancho Promedio*: Calculado a partir de la detección de bordes (simulado en v1).
    *   *Altura Refuerzo*: Estimación basada en perfil (simulado en v1).
    *   *Ángulos de Mojado*: Indicadores de fusión lateral.

### 3. Ficha de Defectología
El núcleo del análisis de calidad. Sigue normativas como ISO 5817 o AWS D1.1.
*   **Manual**: Norma de referencia.
*   **Automático (IA)**:
    *   **Poros**: Conteo de detecciones de clase `Porosity`.
    *   **Grietas**: Conteo de clase `Crack`.
    *   **Socavado**: Conteo de clase `Undercut`.
    *   **Cordón Irregular**: Mapeo de clase `Bad Welding` o `Irregular`.
    *   **Spatter**: Nivel estimado basado en conteo de `Spatters`.

### 4. Ficha de Dimensionalidad
Verifica si el cordón cumple con las tolerancias del proyecto.
*   **Manual**: Proyecto, Número de Junta, Longitud total.
*   **Automático**: Hereda valores de la ficha de geometría (Ancho, Altura) para compararlos con las especificaciones.

## Flujo de Trabajo en la Aplicación

### Paso 1: Datos de Entrada (Pre-Soldadura)
*   El usuario llena los datos de trazabilidad.
*   **Inspección de Superficie**: Se sube una foto del material base. El modelo `surface_model.pt` analiza la limpieza. Si detecta aceite u óxido, sugiere "RECHAZADO" en la condición superficial.

### Paso 2: Inspección (Detección)
*   Se sube la foto del cordón de soldadura.
*   El modelo `welding_model.pt` procesa la imagen.
*   Se dibujan las cajas delimitadoras (bounding boxes) sobre la imagen.
*   Se cuentan las ocurrencias de cada defecto.

### Paso 3: Resultados y Validación
*   El sistema presenta los valores automáticos sugeridos.
*   **Validación Humana**: El inspector puede sobrescribir cualquier valor automático si la IA cometió un error.
*   Se emite el veredicto final (APROBADO/RECHAZADO).

### Paso 4: Reporte
*   Se consolidan todos los datos (manuales + automáticos validados).
*   Se presentan las 4 fichas en formato tabular.
*   Opción de descarga (CSV/Excel).
