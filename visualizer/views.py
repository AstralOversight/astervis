from django.shortcuts import render, get_object_or_404
from visualizer.models import ObservationSet
from visualizer import getfits

# Create your views here.

def set(request, observation_id):
    obs_set = get_object_or_404(ObservationSet, obs_id=observation_id)
    context = {"set": obs_set,
            #    "location": "ftp://data.asc-csa.gc.ca/users/OpenData_DonneesOuvertes/pub/NEOSSAT/ASTRO/"+obs_set.year.__str__()+"/"+obs_set.day.__str__()+"/"+observation_id+".fits.gz",}
               "location": "/static/NEOS_SCI_2026109004941.fits.gz",}
    return render(request, "visualizer/display.html", context)