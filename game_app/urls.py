from game_app import views
from django.urls import path
from game_app.views import add_game

urlpatterns = [
    path('', add_game, name='add_game'),
    path("approval", views.approval_view, name='approval')
    ]
