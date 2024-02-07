from django.core.serializers.json import DjangoJSONEncoder
import json
from django.core import serializers
from .query_function_register import API_REGISTER
from django.db.models import QuerySet

class InputOption():
    def __init__(self, id, string):
        self.id = id
        self.string = string
    
    def to_dict(self):
        return {
            'id': self.id,
            'text': self.string
        }

class ModelOption():
    def __init__(self, item, serializer=None ,str_function=None):
        # django model serializer
        self.item = item
        self.id = item.pk
        self.string = str_function(item) if str_function else str(item)
        if serializer:
            self.json = serializer(item).data
        
        else:
            object = json.loads(serializers.serialize('json', [item,]))[0]
            fields_data = object['fields']
        
        self.json = fields_data
    
    def to_dict(self):
        return {
            'id': self.id,
            'text': self.string,
            'fields_data': self.json
        }        
        
        
        
class SearchModelOptions():
    model = None
    query_function_name = None
    serializer = None
    
    def object_str(self, obj):
        return str(obj)
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        API_REGISTER().register(cls, cls.query_function_name)
    
    
    def get_permissions(self, request):
        return request.user.is_authenticated
    
    def get_queryset(self)->QuerySet:
        return self.model.objects.all()
    
    def get_queryset_by_pk(self, pk)->QuerySet:
        return self.model.objects.get(pk=pk)
        
    def get_object_by_pk(self, pk):
        return ModelOption(self.get_queryset_by_pk(pk), self.serializer, self.object_str)
    
    def get_filtered_queryset(self, function_filters:dict, search_key)->QuerySet:
        for key, value in function_filters.copy().items():
            del function_filters[key]
            if search_key == key:
                key = key + '__icontains'
            function_filters[key] = value
        
        return self.get_queryset().filter(**function_filters)
        
    def get_filtered_options(self, function_filters, search_key):
        options = self.get_filtered_queryset(function_filters, search_key)
        return [ModelOption(option, self.serializer, self.object_str) for option in options]