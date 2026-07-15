const specialTerms = ["page"];
// Arrays containing id, name, type (s:string, n:number, d:date)
const options = new Map();
const types = new Map();
types.set("m", "Matches");
types.set("c", "Contains");
types.set("l", "Lesser than");
types.set("g", "Greater than");
types.set("e", "Excludes");

function addFilter(selected, value) {
    var row = document.createElement("tr");
    var select = "<select name='filter-value' id='filter-value' onchange='typeFields()'>";
    var filterType = "<select name='filter-type' id='filter-type'>";
    var selType = "";

    // Create the options in the filter dropdown
    options.forEach((settings, optionId) => {
        // If an option was selected and it's this one, mark it as such
        if (selected === optionId) {
            select += "<option value='"+optionId+"' selected>"+settings[0]+"</option>";
            selType = settings[1];
        } else 
        select += "<option value='"+optionId+"'>"+settings[0]+"</option>";
    })
    select += "</select>";

    // Create the filter type dropdown
    types.forEach((typeName, typeKey) => {
        // If this type was selected
        if (value && value.substring(0, 1) === typeKey) {
            filterType += "<option value='"+typeKey+"' selected>"+typeName+"</option>";
        } else 
        filterType += "<option value='"+typeKey+"'>"+typeName+"</option>";
    })
    filterType += "</select>";

    // Create the input field and format it correctly.
    var input = "<input id='value' name='value'";
    switch (options.has(selected) ? options.get(selected)[1] : null) {
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
        switch (options.get(filter.selectedOptions[0].value)[1]) {
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