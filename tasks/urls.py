from django.urls import path
from .views import task_list, task_create, task_update, task_delete

urlpatterns = [
    path('', task_list, name='task_list'),
    path('create/', task_create, name='task_create'),  # Crear una tarea
    path('update/<int:task_id>/', task_update, name='task_update'),  # Editar una tarea
    path('delete/<int:task_id>/', task_delete, name='task_delete'),  # Eliminar una tarea
]
