from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from os import environ

def index(request):
    return HttpResponse("Hello, you are at the main index.")

def setup(request):
    # If a name and password are provided, and there are no pre-existing superusers, create the default one.
    name = environ.get("DJANGO_SUPERUSER_NAME","")
    pword = environ.get("DJANGO_SUPERUSER_PWORD","")
    if name and pword and not User.objects.all():
        User.objects.create_superuser(name, None, pword).save()
    
    return HttpResponse("Initial setup executed.")

def page(request):
    return render(request, "astervis/home.html")