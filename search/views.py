from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from visualizer.models import ObservationSet
from django.db.models import fields
import datetime

searches = [
    # Types
    # String
    [
        # Operation - Figure out how to add the %
        # Match
        "{param} LIKE '{value}'",
        # Contains
        "{param} LIKE '{value}'",
        # Greater
        "{param} LIKE '{value}'",
        # Lesser
        "{param} LIKE '{value}'",
        # Exclude
        "NOT ({param} LIKE '{value}')",
    ],
    # Number
    [
        # Operation
        # Match
        "{param} = {value}",
        # Contains
        "{param} = {value}",
        # Greater
        "{param} > {value}",
        # Lesser
        "{param} < {value}",
        # Exclude
        "NOT ({param} = {value})",
    ],
    # Date
    [
        # Operation
        # Match
        "{param} = '{value}'",
        # Contains
        "{param} = '{value}'",
        # Greater
        "{param} > '{value}'",
        # Lesser
        "{param} < '{value}'",
        # Exclude
        "NOT ({param} = '{value}')",
    ],
    # Bool
    [
        # Operation
        # Match
        "{param} IS {value}",
        # Contains
        "{param} IS {value}",
        # Greater
        "{param} IS {value}",
        # Lesser
        "{param} IS {value}",
        # Exclude
        "NOT ({param} IS {value})",
    ],
]

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
        
        type = 0
        value = request.GET[param][1:]
        field = ObservationSet._meta.get_field(param)
        match field.__class__:
            case fields.IntegerField | fields.FloatField | fields.BigAutoField:
                type = 1
            case fields.DateTimeField:
                type = 2
                value = " ".join(request.GET[param][1:].split("T"))
            case fields.BooleanField:
                type = 3
                value = "True" if request.GET[param][1:] == "on" else "False"
            case fields.CharField | fields.TextField | _:
                type = 0
        
        comp = 0
        match request.GET[param][0]:
            case "c":
                comp = 1
            case "g":
                comp = 2
            case "l":
                comp = 3
            case "e":
                comp = 4
            case "m" | _:
                comp = 0
        
        search += searches[type][comp].format(param=param, value=value)
    
    sql = "SELECT id, obs_id FROM visualizer_observationset"
    if search:
        sql += " WHERE " + search

    obss = ObservationSet.objects.raw(sql)

    context = {"observation_list": obss[:50],
               "fields": stringed}
    return render(request, "search/search.html", context)