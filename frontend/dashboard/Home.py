import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from streamlit_folium import st_folium
from services.api_service import APIService
from services.filter_service import FilterService
from services.map_service import MapService

st.set_page_config(page_title="Mapa de Sensores - UrbIA", layout="wide")

# --- Botón manual de actualización
if st.button("🔄 Actualizar Lecturas"):
    st.rerun()


# --- Cargar datos
sensores = APIService.get_sensores()
lecturas = APIService.get_lecturas()

# --- Filtros de tipo y fecha
tipos_sensores = sorted(set(sensor["tipo"] for sensor in sensores))
filtro_tipo = st.multiselect(
    "📚 Filtrar por tipo de sensor:",
    tipos_sensores,
    default=[]
)

if lecturas:
    fechas = [l["timestamp"] for l in lecturas]
    fecha_min, fecha_max = min(fechas).date(), max(fechas).date()
else:
    fecha_min = fecha_max = st.date_input("📅 No hay datos disponibles")

filtro_fecha = st.date_input(
    "📅 Filtrar por rango de fechas:",
    (fecha_min, fecha_max),
    min_value=fecha_min,
    max_value=fecha_max
)

# --- Aplicar filtros
if filtro_tipo:
    sensores_filtrados = FilterService.filtrar_sensores(sensores, filtro_tipo)
    lecturas_filtradas = FilterService.filtrar_lecturas(lecturas, sensores_filtrados, filtro_fecha)
    ultimas_lecturas = FilterService.ultimas_lecturas_por_sensor(lecturas_filtradas, n=10)
else:
    sensores_filtrados = []
    ultimas_lecturas = {}

if not ultimas_lecturas:
    ultimas_lecturas = {}

# --- 🔥 Cálculo de estadísticas
cantidad_sensores = len(sensores_filtrados)
promedios = list(ultimas_lecturas.values())

if promedios:
    promedio_general = round(sum(promedios) / len(promedios), 2)
    id_sensor_max = max(ultimas_lecturas, key=ultimas_lecturas.get)
    id_sensor_min = min(ultimas_lecturas, key=ultimas_lecturas.get)

    nombre_sensor_max = next((s["nombre"] for s in sensores_filtrados if s["id"] == id_sensor_max), "N/A")
    nombre_sensor_min = next((s["nombre"] for s in sensores_filtrados if s["id"] == id_sensor_min), "N/A")

    valor_max = round(ultimas_lecturas[id_sensor_max], 2)
    valor_min = round(ultimas_lecturas[id_sensor_min], 2)
else:
    promedio_general = 0
    nombre_sensor_max = "N/A"
    nombre_sensor_min = "N/A"
    valor_max = 0
    valor_min = 0

# --- 🔥 Mostrar tarjetas KPI
st.title("🗺️ Mapa de Sensores - Proyecto UrbIA")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric(label="📍 Sensores Filtrados", value=cantidad_sensores)
kpi2.metric(label="📈 Promedio General", value=f"{promedio_general}")
kpi3.metric(label="🔺 Máximo", value=f"{nombre_sensor_max} ({valor_max})")
kpi4.metric(label="🔻 Mínimo", value=f"{nombre_sensor_min} ({valor_min})")

st.divider()

# --- Crear mapa
mostrar_leyenda = (len(filtro_tipo) == 1)
tipo_seleccionado = filtro_tipo[0] if mostrar_leyenda else None

m = MapService.crear_mapa(sensores_filtrados, ultimas_lecturas, tipo_seleccionado, mostrar_leyenda)

st_folium(m, width=1200, height=600)

# --- Mensaje de advertencia si no hay lecturas
if not ultimas_lecturas:
    st.warning("⚠️ No hay lecturas recientes para los sensores seleccionados. Se muestran en gris.")
