from django.shortcuts import render, get_object_or_404
from visualizer.models import ObservationSet
from visualizer import getfits

# Create your views here.

def set(request, obs_name):
    obs_set = get_object_or_404(ObservationSet, name=obs_name)
    getfits.prep_file(obs_set, getfits.ObsType.RAW)
    
    context = {"set": obs_set,
               "location": "/" + getfits.STORED_LOCATION + obs_set.name + ".fits.gz",}
    return render(request, "visualizer/display.html", context)