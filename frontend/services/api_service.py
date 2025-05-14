import requests
from datetime import datetime
from config.settings import SENSOR_URL, LECTURA_URL

# 🔥 Diccionario para traducir IDs a nombres
ID_TIPO_MAPA = {
    1: "temperatura",
    2: "humedad",
    3: "pm25",
    4: "co2",
    5: "presion"
}

class APIService:
    @staticmethod
    def get_sensores():
        try:
            resp = requests.get(SENSOR_URL)
            sensores = resp.json()
            # 🔥 Traducción de tipo_id a nombre
            for sensor in sensores:
                tipo_id = sensor.get("tipo")
                sensor["tipo"] = ID_TIPO_MAPA.get(tipo_id, "desconocido")
            return sensores
        except Exception as e:
            print(f"Error cargando sensores: {e}")
            return []

    @staticmethod
    def get_lecturas():
        try:
            resp = requests.get(LECTURA_URL)
            lecturas = resp.json()
            for lectura in lecturas:
                lectura["timestamp"] = datetime.fromisoformat(lectura["timestamp"].replace("Z", "+00:00"))
            return lecturas
        except Exception as e:
            print(f"Error cargando lecturas: {e}")
            return []
