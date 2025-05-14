import requests
import time
import random

# Configuración
API_SENSORES = "http://127.0.0.1:8000/api/sensores/"
API_LECTURAS = "http://127.0.0.1:8000/api/lecturas/"

def obtener_sensores():
    try:
        response = requests.get(API_SENSORES)
        if response.status_code == 200:
            sensores = response.json()
            sensores_activos = [s for s in sensores if s['activo']]
            return sensores_activos
        else:
            print(f"⚠️ Error al obtener sensores: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return []

def generar_lectura(sensor):
    tipo = sensor['tipo']
    rangos = {
        "temperatura": (18, 38, "°C"),
        "humedad": (30, 100, "%"),
        "pm25": (5, 80, "µg/m³"),
        "co2": (400, 1200, "ppm"),
        "presion": (900, 1050, "hPa")
    }
    if tipo in rangos:
        min_val, max_val, unidad = rangos[tipo]
    else:
        # Default genérico si no está en los rangos
        min_val, max_val, unidad = 0, 100, "u"

    return {
        "sensor": sensor['id'],
        "valor": round(random.uniform(min_val, max_val), 2),
        "unidad": unidad
    }

def enviar_lectura(sensor):
    datos = generar_lectura(sensor)
    try:
        response = requests.post(API_LECTURAS, json=datos)
        if response.status_code == 201:
            print(f"✅ Lectura enviada: {datos}")
        else:
            print(f"⚠️ Error al enviar lectura: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    print("🌡️ Emulador de múltiples sensores iniciado...")
    sensores = obtener_sensores()
    
    if not sensores:
        print("🚫 No se encontraron sensores activos. Abortando...")
        exit(1)

    while True:
        sensor = random.choice(sensores)
        enviar_lectura(sensor)
        time.sleep(5)  # Puedes ajustar el tiempo entre lecturas

