import folium
from branca.element import Template, MacroElement
from config.settings import MAP_CENTER, MAP_ZOOM_START

class MapService:
    @staticmethod
    def crear_mapa(sensores, promedio_lecturas_por_sensor, tipo_seleccionado, mostrar_leyenda):
        m = folium.Map(location=MAP_CENTER, zoom_start=MAP_ZOOM_START, tiles="CartoDB positron")

        for sensor in sensores:
            lat = sensor.get("latitud")
            lon = sensor.get("longitud")
            if lat and lon:
                promedio = promedio_lecturas_por_sensor.get(sensor["id"]) if promedio_lecturas_por_sensor else None
                valor_mostrar = f"{round(promedio, 2)}" if promedio is not None else "N/A"

                color = "gray"
                if promedio is not None:
                    try:
                        valor_float = promedio
                        if tipo_seleccionado == "temperatura":
                            if valor_float < 25:
                                color = "blue"
                            elif valor_float < 30:
                                color = "orange"
                            else:
                                color = "red"
                        elif tipo_seleccionado == "humedad":
                            if valor_float < 50:
                                color = "blue"
                            elif valor_float < 80:
                                color = "orange"
                            else:
                                color = "red"
                        elif tipo_seleccionado == "pm25":
                            if valor_float < 12:
                                color = "blue"
                            elif valor_float < 35:
                                color = "orange"
                            else:
                                color = "red"
                        elif tipo_seleccionado == "co2":
                            if valor_float < 600:
                                color = "blue"
                            elif valor_float < 1000:
                                color = "orange"
                            else:
                                color = "red"
                        elif tipo_seleccionado == "presion":
                            if valor_float < 950:
                                color = "blue"
                            elif valor_float < 1000:
                                color = "orange"
                            else:
                                color = "red"
                    except:
                        color = "gray"

                url_grafica = f"/SensorDetail?sensor_id={sensor['id']}"


                popup_text = f"""
                <b>{sensor['nombre']}</b><br>
                Tipo: {sensor['tipo']}<br>
                Ubicación: {sensor['ubicacion']}<br>
                Promedio últimas lecturas: {valor_mostrar}<br>
                Lat/Lon: {lat}, {lon}<br><br>
                <a href="{url_grafica}" target="_blank">📈 Ver gráfica de mediciones</a>
                """



                folium.Marker(
                    location=[lat, lon],
                    popup=popup_text,
                    icon=folium.Icon(color=color, icon="info-sign")
                ).add_to(m)

        if mostrar_leyenda and tipo_seleccionado:
            MapService.agregar_leyenda(m, tipo_seleccionado)
        
        return m
    

    @staticmethod
    def agregar_leyenda(mapa, tipo_sensor):
        if tipo_sensor == "temperatura":
            legend_title = "Leyenda - Temperatura"
            rango1 = "Normal (<25°C)"
            rango2 = "Alerta (25–30°C)"
            rango3 = "Crítico (≥30°C)"
        elif tipo_sensor == "humedad":
            legend_title = "Leyenda - Humedad"
            rango1 = "Baja (<50%)"
            rango2 = "Moderada (50–80%)"
            rango3 = "Alta (≥80%)"
        elif tipo_sensor == "pm25":
            legend_title = "Leyenda - PM2.5"
            rango1 = "Buena (<12 µg/m³)"
            rango2 = "Moderada (12–35 µg/m³)"
            rango3 = "Peligrosa (>35 µg/m³)"
        elif tipo_sensor == "co2":
            legend_title = "Leyenda - CO₂"
            rango1 = "Excelente (<600 ppm)"
            rango2 = "Aceptable (600–1000 ppm)"
            rango3 = "Mala (>1000 ppm)"
        else:
            legend_title = "Leyenda General"
            rango1 = "Valor bajo"
            rango2 = "Valor moderado"
            rango3 = "Valor alto"

        legend_html = f"""
        {{% macro html(this, kwargs) %}}
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
        <b>📘 {legend_title}</b><br>
        <i style="background:blue; width:12px; height:12px; display:inline-block;"></i> {rango1}<br>
        <i style="background:orange; width:12px; height:12px; display:inline-block;"></i> {rango2}<br>
        <i style="background:red; width:12px; height:12px; display:inline-block;"></i> {rango3}<br>
        <i style="background:gray; width:12px; height:12px; display:inline-block;"></i> Sin dato
        </div>
        {{% endmacro %}}
        """
        legend = MacroElement()
        legend._template = Template(legend_html)
        mapa.get_root().add_child(legend)
