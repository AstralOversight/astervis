from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from visualizer.models import ObservationSet
from django.db.models import fields
import datetime


def index(request):
    return HttpResponse("Hello, you are at the search index.")

def page(request):
    stringed = ""
    for field in ObservationSet._meta.get_fields():
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
    
    search = ""
    for param in request.GET:
        if search: 
            search += " AND "
        
        field = ObservationSet._meta.get_field(param)
        match field.__class__:
            case fields.IntegerField | fields.FloatField | fields.BigAutoField:
                search += param + " = " + request.GET[param]
            case fields.DateTimeField:
                search += param + " = '" + " ".join(request.GET[param].split("T")) + "'"
            case fields.BooleanField:
                val = "True" if request.GET[param] == "on" else "False"
                search += param + " IS " + val
            case fields.CharField | fields.TextField | _:
                search += param + " LIKE '" + request.GET[param] + "'"
    
    sql = "SELECT id, obs_id FROM visualizer_observationset"
    if search:
        sql += " WHERE " + search

    obss = ObservationSet.objects.raw(sql)

    context = {"observation_list": obss[:50],
               "fields": stringed}
    return render(request, "search/search.html", context)