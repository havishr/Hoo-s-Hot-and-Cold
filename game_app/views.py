from django.urls import reverse
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from .forms import GameForm

from .models import Game, ActiveGame
from django.views.generic import UpdateView, TemplateView, DetailView, ListView
from game_app.play import *
from django.http import JsonResponse


def add_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('add_location')
            return redirect('home')
    else:
        form = GameForm()

    context = {
        'form': form,
        'default_lat': 38.053,  # UVA
        'default_lng': -78.5035,
    }

    return render(request, 'add_game.html', {'form': form})


# Adapted from: Django practice
class ApproveView(ListView):
    template_name = "approval.html"
    context_object_name = "game_submissions"

    def get_queryset(self):
        """
        Return the games that have been submitted for approval.
        """
        return Game.objects.filter(is_approved=False)[:1]

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin:
            return HttpResponseForbidden("Must be logged in with admin permissions.")

        return super().dispatch(request, *args, **kwargs)


# Adapted from: Django practice
def approve_game(request, pk):
    # Check if the user is an admin before performing approval
    if request.user.is_authenticated and request.user.is_admin:
        game = Game.objects.get(pk=pk)
        game.is_approved = True
        game.save()
    return redirect('approval')


# Adapted from: Django practice
def deny_game(request, pk):
    # Check if the user is an admin before performing denial
    if request.user.is_authenticated and request.user.is_admin:
        game = Game.objects.get(pk=pk)
        game.delete()

    return redirect('approval')


def static_play(request):
    # Must be logged in to play the game
    if not request.user.is_authenticated:
        return HttpResponseForbidden("Must be logged in to play!")

    try:
        active_game = ActiveGame.objects.get(user=request.user)

        context0 = {
            'hint': active_game.get_curr_hint_display(),
            'lat': active_game.last_latitude,
            'lon': active_game.last_longitude,
        }
        context1 = {
            'name': active_game.game.name,
            'hint_count': active_game.hint_counter,
        }
        if active_game.is_finished:
            return render(request, 'completed_game.html', context1)
        return render(request, 'static_play.html', context0)
    except ActiveGame.DoesNotExist:
        return render(request, 'static_no_game.html')

    # Should be unreachable
    return HttpResponseForbidden("If you're seeing this, something went really wrong...")


# From: ChatGPT
# Used: How to set up a function that handles AJAX requests
def update_hint(request):
    if request.method == 'GET':

        # This part was not from ChatGPT
        latitude = request.GET.get('lat', None)
        longitude = request.GET.get('lng', None)

        print("(", latitude, ",", longitude, ")") # REMOVE LINE

        if get_hint(request, latitude, longitude):
            return JsonResponse({'message': 'Coordinates received successfully'})

    return JsonResponse({'message': 'Invalid request'})
