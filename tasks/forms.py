# from django.forms import ModelForm
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        # Esto es para estilizar los fields
        widgets = { # Aquí estoy pasando las clases de boostrap a los atributos de arriba
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder':  'Write a title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder':  'Write a description'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'})
        }