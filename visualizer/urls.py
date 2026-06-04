from django.urls import path

from . import views

urlpatterns = [
    path("<int:observation_id>/", views.set, name="visualizer"),
]