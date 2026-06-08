from django.shortcuts import render, get_object_or_404
from visualizer.models import ObservationSet
from visualizer import getfits

# Create your views here.

def set(request, observation_id):
    context = {"set": get_object_or_404(ObservationSet, obs_id=observation_id)}
    return render(request, "visualizer/display.html", context)