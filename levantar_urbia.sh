#!/bin/bash

# Activar entorno virtual
source venv/bin/activate

# Levantar backend Django en segundo plano
echo "🚀 Levantando Backend Django..."
cd backend
python manage.py runserver > ../logs_backend.log 2>&1 &
cd ..

# Esperar unos segundos para asegurar que backend esté listo
sleep 3

# Levantar emulador de sensores
echo "🌡️ Iniciando Emulador de Sensores..."
python iot_ingest/simulators/emulador_sensor.py > logs_emulador.log 2>&1 &

# Levantar frontend Streamlit
echo "🗺️ Iniciando Frontend Dashboard..."
cd frontend/dashboard
streamlit run streamlit_mapa.py > ../../logs_frontend.log 2>&1 &

# Mensaje final
echo "✅ Todo levantado. Puedes abrir http://localhost:8501 para ver el dashboard."

wait

