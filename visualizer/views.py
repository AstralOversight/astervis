from django.shortcuts import render, get_object_or_404
from visualizer.models import ObservationSet

# Create your views here.

def set(request, set_id):
    context = {"set": get_object_or_404(ObservationSet, pk=set_id)}
    return render(request, "visualizer/display.html", context)