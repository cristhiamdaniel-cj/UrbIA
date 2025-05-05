from rest_framework import serializers
from .models import Sensor, Lectura

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'


class LecturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lectura
        fields = '__all__'
