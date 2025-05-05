# 🌎 UrbIA - Plataforma Abierta de Monitoreo Urbano Inteligente

_UrbIA_ es una plataforma modular, de código abierto, desarrollada para el monitoreo urbano inteligente, iniciando con variables climáticas y de calidad del aire en Manizales, Colombia. Está diseñada para ser escalable, replicable y mantenida por la comunidad académica y ciudadana.

## 🧩 Arquitectura de componentes

- **backend/**: API en Django para gestión de datos, sensores y usuarios
- **iot_ingest/**: scripts y configuraciones para recibir datos vía MQTT/HTTP
- **satellite/**: módulos para consulta de imágenes satelitales (Copernicus)
- **geo_simac/**: comparación con datos del Geoportal SIMAC (UNAL)
- **frontend/**: dashboards de visualización (Home Assistant / Streamlit)
- **data/**: archivos de datos (crudos y procesados)
- **docs/**: documentación técnica, manuales y propuestas
- **scripts/**: utilidades generales de automatización

## 🛠 Tecnologías utilizadas

- Python / Django / PostgreSQL
- MQTT / HTTP / ThingsBoard
- API Sentinel / Copernicus
- Home Assistant / Streamlit
- Git + GitHub + MkDocs

## 🚀 Estado del proyecto

- [x] Estructura inicial
- [ ] Nodo IoT funcional
- [ ] Ingesta de datos a backend
- [ ] Dashboard local y remoto
- [ ] Integración satelital
- [ ] Comparación SIMAC

## 🤝 Cómo contribuir

1. Haz un fork del repositorio
2. Clona tu fork: `git clone https://github.com/tu_usuario/UrbIA.git`
3. Crea una rama: `git checkout -b feature/nombre-funcionalidad`
4. Haz tus cambios y realiza commits claros
5. Envía un pull request

## 📄 Licencia

Este proyecto está licenciado bajo la [MIT License](LICENSE).

---

*Desarrollado en la Universidad Nacional de Colombia - Sede Manizales. Proyecto de investigación doctoral.*
