from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import NewUserForm


@login_required
def user_logout(request):
    logout(request)

    return redirect("login")


@login_required
def profile(request):
    user = request.user

    return render(request, "user/profile.html", {"user": user})


def user_login(request):
    message = ""
    username = ""

    if request.method == "GET":
        if "username" in request.session:
            username = request.session.get("username")
            del request.session["username"]

    if request.method == "POST":
        if request.POST.get("register"):
            return redirect("register")
        elif request.POST.get("login"):
            username = request.POST["username"]
            password = request.POST["password"]
            email = request.POST["email"]
            user = User.objects.filter(username=username)
            if not user:
                message = "無此帳號"
            else:
                user = user[0]
                if user.email != email:
                    message = "Email不正確"
                else:
                    # 進行驗證
                    user = authenticate(request, username=username, password=password)
                    if not user:
                        message = "密碼錯誤!"
                    else:
                        # 使用者完成登入
                        login(request, user)
                        message = "登入成功!"
                        return redirect("todo")

            print(user)
    return render(
        request, "user/login.html", {"message": message, "username": username}
    )


# Create your views here.
def register(request):
    message = ""
    if request.method == "POST":
        print(request.POST)
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        email = request.POST["email"]

        print(username, password1, password2, email)
        if password1 != password2:
            message = "兩次輸入密碼不相同"
        elif len(password1) < 8:
            message = "密碼長度過短"
        else:
            # 確認帳號是否重複
            if User.objects.filter(username=username):
                message = "帳號重複!"
            else:
                # 建立使用者
                user = User.objects.create_user(
                    username=username, password=password1, email=email
                )
                user.save()
                message = "註冊成功!"
                request.session["username"] = username
                return redirect("login")

    form = NewUserForm()
    return render(request, "user/register.html", {"form": form, "message": message})
