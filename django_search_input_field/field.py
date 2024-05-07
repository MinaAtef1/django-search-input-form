# fields.py
from typing import Any
from django import forms
from django.forms.widgets import Widget
from .widgets import SelectSearchTextInput
import random


class SelectSearchCharField(forms.CharField):
    widget = SelectSearchTextInput

    def __init__(self, query_function_name='',field=None, min_search_length=1,*args, **kwargs):
        assert query_function_name is not None, f"The query function name cannot be None."
        self.query_function_name = query_function_name
        self.min_search_length = min_search_length
        self.field = field
        super().__init__(*args, **kwargs)

    def widget_attrs(self, widget: Widget) -> Any:
        attrs = super().widget_attrs(widget)            
        attrs.update({'query_function_name': self.query_function_name,
                      'min_search_length': self.min_search_length,
                      "search_field" : self.field,
                      "id": f"search-input-{random.randint(0, 1000000000)}",
                      })
        return attrs


class SearchModelField(forms.CharField):
    widget = SelectSearchTextInput

    def __init__(self, model, search_field, query_function_name='', min_search_length=1,*args, **kwargs):
        assert query_function_name is not None, f"The query function name cannot be None."
        self.query_function_name = query_function_name
        self.min_search_length = min_search_length
        self.search_field = search_field
        self.model = model
        super().__init__(*args, **kwargs)

    def widget_attrs(self, widget: Widget) -> Any:
        attrs = super().widget_attrs(widget)        
        attrs.update({'query_function_name': self.query_function_name,
                      'min_search_length': self.min_search_length,
                      'id': f"search-input-{random.randint(0, 1000000000)}",
                      "search_field" : self.search_field,
                      "model_field": True
                      })
        return attrs
    
    def to_python(self, value):
        if not value :
            return None
        return self.model.objects.get(id=value)
    
    
class MainModelRelatedField():
    def __init__(self, related_search_input, related_field, *args, **kwargs):
        assert related_search_input is not None, f"The related search input cannot be None."
        assert related_field is not None, f"The related field cannot be None."
        self.related_search_input = related_search_input
        self.related_field = related_field
        
        super().__init__(*args, **kwargs)


    def widget_attrs(self, widget: Widget) -> Any:
        attrs = super().widget_attrs(widget)        
        attrs.update({'related_search_input': self.related_search_input,
                      'related_field': self.related_field,
                      'id': f"char-model-related-field-{random.randint(0, 1000000000)}",
                      })
        return attrs


class CharModelRelatedField(MainModelRelatedField, forms.CharField):
    pass

class IntegerModelRelatedField(MainModelRelatedField, forms.IntegerField):
    pass

class FloatModelRelatedField(MainModelRelatedField, forms.FloatField):
    pass

class DecimalModelRelatedField(MainModelRelatedField, forms.DecimalField):
    pass

class DateModelRelatedField(MainModelRelatedField, forms.DateField):
    pass
    