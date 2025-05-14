import requests
from datetime import datetime
from config.settings import SENSOR_URL, LECTURA_URL

class APIService:
    @staticmethod
    def get_sensores():
        try:
            resp = requests.get(SENSOR_URL)
            sensores = resp.json()
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
