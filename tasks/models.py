from django.db import models
from django.contrib.auth.models import User #Esto es para la ForeignKey de models

# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # -este método es para personalizar el panel de administrador
    def __str__(self): #Self es una referencia a la pripia clase
        return self.title + '- by ' + self.user.username
