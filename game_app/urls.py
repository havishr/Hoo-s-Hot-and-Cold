from django.urls import path, include
from game_app.views import add_game

urlpatterns = [
    path('', add_game, name='add_game'),
]
