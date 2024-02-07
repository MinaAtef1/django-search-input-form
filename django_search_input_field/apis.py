

import traceback
from .query_function_register import API_REGISTER
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from uuid import uuid4

def get_query_result(request):
    query_name = request.GET.get('query_name')
    query = request.GET.get('q')
    search_field = request.GET.get('search_field')
    
    function_filters = {k.replace('function_filters__', ''): v for k, v in request.GET.items() if k.startswith('function_filters__')}
    function_filters.update({search_field: query})

    for key, value in function_filters.copy().items():
        if value == "null":
            function_filters[key] = None
        elif value.lower() in ["true", "false"]:
            function_filters[key] = value.lower() == "true"
        elif value.isdigit():
            function_filters[key] = int(value)
        elif value.replace('.', '', 1).isdigit():
            function_filters[key] = float(value)

    # get the query function
    query_class = API_REGISTER().get(query_name)
    if not query_class:
        print(f"ERROR: The query function '{query_name}' is not registered.")
        return JsonResponse({"error":""},status=400)
    
    if not query_class().get_permissions(request):
        print(f"ERROR: The user does not have permission to access the query function '{query_name}'.")
        return JsonResponse({"error":""},status=403)
    
    # get the result
    try:
        options = query_class().get_filtered_options(function_filters, search_field)
        result = []
        for option in options:
            result.append(option.to_dict())
        
    except Exception as e:
        uuid = uuid4()
        print(uuid, "ERROR: ", e, traceback.format_exc())
        result = {"error": f"An error occurred. Please contact the administrator. The error id is {uuid}"}
        
    # return the result
    return JsonResponse(result, safe=False)
