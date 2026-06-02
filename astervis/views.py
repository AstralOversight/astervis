from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

def index(request):
    return HttpResponse("Hello, you are at the main index.")

def page(request):
    return render(request, "astervis/home.html")