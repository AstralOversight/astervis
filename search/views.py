from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from visualizer import getfits


def index(request):
    return HttpResponse("Hello, you are at the search index.")

def page(request):
    context = {"asteroids_list": getfits.all_for_day(2026, 109)}
    return render(request, "search/search.html", context)