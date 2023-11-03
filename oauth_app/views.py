from django.shortcuts import render, redirect
from django.contrib.auth import logout


# Create your views here.

# From https://www.youtube.com/watch?v=yO6PP0vEOMc
def home(request):
    if request.user.is_authenticated:
        return render(request, "home.html")
    return render(request, "login.html")


# From https://www.youtube.com/watch?v=yO6PP0vEOMc
def logout_view(request):
    logout(request)
    return redirect("/")


def login_game(request):
    return render(request, "login.html")
