from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your views here.
def register(request):
    message = ""
    if request.method == "POST":
        print(request.POST)
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        print(username, password1, password2)
        if password1 != password2:
            message = "兩次輸入密碼不相同"
        elif len(password1) < 8:
            message = "密碼長度過短"

    form = UserCreationForm()
    return render(request, "user/register.html", {"form": form, "message": message})
