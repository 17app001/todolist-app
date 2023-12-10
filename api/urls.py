"""
URL configuration for todolist project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # 程式練習(取得所有使用者跟單一使用者api)
    # path("users/", views.users_api, name="users_api"),
    # path("users/<int:id>", views.user_api, name="user_api"),
    path("delete-todo/<int:id>/", views.delete_todo_api, name="delete_todo_api"),
    path("update-todo/<int:id>/", views.update_todo_api, name="update_todo_api"),
    path("add-todo/", views.add_todo_api, name="add_todo_api"),
    path("todos/", views.todos_api, name="todos_api"),
    path("todos/<int:id>/", views.todo_api, name="todo_api"),
    path("todos/user/<int:id>/", views.user_todos_api, name="user_todos_api"),
]
