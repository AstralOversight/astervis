from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from visualizer.models import ObservationSet, ObsHeader
from django.db.models import fields, ManyToOneRel
import datetime

specialTerms = ["page"]
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
        "NOT {param} LIKE '{value}'",
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
        "NOT {param} = {value}",
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
        "NOT {param} = '{value}'",
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
        "NOT {param} IS {value}",
    ],
]

operations = '[{"id":"s","values":[' \
'{"id":"m","name":"matches"},' \
'{"id":"c","name":"contains"},' \
'{"id":"l","name":"starts with"},' \
'{"id":"g","name":"ends with"},' \
'{"id":"e","name":"excludes"}]},' \
'{"id":"n","values":[' \
'{"id":"m","name":"matches"},' \
'{"id":"l","name":"lesser than"},' \
'{"id":"g","name":"greater than"},' \
'{"id":"e","name":"not"}]},' \
'{"id":"d","values":[' \
'{"id":"m","name":"matches"},' \
'{"id":"c","name":"within 24h"},' \
'{"id":"l","name":"before"},' \
'{"id":"g","name":"after"},' \
'{"id":"e","name":"is not"}]},' \
'{"id":"b","values":[' \
'{"id":"m","name":"is"},' \
'{"id":"e","name":"is not"}]}]'

def index(request):
    return HttpResponse("Hello, you are at the search index.")

def page(request):
    fieldsJSON = '[{"id":"set","name":"Set","values":['
    for field in ObservationSet._meta.get_fields():
        type = field
        match field.__class__:
            case fields.IntegerField | fields.FloatField | fields.BigAutoField | fields.BigIntegerField | fields.related.ForeignKey:
                type = "n"
            case fields.DateTimeField:
                type = "d"
            case fields.BooleanField:
                type = "b"
            case fields.CharField | fields.TextField | _:
                type = "s"
        fieldsJSON += '{"id":"'+field.attname+'","type":"'+type+'"},'
    fieldsJSON = fieldsJSON[:-1] + ']},{"id":"header","name":\"Header\","values":['
    for field in ObsHeader._meta.get_fields():
        if (not isinstance(field, ManyToOneRel)):
            type = field
            match field.__class__:
                case fields.IntegerField | fields.FloatField | fields.BigAutoField | fields.BigIntegerField | fields.related.ForeignKey:
                    type = "n"
                case fields.DateTimeField:
                    type = "d"
                case fields.BooleanField:
                    type = "b"
                case fields.CharField | fields.TextField | _:
                    type = "s"
            fieldsJSON += '{"id":"'+field.attname+'","type":"'+type+'"},'
    fieldsJSON = fieldsJSON[:-1] + "]}]"

    search = ""
    for param in request.GET:
        if param not in specialTerms:
            if search: 
                search += " AND "
            
            type = 0
            value = request.GET[param][1:]
            field = ObservationSet._meta.get_field(param)
            match field.__class__:
                case fields.IntegerField | fields.FloatField | fields.BigAutoField | fields.BigIntegerField | fields.related.ForeignKey:
                    type = 1
                case fields.DateTimeField:
                    type = 2
                    value = " ".join(request.GET[param][1:].split("T"))
                case fields.BooleanField:
                    type = 3
                    value = "True" if (request.GET[param][1:] == "on" or request.GET[param][1:] == "true") else "False"
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
    
    sql = "SELECT id, name FROM visualizer_observationset"
    if search:
        sql += " WHERE " + search + " ORDER BY dt ASC"

    obss = ObservationSet.objects.raw(sql)

    # What page to display
    pageN = 1
    perPage = 50
    try:
        pageN = int(request.GET["page"])
    except:
        pass

    context = {"observation_list": obss[(pageN-1)*perPage:pageN*perPage],
               "fields": fieldsJSON,
               "ops": operations,
               "obs_len": obss.__len__(),
               "page": pageN,
               "tot_pages": (obss.__len__() // perPage) + 1}
    return render(request, "search/search.html", context)