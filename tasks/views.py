from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm

form = TaskForm()  # Instancia del formulario
# 📌 1️⃣ Ver lista de tareas
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

# 📌 2️⃣ Crear una tarea
def task_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        Task.objects.create(title=title, description=description)
        return redirect('task_list')  # Redirige a la lista de tareas
    return render(request, 'tasks/task_form.html', {'form': form})  # Muestra el formulario

# 📌 3️⃣ Editar una tarea
def task_update(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.completed = request.POST.get('completed') == 'on'
        task.save()
        return redirect('task_list')
    return render(request, 'tasks/task_form.html', {'form': form})  # Reutilizamos la plantilla

# 📌 4️⃣ Eliminar una tarea
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':  # Si el usuario confirma la eliminación
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

