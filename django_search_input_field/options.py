import json
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers


class InputOption:
    def __init__(self, id, string):
        self.id = id
        self.string = string

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.string
        }

class DictOption:
    def __init__(self, id, string, json_data):
        self.id = id
        self.string = string
        self.json = json_data

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.string,
            'fields_data': self.json
        }

class ModelOption:
    def __init__(self, item, serializer=None, str_function=None):
        self.item = item
        self.id = item.pk
        self.string = str_function(item) if str_function else str(item)
        self.json = serializer(item).data if serializer else json.loads(serializers.serialize('json', [item]))[0]['fields']

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.string,
            'fields_data': self.json
        }
