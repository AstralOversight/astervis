from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from visualizer import models
from django.db.models import fields


def index(request):
    return HttpResponse("Hello, you are at the search index.")

def page(request):
    stringed = ""
    for field in models.ObservationSet._meta.get_fields():
        type = field
        match field.__class__:
            case fields.IntegerField | fields.FloatField | fields.BigAutoField:
                type = "n"
            case fields.DateTimeField:
                type = "d"
            case fields.BooleanField:
                type = "b"
            case fields.CharField | fields.TextField | _:
                type = "s"
        stringed += "," + type + field.attname
    context = {"observation_list": models.ObservationSet.objects.order_by("-obs_id")[:50],
               "fields": stringed}
    return render(request, "search/search.html", context)