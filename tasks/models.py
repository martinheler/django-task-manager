from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)  # Título de la tarea
    description = models.TextField(blank=True)  # Descripción opcional
    completed = models.BooleanField(default=False)  # Estado de la tarea
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación

    def __str__(self):
        return self.title
