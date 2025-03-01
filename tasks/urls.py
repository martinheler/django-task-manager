from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import task_list, task_create, task_update, task_delete, register_page, login_page, logout_view



urlpatterns = [
    path('', task_list, name='task_list'),
    path('create/', task_create, name='task_create'),  # Crear una tarea
    path('update/<int:task_id>/', task_update, name='task_update'),  # Editar una tarea
    path('delete/<int:task_id>/', task_delete, name='task_delete'),  # Eliminar una tarea
    path('register/', register_page, name='register_page'),  # GUI para registro
    path('login/', login_page, name='login_page'),  # GUI para inicio de sesion
    path('logout/', logout_view, name='logout_page'),  # Cerrar sesion
]
