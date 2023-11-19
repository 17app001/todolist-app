from django.shortcuts import render, HttpResponse

# Create your views here.


def todo(request):
    return render(request, "todo/todo.html")
