from django import template
from ..query_function_register import API_REGISTER

register = template.Library()

@register.simple_tag(name='search_field_get_init_value')
def get_init_selected(function_name, value):
    if not value:
        return None
    option =  API_REGISTER().get(function_name)().get_object_by_pk(value)
    return {'id': option.id, 'string': option.string}
    