from typing import Any
from django import forms
from django.forms.widgets import Widget
import random

class MainRelatedField():
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

class CharRelatedField(MainRelatedField, forms.CharField):
    pass

class IntegerRelatedField(MainRelatedField, forms.IntegerField):
    pass

class FloatRelatedField(MainRelatedField, forms.FloatField):
    pass

class DecimalRelatedField(MainRelatedField, forms.DecimalField):
    pass

class DateRelatedField(MainRelatedField, forms.DateField):
    pass
    