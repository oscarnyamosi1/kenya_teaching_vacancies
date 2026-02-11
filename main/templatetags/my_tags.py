from django import template

register = template.Library()

@register.simple_tag
def rename_var(var):
    return var