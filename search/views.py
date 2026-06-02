from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, you are at the search index.")

def page(request):
    return render(request, "search/search.html")