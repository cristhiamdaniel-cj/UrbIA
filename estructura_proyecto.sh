#!/bin/bash

# Crear estructura básica del proyecto UrbIA
mkdir -p backend/{app,api,models,tests}
mkdir -p iot_ingest/{mqtt,http,simulators}
mkdir -p satellite/scripts
mkdir -p frontend/{dashboard,public}
mkdir -p docs
mkdir -p data/{raw,processed}
mkdir -p geo_simac
mkdir -p deploy
mkdir -p scripts

# Crear archivos iniciales
touch README.md
touch LICENSE
touch .gitignore
touch backend/__init__.py
touch iot_ingest/__init__.py
touch satellite/__init__.py
touch geo_simac/__init__.py
touch frontend/__init__.py

echo "Estructura del proyecto UrbIA creada con éxito 🚀"

