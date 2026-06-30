from django.http import FileResponse
from django.shortcuts import render, get_object_or_404
from visualizer.models import ObservationSet
from visualizer import getfits

# Create your views here.

def set(request, obs_name):
    obs_set = get_object_or_404(ObservationSet, name=obs_name)
    getfits.prep_file(obs_set, getfits.ObsType.RAW)
    obs_set.refresh_from_db()
    
    context = {"set": obs_set,
               "location": "/" + getfits.STORED_LOCATION + obs_set.name + ".fits.gz",}
    return render(request, "visualizer/display.html", context)

def get(request, obs_name):
    obs_set = get_object_or_404(ObservationSet, name=obs_name)
    # r = requests.get(url, stream=True)
    response = FileResponse(getfits.stream_file(obs_set, getfits.ObsType.RAW), filename="NEOS_SCI_2026109114040.fits.gz")
    filename = "NEOS_SCI_2026109114040.fits.gz" # should be changed to actual name later.
    # response['Content-Disposition'] = f'attachement; filename={filename}'
    return response