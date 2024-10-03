from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task  # Specify the model to use
        fields = ['task_name', 'description', 'priority', 'deadline']  # Fields to include in the form


class Task_edit(forms.ModelForm):
    class Meta:
        model = Task  # Specify the model to use
        fields = ['task_name', 'description', 'priority','status', 'deadline']

