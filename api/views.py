from django.shortcuts import render, HttpResponse
from todo.models import Todo
from django.contrib.auth.models import User
from datetime import datetime
import json


# Create your views here.


# 轉換時間格式
def convert_date(date, format="%Y-%m-%d %H:%M:%S"):
    try:
        return date.strftime(format)
    except Exception as e:
        print(e)
    return None


# get/all/filter
def user_todos_api(request, id):
    todo_list = []
    message = ""
    success = True
    try:
        user = User.objects.get(id=id)
        todos = Todo.objects.filter(user=user)
        for todo in todos:
            todo_list.append(
                {
                    "id": todo.id,
                    "title": todo.title,
                    "text": todo.text,
                    "created": convert_date(todo.created),
                    "date_completed": convert_date(todo.date_completed),
                    "important": todo.important,
                    "completed": todo.completed,
                    "user": {"name": todo.user.username, "email": todo.user.email},
                },
            )
    except Exception as e:
        print(e)
        message = str(e)
        success = False

    # print(todo_list)
    response_data = {
        "success": success,
        "request_date": convert_date(datetime.now()),
        "data": todo_list,
        "message": message,
    }

    response_data = json.dumps(response_data, ensure_ascii=False)

    return HttpResponse(response_data, content_type="application/json")


def todo_api(request, id):
    success = True
    todo = None
    message = ""
    try:
        todo = Todo.objects.get(id=id)
        todo = {
            "id": todo.id,
            "title": todo.title,
            "text": todo.text,
            "created": convert_date(todo.created),
            "date_completed": convert_date(todo.date_completed),
            "important": todo.important,
            "completed": todo.completed,
            "user": {"name": todo.user.username, "email": todo.user.email},
        }
    except Exception as e:
        print(e)
        message = "id編號不正確"
        success = False

    response_data = {
        "success": success,
        "request_date": convert_date(datetime.now()),
        "data": todo,
        "message": message,
    }

    response_data = json.dumps(response_data, ensure_ascii=False)

    return HttpResponse(response_data, content_type="application/json")


# 取得所有的代辦事項
def todos_api(request):
    todo_list = []
    success = True
    try:
        todos = Todo.objects.all()
        for todo in todos:
            todo_list.append(
                {
                    "id": todo.id,
                    "title": todo.title,
                    "text": todo.text,
                    "created": convert_date(todo.created),
                    "date_completed": convert_date(todo.date_completed),
                    "important": todo.important,
                    "completed": todo.completed,
                    "user": {"name": todo.user.username, "email": todo.user.email},
                },
            )
    except Exception as e:
        print(e)
        success = False

    # print(todo_list)
    response_data = {
        "success": success,
        "request_date": convert_date(datetime.now()),
        "data": todo_list,
    }

    response_data = json.dumps(response_data, ensure_ascii=False)

    return HttpResponse(response_data, content_type="application/json")
