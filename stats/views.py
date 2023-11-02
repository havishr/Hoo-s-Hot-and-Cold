from django.shortcuts import render
from .models import UserStats

def leaderboard(request):
    top_users = UserStats.objects.order_by('-score')[:10]
    return render(request, 'stats_app/leaderboard.html', {'top_users': top_users})
