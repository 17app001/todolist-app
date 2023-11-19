from django.shortcuts import render, HttpResponse
from .models import Todo
from .forms import TodoForm

# Create your views here.


def createtodo(request):
    form = TodoForm()
    message = ""
    if request.method == "POST":
        print(request.POST)
        form = TodoForm(request.POST)
        todo = form.save(commit=False)
        todo.user = request.user
        todo.save()
        message = "建立todo成功!"

    return render(request, "todo/createtodo.html", {"form": form, "message": message})


def viewtodo(request, id):
    todo = Todo.objects.get(id=id)
    return render(request, "todo/viewtodo.html", {"todo": todo})


def todo(request):
    user = request.user
    todos = None
    if user.is_authenticated:
        todos = Todo.objects.filter(user=user)

    return render(request, "todo/todo.html", {"todos": todos})
