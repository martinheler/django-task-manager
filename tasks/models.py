from django.contrib.auth.models import User
from django.db import models

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 🔹 Relación con el usuario
    title = models.CharField(max_length=255)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación

    def __str__(self):
        return self.title
