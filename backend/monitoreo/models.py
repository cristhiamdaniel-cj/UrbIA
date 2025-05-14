'''
from django.db import models

class Sensor(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)  # Ej: temperatura, PM2.5, humedad
    ubicacion = models.CharField(max_length=255)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"



class Lectura(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    valor = models.FloatField()
    unidad = models.CharField(max_length=20)  # Ej: °C, µg/m³, %

    def __str__(self):
        return f"{self.sensor.nombre} - {self.timestamp} - {self.valor}{self.unidad}"
'''

# backend/monitoreo/models.py

from django.db import models

class TipoSensor(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        managed = False
        db_table = 'tipo_sensor'

    def __str__(self):
        return self.nombre

class Sensor(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.ForeignKey(TipoSensor, on_delete=models.CASCADE, db_column='tipo_id')
    ubicacion = models.TextField(blank=True, null=True)
    latitud = models.FloatField(blank=True, null=True)
    longitud = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sensor'

    def __str__(self):
        return f"{self.nombre} ({self.tipo.nombre})"

class Lectura(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, db_column='sensor_id')
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    unidad = models.CharField(max_length=20, blank=True, null=True)
    timestamp = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'lectura'

    def __str__(self):
        return f"{self.sensor.nombre} - {self.timestamp} - {self.valor}{self.unidad}"
