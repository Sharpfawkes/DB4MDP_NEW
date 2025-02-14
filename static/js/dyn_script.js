/* lang_langs */
function generate_url(method_id) {
    var url_path = location.href.split('/')[0] + '/{{ reroute_string }}/' + method_id.toString();
    return url_path;
}

/* mdp_advanced */
/* Setting the initial value of the All and Include buttons so that they appear to be chosen by default */
$(document).ready(function() {
    var temp1 = document.getElementById("All");
    var temp2 = document.getElementById("Inc");
    temp1.style.backgroundColor = "#f44336";
    temp1.value = 1;
    temp2.style.backgroundColor = "#f44336";
    temp2.value = 1;
});
function generate2(id_no) {
    var url_path = location.href.split('/')[0] + '/mdpbasic/' + id_no.toString();
    return url_path;
}
    function btn_fn2(elem) {
        var temp_elem;
        if (elem.value == 0){
            if (elem.id == "All"){
                temp_elem = document.getElementById("Any");
            }
            else{
                temp_elem = document.getElementById("All");
            }
            temp_elem.value = 0;
            temp_elem.style.backgroundColor = "#cecece";
            elem.value = 1;
            elem.style.backgroundColor = "#f44336";
        }
    }
    function btn_fn3(elem) {
        var temp_elem;
        if (elem.value == 0){
            if (elem.id == "Inc"){
                temp_elem = document.getElementById("Exc");
            }
            else{
                temp_elem = document.getElementById("Inc");
            }
            temp_elem.value = 0;
            temp_elem.style.backgroundColor = "#cecece";
            elem.value = 1;
            elem.style.backgroundColor = "#f44336";
        }
    }
    function btn_fn1(elem) {

  if (elem.value == 0){
  elem.style.backgroundColor = "#f44336";
  elem.value = 1;
}
else if (elem.value == 1){
    elem.style.backgroundColor = "#cecece";
elem.value = 0;
}
}
function generate(el) {
    var url_path;
    /* Base url path has been defined. After that link_data|id_names:0 will return the list of element ids on the
    page following which we get each element by id after typecasting it to a string (this is necessary because otherwise
    if you check the generated source code you will see that there are no quotes around the id name and this raises
    a getElementById null error. The query_update filter will append =Yes& to the id field. Then the string is returned
    at the end. */
    /* Can't just directly use location.href and keep appending to that because otherwise every time the page is loaded
    the previous parameters will get retained regardless of whether the user has selected them or not. So we split the
    URL at the first occurrence of the ? (after which the previously selected parameters will be found) and retain
    only the 0th element of the split which corresponds to the base URL we want. */
    url_path = location.href.split('?')[0] + "?";
    console.log(url_path);
    {% for elem_id in link_data|id_names:0 %}
    if (document.getElementById("{{ elem_id }}").value == 1) {
        url_path += "{{ elem_id }}=Yes&";
    }
    {% endfor %}
    {% for elem_id in link_props|id_names:0 %}
    if (document.getElementById("{{ elem_id }}").value == 1) {
        url_path += "{{ elem_id }}=Yes&";
    }
    {% endfor %}
    {% for elem_id in filter_options %}
    if (document.getElementById("{{ elem_id }}").value == 1) {
        url_path += "{{ elem_id }}=Yes&";
    }
    {% endfor %}
    console.log(url_path);
return url_path;
}

/* qm_advanced */
{#This function will make sure that only one of the range options is selected by iterating through all the range_options#}
{#within the option set and resetting their values except for the value of the clicked button.#}
function single_select(elem){
    var button_temp;
    {% for option_id in range_strings %}
        if (elem.id != "{{ option_id }}") {
            button_temp = document.getElementById("{{option_id}}");
            console.log(button_temp);
            button_temp.style.backgroundColor = "#cecece";
            button_temp.value = 0;
        } else {
            if (elem.value == 0){
                elem.value = 1;
                elem.style.backgroundColor = "#f44336";
        }
            else{
                elem.value = 0;
                elem.style.backgroundColor = "#cecece";
            }
        }
    {% endfor %}
}
/* Setting the initial value of the All and Include buttons so that they appear to be chosen by default */
$(document).ready(function() {
    var temp1 = document.getElementById("All");
    var temp2 = document.getElementById("Inc");
    temp1.style.backgroundColor = "#f44336";
    temp1.value = 1;
    temp2.style.backgroundColor = "#f44336";
    temp2.value = 1;
});
function generate2(id_no) {
    var url_path = location.href.split('/')[0] + '/qmbasic/' + id_no.toString();
    return url_path;
}
    function btn_fn2(elem) {
        var temp_elem;
        if (elem.value == 0){
            if (elem.id == "All"){
                temp_elem = document.getElementById("Any");
            }
            else{
                temp_elem = document.getElementById("All");
            }
            temp_elem.value = 0;
            temp_elem.style.backgroundColor = "#cecece";
            elem.value = 1;
            elem.style.backgroundColor = "#f44336";
        }
    }
    function btn_fn3(elem) {
        var temp_elem;
        if (elem.value == 0){
            if (elem.id == "Inc"){
                temp_elem = document.getElementById("Exc");
            }
            else{
                temp_elem = document.getElementById("Inc");
            }
            temp_elem.value = 0;
            temp_elem.style.backgroundColor = "#cecece";
            elem.value = 1;
            elem.style.backgroundColor = "#f44336";
        }
    }
    function btn_fn1(elem) {

  if (elem.value == 0){
  elem.style.backgroundColor = "#f44336";
  elem.value = 1;
}
else if (elem.value == 1){
    elem.style.backgroundColor = "#cecece";
elem.value = 0;
}
}
function generate(el) {
    var url_path;
    /* Base url path has been defined. After that link_data|id_names:0 will return the list of element ids on the
    page following which we get each element by id after typecasting it to a string (this is necessary because otherwise
    if you check the generated source code you will see that there are no quotes around the id name and this raises
    a getElementById null error. The query_update filter will append =Yes& to the id field. Then the string is returned
    at the end. */
    /* Can't just directly use location.href and keep appending to that because otherwise every time the page is loaded
    the previous parameters will get retained regardless of whether the user has selected them or not. So we split the
    URL at the first occurrence of the ? (after which the previously selected parameters will be found) and retain
    only the 0th element of the split which corresponds to the base URL we want. */
    url_path = location.href.split('?')[0] + "?";
    console.log(url_path);

    {% for _, value in qm_fieldnames.items %}
        {% for elem_id in value %}
            {#Have to do this otherwise I get element document.getElementbyId null error while trying to get the rangee #}
            {#button since it doesn't exist#}
            {% if elem_id != "rangee" %}
            if (document.getElementById("{{ elem_id }}").value == 1) {
            url_path += "{{ elem_id }}=Yes&";
    }
            {% endif %}
        {% endfor %}
    {% endfor %}
    {% for elem_id in filter_options %}
    if (document.getElementById("{{ elem_id }}").value == 1) {
        url_path += "{{ elem_id }}=Yes&";
    }
    {% endfor %}
{% for range_eqn, eqn_id in range_options %}
    if (document.getElementById("range_eqn{{ eqn_id }}").value == 1) {
                url_path += "range_eqn{{ eqn_id }}=Yes&";
        }
    {% endfor %}

    //console.log(url_path);
return url_path;
}

/* task_advanced */
{#This function will make sure that only one of the range options is selected by iterating through all the range_options#}
{#within the option set and resetting their values except for the value of the clicked button.#}
function single_select(elem){
    var button_temp;
    {% for option_id in range_strings %}
        if (elem.id != "{{ option_id }}") {
            button_temp = document.getElementById("{{option_id}}");
            console.log(button_temp);
            button_temp.style.backgroundColor = "#cecece";
            button_temp.value = 0;
        } else {
            if (elem.value == 0){
                elem.value = 1;
                elem.style.backgroundColor = "#f44336";
        }
            else{
                elem.value = 0;
                elem.style.backgroundColor = "#cecece";
            }
        }
    {% endfor %}
}
/* Setting the initial value of the All and Include buttons so that they appear to be chosen by default */
$(document).ready(function() {
    var temp1 = document.getElementById("All");
    var temp2 = document.getElementById("Inc");
    temp1.style.backgroundColor = "#f44336";
    temp1.value = 1;
    temp2.style.backgroundColor = "#f44336";
    temp2.value = 1;
});
function generate2(id_no) {
    var url_path = location.href.split('/')[0] + '/qmbasic/' + id_no.toString();
    return url_path;
}
    function btn_fn2(elem) {
        var temp_elem;
        if (elem.value == 0){
            if (elem.id == "All"){
                temp_elem = document.getElementById("Any");
            }
            else{
                temp_elem = document.getElementById("All");
            }
            temp_elem.value = 0;
            temp_elem.style.backgroundColor = "#cecece";
            elem.value = 1;
            elem.style.backgroundColor = "#f44336";
        }
    }
    function btn_fn3(elem) {
        var temp_elem;
        if (elem.value == 0){
            if (elem.id == "Inc"){
                temp_elem = document.getElementById("Exc");
            }
            else{
                temp_elem = document.getElementById("Inc");
            }
            temp_elem.value = 0;
            temp_elem.style.backgroundColor = "#cecece";
            elem.value = 1;
            elem.style.backgroundColor = "#f44336";
        }
    }
    function btn_fn1(elem) {

  if (elem.value == 0){
  elem.style.backgroundColor = "#f44336";
  elem.value = 1;
}
else if (elem.value == 1){
    elem.style.backgroundColor = "#cecece";
elem.value = 0;
}
}
function generate(el) {
    var url_path;
    /* Base url path has been defined. After that link_data|id_names:0 will return the list of element ids on the
    page following which we get each element by id after typecasting it to a string (this is necessary because otherwise
    if you check the generated source code you will see that there are no quotes around the id name and this raises
    a getElementById null error. The query_update filter will append =Yes& to the id field. Then the string is returned
    at the end. */
    /* Can't just directly use location.href and keep appending to that because otherwise every time the page is loaded
    the previous parameters will get retained regardless of whether the user has selected them or not. So we split the
    URL at the first occurrence of the ? (after which the previously selected parameters will be found) and retain
    only the 0th element of the split which corresponds to the base URL we want. */
    url_path = location.href.split('?')[0] + "?";
    console.log(url_path);

    {% for _, value in qm_fieldnames.items %}
        {% for elem_id in value %}
            {#Have to do this otherwise I get element document.getElementbyId null error while trying to get the rangee #}
            {#button since it doesn't exist#}
            {% if elem_id != "rangee" %}
            if (document.getElementById("{{ elem_id }}").value == 1) {
            url_path += "{{ elem_id }}=Yes&";
    }
            {% endif %}
        {% endfor %}
    {% endfor %}
    {% for elem_id in filter_options %}
    if (document.getElementById("{{ elem_id }}").value == 1) {
        url_path += "{{ elem_id }}=Yes&";
    }
    {% endfor %}
{% for range_eqn, eqn_id in range_options %}
    if (document.getElementById("range_eqn{{ eqn_id }}").value == 1) {
                url_path += "range_eqn{{ eqn_id }}=Yes&";
        }
    {% endfor %}

    //console.log(url_path);
return url_path;
}