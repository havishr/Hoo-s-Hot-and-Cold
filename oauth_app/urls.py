from django.urls import path, include
from . import views



urlpatterns = [

    #From https://www.youtube.com/watch?v=yO6PP0vEOMc
    path("", views.home, name='home'),
    path("logout", views.logout_view),
    path('game/', include('game_app.urls')),

]
