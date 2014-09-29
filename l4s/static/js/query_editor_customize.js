/*
   This file is part of Lod4stat.

   Copyright (c) 2014 Provincia autonoma di Trento


   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU Affero General Public License as
   published by the Free Software Foundation, either version 3 of the
   License, or (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU Affero General Public License for more details.

   You should have received a copy of the GNU Affero General Public License
   along with this program. If not, see <http://www.gnu.org/licenses/>.
*/

/*
  Query editor customization popup
  This contains all the javascript used by the query editor customization popup.
*/

function get_aggregation_color() {
        return "#A1284C";
}

function colour(field) {
        element = document.getElementById(field);
        element.setAttribute("style", "background:" + get_aggregation_color());
    }

function load_selected_values(myRadio, field, values, agg){
    var array = eval('(' + values + ')');
    id = "select_" + field;
    var radio = document.getElementById(id);
    var html = "";
    for (var i = 0; i < array.length; i++) {
        if (agg) {
            id =  'agg_input_'  + myRadio.id +'_' + array[i][0]
            name = 'agg_input_' + myRadio.id;
            radio.name =  'select_input_' + myRadio.id;
        }
        else {
            id =  field + '_input_' + array[i][0]
            name = 'input_' +  field;
        }
        html += '<input type="checkbox" name="' +  name + '" id="' + id + '" value="' + array[i][0] + '">'
        if (array[i].length>1) {
            html+= array[i][1] + '<br>';
        }
        else {
             html+= array[i][0] + '<br>';
        }
    }
    radio.innerHTML = html;
}

function change_field_label(myRadio, field) {
    html = myRadio.value;
    var span = document.getElementById(field);
    var spans = span.getElementsByTagName("span");
    html = html + '<span style="display:None">' + spans[0].innerHTML + '</span>';
    html = html + '<span class="caret"></span>';
    span.innerHTML = html;
}

function handleRadio(myRadio, field, values, agg, select_all) {
    change_field_label(myRadio, field);
    load_selected_values( myRadio, field, values, agg);
    if (select_all) {
        checkByParent('select_'+ field, true);
    }
}

function setFieldLabel(id, field, values) {
   var myRadio = document.getElementById(id);
   handleRadio(myRadio, field, values, true, false);
}

function get_lis(id) {
    ret = ""
    element = document.getElementById(id);
    var lis = element.getElementsByTagName('li');
    var output = [];
    for (var i = 0; i < lis.length; i++) {
         var span = lis[i].getElementsByTagName("span")[0];
         output.push(span.getElementsByTagName("span")[0].innerHTML);
    }
    return output.join(",");
}

function get_aggregations() {
    col_el = document.getElementById('columnFields');
    row_el = document.getElementById('rowFields');
    
    var radios = document.getElementsByTagName('input');
    var output = [];
    for (var i = 0; i < radios.length; i++) {
        var name = radios[i].name;
        var type = radios[i].type;
        if (type == 'radio' && radios[i].checked) {
            id = radios[i].id;
            if (id != "") {
                output.push(id);
           }
       }
    }
    return output.join(",");
}

function checkByParent(aId, aChecked) {
    el = document.getElementById(aId);
    var coll= el.getElementsByTagName('input');
    for (var x=0; x<coll.length; x++) {
        coll[x].checked = aChecked;
    }
}

function create_selection(values) {
    var selection_obj = new Object();
    var value_hash = eval('(' + values + ')');
    for (var key in value_hash) {
        field_obj = [];
        selection_obj[key] = field_obj
        field_value = value_hash[key];  
        sel_name = "input_" + key;
        var coll = document.getElementsByName(sel_name);
        if (coll != null) {
             for (var x=0; x<coll.length; x++) {
                if (coll[x].checked) {
                    field_obj.push(field_value[x]);
                }
             }
        }   
    }    
   return selection_obj;
}

function create_agg_selection(agg_values) {
    var selection_obj = new Object();
    var value_hash = eval('(' + agg_values + ')');
    for (var key in value_hash) {
        field_obj = [];
        selection_obj[key] = field_obj
        field_value = value_hash[key];  
        sel_name = "agg_input_" + key;
        var coll = document.getElementsByName(sel_name);
             for (var x=0; x<coll.length; x++) {
                if (coll[x].checked) {
                    field_obj.push(field_value[x]);
                }
        }     
    }
   return selection_obj;
}

function select_filters(filters){
    var filter_hash = eval('(' + filters + ')');
    for (var key in filter_hash) {
        field_values = filter_hash[key]; 
        for (var x=0; x<  field_values.length; x++) {
            var val =  field_values[x][0];
            id = key + '_input_' + val
            el = document.getElementById(id);
            if (el != null) {
                el.checked = true;
            }
        }    
    }
}

function select_agg_filters(filters){
    var filter_hash = eval('(' + filters + ')');
    for (var key in filter_hash) {
        field_values = filter_hash[key]; 
        for (var x=0; x<  field_values.length; x++) {
            var val =  field_values[x][0];
            id= "agg_input_" + key + "_" + val;
            el = document.getElementById(id);
            if (el != null) {
                el.checked = true;
            }
        }    
    }
}

function addHiddenInput(form, id, value) {
    var hiddenField = document.createElement("input");
    hiddenField.setAttribute("type", "hidden");
    hiddenField.setAttribute("id", "id_" + id);
    hiddenField.setAttribute("name", id);
    hiddenField.setAttribute("value", value);
    form.appendChild(hiddenField);
}


function submit_popup (values, agg_values, table_name, no_rows, no_columns) {
    selection = create_selection(values);
    filter_value = JSON.stringify(selection);
        
    rows = get_lis('rowFields');
    if (rows == "") {
        alert(no_rows);
        return;
    }
    cols = get_lis('columnFields');
    if (cols == "") {
        alert(no_columns);
        return;
    }
    
    var form = window.opener.document.getElementById("form");
    addHiddenInput(form, 'filters', filter_value);
    addHiddenInput(form, 'table', table_name);
    addHiddenInput(form, 'rows', rows);
    addHiddenInput(form, 'columns', cols);
    
    sel_aggregations = get_aggregations();
    if (sel_aggregations != "") {
        addHiddenInput(form, 'aggregate', sel_aggregations);
     }
     
     agg_selection = create_agg_selection(agg_values);
     agg_selection_value = JSON.stringify(agg_selection);
     addHiddenInput(form, 'agg_filters', agg_selection_value);
         
     var debug = document.getElementById('debug');  
      if (debug!=null && debug.checked == 1) {
        addHiddenInput(form, 'debug', 'true');
     }
    
    form.submit();
    
    //window.opener.location = '/query_editor_view' + params;
    
    window.close();
}

$(function () {
    $("#unselectedFields,#columnFields,#rowFields").sortable({
         connectWith: "#unselectedFields,#columnFields,#rowFields",
    });
    $("#unselectedFields,#columnFields,#rowFields").disableSelection();
});

$(function () {
   $('.dropdown-menu').on({
	"click":function(e){
      e.stopPropagation();
    }
   });
});