from django.urls import reverse
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from .forms import GameForm

from .models import Game, ActiveGame
from django.views.generic import UpdateView, TemplateView, DetailView, ListView


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


def static_play(TemplateView):
    active_game = ActiveGame.objects.select_related().filter(user=request.user)

    return render(request, 'static_play.html')


def get_hint(request):
    redirect('static_play')
