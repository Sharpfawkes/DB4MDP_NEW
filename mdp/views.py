from django.shortcuts import render
from django.forms.models import model_to_dict
from .models import *
from django.db.models import Q, Count
from django.core.exceptions import ObjectDoesNotExist

# Allow to filter horizontal ie search bar for references in admin
# Allow to clear options for range section and also for tasks input/output space
# The single_select option only needs to be there when All is selected. For any, multi-select should be allowed.
# Task when displaying results in the advanced section, should the children be left out?
# When reloading the page after a query, don't reset the state of the buttons. I think this should be taken care of
# by an AJAX request though.

# Have a clear all selected options button. Just have a div within which all the options are present.
# Find all elements that are buttons within that div and reset their state.
# Tables
# QM - Done both Basic and Advanced
# Langs - Both MDPs and Langs done
# Task - Done both Basic and Advanced
# MDP - Done but have to make get changes to basic
# Enrichment - Not started

# Things to check with Dr. Michael
# What to call the QM_Parameter Options
# How to introduce the child tasks section etc in the Task Table

# Create your views here.
# https://stackoverflow.com/questions/52428124/django-manytomany-field-returns-none-but-it-has-related-records
# https://stackoverflow.com/questions/48176774/django-path-doesnt-find-the-right-primary-key-in-url-path
# https://stackoverflow.com/questions/21925671/convert-django-model-object-to-dict-with-all-of-the-fields-intact
# https://stackoverflow.com/questions/14456503/how-to-get-a-particular-attribute-from-queryset-in-django-in-view
# https://stackoverflow.com/questions/4424435/how-to-convert-a-django-queryset-to-a-list Check itertools here
# Retrieving many-to-many field information from a returned queryset
# https://stackoverflow.com/questions/52428124/django-manytomany-field-returns-none-but-it-has-related-records
# Checking the size of a passed parameter from within the template. If the size is 0 then we don't have to render the
# element. This can prevent subsection headings from being rednered even when there is no information to be displayed
# within the subsection.
# https://stackoverflow.com/questions/902034/how-can-i-check-the-size-of-a-collection-within-a-django-template
# Checking variable values passed back using the url
# https://stackoverflow.com/questions/150505/capturing-url-parameters-in-request-get
# Q objects
# https://stackoverflow.com/questions/20222457/django-building-a-queryset-with-q-objects
# https://stackoverflow.com/questions/8144582/django-how-do-i-use-a-string-as-the-keyword-in-a-q-statement
# Viewing raw SQL Queries
# https://stackoverflow.com/questions/971667/how-to-view-corresponding-sql-query-of-the-django-orms-queryset
# Setting up the django debug toolbar https://www.youtube.com/watch?v=XdArRS9kP6U
# https://stackoverflow.com/questions/971667/how-to-view-corresponding-sql-query-of-the-django-orms-queryset

# https://stackoverflow.com/questions/14327036/count-vs-len-on-a-django-queryset
# https://stackoverflow.com/questions/27213752/collecting-staticfiles-throws-improperlyconfigured
# Django modifying admin templates
# https://stackoverflow.com/questions/398163/ordering-admin-modeladmin-objects
# https://books.agiliq.com/projects/django-admin-cookbook/en/latest/set_ordering.html
# https://stackoverflow.com/questions/12308530/how-to-catch-specific-error-in-any-template-in-django
# https://stackoverflow.com/questions/20952156/how-to-pass-javascript-variable-to-django-custom-filter
# https://stackoverflow.com/questions/47648886/difference-between-strdict-and-json-dumpsdict
# https://stackoverflow.com/questions/1413122/is-autoescape-off-in-django-safe
# https://stackoverflow.com/questions/45163299/django-group-by-field-value
# https://stackoverflow.com/questions/12809416/django-static-files-404

data_type_fieldnames = ['dissimilarity_id', 'ordinal_id', 'cartesian_id', 'ne_structures_id', 'categorical_id']
tax_fieldnames = ['linearity_id', 'supervision_id', 'multi_level_id', 'locality_id', 'steerability_id',
                  'stability_id', 'out_of_core_data_id']
qm_fieldnames = {'Span': ['local', 'glob'], 'Distortion Type': ['dissimilarity', 'correlation',
                                                                'probability', 'rank', 'geometric',
                                                                'set_difference', 'homology'],
                 'Output': ['rangee', 'best']}
task_fieldnames = [['Task Type', 'task_type'], ['Input Space', 'input_space'], ['Output Space', 'output_space'],
                   ['Actor', 'actor'], ['Target Space', 'ts']
                   ]
parameter_text = [['Local', 'Global'], ['Dissimilarity', 'Correlation', 'Probability', 'Rank', 'Geometric',
                                        'Set Difference', 'Homology'],
                  ['Range', 'Best']]
filter_options = ['All', 'Any', 'Inc', 'Exc']
projtech_fieldname = ['mdp_fullname', 'mdp_name']
txtdisp_data = ['Dissimilarity', 'Ordinal', 'Cartesian', 'Neighbouring Structures', 'Categorical']
txtdisp_tax = [((i.split('_id')[0]).replace('_', ' ')).title() for i in tax_fieldnames]
# A list of sublists where sublist[0] = Parameter Display Name
#                          sublist[1] = Parameter Query Name
#                          sublist[2] = Parameter used to query returned object
task_fields = [
    ['Task Type', 'task_type', 'type_name'],
    ['Input Space', 'input_space', 'mathjaxeqn'], ['Output Space', 'output_space', 'mathjaxeqn'],
    ['Actor', 'actor', None], ['Target Space', 'ts', 'mathjaxeqn'],
    ['MDP Property', 'task_property', 'mdp_property'],
    ['Best Matching MDPs', 'best_mdp_list', 'best_matching_mdp'],
    # ['Parent Task', 'parent_id', 'task_name'],
    # ['Reference', 'reference_list', None]
]


def getvalues(queryset, fieldnames):
    data = []
    for i in range(len(fieldnames)):
        data.append(getattr(queryset, fieldnames[i]))
    return data


def mdpbasic(request, pk=None):
    # batch_size = 3  # Change to change the number of boxes displayed per row on the basic page.
    data = MDP.objects.values('mdp_name', 'mdp_id').order_by('mdp_id')
    # Will contain a dictionary of the handling ability id and the text mapped to that id. So that I don't have to
    # make queries for every single attribute in the database whenever i need to fetch the text.
    handling_text = {}
    for c in HandlingAbility.objects.all():
        handling_text[c.id] = c.technique_handling_ability
    # using get will return the verbose name of the object retrieved. In order to access the individual attributes,
    # we can either use the dot operator or python's getattr function
    try:
        projection_technique = MDP.objects.get(mdp_id=pk)
        # No need to use filter here because we will only be retrieving one item
        complexity = (MathJaxFormulas.objects.get(id=projection_technique.complexity_id)).mathjaxeqn
        datatype_vals = getvalues(projection_technique, data_type_fieldnames)
        tax_vals = getvalues(projection_technique, tax_fieldnames)
        projtech_name = getvalues(projection_technique, projtech_fieldname)
        # print(datatype_vals)
        # datatype_vals = (list(projection_technique.values_list('dissimilarity_id', 'ordinal_id', 'cartesian_id',
        #                                                       'ne_structures_id', 'categorical_id'
        #                                                       )
        #                      )
        #                 )[0]
        reference = projection_technique.reference_paper
        print(projection_technique.variant_refs.all())
        # These numbers are those that don't have a projection technique associated wiht them in the paper
        variant_ref_nos = projection_technique.variant_refs.all()
        # These are those that have a name associated with them ex: iPCA
        # Till .all() will return a set of objects from the variants table and then we retrieve only the
        # variant_name and variant_references attributes in a queryset.
        # need to typecast the tuples into a list so that i can modify them later on. That's why list(i)
        tech_variants = [list(i) for i in
                         list(projection_technique.tech_variants.all().values_list('variant_name', 'variant_reference'))]
        variant_refs = [variant_ref for (_, variant_ref) in tech_variants]
        # This will give us the __str__ of the object which will have both the id as well as the citation text
        ref_vals = Reference.objects.filter(id__in=variant_refs)
        for tech_variant in tech_variants:
            for ref_val in ref_vals:
                if tech_variant[1] == ref_val.id:
                    tech_variant[1] = ref_val
        description = projection_technique.description
        # print(tech_variants, ref_vals)
        return render(request, 'mdpbasictemp.html',
                      {"mdp_list": data, "projtechname": projtech_name,
                       "handling_text": handling_text,
                       "text_display": txtdisp_data, "data_type_vals": datatype_vals,
                       "text_tax": txtdisp_tax, "tax_vals": tax_vals,
                       "complexity": complexity, "reference": reference,
                       "varrefno": variant_ref_nos, "tech_variants": tech_variants,
                       "description": description,
                       "reroute_string": "mdpbasic",
                       'got_item': True}
                      )
    except ObjectDoesNotExist:
        return render(request, 'mdpbasic.html',
                      {'mdp_list': data, 'got_item': False}
                      )




def qmbasic(request, pk):
    data = QualityMeasure.objects.values('measure_name', 'measure_id').order_by('measure_id')
    measure_method = QualityMeasure.objects.get(measure_id=pk)
    # No need to use filter here because we will only be retrieving one item
    rangee = measure_method.rangee
    field_vals = []
    qm_fieldsets = [value for _, value in qm_fieldnames.items()]
    # field_vals is a list of lists. Each list within the main list has exactly 2 elements (also lists). The first
    # element contains the values returned from the query corresponding to a particular section. Example for the Span
    # section we get the values [None, None] for example corresponding to ['Local', 'Global'] in the second element
    # The filter chaining in the template can be understood based on this. There are 2 possible objects that can be
    # returned as can be inferred from above i.e. a mathjaxformula object or a qm_parameter object. So in the template
    # I am checking if the object contains the mathjaxeqn parameter and if it doesn't I know it is a qm_parameter option
    # and then I can go for the parameter_option passed through the filter
    for index in range(len(qm_fieldsets)):
        fieldset = qm_fieldsets[index]
        field_vals.append([list(getvalues(measure_method, fieldset)), parameter_text[index]])
    references = measure_method.reference.all()
    description = measure_method.description

    return render(request, 'qmbasic.html',
                  {"qm_list": data, "measure_method": measure_method,
                   "qm_fielditems": qm_fieldnames.items(),
                   "parameter_text": parameter_text,
                   "field_vals": field_vals,
                   "references": references,
                   "description": description,
                   "reroute_string": "qmbasic"
                   }
                  )


def taskbasic(request, pk):
    # If it is a child task, then we need to use the parent_id to retrieve the
    # reference from the parent. This is because only the parent will have the reference number.
    data = Task.objects.values('task_name', 'task_id').order_by('task_id')
    task_retd = Task.objects.get(task_id=pk)
    description = task_retd.description
    parent_id = task_retd.parent_id
    numbers_ids = task_retd.numbers
    parent_obj = None
    numbers = None
    children = None
    if parent_id:
        print((Task.objects.get(task_id=parent_id.task_id)).task_id)
        parent_obj = getvalues(Task.objects.get(task_id=parent_id.task_id),
                               ['task_id', 'task_name', 'reference_list'])
        reference = parent_obj[2]
    else:
        reference = task_retd.reference_list
        child_objs = task_retd.child_id.all()
        if child_objs:
            children = child_objs.values('task_id', 'task_name')
    if numbers_ids:
        numbers = numbers_ids.all().values('task_id', 'task_name')

    return render(request, 'taskbasic.html',
                  {"task_list": data, "task_fields": task_fields,
                   "task_retd": task_retd, "reference": reference, "children": children, "parent_obj": parent_obj,
                   "numbers": numbers, "description": description,
                   "reroute_string": "taskbasic"
                   }
                  )


def get_lang_vals(object_data, parameter_name, language_data):
    language_data[parameter_name] = []
    for language in object_data.all():
        language_data[parameter_name].append([
            getvalues(language, ['language_id', 'language_name', 'description']),
            language.toolboxes_suppd.all()
        ])
    return language_data


def lang_mdps(request, pk):
    # If it is a child task, then we need to use the parent_id to retrieve the
    # reference from the parent. This is because only the parent will have the reference number.
    data = MDPsForLang.objects.values('mdp_name', 'mdp_id').order_by('mdp_id')
    projtech_retd = MDPsForLang.objects.get(mdp_id=pk)
    description = projtech_retd.description
    language_data = {}
    language_data = get_lang_vals(projtech_retd.circle_list, "Toolboxes_list", language_data)
    language_data = get_lang_vals(projtech_retd.square_list, "Libraries_List", language_data)
    print("lang_data", language_data)
    references = projtech_retd.reference_list.all()

    return render(request, 'lang_mdps.html',
                  {"methods_list": data, "description": description,
                   "language_data": language_data, "references": references,
                   "reroute_string": "lang_mdps"
                   }
                  )

def get_operator(request):
    operator = "~" if (request.GET.get("Exc", '') == "Yes") else ""
    if request.GET.get("All", '') == "Yes":
        operator += "&"
    else:
        operator += "|"
    return operator

def nonetype_query_generator_fn(request, field_name_list, id_field = "mdp_id"):
    # Since the fields we are going to be querying from are strings, I'm putting the string of the column name into a
    # dictionary and packing it using the ** operator to pass as an argument. If the request returns the value Yes, that
    # means that the object was selected. We put the column string as the key of the dictionary and have the value as
    # None. This is because if the Include button is selected (as by default), we will be forming the query as
    # ~Q(parameter_name = None) so that all objects for which the parameter_name is not None will be returned in the
    # queryset.
    options = {}
    # # Basically if the Exc button has been selected that means we need to search for all the objects in which the
    # # parameters OTHER than the ones currently selected are non-null. So that means if dissimilarity is selected and
    # # so is exclude, that means we need to search for non-null values in every field EXCEPT for dissimilarity.
    # # The below code section will do that.
    for query_obj in field_name_list:
        request_val = request.GET.get(query_obj,'')
        # range_eqn not in query obj is used in the case of the qm advd section. This is because to render the rangee
        # section, we are not using the rangee field name but instead getting the mathjaxeqns. So range_eqn15 and so on
        # don't actually corresponds to fields in the database and so if we try to query from such fields we will get
        # errors. That's why the second if condition has been put. Objects with range_eqn15 will be handled separately.
        if request_val == "Yes" :
            # The database represents the absence of a value in a field using None. However, this is not the "None"
            # but the None datatype. And so we have to use None and not "None".
            options[query_obj] = None
    operator = get_operator(request)
    queries = Q()
    for key in options:
        # This will take care of the case where ALL techniques that are capable of handling a particular property
        # need to be retrieved.
        base_query = Q(**{key: options[key]})
        if "&" in operator:
            if "~" in operator:
                queries &= base_query
            else:
                queries &= (~base_query)
        # This will take care of the case where ANY techniques that are capable of handling a particular property
        # need to be retrieved.
        else:
            if "~" in operator:
                queries |= base_query
            else:
                queries |= (~base_query)
    # When the advanced pages are first rendered no fields are selected by default. So the options field doesn't
    # contain any parameters and as a results, queries is empty i.e. there is no filter applied to the objects. Thus,
    # the objects will be returned the first time the page is rendered and all the techniques will be displayed in the
    # results section. To circumvent this, I check if options is empty and if it is, I check for all objects where the
    # id field is NULL. Since the id field is a primary key and can't ever be NULL, no objects will be returned. This
    # is why the options parameter also needs to be passed back. On the advanced pages where both the reg and none_type
    # query generator are used, both option dictionaries need to be checked before it can be concluded that no options
    # was selected.
    return (queries, options)


def mdpadvanced(request):
    link_data = list(zip(data_type_fieldnames, txtdisp_data))
    link_props = list(zip(tax_fieldnames, txtdisp_tax))
    queries, options = nonetype_query_generator_fn(request, data_type_fieldnames + tax_fieldnames)
    if not options:
        queries = Q(**{"mdp_id": None})
    results = MDP.objects.filter(queries).values('mdp_id', 'mdp_name', 'mdp_fullname')
    # print(results)
    # print(len(results), results)
    return render(request, "mdpadvanced.html",
                  {
                      "link_data": link_data, "link_props": link_props,
                      "filter_options": filter_options, "results": results,
                  })

def reg_query_generator_fn(request, regquery_strings, trivial_string = "range_eqn", field_name = "rangee"):
    # For the none_type query generator, each string that was passed as an options key was unique. However here,
    # range_eqn15 and range_eqn16 both correspond to one key i.e. the rangee field in the main table. This is why on the
    # site, we need to make sure that when only 1 button in the range section has been selected because each technique
    # can have only one range formula. The same will apply for when we are doing the input space.
    options = {}
    for query_obj in regquery_strings:
        request_val = request.GET.get(query_obj,'')
        # Suppose range_eqn15 gives us the value true, we need only the integer value to query against the rangee_id
        # field in the database. The trivial string here is range_eqn, so we split on that and take the 2nd element of
        # the list which is the id. So now that we have the id of the field, we want to check if the id is present in
        # the rangee field. But since we have the range id and not the value of the equation, we need to use rangee_id
        # not just rangee and that's why I have added the _id below.
        if request_val == "Yes":
            id_obtd = int(query_obj.split(trivial_string)[1])
            options[(field_name+"_id")] = id_obtd
            break
    operator = get_operator(request)
    queries = Q()
    for key in options:
        # This will take care of the case where ALL techniques that are capable of handling a particular property
        # need to be retrieved.
        base_query = Q(**{key: options[key]})
        if "&" in operator:
            if "~" in operator:
                queries &= (~base_query)
            else:
                queries &= base_query
        # This will take care of the case where ANY techniques that are capable of handling a particular property
        # need to be retrieved.
        else:
            if "~" in operator:
                queries |= (~base_query)
            else:
                queries |= base_query
    return (queries, options)


def qmadvanced(request):
    qmfield_strings = []
    for i in qm_fieldnames.values():
        qmfield_strings += i
    # In the view we will use the dictionary to dynamically display sections. Except for the rangee parameter. There
    # instead of just displaying rangee text, we will instead query for all the objects from mathjaxeqns whose type is
    # rangee and then display those as options. We just need to append those generated ids to qm_fieldstrings
    # before generating the queries. The id for the range objects will be range_eqn_16 for an equation whose id is 16.
    range_options = list(MathJaxFormulas.objects.filter(equation_type_id=2).values_list('mathjaxeqn', 'id'))
    # print(range_options)
    qmfield_strings.remove('rangee')
    regquery_strings = ["range_eqn"+str(id) for _, id in range_options]
    queries, options1 = nonetype_query_generator_fn(request, qmfield_strings, 'measure_id')
    reg_queries, options2 = reg_query_generator_fn(request, regquery_strings)
    # print(reg_queries)
    # range_eqn not in query obj is used in the case of the qm advd section. This is because to render the rangee
    # section, we are not using the rangee field name but instead getting the mathjaxeqns. So range_eqn15 and so on
    # don't actually corresponds to fields in the database and so if we try to query from such fields we will get
    # errors. That's why the second if condition has been put. Objects with range_eqn15 will be handled separately.
    operator = get_operator(request)
    # The individual query generator functions have already handled for include/exclude. Now the just need to AND or
    # OR the resultant generated queries together.
    if "&" in operator:
        queries &= reg_queries
        print(queries)
    else:
        queries |= reg_queries
    # Check in mdp_advanced for the explanation of this statement.
    if not options1 and not options2:
        queries = Q(**{"measure_id": None})

    results = QualityMeasure.objects.filter(queries).values('measure_id', 'measure_name')
    # print(len(results), results)
    return render(request, "qmadvanced.html",
                  {
                      "parameter_text": parameter_text, "qm_fieldnames": qm_fieldnames,
                      "filter_options": filter_options, "results": results, "range_options": range_options,
                      "range_strings": regquery_strings
                  })

def taskadvanced(request):
    # This will be a dictionary. The key is going to be the trivial string that will be passed to the query_generator.
    # The values are going to be 2-element lists that have the id of the element from the respective table and also
    # the string to be displayed on the webpage.
    task_fieldoptions = {}
    task_types = list(TaskType.objects.all().values_list('id', 'type_name'))
    task_fieldoptions['task_type'] = task_types
    # print(task_types)
    spaces = list(Task.objects.all().values_list('input_space', 'output_space'))
    input_space_ids, output_space_ids = [i[0] for i in spaces], [i[1] for i in spaces]
    input_space_objects = list((MathJaxFormulas.objects.filter(id__in=input_space_ids)).values_list('id', 'mathjaxeqn'))
    # print(input_space_objects)
    output_space_objects = list((MathJaxFormulas.objects.filter(id__in=output_space_ids)).values_list(
        'id', 'mathjaxeqn')
    )
    task_fieldoptions['in_sp'] = input_space_objects
    task_fieldoptions['out_sp'] = output_space_objects
    ts_options = list(MathJaxFormulas.objects.filter(equation_type_id=4).values_list('id', 'mathjaxeqn'))
    # print(ts_options)
    task_fieldoptions['ts_opt'] = ts_options
    task_fieldoptions['actor'] = [("U", "U"), ("M", "M"), ("U&M", "U&M")]
    regquery_strings = []
    for key, values in task_fieldoptions.items():
        temp = []
        for value in values:
            # value[0] is the id of the object and key is the trivial string.
            temp.append(key + str(value[0]))
        regquery_strings.append(temp)
    # print(regquery_strings)
    # print(task_fieldoptions)
    query_sets = []
    option_set = []
    operator = get_operator(request)
    trivial_strings = list(task_fieldoptions.keys())
    index = 0
    for _, field_name in task_fieldnames:
        reg_queries, options = reg_query_generator_fn(request, regquery_strings[index],
                                                      trivial_string=trivial_strings[index], field_name=field_name)
        index += 1
        query_sets.append(reg_queries)
        option_set.append(options)
    combined_query = Q()
    for query_set in query_sets:
        if "&" in operator:
            combined_query &= query_set
        else:
            combined_query |= query_set
    flag = 1
    for options in option_set:
        if options:
            flag = 0
            break
    if flag == 1:
        combined_query = Q(**{"task_id": None})

    results = Task.objects.filter(combined_query).values('task_id', 'task_name')
    # print(len(results), results)
    return render(request, "taskadvanced.html",
                  {
                      "task_fieldnames": task_fieldnames, "task_fieldoptions": task_fieldoptions,
                      "filter_options": filter_options, "results": results,
                      "query_strings": regquery_strings
                  })

def lang_langs(request, pk):
    data = Languages.objects.values('language_name', 'language_id').order_by('language_id')
    language_retd = Languages.objects.get(language_id=pk)
    all_mdps_handled = MDPsForLang.objects.all()
    mdps_handled = []
    for mdp_object in all_mdps_handled:
        # Getting the list of querysets containing toolboxes and libraries separately
        mdp_langs = [i.all() for i in getvalues(mdp_object, ['circle_list', 'square_list'])]
        for query_set in mdp_langs:
            # The below if statements generates a ton of queries that use inner join etc. Instead using the .exists
            # property to search for whether the object is present in the query should be faster.
            # if language_retd in query_set:
            #     mdps_handled.append(mdp_object)
                # If I've already found it in the first i.e. toolboxes queryset I don't want to search libraries also.
            if query_set.filter(language_id=pk).exists():
                mdps_handled.append(mdp_object)
                break
    description = language_retd.description
    toolboxes_suppd = language_retd.toolboxes_suppd.all()

    return render(request, 'lang_langs.html',
                  {"language_list": data, "description": description,
                   "toolboxes_suppd": toolboxes_suppd, "mdps_handled": mdps_handled,
                   "reroute_string": "lang_langs"
                   }
                  )

def enrichbasic(request, pk):
    type_objects = EnrichmentType.objects.all()
    type_strings = list(type_objects.values_list('type_name', flat=True))
    enrich_dict = {}
    for index in range(len(type_strings)):
        type_name = type_strings[index]
        type_object = type_objects[index]
        enrich_dict[type_name] = Enrichment.objects.filter(enrichment_type=type_object)
    enrichment_retd = Enrichment.objects.get(enrichment_id=pk)
    references = enrichment_retd.references.all()
    return render(request, 'enrichbasic.html',
                  {'enrichment_info': enrich_dict,
                   "enrichment_retd": enrichment_retd,
                   "references": references
                   }
                  )

def do_nothing(request):
    return render(request, 'introduction.html')


