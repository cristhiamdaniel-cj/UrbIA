# 🌎 UrbIA - Plataforma Abierta de Monitoreo Urbano Inteligente

*UrbIA* es una plataforma modular y de código abierto para el monitoreo urbano en tiempo real. Iniciamos con variables climáticas y de calidad del aire en Manizales, Colombia.
Está diseñada para ser **escalable, replicable y mantenida por la comunidad académica**.

## 🏦 Estructura general del proyecto

* **backend/**: API REST en Django conectada a PostgreSQL
* **frontend/**: Dashboards de visualización interactiva en Streamlit
* **iot\_ingest/**: Scripts de emulación y recepción de datos de sensores
* **data/**: Archivos de apoyo para pruebas y configuraciones iniciales
* **docs/**: Documentación técnica y manuales de operación

## 🛠️ Tecnologías principales

* **Python 3.12**, **Django 5.2**, **PostgreSQL 16**
* **Streamlit** para visualización web
* **Folium** para mapas georreferenciados
* **Altair** para gráficos de series de tiempo
* **Requests** para comunicación HTTP API
* **Docker** (en preparación para despliegue futuro)

## 🔥 Funcionalidades implementadas

* Registro automático de lecturas de sensores en base de datos
* Emulador de múltiples sensores con variabilidad controlada
* Filtro dinámico por tipo de sensor y rango de fecha en frontend
* Cálculo de KPIs de monitoreo: sensores activos, promedio, máximo y mínimo
* Mapa interactivo de ubicación de sensores en tiempo real
* Gráficas detalladas por sensor, exportables a CSV
* Integración completa Django ↔️ Streamlit sin pérdida de sincronía

## 🚀 Estado actual del proyecto

| Componente                                            | Estado          |
| :---------------------------------------------------- | :-------------- |
| Estructura API backend                                | ✅ Completa      |
| Conexión a base de datos                              | ✅ Completa      |
| Emulador de sensores                                  | ✅ Completo      |
| Dashboard web principal                               | ✅ Completo      |
| Filtros avanzados y KPIs                              | ✅ Completo      |
| Integración con servicios externos (satelital, SIMAC) | ⏳ En desarrollo |

## 🤝 Cómo contribuir

1. Haz un **fork** del repositorio
2. Clona tu fork:

   ```bash
   git clone https://github.com/tu_usuario/UrbIA.git
   ```
3. Crea una rama:

   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
4. Realiza tus cambios, escribe commits descriptivos
5. Envía un **pull request** para revisión

## 📄 Licencia

Este proyecto está licenciado bajo la [MIT License](LICENSE).

---

> *Desarrollado en la Universidad Nacional de Colombia - Sede Manizales.*
> *Proyecto de investigación doctoral sobre plataformas abiertas de monitoreo urbano.*
