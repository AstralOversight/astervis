const specialTerms = ["page"];
var filterCount = 0;

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
    var filterName = "<select name='filter-name' id='filter-name-"+filterCount+"' onchange='reloadFilter("+filterCount+")' alt='Field to filter'>";
    var filterType = "<select name='filter-type' id='filter-type-"+filterCount+"' alt='Method of filtering'>";
    var filterValue = "<input name='filter-value' id='filter-value-"+filterCount+"' alt='Filter value'";
    var selType = fieldGroups[0].values[0].type;

    // Create the options in the filter dropdown
    fieldGroups.forEach((group) => {
        filterName += "<optgroup label='"+group.name+"'>";
        group.values.forEach((option) => {
            // If an option was selected and it's this one, mark it as such
            if (selected === group.id+"."+option.id) {
                filterName += "<option value='"+group.id+"."+option.id+"' selected>"+option.id+"</option>";
                selType = option.type;
            } else filterName += "<option value='"+group.id+"."+option.id+"'>"+option.id+"</option>";
        })
        filterName += "</optgroup>";
    })
    filterName += "</select>";

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
            filterValue += " type='number'";
            break
        case 'd':
            filterValue += " type='datetime-local'";
            break
        case 'b':
            filterValue += " type='checkbox'";
            if (value.substring(1).toLowerCase() == "true") {filterValue += " checked";}
            break
        case 's':
        default:
            filterValue += " type='text' maxlength='32'";
    }
    if (value) {
        filterValue += " value='"+value.substring(1)+"'";
    }
    filterValue += "/>";
    
    // Final HTML for the element
    row.innerHTML = 
        filterName+
        filterType+
        filterValue;
    document.getElementById("filters").appendChild(row);
    filterCount++;

    document.getElementById("filter-expand").setAttribute("open", "");
}

function reloadFilter(filterNum) {
    var filter = document.getElementById("filter-name-"+filterNum);
    var option = chainGet(fieldGroups, filter.selectedOptions[0].value);

    var filterOperation = document.createElement("select");
    filterOperation.setAttribute("name", "filter-type")
    filterOperation.setAttribute("id", "filter-type-"+filterNum);
    getFromId(opTypes, option.type).values.forEach((operation) => {
        filterOperation.innerHTML += "<option value='"+operation.id+"'>"+operation.name+"</option>";
    });
    document.getElementById("filter-type-"+filterNum).replaceWith(filterOperation);

    var field = document.getElementById("filter-value-"+filterNum);
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
    }
}

function search(newPage) {
    var urlPage = new URLSearchParams(document.location.search).get("page");
    if (!newPage) {
        if (urlPage) newPage = urlPage;
        else newPage = 1;
    }

    var newURL = baseURL+"?page="+newPage;
    var filters = document.getElementsByName("filter-name");
    filters.forEach(filter => {
        field = filter.nextElementSibling.nextElementSibling;
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