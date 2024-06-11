# fields.py
from typing import Any
from django import forms
from django.forms.widgets import Widget
from ..widgets import SelectSearchTextInput
import random
from ..providers import create_model_field_provider_from_model, create_model_provider_from_model
from ..providers import OnlyAuthenticated

class SelectSearchCharField(forms.CharField):
    widget = SelectSearchTextInput

    def __init__(self,field,model=None, permissions=[OnlyAuthenticated], query_function_name=None, min_search_length=1,*args, **kwargs):
        assert query_function_name or model, f"The query function name cannot be None."
        if model:
            self.model = model
            provider = create_model_field_provider_from_model(model, permission_classes=[permissions])
            self.query_function_name = provider.query_function_name
        else:
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

