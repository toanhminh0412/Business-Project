from django import template

register = template.Library()

# Custom filter: remove quotation marks from strings in templates
@register.filter
def strip_double_quotes(quoted_string):
    return quoted_string.replace("'", '')