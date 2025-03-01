from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task  # Indica que usamos el modelo Task
        fields = '__all__'  # Incluye todos los campos del modelo
