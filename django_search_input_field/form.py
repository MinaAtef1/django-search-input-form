from django import forms
from .field import MainModelRelatedField, SearchModelField

class RelatedFillForm(forms.Form):
    
    def extract_function_attrs(self, kwargs:dict):
        """
        Extract the function attrs from the kwargs
        """
        function_attrs = {}
        for key, value in kwargs.copy().items():
            if key.endswith('__function_filters'):
                function_attrs[key] = value
                del kwargs[key]
        
        return function_attrs
    
    def __init__(self, *args, **kwargs):
        
        function_attrs = self.extract_function_attrs(kwargs)
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            # check if the field is class is inherited from MainModelRelatedField
            if issubclass(field.__class__, MainModelRelatedField):
                related_search_input_name = field.related_search_input
                related_field = self.fields[related_search_input_name]
                related_field_id = related_field.widget.attrs['id']
                self.fields[field_name].widget.attrs['related_search_input_id'] = related_field_id
                
            elif isinstance(field, SearchModelField):
                field_attrs_name = f'{field_name}__function_filters'
                attrs = function_attrs.get(field_attrs_name)
                if not attrs:
                    continue
                
                for attr_name, attr in attrs.items():
                    attr_name= f'function_filters__{attr_name}'
                    self.fields[field_name].widget.attrs[attr_name] = attr
                