import streamlit as st
from ultralytics import YOLO
import cv2
import tempfile
import os
from PIL import Image
import numpy as np
import pandas as pd
from datetime import datetime
import uuid
import fichas_config as fc

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Fichas Técnicas de Soldadura",
    page_icon="📋",
    layout="wide"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
        color: #fafafa;
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #ff6b6b;
    }
    h1, h2, h3 {
        color: #ff4b4b;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .report-box {
        border: 1px solid #444;
        padding: 20px;
        border-radius: 10px;
        background-color: #262730;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #ff4b4b;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar Session State
if 'ficha' not in st.session_state:
    st.session_state.ficha = {
        'id_cordon': str(uuid.uuid4())[:8].upper(),
        'fecha': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'manual_data': {},
        'auto_data': {},
        'image_analyzed': False,
        'step': 1
    }

def reset_ficha():
    st.session_state.ficha = {
        'id_cordon': str(uuid.uuid4())[:8].upper(),
        'fecha': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'manual_data': {},
        'auto_data': {},
        'image_analyzed': False,
        'step': 1
    }

# Sidebar
st.sidebar.title("🔧 Configuración")
st.sidebar.markdown("---")
confidence = st.sidebar.slider("Umbral de Confianza IA", 0.0, 1.0, 0.25, 0.05)
model_path = st.sidebar.text_input("Ruta Modelo Soldadura (.pt)", "yolov8n.pt")
surface_model_path = st.sidebar.text_input("Ruta Modelo Superficie (.pt)", "runs/detect/train/weights/best.pt")

try:
    model = YOLO(model_path)
    st.sidebar.success(f"Modelo Soldadura: OK")
except Exception as e:
    st.sidebar.error(f"Error Modelo Soldadura: {e}")

try:
    surface_model = YOLO(surface_model_path)
    st.sidebar.success(f"Modelo Superficie: OK")
except Exception as e:
    st.sidebar.warning(f"Modelo Superficie no encontrado (usando dummy): {e}")
    surface_model = None

st.sidebar.markdown("---")
if st.sidebar.button("Nueva Ficha"):
    reset_ficha()
    st.rerun()

st.title("📋 Sistema de Gestión de Calidad de Soldadura")

# Progress Bar
steps = ["1. Datos de Entrada", "2. Inspección", "3. Resultados", "4. Reporte"]
current_step = st.session_state.ficha['step']
st.progress(current_step / 4)
st.subheader(f"Paso {current_step}: {steps[current_step-1]}")

# --- STEP 1: DATOS DE ENTRADA ---
if current_step == 1:
    st.markdown("### 📝 Ingreso de Datos Manuales (Pre-Soldadura)")
    
    # --- SECCIÓN DE INSPECCIÓN DE SUPERFICIE ---
    with st.expander("🔍 Inspección de Superficie (Pre-Soldadura)", expanded=True):
        st.info("Cargue una imagen del material base para detectar contaminación (Óxido, Aceite, etc.)")
        surf_file = st.file_uploader("Imagen Superficie", type=['jpg', 'png', 'jpeg'], key="surf_uploader")
        
        if surf_file:
            surf_img = Image.open(surf_file).convert("RGB")
            c1, c2 = st.columns(2)
            c1.image(surf_img, caption="Superficie Material", use_column_width=True)
            
            if st.button("Analizar Superficie"):
                if surface_model:
                    res_surf = surface_model.predict(np.array(surf_img), conf=confidence)
                    res_plotted_surf = res_surf[0].plot()
                    c2.image(res_plotted_surf, caption="Detección de Contaminantes", use_column_width=True)
                    
                    # Contar defectos
                    surf_boxes = res_surf[0].boxes
                    surf_defects = []
                    if len(surf_boxes) > 0:
                        for box in surf_boxes:
                            cls = int(box.cls[0])
                            surf_defects.append(surface_model.names[cls])
                    
                    if surf_defects:
                        st.error(f"Contaminación Detectada: {', '.join(set(surf_defects))}")
                        st.session_state.ficha['manual_data']['condicion_superficial'] = f"RECHAZADO ({', '.join(set(surf_defects))})"
                    else:
                        st.success("Superficie Limpia")
                        st.session_state.ficha['manual_data']['condicion_superficial'] = "ACEPTADO (Limpio)"
                else:
                    st.warning("Modelo de superficie no cargado.")

    with st.form("manual_data_form"):
        # Trazabilidad
        st.markdown("#### Ficha de Trazabilidad")
        cols = st.columns(3)
        for i, field in enumerate(fc.TRAZABILIDAD_FIELDS["manual"]):
            col = cols[i % 3]
            with col:
                key = field["key"]
                val = st.session_state.ficha['manual_data'].get(key)
                if field["type"] == "number":
                    st.number_input(field["label"], key=key, step=field.get("step", 1.0), value=val if val else 0.0)
                else:
                    st.text_input(field["label"], key=key, value=val if val else "")

        st.markdown("---")
        # Geometría y Dimensionalidad (Manuales)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Geometría (Config)")
            for field in fc.GEOMETRIA_FIELDS["manual"]:
                key = field["key"]
                val = st.session_state.ficha['manual_data'].get(key)
                if field["type"] == "number":
                    st.number_input(field["label"], key=key, step=field.get("step", 1.0), value=val if val else 0.0)
                else:
                    st.text_input(field["label"], key=key, value=val if val else "")
        
        with col2:
            st.markdown("#### Dimensionalidad (Datos)")
            for field in fc.DIMENSIONALIDAD_FIELDS["manual"]:
                key = field["key"]
                val = st.session_state.ficha['manual_data'].get(key)
                if field["type"] == "number":
                    st.number_input(field["label"], key=key, step=field.get("step", 1.0), value=val if val else 0.0)
                else:
                    st.text_input(field["label"], key=key, value=val if val else "")
        
        st.markdown("---")
        # Defectología (Manuales)
        st.markdown("#### Defectología (Normativa)")
        for field in fc.DEFECTOLOGIA_FIELDS["manual"]:
            key = field["key"]
            val = st.session_state.ficha['manual_data'].get(key)
            if field["type"] == "selectbox":
                st.selectbox(field["label"], field["options"], key=key, index=field["options"].index(val) if val in field["options"] else 0)
            else:
                st.text_input(field["label"], key=key, value=val if val else "")
        
        # Campo extra para resultado de superficie
        st.text_input("Condición Superficial (Auto)", key="condicion_superficial_display", 
                      value=st.session_state.ficha['manual_data'].get('condicion_superficial', 'Pendiente'), disabled=True)

        submitted = st.form_submit_button("Guardar y Continuar ➡️")
        
        if submitted:
            # Save all manual inputs to session state
            for field_list in [fc.TRAZABILIDAD_FIELDS["manual"], fc.GEOMETRIA_FIELDS["manual"], fc.DIMENSIONALIDAD_FIELDS["manual"], fc.DEFECTOLOGIA_FIELDS["manual"]]:
                for field in field_list:
                    st.session_state.ficha['manual_data'][field["key"]] = st.session_state[field["key"]]
            
            st.session_state.ficha['step'] = 2
            st.rerun()


# --- STEP 2: INSPECCIÓN ---
elif current_step == 2:
    st.markdown("### 👁️ Inspección y Detección")
    
    uploaded_file = st.file_uploader("Cargar Imagen del Cordón", type=['jpg', 'png', 'jpeg'])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Imagen Original", use_column_width=True)
        
        if st.button("Ejecutar Análisis IA ⚡"):
            with st.spinner('Analizando imagen y calculando métricas...'):
                # Análisis YOLO
                img_array = np.array(image)
                results = model.predict(img_array, conf=confidence)
                res_plotted = results[0].plot()
                
                # Guardar imagen procesada
                st.session_state.ficha['processed_image'] = cv2.cvtColor(res_plotted, cv2.COLOR_BGR2RGB)
                
                # Extraer datos reales de detección
                boxes = results[0].boxes
                defect_counts = {}
                detections = []
                
                if len(boxes) > 0:
                    for box in boxes:
                        cls = int(box.cls[0])
                        name = model.names[cls]
                        detections.append(name)
                        defect_counts[name] = defect_counts.get(name, 0) + 1
                
                # --- SIMULACIÓN DE MÉTRICAS (Post-Procesamiento) ---
                # En un sistema real, esto vendría de algoritmos de visión computacional específicos
                
                # Geometría
                ancho_px = results[0].boxes.xywh[:, 2].mean() if len(boxes) > 0 else 0 # width in pixels (dummy)
                # Conversión dummy px -> mm
                ancho_mm = np.random.uniform(8.0, 12.0) 
                
                auto_data = {}
                
                # Llenar campos automáticos de Geometría
                auto_data['ancho_promedio'] = f"{ancho_mm:.2f}"
                auto_data['altura_refuerzo'] = f"{np.random.uniform(1.5, 3.0):.2f}"
                auto_data['radio_curvatura'] = f"{np.random.uniform(5.0, 8.0):.2f}"
                auto_data['simetria'] = f"{np.random.uniform(90, 100):.1f}"
                auto_data['angulo_mojado_l'] = f"{np.random.uniform(130, 150):.1f}"
                auto_data['angulo_mojado_r'] = f"{np.random.uniform(130, 150):.1f}"
                auto_data['rugosidad'] = f"{np.random.uniform(0.5, 2.0):.2f}"
                auto_data['secciones_criticas'] = "Ninguna" if len(boxes) == 0 else f"{len(boxes)} zonas"

                # Llenar campos automáticos de Defectología
                auto_data['def_poros'] = f"{defect_counts.get('Porosity', 0)}"
                auto_data['def_porosidad_lineal'] = "0 mm" # Simulado
                auto_data['def_socavado'] = f"{defect_counts.get('Undercut', 0)}"
                auto_data['def_grietas'] = f"{defect_counts.get('Crack', 0)}"
                auto_data['def_falta_fusion'] = f"{defect_counts.get('Lack of Fusion', 0)}"
                auto_data['def_exceso_refuerzo'] = "No detectado"
                auto_data['def_mordeduras'] = "0"
                auto_data['def_spatter'] = "Bajo"
                auto_data['def_irregular'] = "Bajo"

                # Llenar campos automáticos de Dimensionalidad
                auto_data['dim_ancho'] = auto_data['ancho_promedio']
                auto_data['dim_altura'] = auto_data['altura_refuerzo']
                auto_data['dim_angulo_l'] = auto_data['angulo_mojado_l']
                auto_data['dim_angulo_r'] = auto_data['angulo_mojado_r']
                auto_data['dim_uniformidad'] = "5%"
                auto_data['dim_rectitud'] = "1 mm"
                auto_data['dim_penetracion'] = "N/A (Visual)"

                # Trazabilidad Automática
                auto_data['id_cordon'] = st.session_state.ficha['id_cordon']
                auto_data['mapa_defectos'] = str(defect_counts)
                auto_data['aprobacion_final'] = "RECHAZADO" if len(boxes) > 0 else "ACEPTADO"

                st.session_state.ficha['auto_data'] = auto_data
                st.session_state.ficha['image_analyzed'] = True
                
                st.session_state.ficha['step'] = 3
                st.rerun()
    
    if st.button("⬅️ Volver"):
        st.session_state.ficha['step'] = 1
        st.rerun()

# --- STEP 3: RESULTADOS Y VALIDACIÓN ---
elif current_step == 3:
    st.markdown("### 📊 Resultados y Validación")
    
    col_img, col_info = st.columns([1, 1])
    with col_img:
        st.image(st.session_state.ficha['processed_image'], caption="Imagen Analizada", use_column_width=True)
    
    with col_info:
        st.markdown("#### Resumen de Detección")
        auto = st.session_state.ficha['auto_data']
        st.info(f"Estado Sugerido: **{auto.get('aprobacion_final', 'PENDIENTE')}**")
        
        # Mostrar métricas clave
        c1, c2 = st.columns(2)
        c1.metric("Ancho Promedio", f"{auto.get('ancho_promedio', 0)} mm")
        c2.metric("Altura Refuerzo", f"{auto.get('altura_refuerzo', 0)} mm")
    
    st.markdown("---")
    st.markdown("#### Revisión de Datos Automáticos")
    st.caption("Puede ajustar manualmente los valores si la detección fue imprecisa.")
    
    with st.form("validation_form"):
        # Mostrar todos los campos automáticos para posible edición
        tabs = st.tabs(["Geometría", "Defectología", "Dimensionalidad"])
        
        with tabs[0]:
            for field in fc.GEOMETRIA_FIELDS["automatic"]:
                key = field["key"]
                st.text_input(field["label"], value=st.session_state.ficha['auto_data'].get(key, ""), key=f"val_{key}")
        
        with tabs[1]:
            for field in fc.DEFECTOLOGIA_FIELDS["automatic"]:
                key = field["key"]
                st.text_input(field["label"], value=st.session_state.ficha['auto_data'].get(key, ""), key=f"val_{key}")
                
        with tabs[2]:
            for field in fc.DIMENSIONALIDAD_FIELDS["automatic"]:
                key = field["key"]
                st.text_input(field["label"], value=st.session_state.ficha['auto_data'].get(key, ""), key=f"val_{key}")
        
        st.markdown("#### Validación Humana")
        obs = st.text_area("Observaciones del Inspector", key="observaciones_finales")
        veredicto = st.selectbox("Dictamen Final", ["APROBADO", "RECHAZADO"], index=0 if auto.get('aprobacion_final') == "ACEPTADO" else 1)
        
        if st.form_submit_button("Confirmar y Generar Reporte ➡️"):
            # Actualizar datos con los valores del formulario (si se editaron)
            for field_list in [fc.GEOMETRIA_FIELDS["automatic"], fc.DEFECTOLOGIA_FIELDS["automatic"], fc.DIMENSIONALIDAD_FIELDS["automatic"]]:
                for field in field_list:
                    st.session_state.ficha['auto_data'][field["key"]] = st.session_state[f"val_{field['key']}"]
            
            st.session_state.ficha['manual_data']['observaciones'] = obs
            st.session_state.ficha['manual_data']['veredicto_final'] = veredicto
            
            st.session_state.ficha['step'] = 4
            st.rerun()

    if st.button("⬅️ Volver a Inspección"):
        st.session_state.ficha['step'] = 2
        st.rerun()

# --- STEP 4: REPORTE ---
elif current_step == 4:
    st.markdown("### 📑 Fichas Técnicas Generadas")
    st.success("¡Proceso completado! Las fichas se han generado correctamente.")
    
    manual = st.session_state.ficha['manual_data']
    auto = st.session_state.ficha['auto_data']
    
    # Función helper para mostrar ficha
    def mostrar_ficha(titulo, fields_manual, fields_auto):
        st.markdown(f"#### {titulo}")
        data = {}
        # Combinar manual y auto
        for f in fields_manual:
            data[f["label"]] = manual.get(f["key"], "-")
        for f in fields_auto:
            data[f["label"]] = auto.get(f["key"], "-")
            
        df = pd.DataFrame(list(data.items()), columns=["Campo", "Valor"])
        st.table(df)
    
    tab_traz, tab_geom, tab_def, tab_dim = st.tabs(["Trazabilidad", "Geometría", "Defectología", "Dimensionalidad"])
    
    with tab_traz:
        mostrar_ficha("Ficha de Trazabilidad", fc.TRAZABILIDAD_FIELDS["manual"], fc.TRAZABILIDAD_FIELDS["automatic"])
        
    with tab_geom:
        mostrar_ficha("Ficha de Geometría de Cordón", fc.GEOMETRIA_FIELDS["manual"], fc.GEOMETRIA_FIELDS["automatic"])
        
    with tab_def:
        mostrar_ficha("Ficha de Defectología", fc.DEFECTOLOGIA_FIELDS["manual"], fc.DEFECTOLOGIA_FIELDS["automatic"])
        
    with tab_dim:
        mostrar_ficha("Ficha de Dimensionalidad", fc.DIMENSIONALIDAD_FIELDS["manual"], fc.DIMENSIONALIDAD_FIELDS["automatic"])

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Nueva Inspección"):
            reset_ficha()
            st.rerun()
    with col2:
        st.download_button("📥 Descargar Reporte (CSV)", data="Simulacion de descarga CSV", file_name="reporte.csv")
