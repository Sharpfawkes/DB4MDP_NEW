from django.shortcuts import render

from django.template.response import TemplateResponse
from mdp.models import MDP, Languages, QualityMeasure, Task, Enrichment, AboutPage, Reference

from django.template.context import RequestContext
import mdp.dictionary as dicti

from django.db.models import Q, Max

from django.http import HttpResponse
from .resources import QualityResource, MDPResource, TaskResource, EnrichmentResource, LanguagesResource
from itertools import chain

from tracking_analyzer.models import Tracker
from django.shortcuts import get_object_or_404

'''Instead of having 4 columns as it is currently, I have an idea for a drop down. In the advanced section, allow the user to choose multiple parameters for each 
column. Display the possible parameters, ask them to enter the number of parameters to be applied or add a plus feature where they can keep adding as desired. The
benefit of this is you won't have to individually check every button on the page for its state. Have an add all button that will let the user add all options under
a particular column immediately so that they can later remove whatever they want. Atleast create a dropdown table if nothing else (ie separate tables for each column
that can be opened or closed as desired)'''


def dictionary():
    return dicti.referencesdict


'''Instead of having just one column for mdp basic, we'll have two. One will have everything specific to the method. i.e. latex symbols, references etc.
The second table will be a list of all parameters such as dissimilarity etc. (as rows) and with the method names as columns. Depending on the data returned, the name is passed to the 
second table and used to filter out the parameters to be displayed.'''


def mdp(request):
    # data= MDP.objects.filter(mdp_id=pk)
    # data= get_object_or_404(MDP, mdp_id=pk) get not working
    return TemplateResponse(request, 'homepage.html', {})


def contact(request):
    return TemplateResponse(request, 'contact.html', {})


def filter_keep_index(type_list):
    new_list = []
    for i in range(len(type_list)):
        if type_list[i] not in new_list:
            new_list.append(type_list[i])
    return new_list


def content_order(content, batch_size=3, key="mdp_name"):
    height = int(len(content) / batch_size)
    loop = 0
    for method_dict in content:
        loop += 1
        method_dict[key] = [method_dict[key], loop]
        if loop == batch_size:
            loop = 0
    return (content, height)


def about(request):
    people = AboutPage.objects.values('name', 'email', 'designation', 'employee_of', 'image_name').order_by('id')
    batch_size = 2
    content = content_order(people, batch_size, key="name")
    ordered_content, height = content[0], content[1]
    return TemplateResponse(request, 'about.html',
                            {'height': height, 'batch_size': batch_size, 'ordered_content': ordered_content})


def get_references_1(pk, id_query, id_field='mdp_id', ref_field_name='reference'):
    # print(list(MDP.objects.values(id_field)))
    max_id = id_query.aggregate(Max(id_field))[id_field + '__max']
    min_id = max_id - len(id_query)
    # print(min_id, max_id)
    return (max_id, min_id)


def data_clean_up(messy_data):
    temp = ((((((messy_data.replace('[', ' ')).replace(']', ' '))).replace(',', ' ')).replace('.', ' ')).replace('-',
                                                                                                                 ' ').split(
        ' '))
    while '' in temp:
        temp.remove('')
    return temp


def get_references_2(data, ref_field_name='reference'):
    reference_list = (' ').join([ref_dict[ref_field_name] for ref_dict in data])
    # print(reference_list, 'getref2reflist')
    reference_ids = data_clean_up(reference_list)
    references = []
    query = list(Reference.objects.values('citation').filter(id__in=reference_ids))
    # print(query)
    for reference in query:
        references.append(reference['citation'])
    # print(references)
    return references


def mdpbasic(request, pk):
    # changes_file = open("new_changes.txt",'r')
    # content2 = changes_file.read()
    batch_size = 3  # Change to change the number of boxes displayed per row on the basic page.
    data = content_order(MDP.objects.values('mdp_name').order_by('mdp_id'), batch_size)
    ordered_content, height = data[0], data[1]
    data = MDP.objects.filter(mdp_id=pk)
    data2 = Variants.objects.filter(mdp_id_id=pk)
    data3 = Languages.objects.filter(mdp_id_id=pk)
    data4 = Task.objects.filter(mdp_id_id=pk)
    reference_temp, references = '', ''
    id_query = MDP.objects.values('mdp_id')
    print(data)
    print(data['dissimilarity'], 'this is many to many field')
    max_id, min_id = get_references_1(id_query=id_query, pk=pk)
    print('this is pk', [pk])
    if int(pk) > min_id and int(pk) < max_id + 1:
        reference_temp = (list((MDP.objects.values('reference')).filter(mdp_id=pk)))
        # projection_method = get_object_or_404(MDP, mdp_id=int(pk))
        # print(type(projection_method))
        # Tracker.objects.create_from_request(request, projection_method)
    print(reference_temp, [pk])
    if reference_temp != '':
        references = get_references_2(reference_temp)

    return TemplateResponse(request, 'mdp-basic.html',
                            {"index": pk, "ordered_content": ordered_content, "batch_size": batch_size,
                             "height": height, "data": data, "data2": data2, "data3": data3, \
                             "data4": data4, "references": references, 'referencesdict': dictionary()})


def mdpbasicexport(request, pk):
    resource_class = MDPResource()
    queryset = MDP.objects.filter(mdp_id=pk)
    dataset = resource_class.export(queryset)
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="mdpbasic.csv"'
    return response


def mdpadvanced(request):
    # AND --> &
    # OR  --> |
    ## this is for mdp table
    data = Q()  # or
    datafinal = Q()  # and

    # this is for language table
    data11 = Q()  # or
    data33 = Q()  # and

    ##    #this is for FM and MN checkboxes
    ##    dataone=Q()
    ##    datatwo=Q()
    ##
    querylist = ['cartesian', 'cplusplus', 'categorical', 'java', 'dissimilarity', 'linearity', 'matlab', 'ordinal',
                 'locality', 'python', 'nestructures', 'multilevel' \
                                                       'javascript', 'stability', 'outofcoredata', 'steerability',
                 'pcaimage.png']
    for i in range(1, 14):
        querylist.append(str(i) + ".png")

    queryy = request.GET.get('cartesian', 'None')
    if (queryy != "None"):
        data = Q(mdp_id__cartesian=queryy)
        datafinal = Q(mdp_id__cartesian=queryy)
    ###
    queryy2 = request.GET.get('cplusplus', 'None')
    if (queryy2 != "None"):
        data11 = data11 | Q(cplusplus=queryy2)
        data33 = data33 & Q(cplusplus=queryy2)

    queryy3 = request.GET.get('categorical', 'None')
    if (queryy3 != "None"):
        data = data | Q(mdp_id__categorical=queryy3)
        datafinal = datafinal & Q(mdp_id__categorical=queryy3)

    ##
    queryy5 = request.GET.get('java', 'None')
    if (queryy5 != "None"):
        data11 = data11 | Q(java=queryy5)
        data33 = data33 & Q(java=queryy5)

    queryy6 = request.GET.get('dissimilarity', 'None')
    if (queryy6 != "None"):
        data = data | Q(mdp_id__dissimilarity=queryy6)
        datafinal = datafinal & Q(mdp_id__dissimilarity=queryy6)

    queryy7 = request.GET.get('linearity', 'None')
    if (queryy7 != "None"):
        data = data | Q(mdp_id__linearity=queryy7)
        datafinal = datafinal & Q(mdp_id__linearity=queryy7)
    ###
    queryy8 = request.GET.get('matlab', 'None')
    if (queryy8 != "None"):
        data11 = data11 | Q(matlab=queryy8)
        data33 = data33 & Q(matlab=queryy8)

    queryy9 = request.GET.get('ordinal', 'None')
    if (queryy9 != "None"):
        data = data | Q(mdp_id__ordinal=queryy9)
        datafinal = datafinal & Q(mdp_id__ordinal=queryy9)

    queryy10 = request.GET.get('locality', 'None')
    if (queryy10 != "None"):
        data = data | Q(mdp_id__locality=queryy10)
        datafinal = datafinal & Q(mdp_id__locality=queryy10)
    ###
    queryy11 = request.GET.get('python', 'None')
    if (queryy11 != "None"):
        data11 = data11 | Q(python=queryy11)
        data33 = data33 & Q(python=queryy11)

    queryy12 = request.GET.get('nestructures', 'None')
    if (queryy12 != "None"):
        data = data | Q(mdp_id__ne_structures=queryy12)
        datafinal = datafinal & Q(mdp_id__ne_structures=queryy12)

    queryy123 = request.GET.get('multilevel', 'None')
    if (queryy123 != "None"):
        data = data | Q(mdp_id__multi_level=queryy123)
        datafinal = datafinal & Q(mdp_id__multi_level=queryy123)

    ###
    queryy13 = request.GET.get('javascript', 'None')
    if (queryy13 != "None"):
        data11 = data11 | Q(javascript=queryy13)
        data33 = data33 & Q(javascript=queryy13)

    queryy14 = request.GET.get('outofcoredata', 'None')
    if (queryy14 != "None"):
        data = data | Q(mdp_id__out_of_core_data=queryy14)
        datafinal = datafinal & Q(mdp_id__out_of_core_data=queryy14)

    queryy16 = request.GET.get('stability', 'None')
    if (queryy16 != "None"):
        data = data | Q(mdp_id__stability=queryy16)
        datafinal = datafinal & Q(mdp_id__stability=queryy16)

    queryy17 = request.GET.get('steerability', 'None')
    if (queryy17 != "None"):
        data = data | Q(mdp_id__steerablity=queryy17)
        datafinal = datafinal & Q(mdp_id__steerablity=queryy17)

    queryy18 = request.GET.get('supervision', 'None')
    if (queryy18 != "None"):
        data = data | Q(mdp_id__supervision=queryy18)
        datafinal = datafinal & Q(mdp_id__supervision=queryy18)

    queryy19 = request.GET.get('pcaimage.png', 'None')
    if (queryy19 != "None"):
        data = data | Q(mdp_id__complexity=queryy19)
        datafinal = datafinal & Q(mdp_id__complexity=queryy19)

    queryy20 = request.GET.get('1.png', 'None')
    if (queryy20 != "None"):
        data = data | Q(mdp_id__complexity=queryy20)
        datafinal = datafinal & Q(mdp_id__complexity=queryy20)

    queryy21 = request.GET.get('4.png', 'None')
    if (queryy21 != "None"):
        data = data | Q(mdp_id__complexity=queryy21)
        datafinal = datafinal & Q(mdp_id__complexity=queryy21)

    queryy22 = request.GET.get('3.png', 'None')
    if (queryy22 != "None"):
        data = data | Q(mdp_id__complexity=queryy22)
        datafinal = datafinal & Q(mdp_id__complexity=queryy22)

    queryy23 = request.GET.get('4.png', 'None')
    if (queryy23 != "None"):
        data = data | Q(mdp_id__complexity=queryy23)
        datafinal = datafinal & Q(mdp_id__complexity=queryy23)

    queryy24 = request.GET.get('5.png', 'None')
    if (queryy24 != "None"):
        data = data | Q(mdp_id__complexity=queryy24)
        datafinal = datafinal & Q(mdp_id__complexity=queryy24)

    queryy25 = request.GET.get('6.png', 'None')
    if (queryy25 != "None"):
        data = data | Q(mdp_id__complexity=queryy25)
        datafinal = datafinal & Q(mdp_id__complexity=queryy25)

    queryy26 = request.GET.get('7.png', 'None')
    if (queryy26 != "None"):
        data = data | Q(mdp_id__complexity=queryy26)
        datafinal = datafinal & Q(mdp_id__complexity=queryy26)

    queryy27 = request.GET.get('8.png', 'None')
    if (queryy27 != "None"):
        data = data | Q(mdp_id__complexity=queryy27)
        datafinal = datafinal & Q(mdp_id__complexity=queryy27)

    queryy28 = request.GET.get('9.png', 'None')
    if (queryy28 != "None"):
        data = data | Q(mdp_id__complexity=queryy28)
        datafinal = datafinal & Q(mdp_id__complexity=queryy28)

    queryy29 = request.GET.get('10.png', 'None')
    if (queryy29 != "None"):
        data = data | Q(mdp_id__complexity=queryy29)
        datafinal = datafinal & Q(mdp_id__complexity=queryy29)

    queryy30 = request.GET.get('11.png', 'None')
    if (queryy30 != "None"):
        data = data | Q(mdp_id__complexity=queryy30)
        datafinal = datafinal & Q(mdp_id__complexity=queryy30)

    queryy31 = request.GET.get('12.png', 'None')
    if (queryy31 != "None"):
        data = data | Q(mdp_id__complexity=queryy31)
        datafinal = datafinal & Q(mdp_id__complexity=queryy31)

    queryy32 = request.GET.get('13.png', 'None')
    if (queryy32 != "None"):
        data = data | Q(mdp_id__complexity=queryy32)
        datafinal = datafinal & Q(mdp_id__complexity=queryy32)

    ##    query= request.GET.get('FM','None')
    ##    if(query !="None"):
    ##        data = Q(mdp_id__task_property__contains='FN')
    ##        datafinal = Q(mdp_id__task_property__contains='FN')
    ##
    ##    query= request.GET.get('MN','None')
    ##    if(query !="None"):
    ##        data = Q(mdp_id__task_property__contains='MN')
    ##        datafinal = Q(mdp_id__task_property__contains='MN')

    ##    ##or include
    ##    global queryset8
    ##    queryset8=MDP.objects.filter(data) #or include mdp table
    ##    global queryset9
    ##    queryset9=Languages.objects.filter(data11) #or include language table
    ##
    ##    ##or exclude
    ##    global queryset88
    ##    queryset88= MDP.objects.exclude(data)#or exclude mdp table
    ##    global queryset99
    ##    queryset99= Languages.objects.exclude(data11)#or exclude language table

    ##    ## and include
    ##    global queryset10
    ##    queryset10=MDP.objects.filter(data2)#and include mdp table
    ##    global queryset11
    ##    queryset11=Languages.objects.filter(data33)#and include language table
    ##
    ##    ## and exclude
    ##    global queryset100
    ##    queryset100=MDP.objects.exclude(data2)#and exclude mdp table
    ##    global queryset110
    ##    queryset110=Languages.objects.exclude(data33)#and exclude language table

    # global final
    # final = list(chain(queryset6, queryset7))

    check = Task.objects.filter(task_property__contains="FN")
    # and include
    global final
    final = Languages.objects.filter(data33) \
        .values_list('mdp_id__mdp_name', 'mdp_id__reference').filter(datafinal)

    # and exclude
    global final2
    final2 = Languages.objects.exclude(data33) \
        .values_list('mdp_id__mdp_name', 'mdp_id__reference').exclude(datafinal)

    # or include
    global final3
    final3 = Languages.objects.filter(data11) \
        .values_list('mdp_id__mdp_name', 'mdp_id__reference').filter(data)

    # or exclude
    global final4
    final4 = Languages.objects.exclude(data11) \
        .values_list('mdp_id__mdp_name', 'mdp_id__reference').exclude(data)

    return TemplateResponse(request, 'mdp-advanced.html',
                            {"check": check, "andinclude": final, "andexclude": final2, "orinclude": final3,
                             "orexclude": final4, "referencesdict": dictionary()})


def I_just_want_to_compress_this():
    ### or include
    ##def mdpadvancedexport1(request):
    ##    person_resource = MDPResource()
    ##    dataset = person_resource.export(final3)
    ##    response = HttpResponse(dataset.csv, content_type='text/csv')
    ##    response['Content-Disposition'] = 'attachment; filename="mdpadvanced.csv"'
    ##    return response
    ##
    ### or exclude
    ##def mdpadvancedexport2(request):
    ##    person_resource = MDPResource()
    ##    dataset = person_resource.export(final4)
    ##    response = HttpResponse(dataset.csv, content_type='text/csv')
    ##    response['Content-Disposition'] = 'attachment; filename="mdpadvanced.csv"'
    ##    return response
    ##
    ### and include
    ##def mdpadvancedexport3(request):
    ##    person_resource = LanguagesResource()
    ##    dataset = person_resource.export(final)
    ##    response = HttpResponse(dataset.csv, content_type='text/csv')
    ##    response['Content-Disposition'] = 'attachment; filename="mdpadvanced.csv"'
    ##    return response
    ##
    ### and exclude
    ##def mdpadvancedexport4(request):
    ##    person_resource = MDPResource()
    ##    dataset = person_resource.export(final2)
    ##    response = HttpResponse(dataset.csv, content_type='text/csv')
    ##    response['Content-Disposition'] = 'attachment; filename="mdpadvanced.csv"'
    ##    return response
    pass


def qualitybasic(request, pk):
    batch_size = 4  # Change to change the number of boxes displayed per row on the basic page.
    content = content_order(QualityMeasure.objects.values('measure_name', 'measure_id').order_by('measure_id'),
                            batch_size, "measure_name")
    ordered_content, height = content[0], content[1]
    data = QualityMeasure.objects.filter(measure_id=pk)
    reference_temp, references = '', ''
    id_query = QualityMeasure.objects.values('measure_id')
    max_id, min_id = get_references_1(id_query=id_query, id_field='measure_id', pk=pk)
    if int(pk) > min_id and int(pk) < max_id + 1:
        reference_temp = (list((QualityMeasure.objects.values('reference')).filter(measure_id=pk)))
    if reference_temp != '':
        references = get_references_2(reference_temp)
    return TemplateResponse(request, 'quality-basic.html',
                            {"ordered_content": ordered_content, "batch_size": batch_size, "height": height,
                             "data": data, "references": references})


def qualitybasicexport(request, pk):
    person_resource = QualityResource()
    queryset = QualityMeasure.objects.filter(measure_id=pk)
    dataset = person_resource.export(queryset)
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="qualitybasic.csv"'
    return response


def qualityadvanced(request):
    # AND --> &
    # OR  --> |
    data = Q()
    data2 = Q()
    queryy = request.GET.get('correlation', 'None')
    if (queryy != "None"):
        data = Q(correlation=queryy)
        data2 = Q(correlation=queryy)

    queryy2 = request.GET.get('rank', 'None')
    if (queryy2 != "None"):
        data = data | Q(rank=queryy2)
        data2 = data2 & Q(rank=queryy2)

    queryy3 = request.GET.get('globall', 'None')
    if (queryy3 != "None"):
        data = data | Q(globall=queryy3)
        data2 = data2 & Q(globall=queryy3)

    queryy5 = request.GET.get('local', 'None')
    if (queryy5 != "None"):
        data = data2 | Q(local=queryy5)
        data2 = data2 & Q(local=queryy5)

    queryy6 = request.GET.get('dissimilarity', 'None')
    if (queryy6 != "None"):
        data = data | Q(dissimilarity=queryy6)
        data2 = data2 & Q(dissimilarity=queryy6)

    queryy7 = request.GET.get('probability', 'None')
    if (queryy7 != "None"):
        data = data | Q(probability=queryy7)
        data2 = data2 & Q(probability=queryy7)

    queryy8 = request.GET.get('geometric', 'None')
    if (queryy8 != "None"):
        data = data | Q(geometric=queryy8)
        data2 = data2 & Q(geometric=queryy8)

    queryy9 = request.GET.get('set_difference', 'None')
    if (queryy9 != "None"):
        data = data | Q(set_difference=queryy9)
        data2 = data2 & Q(set_difference=queryy9)

    queryy10 = request.GET.get('homology', 'None')
    if (queryy10 != "None"):
        data = data | Q(homology=queryy10)
        data2 = data2 & Q(homology=queryy10)

    queryy11 = request.GET.get('16.png', 'None')
    if (queryy11 != "None"):
        data = data | Q(rangee=queryy11)
        data2 = data2 & Q(rangee=queryy11)

    queryy12 = request.GET.get('17.png', 'None')
    if (queryy12 != "None"):
        data = data | Q(rangee=queryy12)
        data2 = data2 & Q(rangee=queryy12)

    queryy13 = request.GET.get('18.png', 'None')
    if (queryy13 != "None"):
        data = data | Q(rangee=queryy13)
        data2 = data2 & Q(rangee=queryy13)

    queryy14 = request.GET.get('19.png', 'None')
    if (queryy14 != "None"):
        data = data | Q(rangee=queryy14)
        data2 = data2 & Q(rangee=queryy14)

    queryy15 = request.GET.get('20.png', 'None')
    if (queryy15 != "None"):
        data = data | Q(rangee=queryy15)
        data2 = data2 & Q(rangee=queryy15)

    global queryset1
    queryset1 = QualityMeasure.objects.filter(data)  # or include
    global queryset11
    queryset11 = QualityMeasure.objects.exclude(data)  # or exclude
    global queryset2
    queryset2 = QualityMeasure.objects.filter(data2)  # and include
    global queryset22
    queryset22 = QualityMeasure.objects.exclude(data2)  # and exclude

    return render(request, 'quality-advanced.html',
                  {"queryy3": queryy3, "data1": data, "data2": data2, "orqueryinclude": queryset1,
                   "orqueryexclude": queryset11, "andqueryinclude": queryset2, "andqueryexclude": queryset22,
                   "referencesdict": dictionary()})


# or include
def qualityadvancedexport1(request):
    person_resource = QualityResource()
    dataset = person_resource.export(queryset1)
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="qualityadvanced.csv"'
    return response


# or exclude
def qualityadvancedexport2(request):
    person_resource = QualityResource()
    dataset = person_resource.export(queryset11)
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="qualityadvanced.csv"'
    return response


# and include
def qualityadvancedexport3(request):
    person_resource = QualityResource()
    dataset = person_resource.export(queryset2)
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="qualityadvanced.csv"'
    return response


# and exclude
def qualityadvancedexport4(request):
    person_resource = QualityResource()
    dataset = person_resource.export(queryset22)
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="qualityadvanced.csv"'
    return response


def tasksbasic(request, pk):
    types = Task.objects.values('task_type')
    list_of_types = filter_keep_index([type['task_type'] for type in types])
    len_of_types = [len(Task.objects.filter(task_type=type_name)) for type_name in list_of_types]
    batch_size = len(list_of_types)
    grouped_names = []
    for i in range(batch_size):
        tasks = Task.objects.filter(task_type=list_of_types[i])
        grouped_names.append([[task.task_name, task.task_id] for task in tasks])

    reference_temp, references = '', ''
    id_query = Task.objects.values('task_id')
    max_id, min_id = get_references_1(id_query=id_query, id_field='task_id', pk=pk)
    best_mdps = [0]
    if int(pk) > min_id and int(pk) < max_id + 1:
        best_mdp_list = list(Task.objects.values('best_mdp_list').filter(task_id=pk))[0]['best_mdp_list']
        best_mdps = best_mdp_list.replace(',', ' ')
        best_mdps = best_mdps.split(' ')
        while '' in best_mdps:
            best_mdps.remove('')
        reference_temp = (list((Task.objects.values('reference_list')).filter(task_id=pk)))
    if reference_temp != '':
        references = get_references_2(reference_temp, ref_field_name='reference_list')

    sect_info, parent_s, subset, child, sect_len = "None", "NULL", "NULL", "NULL", "NULL"
    # print([pk], [task['task_id'] for task in list(Task.objects.values('task_id'))])
    # print([_ for _ in range(min_id+1, max_id+1)])
    if int(pk) in [_ for _ in range(min_id + 1, max_id + 1)]:
        linking = Task.objects.values('parent_id', 'task_subset', 'child_id').filter(task_id=pk)
        link_data = {}
        for key, value in linking[0].items():
            link_data[key] = value
        print(link_data, 'link_data')
        parent_s = link_data['parent_id'].split(' ')
        sect_len = [0, 0]
        sect_info = "None"
        if parent_s != ["NULL"]:
            sect_info = []
            for parent in parent_s:
                query = Task.objects.values('task_subset', 'task_name').filter(task_id=parent)[0]
                if (query['task_subset'] != "NULL"):
                    sect_info.append(['decomp', query['task_name']])
                    sect_len[0] += 1
                else:
                    sect_info.append(['parent', query['task_name']])
                    sect_len[1] += 1
            for i in range(len(sect_info)):
                sect_info[i] = [int(parent_s[i]), *sect_info[i]]
        subset = "NULL" if link_data['task_subset'] == "NULL" else [int(task_no) for task_no in
                                                                    link_data['task_subset'].split(' ')]
        if subset != "NULL":
            for i in range(len(subset)):
                query = Task.objects.values('task_name').filter(task_id=subset[i])
                subset[i] = [query[0]['task_name'], subset[i]]
        child = "NULL" if link_data['child_id'] == "NULL" else [int(task_no) for task_no in
                                                                link_data['child_id'].split(' ')]
        if child != "NULL":
            for i in range(len(child)):
                query = Task.objects.values('task_name').filter(task_id=child[i])
                child[i] = [query[0]['task_name'], child[i]]
        print(sect_info, child, subset)

    max_group = "*" * max(len_of_types)
    data = Task.objects.filter(task_id=pk)

    best_mdp_ids = list(MDP.objects.values('mdp_id', 'mdp_name').filter(mdp_name__in=best_mdps))

    content = content_order(Task.objects.values('task_name').order_by('task_id'), batch_size, 'task_name')
    ordered_content, height = content[0], content[1]
    batch_size_temp = "*" * batch_size
    return TemplateResponse(request, 'tasks-basic.html',
                            {"ordered_content": ordered_content, "list_of_types": list_of_types,
                             "len_of_types": len_of_types, "max_group": max_group, \
                             "height": height, "grouped_names": grouped_names, "batch_size_temp": batch_size_temp,
                             "data": data, "parent_s": parent_s, \
                             "subset": subset, "children": child, "sect_info": sect_info, "sect_len": sect_len,
                             "best_mdps": best_mdp_ids, \
                             "references": references})


def tasksbasicexport(request, pk):
    person_resource = TaskResource()
    queryset = Task.objects.filter(task_id=pk)
    dataset = person_resource.export(queryset)
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="taskbasic.csv"'
    return response


def tasksadvanced(request):
    # AND --> &
    # OR  --> |
    data = Q()
    data2 = Q()
    queryy = request.GET.get('21.png', 'None')
    if (queryy != "None"):
        data = Q(input_space=queryy)
        data2 = Q(input_space=queryy)

    queryy2 = request.GET.get('22.png', 'None')
    if (queryy2 != "None"):
        data = data | Q(input_space=queryy2)
        data2 = data2 & Q(input_space=queryy2)

    queryy3 = request.GET.get('23.png', 'None')
    if (queryy3 != "None"):
        data = data | Q(input_space=queryy3)
        data2 = data2 & Q(input_space=queryy3)

    queryy4 = request.GET.get('24.png', 'None')
    if (queryy3 != "None"):
        data = data | Q(input_space=queryy4)
        data2 = data2 & Q(input_space=queryy4)

    queryy5 = request.GET.get('25.png', 'None')
    if (queryy5 != "None"):
        data = data2 | Q(input_space=queryy5)
        data2 = data2 & Q(input_space=queryy5)

    queryy6 = request.GET.get('26.png', 'None')
    if (queryy6 != "None"):
        data = data | Q(input_space=queryy6)
        data2 = data2 & Q(input_space=queryy6)

    queryy7 = request.GET.get('27.png', 'None')
    if (queryy7 != "None"):
        data = data | Q(input_space=queryy7)
        data2 = data2 & Q(input_space=queryy7)

    queryy8 = request.GET.get('28.png', 'None')
    if (queryy8 != "None"):
        data = data | Q(input_space=queryy8)
        data2 = data2 & Q(input_space=queryy8)

    queryy9 = request.GET.get('29.png', 'None')
    if (queryy9 != "None"):
        data = data | Q(input_space=queryy9)
        data2 = data2 & Q(input_space=queryy9)

    queryy10 = request.GET.get('30.png', 'None')
    if (queryy10 != "None"):
        data = data | Q(input_space=queryy10)
        data2 = data2 & Q(input_space=queryy10)

    queryy11 = request.GET.get('31.png', 'None')
    if (queryy11 != "None"):
        data = data | Q(input_space=queryy11)
        data2 = data2 & Q(input_space=queryy11)

    queryy12 = request.GET.get('32.png', 'None')
    if (queryy12 != "None"):
        data = data | Q(input_space=queryy12)
        data2 = data2 & Q(input_space=queryy12)

    queryy13 = request.GET.get('33.png', 'None')
    if (queryy13 != "None"):
        data = data | Q(input_space=queryy13)
        data2 = data2 & Q(input_space=queryy13)

    queryy14 = request.GET.get('34.png', 'None')
    if (queryy14 != "None"):
        data = data | Q(input_space=queryy14)
        data2 = data2 & Q(input_space=queryy14)

    queryy15 = request.GET.get('35.png', 'None')
    if (queryy15 != "None"):
        data = data | Q(input_space=queryy15)
        data2 = data2 & Q(input_space=queryy15)

    queryy16 = request.GET.get('36.png', 'None')
    if (queryy16 != "None"):
        data = data | Q(input_space=queryy16)
        data2 = data2 & Q(input_space=queryy16)

    queryy17 = request.GET.get('37.png', 'None')
    if (queryy17 != "None"):
        data = data | Q(input_space=queryy17)
        data2 = data2 & Q(input_space=queryy17)

    queryy18 = request.GET.get('38.png', 'None')
    if (queryy18 != "None"):
        data = data | Q(input_space=queryy18)
        data2 = data2 & Q(input_space=queryy18)

    queryy19 = request.GET.get('40.png', 'None')
    if (queryy19 != "None"):
        data = data | Q(input_space=queryy19)
        data2 = data2 & Q(input_space=queryy19)

    queryy20 = request.GET.get('41.png', 'None')
    if (queryy20 != "None"):
        data = data | Q(input_space=queryy20)
        data2 = data2 & Q(input_space=queryy20)

    queryy21 = request.GET.get('42.png', 'None')
    if (queryy21 != "None"):
        data = data | Q(input_space=queryy21)
        data2 = data2 & Q(input_space=queryy21)

    queryy22 = request.GET.get('43.png', 'None')
    if (queryy22 != "None"):
        data = data | Q(input_space=queryy22)
        data2 = data2 & Q(input_space=queryy22)

    queryy23 = request.GET.get('44.png', 'None')
    if (queryy23 != "None"):
        data = data | Q(input_space=queryy23)
        data2 = data2 & Q(input_space=queryy23)

    queryy24 = request.GET.get('45.png', 'None')
    if (queryy24 != "None"):
        data = data | Q(input_space=queryy24)
        data2 = data2 & Q(input_space=queryy24)

    queryy25 = request.GET.get('46.png', 'None')
    if (queryy25 != "None"):
        data = data | Q(input_space=queryy25)
        data2 = data2 & Q(input_space=queryy25)

    queryy26 = request.GET.get('47.png', 'None')
    if (queryy26 != "None"):
        data = data | Q(input_space=queryy26)
        data2 = data2 & Q(input_space=queryy26)

    queryy27 = request.GET.get('48.png', 'None')
    if (queryy27 != "None"):
        data = data | Q(input_space=queryy27)
        data2 = data2 & Q(input_space=queryy27)

    queryy28 = request.GET.get('49.png', 'None')
    if (queryy28 != "None"):
        data = data | Q(input_space=queryy28)
        data2 = data2 & Q(input_space=queryy28)

    queryy29 = request.GET.get('50.png', 'None')
    if (queryy29 != "None"):
        data = data | Q(input_space=queryy29)
        data2 = data2 & Q(input_space=queryy29)

    queryy30 = request.GET.get('51.png', 'None')
    if (queryy30 != "None"):
        data = data | Q(output_space=queryy30)
        data2 = data2 & Q(output_space=queryy30)

    queryy31 = request.GET.get('52.png', 'None')
    if (queryy31 != "None"):
        data = data | Q(output_space=queryy31)
        data2 = data2 & Q(output_space=queryy31)

    queryy32 = request.GET.get('53.png', 'None')
    if (queryy32 != "None"):
        data = data | Q(output_space=queryy32)
        data2 = data2 & Q(output_space=queryy32)

    queryy33 = request.GET.get('54.png', 'None')
    if (queryy33 != "None"):
        data = data | Q(output_space=queryy33)
        data2 = data2 & Q(output_space=queryy33)

    queryy34 = request.GET.get('55.png', 'None')
    if (queryy34 != "None"):
        data = data | Q(output_space=queryy34)
        data2 = data2 & Q(output_space=queryy34)

    queryy35 = request.GET.get('56.png', 'None')
    if (queryy35 != "None"):
        data = data | Q(output_space=queryy35)
        data2 = data2 & Q(output_space=queryy35)

    queryy36 = request.GET.get('57.png', 'None')
    if (queryy36 != "None"):
        data = data | Q(output_space=queryy36)
        data2 = data2 & Q(output_space=queryy36)

    queryy37 = request.GET.get('58.png', 'None')
    if (queryy37 != "None"):
        data = data | Q(output_space=queryy37)
        data2 = data2 & Q(output_space=queryy37)

    queryy38 = request.GET.get('59.png', 'None')
    if (queryy38 != "None"):
        data = data | Q(output_space=queryy38)
        data2 = data2 & Q(output_space=queryy38)

    queryy39 = request.GET.get('60.png', 'None')
    if (queryy39 != "None"):
        data = data | Q(output_space=queryy39)
        data2 = data2 & Q(output_space=queryy39)

    queryy40 = request.GET.get('61.png', 'None')
    if (queryy40 != "None"):
        data = data | Q(output_space=queryy40)
        data2 = data2 & Q(output_space=queryy40)

    queryy41 = request.GET.get('62.png', 'None')
    if (queryy41 != "None"):
        data = data | Q(output_space=queryy41)
        data2 = data2 & Q(output_space=queryy41)

    queryy42 = request.GET.get('63.png', 'None')
    if (queryy42 != "None"):
        data = data | Q(output_space=queryy42)
        data2 = data2 & Q(output_space=queryy42)

    queryy43 = request.GET.get('64.png', 'None')
    if (queryy43 != "None"):
        data = data | Q(output_space=queryy43)
        data2 = data2 & Q(output_space=queryy43)

    queryy44 = request.GET.get('65.png', 'None')
    if (queryy44 != "None"):
        data = data | Q(output_space=queryy44)
        data2 = data2 & Q(output_space=queryy44)

    queryy45 = request.GET.get('66.png', 'None')
    if (queryy45 != "None"):
        data = data | Q(output_space=queryy45)
        data2 = data2 & Q(output_space=queryy45)

    queryy46 = request.GET.get('67.png', 'None')
    if (queryy46 != "None"):
        data = data | Q(output_space=queryy46)
        data2 = data2 & Q(output_space=queryy46)

    queryy47 = request.GET.get('68.png', 'None')
    if (queryy47 != "None"):
        data = data | Q(output_space=queryy47)
        data2 = data2 & Q(output_space=queryy47)

    queryy48 = request.GET.get('U', 'None')
    if (queryy48 != "None"):
        data = data | Q(actor=queryy48)
        data2 = data2 & Q(actor=queryy48)

    queryy49 = request.GET.get('M', 'None')
    if (queryy49 != "None"):
        data = data | Q(actor=queryy49)
        data2 = data2 & Q(actor=queryy49)

    queryy50 = request.GET.get('MandU', 'None')
    if (queryy50 != "None"):
        data = data | Q(actor=queryy50)
        data2 = data2 & Q(actor=queryy50)

    queryy51 = request.GET.get('UandM', 'None')
    if (queryy51 != "None"):
        data = data | Q(actor=queryy51)
        data2 = data2 & Q(actor=queryy51)

    global queryset3
    queryset3 = Task.objects.filter(data)  # or include
    global queryset33
    queryset33 = Task.objects.exclude(data)  # or exclude
    global queryset4
    queryset4 = Task.objects.filter(data2)  # and include
    global queryset44
    queryset44 = Task.objects.exclude(data2)  # and exclude

    return TemplateResponse(request, 'tasks-advanced.html',
                            {"data1": data, "data2": data2, "orqueryinclude": queryset3, "orqueryexclude": queryset33,
                             "andqueryinclude": queryset4, "andqueryexclude": queryset44,
                             "referencesdict": dictionary()})


# or include
def taskadvancedexport1(request):
    person_resource = TaskResource()
    dataset = person_resource.export(queryset3)
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="taskadvanced.csv"'
    return response


# or exclude
def taskadvancedexport2(request):
    person_resource = TaskResource()
    dataset = person_resource.export(queryset33)
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="taskadvanced.csv"'
    return response


# and include
def taskadvancedexport3(request):
    person_resource = TaskResource()
    dataset = person_resource.export(queryset4)
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="taskadvanced.csv"'
    return response


# and exclude
def taskadvancedexport4(request):
    person_resource = TaskResource()
    dataset = person_resource.export(queryset44)
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="taskadvanced.csv"'
    return response


def enrichbasic(request, pk):
    types = Enrichment.objects.values('enrichment_type')
    list_of_types = filter_keep_index([type['enrichment_type'] for type in types])
    len_of_types = [len(Enrichment.objects.filter(enrichment_type=type_name)) for type_name in list_of_types]
    batch_size = len(list_of_types)
    grouped_names = []
    for i in range(batch_size):
        enrichments = Enrichment.objects.filter(enrichment_type=list_of_types[i])
        grouped_names.append([[enrichment.enrichment_name, enrichment.enrichment_id] for enrichment in enrichments])
    reference_temp, references = '', ''
    id_query = Enrichment.objects.values('enrichment_id')
    max_id, min_id = get_references_1(id_query=id_query, id_field='enrichment_id', pk=pk)
    if int(pk) > min_id and int(pk) < max_id + 1:
        reference_temp = (list((Enrichment.objects.values('references_type')).filter(enrichment_id=pk)))
    if reference_temp != '':
        references = get_references_2(reference_temp, ref_field_name='references_type')
    max_group = "*" * max(len_of_types)
    data = Enrichment.objects.filter(enrichment_id=pk)
    content = content_order(Enrichment.objects.values('enrichment_name').order_by('enrichment_id'), batch_size,
                            key='enrichment_name')
    ordered_content, height = content[0], content[1]
    batch_size_temp = "*" * batch_size
    return TemplateResponse(request, 'enrich-basic.html',
                            {"ordered_content": ordered_content, "list_of_types": list_of_types,
                             "len_of_types": len_of_types, "max_group": max_group, \
                             "height": height, "grouped_names": grouped_names, "batch_size_temp": batch_size_temp,
                             "data": data, "references": references})


def enrichbasicexport(request, pk):
    person_resource = EnrichmentResource()
    queryset = Enrichment.objects.filter(enrichment_id=pk)
    dataset = person_resource.export(queryset)
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="enrichment.csv"'
    return response