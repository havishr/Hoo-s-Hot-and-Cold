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
