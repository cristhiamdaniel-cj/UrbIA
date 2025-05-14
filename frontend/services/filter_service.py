class FilterService:
    @staticmethod
    def filtrar_sensores(sensores, tipos_seleccionados):
        return [s for s in sensores if s["tipo"] in tipos_seleccionados]

    @staticmethod
    def filtrar_lecturas(lecturas, sensores_filtrados, rango_fechas):
        lecturas_filtradas = []
        sensor_ids = [s["id"] for s in sensores_filtrados]
        if rango_fechas:
            fecha_inicio, fecha_fin = rango_fechas
        else:
            return lecturas_filtradas

        for lectura in lecturas:
            if lectura["sensor"] in sensor_ids:
                fecha_lectura = lectura["timestamp"].date()
                if fecha_inicio <= fecha_lectura <= fecha_fin:
                    lecturas_filtradas.append(lectura)
        return lecturas_filtradas

    @staticmethod
    def ultimas_lecturas_por_sensor(lecturas, n=10):
        """Devuelve el promedio de las últimas N lecturas por sensor."""
        lecturas_por_sensor = {}

        for lectura in sorted(lecturas, key=lambda x: x["timestamp"], reverse=True):
            sensor_id = lectura["sensor"]
            if sensor_id not in lecturas_por_sensor:
                lecturas_por_sensor[sensor_id] = []
            if len(lecturas_por_sensor[sensor_id]) < n:
                valor = lectura["valor"]
                if isinstance(valor, (int, float)):
                    lecturas_por_sensor[sensor_id].append(valor)
                else:
                    try:
                        lecturas_por_sensor[sensor_id].append(float(valor))
                    except Exception:
                        continue

        promedio_por_sensor = {}
        for sensor_id, valores in lecturas_por_sensor.items():
            if valores:
                promedio = sum(valores) / len(valores)
                promedio_por_sensor[sensor_id] = promedio

        return promedio_por_sensor
