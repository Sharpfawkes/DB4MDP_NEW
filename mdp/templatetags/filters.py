from django import template

register = template.Library()

@register.filter(name='indexing')
def indexing(value, index):
    return value[index]


@register.filter(name="id_names")
def id_names(id_strings, index):
    return [id_data[0] for id_data in id_strings]

# This filter is going to be used for retrieving the value of the parameter after the object has been collected using
# the indexing filter. First we try to get the parameter_name from the object. Either mathjaxeqn (MathJaxFormulas table)
# or parameter_option (QM_Parameters table) will be passed as an argument from the template. However, the best parameter
# is an integer and not an object. So if we try to access it's parameter we'll get an attributeerror and that's why'
# I'm using the try, except statement.

@register.filter(name="param_val")
def param_val(object, param_name):
    try:
        return getattr(object, param_name)
    except AttributeError:
        return object

@register.filter(name="task_filter")
def task_filter(object, param_name):
    try:
        if param_name != None:
            return getattr(object, param_name)
        return object
    except AttributeError:
        return object

@register.filter(name="get_refs")
def get_refs(object, ref_param_name = "references"):
    return getattr(object, ref_param_name).all()

@register.filter(name="display_string")
def display_string(string_input):
    return (' '.join(string_input.split('_'))).title()

@register.filter(name="task_id_gen")
def task_id_gen(object_data, trivial_str):
    return trivial_str+str(object_data[0])
