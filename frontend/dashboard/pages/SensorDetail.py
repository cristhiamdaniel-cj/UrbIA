import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import altair as alt
from services.api_service import APIService

st.set_page_config(page_title="Detalle del Sensor", layout="wide")

# --- Obtener parámetros de la URL
query_params = st.query_params
sensor_id = query_params.get("sensor_id", [None])[0]

if sensor_id is None:
    st.error("❌ No se especificó ningún sensor.")
    st.stop()

# --- Botón de actualización
if st.button("🔄 Actualizar Gráfico"):
    st.rerun()

# --- Obtener sensores y lecturas
sensores = APIService.get_sensores()
lecturas = APIService.get_lecturas()

# --- Encontrar el sensor
sensor_info = next((s for s in sensores if str(s["id"]) == sensor_id), None)

if not sensor_info:
    st.error("❌ Sensor no encontrado.")
    st.stop()

# --- Mostrar información básica
st.title(f"📈 Gráfica del Sensor: {sensor_info['nombre']}")

# --- Filtrar lecturas de este sensor
lecturas_sensor = [l for l in lecturas if str(l["sensor"]) == sensor_id]
lecturas_sensor = sorted(lecturas_sensor, key=lambda x: x["timestamp"], reverse=True)

if not lecturas_sensor:
    st.warning("⚠️ No hay lecturas disponibles para este sensor.")
else:
    df = pd.DataFrame(lecturas_sensor)
    df["Fecha"] = pd.to_datetime(df["timestamp"])
    df["Valor"] = pd.to_numeric(df["valor"], errors="coerce")  # 🔥 Conversión segura a número
    unidad = lecturas_sensor[0].get("unidad", "") or ""  # Capturamos unidad si existe
    df["Unidad"] = unidad

    # --- 🔥 Selector de cantidad de lecturas
    cantidad_mostrar = st.selectbox(
        "📈 ¿Cuántas últimas mediciones quieres visualizar?",
        options=[10, 20, 50],
        index=0
    )

    df = df.head(cantidad_mostrar)
    df = df.sort_values("Fecha")  # Ordenar cronológicamente

    # --- 🔥 Mostrar tarjetas KPI
    kpi1, kpi2, kpi3 = st.columns(3)

    total_lecturas = len(df)
    promedio_valores = round(df["Valor"].mean(), 2) if not df["Valor"].isna().all() else 0
    fecha_ultima = df["Fecha"].max().strftime("%Y-%m-%d %H:%M:%S") if not df.empty else "N/A"

    kpi1.metric(label="📊 Total de Mediciones", value=total_lecturas)
    kpi2.metric(label="📈 Promedio de Valor", value=f"{promedio_valores} {unidad}")
    kpi3.metric(label="📅 Última Medición", value=fecha_ultima)

    st.divider()

    # --- 🔥 Gráfico de líneas
    chart = alt.Chart(df).mark_line(point=True).encode(
        x="Fecha:T",
        y="Valor:Q"
    ).properties(
        width=800,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)

    st.divider()

    # --- 🔥 Botón para descargar CSV
    csv = df[["Fecha", "Valor", "Unidad"]].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Descargar mediciones en CSV",
        data=csv,
        file_name=f"{sensor_info['nombre']}_mediciones.csv",
        mime="text/csv"
    )

# --- 🔙 Botón para volver al mapa
st.markdown("<br>", unsafe_allow_html=True)
st.page_link("Home.py", label="🗺️ Volver al Mapa", icon="🌍")
