import requests
import random

API_URL = "http://127.0.0.1:8000/api/sensores/"

# Coordenadas aproximadas de Manizales
LAT_MIN, LAT_MAX = 5.03, 5.08
LON_MIN, LON_MAX = -75.55, -75.49

tipos = ["temperatura", "humedad", "pm25", "co2", "presion"]
ubicaciones = ["Chipre", "Palogrande", "La Enea", "Centro", "Villa Hermosa", "San Jorge"]

for i in range(1, 101):
    payload = {
        "nombre": f"Sensor_{i:03d}",
        "tipo": random.choice(tipos),
        "ubicacion": f"Barrio {random.choice(ubicaciones)}",
        "latitud": round(random.uniform(LAT_MIN, LAT_MAX), 6),
        "longitud": round(random.uniform(LON_MIN, LON_MAX), 6),
        "descripcion": "Sensor generado automáticamente",
        "activo": True
    }

    response = requests.post(API_URL, json=payload)
    if response.status_code == 201:
        print(f"✅ Sensor {payload['nombre']} creado.")
    else:
        print(f"❌ Error al crear {payload['nombre']}: {response.status_code} - {response.text}")
