import requests
import time
import random

# Configuración del sensor
SENSOR_ID = 1  # Cambia este ID por el del sensor que creaste vía API
API_URL = "http://127.0.0.1:8000/api/lecturas/"

def generar_lectura():
    return {
        "sensor": SENSOR_ID,
        "valor": round(random.uniform(18.0, 25.0), 2),
        "unidad": "°C"
    }

def enviar_lectura():
    datos = generar_lectura()
    try:
        response = requests.post(API_URL, json=datos)
        if response.status_code == 201:
            print(f"✅ Lectura enviada: {datos}")
        else:
            print(f"⚠️ Error al enviar lectura: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    print("🌡️ Emulador de sensor iniciado...")
    while True:
        enviar_lectura()
        time.sleep(10)  # espera 10 segundos entre lecturas
