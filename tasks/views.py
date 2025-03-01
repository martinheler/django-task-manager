from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.contrib.auth.models import User
from .forms import TaskForm
from .serializers import TaskSerializer, UserSerializer
from rest_framework import viewsets, permissions, generics
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect

# 📌 1️⃣ Ver lista de tareas
def task_list(request):
    if not request.user.is_authenticated:  # ✅ Corrección aquí
        return redirect('login_page')
    
    if request.user.is_staff:
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(user=request.user)
    
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

# 📌 2️⃣ Crear una tarea (Corrección)
def task_create(request):
    if not request.user.is_authenticated:  # 🚨 Asegura que el usuario esté logueado
        return redirect('login_page')

    form = TaskForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        task = form.save(commit=False)  # ⏳ No guarda aún la tarea en la BD
        task.user = request.user  # 🔹 Asigna el usuario autenticado
        task.save()  # 🔹 Guarda la tarea con el usuario asignado
        return redirect('task_list')

    return render(request, 'tasks/task_form.html', {'form': form})


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
    if request.user.is_authenticated:
        return redirect('task_list')  # Si ya está autenticado, va a la lista de tareas

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('task_list')  # Redirigir al usuario después del login
        else:
            messages.error(request, "Invalid username or password")  # Mensaje de error

    return render(request, 'tasks/login.html')  # Renderizar el formulario de login

def logout_view(request):
    logout(request)  # 🔹 Cierra la sesión del usuario
    return redirect('login_page')  # 🔹 Redirige a la página de login

# 📌 5️⃣ API con Django REST Framework (DRF)
class TaskViewSet(viewsets.ModelViewSet):
    """
    API REST para gestionar tareas
    """

    def get_queryset(self):
        """ 
        - Los administradores ven todas las tareas.
        - Los usuarios normales solo ven sus propias tareas.
        """
        user = self.request.user
        if user.is_staff:  # 🔹 Si el usuario es admin, ve todas las tareas
            return Task.objects.all()
        return Task.objects.filter(user=user)  # 🔹 Si no, solo sus tareas

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