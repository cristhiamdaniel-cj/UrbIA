import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
from branca.element import Template, MacroElement

st.set_page_config(page_title="Mapa de Sensores - UrbIA", layout="wide")

# --- URLs de la API ---
SENSOR_URL = "http://127.0.0.1:8000/api/sensores/"
LECTURA_URL = "http://127.0.0.1:8000/api/lecturas/"

# --- Obtener sensores ---
try:
    sensores_resp = requests.get(SENSOR_URL)
    sensores = sensores_resp.json()
except Exception as e:
    st.error(f"❌ Error cargando sensores: {e}")
    sensores = []

# --- Obtener lecturas ---
try:
    lecturas_resp = requests.get(LECTURA_URL)
    lecturas = lecturas_resp.json()
except Exception as e:
    st.error(f"❌ Error cargando lecturas: {e}")
    lecturas = []

# --- Última lectura por sensor ---
ultima_lectura_por_sensor = {}
for lectura in lecturas:
    sensor_id = lectura["sensor"]
    if sensor_id not in ultima_lectura_por_sensor:
        ultima_lectura_por_sensor[sensor_id] = lectura
    elif lectura["timestamp"] > ultima_lectura_por_sensor[sensor_id]["timestamp"]:
        ultima_lectura_por_sensor[sensor_id] = lectura

# --- Crear mapa ---
m = folium.Map(location=[5.07, -75.52], zoom_start=13, tiles="CartoDB positron")

# --- Agregar sensores al mapa ---
for sensor in sensores:
    lat = sensor.get("latitud")
    lon = sensor.get("longitud")
    if lat and lon:
        lectura = ultima_lectura_por_sensor.get(sensor["id"])
        valor = lectura["valor"] if lectura else "N/A"
        unidad = lectura["unidad"] if lectura else ""

        # --- Lógica de color ---
        color = "gray"
        try:
            valor_float = float(valor)
            if valor_float < 25:
                color = "blue"
            elif valor_float < 30:
                color = "orange"
            else:
                color = "red"
        except:
            color = "gray"

        # --- Contenido del popup ---
        popup_text = f"""
        <b>{sensor['nombre']}</b><br>
        Tipo: {sensor['tipo']}<br>
        Ubicación: {sensor['ubicacion']}<br>
        Último valor: {valor} {unidad}<br>
        Lat/Lon: {lat}, {lon}
        """

        folium.Marker(
            location=[lat, lon],
            popup=popup_text,
            icon=folium.Icon(color=color, icon="info-sign")
        ).add_to(m)

# --- Agregar leyenda visual ---
legend_html = """
{% macro html(this, kwargs) %}
<div style="
    position: fixed;
    bottom: 150px; left: 20px; width: 220px;
    z-index:9999;
    font-size:14px;
    background-color: rgba(255,255,255,0.95);
    padding: 10px;
    border: 1px solid #999;
    border-radius: 6px;
    box-shadow: 0 0 10px rgba(0,0,0,0.3);
    color: black;
    font-family: sans-serif;
">
<b>📘 Leyenda - Temperatura</b><br>
<i style="background:blue; width:12px; height:12px; display:inline-block;"></i> Normal (&lt; 25°C)<br>
<i style="background:orange; width:12px; height:12px; display:inline-block;"></i> Alerta (25–30°C)<br>
<i style="background:red; width:12px; height:12px; display:inline-block;"></i> Crítico (&ge; 30°C)<br>
<i style="background:gray; width:12px; height:12px; display:inline-block;"></i> Sin dato
</div>
{% endmacro %}
"""


legend = MacroElement()
legend._template = Template(legend_html)
m.get_root().add_child(legend)

# --- Mostrar en Streamlit ---
st.title("🗺️ Mapa de Sensores - Proyecto UrbIA")
st_folium(m, width=1200, height=600)
