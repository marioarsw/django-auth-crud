from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
# es para crear la cookie y decir que si está autenticado
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm  # pedir info por defecto de django
# Para traerme la base de datos, - el punto es para decir que estoy en la misma carpeta
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required #Cuando quieres acceder a páginas sin loggearte
# Create your views here.


def home(request):
    return render(request, 'home.html')


# Si me manda la misma ruta significa que me manda aquí
# Si llega a través del método GET significa que está tratando de ver la interfaz
# Si llega a través del método POST está tratando de procesar datos

def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # register user
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'Username already exist'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            "error": 'Password do not match'
        })

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)

    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def tasks_completed(request): #retorno lo mismo que tasks, pero con los que si tiene el campo lleno en datecompleted
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')

    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
def createTask(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form':  TaskForm
        })
    else:  # Esta retornando con POST (Botón SAVE) SUBE ESTO A LA BASE DE DATOS
        try:
            form = TaskForm(request.POST)
            # print(form)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            print(new_task)
            return redirect('tasks')
        except ValueError:  # Si no lo puedes subir mando la misma vista y un mensaje de error
            return render(request, 'create_task.html', {
                'form':  TaskForm,
                'error': "Plase provide valida data"
            })


@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        # de la base de datos busca esto
        task = get_object_or_404(Task, pk=task_id, user=request.user) #el ultimo parametro es para que solo sea accesible por el usuario loggeado
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id)
            form = TaskForm(request.POST, instance=task) #instance=task, no confundir con la clase Task
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form': form,
            'error': "Error updating task"})

@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })

        login(request, user)
        return redirect('tasks')

        # return render(request, 'signin.html', {
        #     'form': AuthenticationForm
        # })
