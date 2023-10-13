from django.shortcuts import render
from django.http import HttpResponseForbidden

# Create your views here.


def approval_view(request):
    if request.user.is_authenticated and request.user.is_admin:
        return render(request, "approval.html")
    else:
        return HttpResponseForbidden("Admin Permissions Required!")
