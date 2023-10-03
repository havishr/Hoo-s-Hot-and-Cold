from django.shortcuts import render, redirect
from django.contrib.auth import logout


# Create your views here.

#From https://www.youtube.com/watch?v=yO6PP0vEOMc
def home(request):
    return render(request, "home.html")

#From https://www.youtube.com/watch?v=yO6PP0vEOMc
def logout_view(request):
    logout(request)
    return redirect("/")
