import inspect


class API_REGISTER():
    api_classes = {}
    
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(API_REGISTER, cls).__new__(cls)
        return cls.instance
    
    
    # each function should only take one parameter, which is the query
    def register(self, function, name):
        assert callable(function), f"The function '{name}' is not callable."
        assert name is not None, f"The function name cannot be None."
        if name in self.api_classes and self.api_classes[name].__module__ == function.__module__:
            return 
        
        if name in self.api_classes:
            raise ValueError(f"The function name '{name}' is already registered.")
        
        self.api_classes[name] = function
    
    def get(self, name):
        return self.api_classes.get(name)

def register_api_function(name):
    def decorator(function):
        API_REGISTER().register(function, name)
        return function
    return decorator

from django.utils.module_loading import autodiscover_modules
autodiscover_modules('search_field_functions')