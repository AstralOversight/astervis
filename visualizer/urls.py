from django.urls import path

from . import views

urlpatterns = [
    path("<observation_id>/", views.set, name="visualizer"),
]