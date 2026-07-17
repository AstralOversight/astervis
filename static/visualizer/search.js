const specialTerms = ["page"];

// Returns the first element in the array with the desired id.
function getFromId(array, id) {
    for (let i = 0; i < array.length; i++) {
        if (array[i].id == id) return array[i];
    }
}
// Returns the first element in the array with the desired id(s). (seperated by '.')
function chainGet(array, ids) {
    idArr = ids.split('.');

    var cur = array;
    var element = null;

    idArr.forEach(id => {
        element = getFromId(cur, id);
        if (element != null && element.values) cur = element.values;
        else return;
    });
    return element;
}

function addFilter(selected, value) {
    var row = document.createElement("tr");
    var select = "<select name='filter-value' id='filter-value' onchange='typeFields()' alt='Field to filter'>";
    var filterType = "<select name='filter-type' id='filter-type' alt='Method of filtering'>";
    var input = "<input id='value' name='value' alt='Filter value'";
    var selType = fieldGroups[0].values[0].type;

    // Create the options in the filter dropdown
    fieldGroups.forEach((group) => {
        select += "<optgroup label='"+group.name+"'>";
        group.values.forEach((option) => {
            // If an option was selected and it's this one, mark it as such
            if (selected === option.id) {
                select += "<option value='"+group.id+"."+option.id+"' selected>"+option.id+"</option>";
                selType = option.type;
            } else select += "<option value='"+group.id+"."+option.id+"'>"+option.id+"</option>";
        })
        select += "</optgroup>";
    })
    select += "</select>";

    // Create the filter type dropdown
    getFromId(opTypes, selType).values.forEach((operation) => {
        // If this type was selected
        if (value && value.substring(0, 1) === operation.id) {
            filterType += "<option value='"+operation.id+"' selected>"+operation.name+"</option>";
        } else filterType += "<option value='"+operation.id+"'>"+operation.name+"</option>";
    });
    filterType += "</select>";

    // Format the input field.
    switch (selType) {
        case 'n':
            input += " type='number'";
            break
        case 'd':
            input += " type='datetime-local'";
            break
        case 'b':
            input += " type='checkbox'";
            if (value.substring(1).toLowerCase() == "true") {input += " checked";}
            break
        case 's':
        default:
            input += " type='text' maxlength='32'";
    }
    if (value) {
        input += " value='"+value.substring(1)+"'";
    }
    input += "/>";
    
    // Final HTML for the element
    row.innerHTML = 
        select+
        filterType+
        input;
    document.getElementById("filters").appendChild(row);

    document.getElementById("filter-expand").setAttribute("open", "");
}

function typeFields() {
    var filters = document.getElementsByName("filter-value");
    filters.forEach(filter => {
        field = filter.nextElementSibling.nextElementSibling;
        var option = chainGet(fieldGroups, filter.selectedOptions[0].value);
        switch (option.type) {
            case "n":
                field.setAttribute("type", "number");
                field.removeAttribute("maxlength");
                field.value = "";
                break
            case "d":
                field.setAttribute("type", "datetime-local");
                field.removeAttribute("maxlength");
                field.value = "";
                break
            case "b":
                field.setAttribute("type", "checkbox");
                field.removeAttribute("maxlength");
                field.value = "";
                break
            case "s":
            default:
                field.setAttribute("type", "text");
                field.setAttribute("maxlength", "32");
                field.value = "";
        }

        var filterType = document.createElement("select");
        filter.setAttribute("name", "filter-type")
        filter.setAttribute("id", "filter-type");
        getFromId(opTypes, option.type).values.forEach((operation) => {
            filterType.innerHTML += "<option value='"+operation.id+"'>"+operation.name+"</option>";
        });

        filter.nextElementSibling.replaceWith(filterType);
    });
}

function search(newPage) {
    var urlPage = new URLSearchParams(document.location.search).get("page");
    if (!newPage) {
        if (urlPage) newPage = urlPage;
        else newPage = 1;
    }

    var newURL = baseURL+"?page="+newPage;
    var filters = document.getElementsByName("filter-value");
    console.log(filters);
    filters.forEach(filter => {
        field = filter.nextElementSibling.nextElementSibling;
        console.log(field.value);
        if (field.value) {
            newURL += "&" + encodeURIComponent(filter.value) +
                        "=" + encodeURIComponent(filter.nextElementSibling.value) +
                        encodeURIComponent(field.value);
        } else if (field.getAttribute("type") == "checkbox") {
            newURL += "&" + encodeURIComponent(filter.value) +
                        "=" + encodeURIComponent(filter.nextElementSibling.value) +
                        encodeURIComponent(field.checked);
        }
    });
    document.location.href = newURL;
}

function gotoPage() {
    pageNum = document.getElementById("page-select").value;
    search(pageNum);
}