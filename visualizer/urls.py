from django.urls import path

from . import views

urlpatterns = [
    path("<obs_name>/", views.set, name="visualizer"),
]