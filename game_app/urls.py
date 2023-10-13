from django.urls import path
from . import views



urlpatterns = [
    path("approval", views.approval_view, name='approval'),
]
