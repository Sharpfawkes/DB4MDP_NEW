$(document).ready(function () {
    // returns the first child of the div #filters which is the button we want to check by default.
    if (document.getElementById('filters')){
    document.getElementById('filters').querySelector(".button").id = 'watchButton';}
    // Click before the scroll otherwise the click will be performed only after the scroll so it will look messy for a
    // split second when all the options are displayed together.
    // Automatically adds is-checked class to the first button after the click.
    $("#watchButton").trigger('click');
    // Handler for .ready() called only for pages other than the intro page.
    if (document.getElementById('results')){
        $('html, body').animate({
            scrollTop: $('#results').offset().top
        }, 'slow');
    }
    else if (document.getElementById('searchgrid')){
        $('html, body').animate({
            scrollTop: $('#search-options').offset().top
        }, 'slow');
    }
    /* Advanced section */
    else if (document.getElementById('filters')){
        $('html, body').animate({
            scrollTop: $('#search-options').offset().top
        }, 'slow');
    }
});

// This function will make sure that only one of the range options is selected by iterating through all the range_options
// within the option set and resetting their values except for the value of the clicked button.
function single_select(elem, option_set){
    var button_temp;
    var option_id;
    var index;
    if (document.getElementById('All').value == 1) {
        for (index = 0; index < option_set.length; index++) {
            option_id = option_set[index];
            // console.log(option_id);
            if (elem.id != option_id) {
                button_temp = document.getElementById(option_id);
                // console.log(button_temp);
                $(button_temp).removeClass('is-checked');
                button_temp.value = 0;
            } else {
                sel_desel(elem);
            }
        }
    }
    else{
        sel_desel(elem);
    }
}

function generate_url(id_val, reroute_string) {
    var url_path = location.href.split('/')[0] + '/'+reroute_string+'/' + id_val.toString();
    return url_path;
}

function btn_fn(elem, id_vals) {
    var temp_elem;
    if (elem.value == 0){
        if (elem.id == id_vals[0]){
            temp_elem = document.getElementById(id_vals[1]);
        }
        else{
            temp_elem = document.getElementById(id_vals[0]);
        }
        $(temp_elem).removeClass('is-checked');
        temp_elem.value=0;
        elem.value = 1;
        $(elem).addClass('is-checked');
    }
}

function sel_desel(elem) {
    if (elem.value == 0){
          $(elem).addClass('is-checked');
          elem.value = 1;
    }
    else if (elem.value == 1){
        $(elem).removeClass('is-checked');
        elem.value = 0;
    }
    }



function generate(arr_of_ids) {
    var url_path, index, index2, temp;
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
    for (index = 0; index < arr_of_ids.length; index++){
        for (index2 = 0; index2 < arr_of_ids[index].length; index2++){
            temp = arr_of_ids[index][index2];
            if (document.getElementById(temp).value == 1){
                url_path += (temp+"=Yes&");
            }
        }
    }
    // {% for elem_id in link_data|id_names:0 %}
    // if (document.getElementById("{{ elem_id }}").value == 1) {
    //     url_path += "{{ elem_id }}=Yes&";
    // }
    // {% endfor %}
    // {% for elem_id in link_props|id_names:0 %}
    // if (document.getElementById("{{ elem_id }}").value == 1) {
    //     url_path += "{{ elem_id }}=Yes&";
    // }
    // {% endfor %}
    // {% for elem_id in filter_options %}
    // if (document.getElementById("{{ elem_id }}").value == 1) {
    //     url_path += "{{ elem_id }}=Yes&";
    // }
    // {% endfor %}
return url_path;
}
