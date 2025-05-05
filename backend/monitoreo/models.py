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
