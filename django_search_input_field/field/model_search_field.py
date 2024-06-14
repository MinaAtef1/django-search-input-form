# fields.py
from typing import Any
from django import forms
from django.forms.widgets import Widget
from ..widgets import SelectSearchTextInput
import random
from ..providers import create_model_provider_from_model
from rest_framework.permissions import IsAuthenticated

class SearchModelField(forms.CharField):
    widget = SelectSearchTextInput

    def __init__(self, model, search_field, permissions=IsAuthenticated, query_function_name='', min_search_length=1,*args, **kwargs):
        if not query_function_name:
            provider = create_model_provider_from_model(model, permissions)
            query_function_name = provider.query_function_name
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
    