
# Definición de campos para las Fichas Técnicas

# Ficha de Trazabilidad
TRAZABILIDAD_FIELDS = {
    "manual": [
        {"label": "Soldador (Nombre/Código)", "key": "soldador", "type": "text"},
        {"label": "Máquina de Soldar (Modelo/Potencia)", "key": "maquina", "type": "text"},
        {"label": "Proceso", "key": "proceso", "type": "text"},
        {"label": "WPS Aplicado", "key": "wps", "type": "text"},
        {"label": "Material Base (Norma/Lote/Espesor)", "key": "material_base", "type": "text"},
        {"label": "Consumible (Tipo/Lote/Fabricante)", "key": "consumible", "type": "text"},
        {"label": "Voltaje (V)", "key": "voltaje", "type": "number", "step": 0.1},
        {"label": "Corriente (A)", "key": "amperaje", "type": "number", "step": 1.0},
        {"label": "Velocidad de Avance (cm/min)", "key": "velocidad", "type": "number", "step": 0.1},
        {"label": "Caudal de Gas (L/min)", "key": "gas", "type": "number", "step": 0.5},
        {"label": "Temperatura Ambiente (°C)", "key": "temp_amb", "type": "number", "step": 0.5},
    ],
    "automatic": [
        {"label": "Código Único de Cordón", "key": "id_cordon"},
        {"label": "Imagen del Cordón", "key": "img_cordon"},
        {"label": "Mapa de Defectos", "key": "mapa_defectos"},
        {"label": "Perfil Geométrico", "key": "perfil_geom"},
        {"label": "Reporte Exportado", "key": "reporte_pdf"},
        {"label": "Aprobación Final", "key": "aprobacion_final"},
    ]
}

# Ficha de Geometría de Cordón
GEOMETRIA_FIELDS = {
    "manual": [
        {"label": "Distancia Cámara-Pieza (mm)", "key": "distancia_camara", "type": "number", "step": 1.0},
        {"label": "Tipo de Junta", "key": "tipo_junta", "type": "text"},
    ],
    "automatic": [
        {"label": "Ancho Promedio (W) [mm]", "key": "ancho_promedio"},
        {"label": "Altura del Refuerzo (H) [mm]", "key": "altura_refuerzo"},
        {"label": "Radio de Curvatura [mm]", "key": "radio_curvatura"},
        {"label": "Simetría del Cordón [%]", "key": "simetria"},
        {"label": "Ángulo de Mojado L [°]", "key": "angulo_mojado_l"},
        {"label": "Ángulo de Mojado R [°]", "key": "angulo_mojado_r"},
        {"label": "Rugosidad Aparente [Índice]", "key": "rugosidad"},
        {"label": "Secciones Críticas [mm pos]", "key": "secciones_criticas"},
    ]
}

# Ficha de Defectología
DEFECTOLOGIA_FIELDS = {
    "manual": [
        {"label": "Norma de Referencia", "key": "norma", "type": "selectbox", "options": ["ISO 5817", "AWS D1.1", "API 1104", "ASME IX"]},
        # Soldador y Material se heredan de Trazabilidad, pero se pueden mostrar como read-only o re-ingresar si cambia
    ],
    "automatic": [
        {"label": "Poros (Cant/Diám)", "key": "def_poros"},
        {"label": "Porosidad Lineal (Long)", "key": "def_porosidad_lineal"},
        {"label": "Socavado (Prof/Long)", "key": "def_socavado"},
        {"label": "Grietas Superficiales (Long)", "key": "def_grietas"},
        {"label": "Falta de Fusión (% Área)", "key": "def_falta_fusion"},
        {"label": "Exceso de Refuerzo (Alt)", "key": "def_exceso_refuerzo"},
        {"label": "Mordeduras (Cant/Long)", "key": "def_mordeduras"},
        {"label": "Spatter Excesivo (% Sup)", "key": "def_spatter"},
        {"label": "Cordón Irregular (Índice)", "key": "def_irregular"},
    ]
}

# Ficha de Dimensionalidad
DIMENSIONALIDAD_FIELDS = {
    "manual": [
        {"label": "Componente/Spool/Pipe", "key": "componente", "type": "text"},
        {"label": "Número de Junta", "key": "num_junta", "type": "text"},
        {"label": "Proyecto / OT", "key": "proyecto_ot", "type": "text"},
        {"label": "Preparación de la Junta", "key": "prep_junta", "type": "text"},
        {"label": "Longitud Total a Soldar (mm)", "key": "longitud_total", "type": "number", "step": 1.0},
    ],
    "automatic": [
        {"label": "Ancho del Cordón (W) [mm]", "key": "dim_ancho"},
        {"label": "Altura del Refuerzo (H) [mm]", "key": "dim_altura"},
        {"label": "Ángulo Mojado Izq [°]", "key": "dim_angulo_l"},
        {"label": "Ángulo Mojado Der [°]", "key": "dim_angulo_r"},
        {"label": "Uniformidad (% Desv)", "key": "dim_uniformidad"},
        {"label": "Rectitud (mm Desv)", "key": "dim_rectitud"},
        {"label": "Penetración Visible [mm]", "key": "dim_penetracion"},
    ]
}
