from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from .forms import GameForm

def add_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_location')
    else:
        form = GameForm()
    return render(request, 'add_game.html', {'form': form})
def approval_view(request):
    if request.user.is_authenticated and request.user.is_admin:
        return render(request, "approval.html")
    else:
        return HttpResponseForbidden("Admin Permissions Required!")

