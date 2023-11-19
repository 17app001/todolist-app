from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Todo
from .forms import TodoForm
from datetime import datetime

# Create your views here.


def completedtodo(request):
    todos = Todo.objects.all()

    return render(request, "todo/completedtodo.html", {"todos": todos})


def page404(request):
    return render(request, "todo/404.html")


@login_required
def deletetodo(request, id):
    todo = Todo.objects.get(id=id)
    todo.delete()

    return redirect("todo")


@login_required
def createtodo(request):
    form = TodoForm()
    message = ""
    if request.method == "POST":
        # 新增
        form = TodoForm(request.POST)
        todo = form.save(commit=False)
        todo.user = request.user
        todo.save()
        message = "建立todo成功!"

    return render(request, "todo/createtodo.html", {"form": form, "message": message})


@login_required
def viewtodo(request, id):
    message = ""
    todo = Todo.objects.get(id=id)
    form = TodoForm(instance=todo)

    if request.method == "POST":
        # 更新
        form = TodoForm(request.POST, instance=todo)
        todo = form.save(commit=False)
        if todo.completed:
            todo.date_completed = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            todo.date_completed = None
        todo.save()
        message = "更新todo成功!"

    return render(
        request, "todo/viewtodo.html", {"todo": todo, "form": form, "message": message}
    )


def todo(request):
    user = request.user
    todos = None
    if user.is_authenticated:
        todos = Todo.objects.filter(user=user)

    return render(request, "todo/todo.html", {"todos": todos})
