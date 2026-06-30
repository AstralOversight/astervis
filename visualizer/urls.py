from django.urls import path

from . import views

urlpatterns = [
    path("<obs_name>/", views.set, name="visualizer"),
    path("<obs_name>/get/", views.get, name="get-obs"),
]