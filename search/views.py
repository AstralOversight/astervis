from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, you are at the search index.")

def page(request):
    context = {"asteroids_list": ["Big Rock", "Small Rock", "Continent Killer"]}
    return render(request, "search/search.html", context)