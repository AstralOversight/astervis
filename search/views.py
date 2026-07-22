from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from visualizer.models import ObservationSet, ObsHeader
from django.db.models import fields, ManyToOneRel, Q
import datetime

specialTerms = ["page"]

def type_code_for_class(field) -> str:
    type_code = "s"
    match field.__class__:
        case fields.CharField | fields.TextField:
            type_code = "s"
        case fields.IntegerField | fields.FloatField | fields.BigAutoField | fields.BigIntegerField | fields.related.ForeignKey:
            type_code = "n"
        case fields.DateTimeField:
            type_code = "d"
        case fields.BooleanField:
            type_code = "b"
    return type_code

operations = {
    "s": {
        "m": ["matches", "iexact", False],
        "c": ["contains", "contains", False],
        "l": ["starts with", "startswith", False],
        "g": ["ends with", "endswith", False],
        "e": ["does not contain", "exact", True],
    },
    "n": {
        "m": ["matches", "exact", False],
        "g": ["greater than", "gt", False],
        "l": ["lesser than", "lt", False],
        "n": ["is not", "exact", True],
    },
    "d": {
        "m": ["matches", "exact", False],
        # within 24h
        "b": ["before", "lt", False],
        "a": ["after", "gt", False],
        "n": ["is not", "exact", True],
    },
    "b": {
        "i": ["is", "exact", False],
        "n": ["is not", "exact", True],
    },
}
operationsJSON = '['
for var_type in operations:
    operationsJSON += '{"id":"'+var_type+'","values":['
    for operation_id in operations[var_type]:
        operationsJSON += '{"id":"'+operation_id+'","name":"'+operations[var_type][operation_id][0]+'"},'
    operationsJSON = operationsJSON[:-1] + ']},'
operationsJSON = operationsJSON[:-1] + ']'

groups = {
    "set":[ObservationSet,"Set"],
    "header":[ObsHeader,"Header"],
}
fieldsJSON = '['
for group in groups:
    fieldsJSON += '{"id":"'+group+'","name":"'+groups[group][1]+'","values":['
    for field in groups[group][0]._meta.get_fields():
        if (not isinstance(field, ManyToOneRel)):
            fieldsJSON += '{"id":"'+field.attname+'","type":"'+type_code_for_class(field)+'"},'
    fieldsJSON = fieldsJSON[:-1] + ']},'
fieldsJSON = fieldsJSON[:-1] + ']'

def index(request):
    return HttpResponse("Hello, you are at the search index.")

def page(request):
    # search = ""
    # has_header = False
    filters = Q()
    for param in request.GET:
        if param not in specialTerms:
            # if search: 
                # search += " AND "
            
            group = param.split('.')[0]
            field = param.split('.')[1]

            key = field
            if (not group == "set") :
                key = group + "__" + key

            op = request.GET[param][0]
            value = request.GET[param][1:]

            type_code = type_code_for_class(groups[group][0]._meta.get_field(field))
            key += "__" + operations[type_code][op][1]
            match type_code:
                case "d":
                    value = " ".join(value.split("T"))
                case "b":
                    value = True if (value == "on" or value == "true") else False

            if (operations[type_code][op][2]):
                filters = filters & ~Q(**{key: value})
            else:
                filters = filters & Q(**{key: value})
            # search += operations[type_code][op][1].format(param=param, value=value)
    
    # sql = "SELECT set.id, set.name FROM visualizer_observationset AS set"
    # if search:
    #     if has_header:
    #         sql += " INNER JOIN visualizer_obsheader AS header ON set.header_id = header.id"
    #     sql += f" WHERE {search}"
    # sql += " ORDER BY dt ASC;"

    obss = ObservationSet.objects.filter(filters).order_by("dt")

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