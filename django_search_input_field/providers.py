from .query_function_register import API_REGISTER
from django.db.models import QuerySet
from .options import InputOption, ModelOption
from rest_framework.permissions import  IsAuthenticated



class SearchModelProvider:
    model = None
    query_function_name = None
    serializer = None
    auto_register = False

    def object_str(self, obj):
        return str(obj)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        API_REGISTER().register(cls, cls.query_function_name, cls.auto_register)

    def get_permissions(self, request):
        return request.user.is_authenticated

    def get_queryset(self) -> QuerySet:
        return self.model.objects.all()

    def get_queryset_by_pk(self, pk) -> QuerySet:
        return self.get_queryset().get(pk=pk)

    def get_object_by_pk(self, pk):
        return ModelOption(self.get_queryset_by_pk(pk), self.serializer, self.object_str)

    def get_filtered_queryset(self, function_filters: dict, search_key) -> QuerySet:
        function_filters = {
            key + '__icontains' if key == search_key else key: value 
            for key, value in function_filters.items()
        }
        return self.get_queryset().filter(**function_filters)

    def get_filtered_options(self, function_filters, search_key):
        options = self.get_filtered_queryset(function_filters, search_key)
        return [ModelOption(option, self.serializer, self.object_str) for option in options]

class SearchModelFieldProvider:
    model = None
    query_function_name = None
    auto_register = False

    def object_str(self, obj):
        return str(obj)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        API_REGISTER().register(cls, cls.query_function_name, cls.auto_register)

    def get_permissions(self, request):
        return request.user.is_authenticated

    def get_queryset(self) -> QuerySet:
        return self.model.objects.all()

    def get_filtered_queryset(self, function_filters: dict, search_key) -> QuerySet:
        function_filters = {
            key + '__icontains' if key == search_key else key: value 
            for key, value in function_filters.items()
        }
        return self.get_queryset().filter(**function_filters).values_list(search_key, flat=True).distinct()

    def get_filtered_options(self, function_filters, search_key):
        options = self.get_filtered_queryset(function_filters, search_key)
        return [InputOption(option, option) for option in options]

class SearchDataProvider:
    json = None
    query_function_name = None
    auto_register = False

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        API_REGISTER().register(cls, cls.query_function_name, cls.auto_register)

    def get_permissions(self, request):
        return request.user.is_authenticated

    def get_filtered_options(self, function_filters, search_key):
        raise NotImplementedError("This method must be implemented in the subclass")

def create_model_provider_from_model(Model, permission_classe=IsAuthenticated):
    class Provider(SearchModelProvider):
        model = Model
        query_function_name = Model.__name__ + '_search'
        auto_register = True
        
        def get_permissions(self, request):
           return permission_classe().has_permission(request, None)
        
    return Provider

def create_model_field_provider_from_model(Model, permission_classe=IsAuthenticated):
    class Provider(SearchModelFieldProvider):
        model = Model
        query_function_name = Model.__name__ + '_search_field'
        auto_register = True

        def get_permissions(self, request):
            return permission_classe().has_permission(request, None)

    return Provider
