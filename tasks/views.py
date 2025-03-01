from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.contrib.auth.models import User
from .forms import TaskForm
from .serializers import TaskSerializer, UserSerializer
from rest_framework import viewsets, permissions, generics
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render, redirect

# 📌 1️⃣ Ver lista de tareas
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

# 📌 2️⃣ Crear una tarea (Corrección)
def task_create(request):
    form = TaskForm(request.POST or None)  # ✅ Inicializamos el formulario correctamente
    if request.method == 'POST' and form.is_valid():
        form.save()  # ✅ Guardamos correctamente la nueva tarea
        return redirect('task_list')
    return render(request, 'tasks/task_form.html', {'form': form})  # ✅ Enviamos el formulario a la plantilla

# 📌 3️⃣ Editar una tarea (Corrección)
def task_update(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    form = TaskForm(request.POST or None, instance=task)  # ✅ Se usa la instancia correcta
    if request.method == 'POST' and form.is_valid():
        form.save()  # ✅ Se guardan los cambios
        return redirect('task_list')
    return render(request, 'tasks/task_form.html', {'form': form})  # ✅ Se pasa el formulario correcto

# 📌 4️⃣ Eliminar una tarea (Corrección)
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':  # ✅ Verificamos si es POST antes de eliminar
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})  # ✅ Se pasa la tarea correcta

def register_page(request):
    return render(request, 'tasks/register.html')

def login_page(request):
    """
    Muestra la página de login. Si el usuario ya está autenticado, lo redirige a /tasks/.
    """
    if request.user.is_authenticated:
        return redirect('task_list')  # 🔹 Si ya está autenticado, va a /tasks/
    
    return render(request, 'tasks/login.html')  # 🔹 Si no, muestra la página de login

# 📌 5️⃣ API con Django REST Framework (DRF)
class TaskViewSet(viewsets.ModelViewSet):
    """
    API REST para gestionar tareas
    """

    def get_queryset(self):
        """ Ensure users only see their own tasks """
        return Task.objects.filter(user=self.request.user)  # 🔹 Filter by logged-in user

    def perform_create(self, serializer):
        """ Assign the task to the authenticated user """
        serializer.save(user=self.request.user)  # 🔹 Assigns task to logged-in user
    
    serializer_class = TaskSerializer  # Usa el serializador para convertir los datos
    permission_classes = [permissions.IsAuthenticated]  # 🔹 Protegemos la API

class RegisterUserView(generics.CreateAPIView):
    """
    API endpoint to register new users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]