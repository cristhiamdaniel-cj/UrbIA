import requests
import random
import time

API_SENSORES = "http://127.0.0.1:8000/api/sensores/"
API_LECTURAS = "http://127.0.0.1:8000/api/lecturas/"

# Rangos por tipo de sensor
rangos = {
    "temperatura": (18, 38, "°C"),
    "humedad": (30, 100, "%"),
    "pm25": (5, 80, "µg/m³"),
    "co2": (400, 1200, "ppm"),
    "presion": (900, 1050, "hPa")
}

# Obtener sensores activos
resp = requests.get(API_SENSORES)
sensores = resp.json()

for sensor in sensores:
    tipo = sensor["tipo"]
    sensor_id = sensor["id"]
    if tipo not in rangos:
        continue

    min_val, max_val, unidad = rangos[tipo]
    valor = round(random.uniform(min_val, max_val), 2)

    payload = {
        "sensor": sensor_id,
        "valor": valor,
        "unidad": unidad
    }

    r = requests.post(API_LECTURAS, json=payload)
    if r.status_code == 201:
        print(f"✅ Lectura enviada: Sensor {sensor_id} → {valor} {unidad}")
    else:
        print(f"❌ Error en sensor {sensor_id}: {r.status_code} - {r.text}")

time.sleep(1)
