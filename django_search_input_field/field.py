# fields.py
from typing import Any
from django import forms
from django.forms.widgets import Widget
from .widgets import SearchTextInput
import random


class SearchCharField(forms.CharField):
    widget = SearchTextInput

    def __init__(self, query_function_name='', min_search_length=1,*args, **kwargs):
        assert query_function_name is not None, f"The query function name cannot be None."
        self.query_function_name = query_function_name
        self.min_search_length = min_search_length
        super().__init__(*args, **kwargs)

    def widget_attrs(self, widget: Widget) -> Any:
        attrs = super().widget_attrs(widget)            
        attrs.update({'query_function_name': self.query_function_name,
                      'min_search_length': self.min_search_length,
                      'id': f"search-input-{random.randint(0, 1000000000)}"
                      })
        return attrs


class SearchModelField(forms.CharField):
    widget = SearchTextInput

    def __init__(self, model, query_function_name='', min_search_length=1,*args, **kwargs):
        assert query_function_name is not None, f"The query function name cannot be None."
        self.query_function_name = query_function_name
        self.min_search_length = min_search_length
        self.model = model
        super().__init__(*args, **kwargs)

    def widget_attrs(self, widget: Widget) -> Any:
        attrs = super().widget_attrs(widget)        
        attrs.update({'query_function_name': self.query_function_name,
                      'min_search_length': self.min_search_length,
                      'id': f"search-input-{random.randint(0, 1000000000)}",
                      })
        return attrs
    
    def to_python(self, value):
        if not value :
            return None
        return self.model.objects.get(id=value)
    
class InputOption():
    def __init__(self, id, string):
        self.id = id
        self.string = string