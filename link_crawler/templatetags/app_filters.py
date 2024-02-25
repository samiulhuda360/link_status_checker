from django.template.defaultfilters import register

@register.filter
def split(value, delimiter=' '):
    """
    Splits the value string into a list by the delimiter.
    """
    return value.split(delimiter)

@register.filter
def cut(value, to_cut):
    """
    Removes a substring from the value.
    """
    return value.replace(to_cut, '')