from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task  # Indica que este formulario trabaja con el modelo Task
        fields = ['title', 'description', 'completed']  # Campos a mostrar en el formulario
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la tarea'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción opcional'}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
