from django.shortcuts import render, HttpResponse
from .models import Todo

# Create your views here.


# 1.登入成功=>首頁
# 2.如果沒代辦事項==>提示"無代辦事項，請先建立"
# 3.重要事項==>title改成紅色
# 4.base.html 登入的username綁定profile


def viewtodo(request, id):
    todo = Todo.objects.get(id=id)
    return render(request, "todo/viewtodo.html", {"todo": todo})


def todo(request):
    user = request.user
    todos = None
    if user.is_authenticated:
        todos = Todo.objects.filter(user=user)

    return render(request, "todo/todo.html", {"todos": todos})
