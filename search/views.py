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
        "{param} LIKE '%%{value}%%'",
        # Starts with
        "{param} LIKE '{value}%%'",
        # Ends with
        "{param} LIKE '%%{value}'",
        # Exclude
        "NOT {param} LIKE '%%{value}%%'",
    ],
    # Number
    [
        # Operation
        # Match
        "{param} = {value}",
        # Error
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
        # Within 24h
        "{param} = '{value}'",
        # Before
        "{param} > '{value}'",
        # After
        "{param} < '{value}'",
        # Exclude
        "NOT {param} = '{value}'",
    ],
    # Bool
    [
        # Operation
        # Is
        "{param} IS {value}",
        # Error
        "{param} IS {value}",
        # Error
        "{param} IS {value}",
        # Error
        "{param} IS {value}",
        # Is not
        "NOT {param} IS {value}",
    ],
]

operationsJSON = '[{"id":"s","values":[' \
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

groups = {"set":[ObservationSet,"Set"],
           "header":[ObsHeader,"Header"]}

fieldsJSON = '['
for group in groups:
    fieldsJSON += '{"id":"'+group+'","name":"'+groups[group][1]+'","values":['
    for field in groups[group][0]._meta.get_fields():
        if (not isinstance(field, ManyToOneRel)):
            field_type = field
            match field.__class__:
                case fields.IntegerField | fields.FloatField | fields.BigAutoField | fields.BigIntegerField | fields.related.ForeignKey:
                    field_type = "n"
                case fields.DateTimeField:
                    field_type = "d"
                case fields.BooleanField:
                    field_type = "b"
                case fields.CharField | fields.TextField | _:
                    field_type = "s"
            fieldsJSON += '{"id":"'+field.attname+'","type":"'+field_type+'"},'
    fieldsJSON = fieldsJSON[:-1] + ']},'
fieldsJSON = fieldsJSON[:-1] + ']'

def index(request):
    return HttpResponse("Hello, you are at the search index.")

def page(request):
    search = ""
    for param in request.GET:
        if param not in specialTerms:
            if search: 
                search += " AND "
            
            search_type = 0
            value = request.GET[param][1:]
            cval = request.GET[param][0]
            group = param.split('.')[0]
            field = param.split('.')[1]
            match groups[group][0]._meta.get_field(field).__class__:
                case fields.IntegerField | fields.FloatField | fields.BigAutoField | fields.BigIntegerField | fields.related.ForeignKey:
                    search_type = 1
                case fields.DateTimeField:
                    search_type = 2
                    value = " ".join(value.split("T"))
                case fields.BooleanField:
                    search_type = 3
                    value = "True" if (value == "on" or value == "true") else "False"
                case fields.CharField | fields.TextField | _:
                    search_type = 0
            
            comp = 0
            match cval:
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
            
            search += searches[search_type][comp].format(param=param, value=value)
    
    sql = "SELECT id, name FROM visualizer_observationset"
    if search:
        sql += f" WHERE {search} ORDER BY dt ASC"

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
               "ops": operationsJSON,
               "obs_len": obss.__len__(),
               "page": pageN,
               "tot_pages": (obss.__len__() // perPage) + 1}
    return render(request, "search/search.html", context)