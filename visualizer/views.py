from django.shortcuts import render, get_object_or_404
from visualizer.models import ObservationSet
from visualizer import getfits

# Create your views here.

def set(request, observation_id):
    obs_set = get_object_or_404(ObservationSet, obs_id=observation_id)
    local_pos = "static/visualizer/stored_observations/"+observation_id+".fits.gz";
    try:
        with open(local_pos) as file:
            1; # idk what to place here, if it is there, we're good.
    except:
        getfits.save_file("data.asc-csa.gc.ca", "/users/OpenData_DonneesOuvertes/pub/NEOSSAT/ASTRO/"+obs_set.year.__str__()+"/"+obs_set.day.__str__()+"/", observation_id+".fits.gz")
    context = {"set": obs_set,
               "location": "/static/visualizer/stored_observations/"+observation_id+".fits.gz",}
    return render(request, "visualizer/display.html", context)