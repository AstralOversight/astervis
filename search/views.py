from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from visualizer import models


def index(request):
    return HttpResponse("Hello, you are at the search index.")

def page(request):
    context = {"observation_list": models.ObservationSet.objects.order_by("-obs_id")[:20]}
    return render(request, "search/search.html", context)