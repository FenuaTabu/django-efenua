from django import template
from django.conf import settings
import re
from importlib import import_module


register = template.Library()

numeric_test = re.compile("^\d+$")

@register.filter(name="is_instance")
def isinst(value, class_str):
    split = class_str.split('.')
    return isinstance(value, getattr(import_module('.'.join(split[:-1])), split[-1]))

@register.filter(name="get_type")
def get_type(ob):
    return ob.__class__.__name__

@register.filter(name="get_attribute")
def get_attribute(value, arg):
    """Gets an attribute of an object dynamically AND recursively from a string name"""
    if "." in str(arg):
        firstarg = str(arg).split(".")[0]
        value = get_attribute(value,firstarg)
        arg = ".".join(str(arg).split(".")[1:])
        return get_attribute(value,arg)
    if hasattr(value, str(arg)):
        return getattr(value, arg)
    elif hasattr(value, 'has_key') and value.has_key(arg):
        return value[arg]
    elif numeric_test.match(str(arg)) and len(value) > int(arg):
        return value[int(arg)]
    else:
        #return settings.TEMPLATE_STRING_IF_INVALID
        return 'no attr.' + str(arg) + 'for:' + str(value)
        
@register.filter(name="get_verbose_field_name")
def get_verbose_field_name(instance, field_name):
    """
    Returns verbose_name for a field.
    """
    return instance._meta.get_field(field_name).verbose_name.title()