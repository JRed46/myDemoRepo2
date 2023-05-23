from django.shortcuts import render, redirect
from .models import Task
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
# Create your views here.

def is_allowed(user):
    return user.groups.filter(name='allowed')

@login_required(login_url=reverse_lazy('login'))
def task_list(request):
    if is_allowed(request.user):
        tasks = Task.objects.all()
        return render(request, 'tasks/list.html', {'tasks':tasks})
    return redirect('/')

@login_required(login_url=reverse_lazy('login'))
def task_create(request):
    if is_allowed(request.user):
        if request.method == 'POST':
            title = request.POST['title']
            description = request.POST['description']
            Task.objects.create(title=title, description=description)
            return redirect('task_list')
        return render(request, 'tasks/create.html')
    return redirect('/')

@login_required(login_url=reverse_lazy('login'))
def task_detail(request, task_id):
    if is_allowed(request.user):
        task = Task.objects.get(id=task_id)
        return render(request, 'tasks/detail.html', {'task':task})
    return redirect('/')

@login_required(login_url=reverse_lazy('login'))
def task_complete(request, task_id):
    if is_allowed(request.user):
        task = Task.objects.get(id=task_id)
        task.completed = True
        task.save()
        return redirect('task_list')
    return redirect('/')

@login_required(login_url=reverse_lazy('login'))
def task_delete(request, task_id):
    if is_allowed(request.user):
        task = Task.objects.get(id=task_id)
        task.delete()
        return redirect('task_list')
    return redirect('/')