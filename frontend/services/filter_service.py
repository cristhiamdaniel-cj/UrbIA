class FilterService:
    @staticmethod
    def filtrar_sensores(sensores, tipos_seleccionados):
        return [s for s in sensores if s["tipo"] in tipos_seleccionados]

    @staticmethod
    def filtrar_lecturas(lecturas, sensores_filtrados, rango_fechas):
        lecturas_filtradas = []
        sensor_ids = [s["id"] for s in sensores_filtrados]  # <-- AQUÍ está bien
        for lectura in lecturas:
            if lectura["sensor"] in sensor_ids:  # <-- corregido
                fecha_lectura = lectura["timestamp"].date()
                if rango_fechas[0] <= fecha_lectura <= rango_fechas[1]:
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
                lecturas_por_sensor[sensor_id].append(lectura["valor"])

        promedio_por_sensor = {}
        for sensor_id, valores in lecturas_por_sensor.items():
            if valores:
                promedio = sum(valores) / len(valores)
                promedio_por_sensor[sensor_id] = promedio

        return promedio_por_sensor