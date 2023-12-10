from django.shortcuts import render, HttpResponse
from todo.models import Todo
from django.contrib.auth.models import User
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.


# 轉換時間格式
def convert_date(date, format="%Y-%m-%d %H:%M:%S"):
    try:
        return date.strftime(format)
    except Exception as e:
        print(e)
    return None


@csrf_exempt
def delete_todo_api(request, id):
    success = True
    if request.method == "DELETE":
        try:
            todo = Todo.objects.get(id=id)
            todo.delete()

            message = {
                "success": success,
                "todo_id": id,
                "message": "刪除資料成功.",
            }

        except Exception as e:
            print(e)
            success = False
            message = {"success": success, "message": str(e)}

        response_data = json.dumps(message, ensure_ascii=False)
        return HttpResponse(response_data, content_type="application/json")


@csrf_exempt
def update_todo_api(request, id):
    success = True
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            todo = Todo.objects.get(id=id)
            user = (
                User.objects.get(username=data.get("user"))
                if data.get("user")
                else todo.user
            )

            todo.title = data.get("title", todo.title)
            todo.text = data.get("text", todo.text)
            todo.date_completed = data.get("date_completed", todo.date_completed)
            todo.important = data.get("important", todo.important)
            todo.completed = data.get("completed", todo.completed)
            todo.user = user
            todo.save()

            message = {
                "success": success,
                "todo_id": todo.id,
                "message": "更新資料成功.",
            }

        except Exception as e:
            print(e)
            success = False
            message = {"success": success, "message": str(e)}

        response_data = json.dumps(message, ensure_ascii=False)
        return HttpResponse(response_data, content_type="application/json")


@csrf_exempt
def add_todo_api(request):
    success = True
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = User.objects.get(username=data.get("user"))
            todo = Todo.objects.create(
                title=data.get("title"),
                text=data.get("text"),
                date_completed=data.get("date_completed"),
                important=data.get("important"),
                completed=data.get("completed"),
                user=user,
            )

            message = {
                "success": success,
                "todo_id": todo.id,
                "title": todo.title,
                "username": user.username,
            }

        except Exception as e:
            print(e)
            success = False
            message = {"success": success, "message": str(e)}

        response_data = json.dumps(message, ensure_ascii=False)
        return HttpResponse(response_data, content_type="application/json")


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
