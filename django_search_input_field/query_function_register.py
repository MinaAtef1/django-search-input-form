import inspect


class API_REGISTER():
    api_functions = {}
    
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(API_REGISTER, cls).__new__(cls)
        return cls.instance
    
    
    # each function should only take one parameter, which is the query
    def register(self, function, name):
        assert callable(function), f"The function '{name}' is not callable."
        assert name not in self.api_functions, f"The function '{name}' is already registered."
        assert name is not None, f"The function name cannot be None."
        
        num_params = len(inspect.signature(function).parameters)
        assert num_params == 1, f"The function '{name}' should take only one parameter."
        
        self.api_functions[name] = function
    
    def get(self, name):
        return self.api_functions[name]
        
    
    
def register_api_function(name):
    def decorator(function):
        API_REGISTER().register(function, name)
        return function
    return decorator
