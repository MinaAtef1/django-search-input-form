# fields.py
from typing import Any
from django import forms
from django.forms.widgets import Widget
from .widgets import SearchTextInput

class SearchCharField(forms.CharField):
    widget = SearchTextInput

    def __init__(self, query_function_name='', *args, **kwargs):
        assert query_function_name is not None, f"The query function name cannot be None."
        self.query_function_name = query_function_name
        super().__init__(*args, **kwargs)

    def widget_attrs(self, widget: Widget) -> Any:
        attrs = super().widget_attrs(widget)
        attrs.update({'query_function_name': self.query_function_name})
        return attrs
    
    
class InoutOptions():
    def __init__(self, id, string):
        self.id = id
        self.string = string