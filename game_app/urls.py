from game_app import views
from django.urls import path
from game_app.views import add_game

urlpatterns = [
    path('', add_game, name='add_game'),
    path("approval", views.ApproveView.as_view(), name='approval'),

    # URLS for approving and denying games, adapted from Django tutorial
    path('approve/<int:pk>/', views.approve_game, name='approve_game'),
    path('deny/<int:pk>/', views.deny_game, name='deny_game'),

    # Game play urls
    path('play/static/', views.static_play, name='static_play'),
    path('update/hint/', views.update_hint, name='update_hint'),
    path('tutorial', views.tutorial, name='tutorial'),
    ]
