from datetime import datetime, timezone
import requests
import time
import random

# Configuración de API
API_SENSORES = "http://127.0.0.1:8000/api/sensores/"
API_LECTURAS = "http://127.0.0.1:8000/api/lecturas/"

# Mapas de tipos
ID_TIPO_MAPA = {
    1: "temperatura",
    2: "humedad",
    3: "pm25",
    4: "co2",
    5: "presion"
}

RANGOS = {
    "temperatura": (18, 38, "°C"),
    "humedad": (30, 100, "%"),
    "pm25": (5, 80, "µg/m³"),
    "co2": (400, 1200, "ppm"),
    "presion": (900, 1050, "hPa")
}

def obtener_sensores():
    """Obtiene sensores válidos del backend."""
    try:
        response = requests.get(API_SENSORES)
        if response.status_code == 200:
            sensores = response.json()
            sensores_validos = [s for s in sensores if s.get('tipo') in ID_TIPO_MAPA]
            print(f"🔎 {len(sensores_validos)} sensores válidos encontrados.")
            return sensores_validos
        else:
            print(f"⚠️ Error al obtener sensores: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error de conexión al obtener sensores: {e}")
        return []

def generar_lectura(sensor):
    """Genera una lectura falsa según el tipo del sensor."""
    tipo_id = sensor.get('tipo')
    tipo_nombre = ID_TIPO_MAPA.get(tipo_id)

    if tipo_nombre in RANGOS:
        min_val, max_val, unidad = RANGOS[tipo_nombre]
    else:
        min_val, max_val, unidad = 0, 100, "u"

    return {
        "sensor": sensor.get('id'),
        "valor": round(float(random.uniform(min_val, max_val)), 2),
        "unidad": unidad,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

def enviar_lectura(sensor):
    """Envía una lectura generada y muestra la respuesta detallada."""
    datos = generar_lectura(sensor)
    try:
        response = requests.post(API_LECTURAS, json=datos)

        if response.status_code == 201:
            print(f"✅ [201] Lectura enviada correctamente:\n{datos}\n")
        else:
            print(f"⚠️ [ERROR {response.status_code}] Falló el envío:")
            print(f"   ➔ Datos enviados: {datos}")
            print(f"   ➔ Respuesta del servidor: {response.text}\n")

    except Exception as e:
        print(f"❌ Error de conexión al enviar lectura: {e}")

if __name__ == "__main__":
    print("🌡️ Emulador de múltiples sensores iniciado...")

    sensores = obtener_sensores()

    if not sensores:
        print("🚫 No se encontraron sensores válidos. Abortando...")
        exit(1)

    while True:
        for sensor in sensores:
            enviar_lectura(sensor)
            time.sleep(0.2)  # Pequeña pausa entre lecturas para no saturar

        print("⏳ Esperando 5 segundos para el siguiente ciclo...\n")
        time.sleep(5)  # Espera entre ciclos completos
