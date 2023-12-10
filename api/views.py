from django.shortcuts import render, HttpResponse
from todo.models import Todo
from datetime import datetime
import json


# Create your views here.
# 取得所有的代辦事項
def convert_date(date, format="%Y-%m-%d %H:%M:%S"):
    try:
        return date.strftime(format)
    except Exception as e:
        print(e)
    return None


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
