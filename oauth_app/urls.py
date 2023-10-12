from django.urls import path
from . import views

urlpatterns = [

    #From https://www.youtube.com/watch?v=yO6PP0vEOMc
    path("", views.home),
    path("logout", views.logout_view),
]
