$(document).ready(function () {
    // returns the first child of the div #filters which is the button we want to check by default.
    if (document.getElementById('filters')){
    document.getElementById('filters').querySelector(".button").id = 'watchButton';}
    // Click before the scroll otherwise the click will be performed only after the scroll so it will look messy for a
    // split second when all the options are displayed together.
    // Automatically adds is-checked class to the first button after the click.
    add_redundant_elements();
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

function add_redundant_elements(){
    /* When there are certain filters sections under which no data is present, then I want this function which will
    run once the page is loaded to added a redundant element to those sections that will say that there is no content
    in this particular filter section. I start by checking if the page contains a filter section. If it does, i query
    all the buttons in that section and get their data-filter attribute and split at '.'. So far '.dt' i'll get ['', 'dt']
    So I take the 1st element. Then I search for all elements that have these class names. If the set of elements returned
    is a null set, that means a redundant element needs to be inserted. But this can't be a gradient-list with numbering.
    So what I do is i add red-grad along with gradient-list to the ol class. In pen_styles.css, red-grad is styled to remove
    the content of the before and after pseudo elements and center the text. I then create the li element and add it to
    the options-grid. However, for some reason isotope can't detect the new element added to the document. This is why
     we need to add the new element to the searchgrid's isotope function call which is what additems does. */
    var filter_div = document.getElementById('filters');
        if (filter_div){
            var buttons = filter_div.querySelectorAll(".button");
            var filter_vals = [];
            var index;
            for (index=0; index<buttons.length; index++){
                filter_vals.push(buttons[index].getAttribute("data-filter").split('.')[1]);
            }
            for (index=0; index<filter_vals.length; index++) {
                if (document.getElementsByClassName(filter_vals[index]).length == 0){
                    var red_ol = document.createElement("ol");
                    red_ol.setAttribute('class', 'red-grad gradient-list');
                    var red_li = document.createElement('li');
                    red_li.innerHTML = 'Nothing in this section';
                    red_li.setAttribute('class', 'grid-item '+filter_vals[index]);
                    red_ol.appendChild(red_li);
                    document.getElementsByClassName("option-grid")[0].appendChild(red_ol);
                    $('.option-grid').isotope( 'addItems', red_ol );
                }
            }
        }
}

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
