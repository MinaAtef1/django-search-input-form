

from .query_function_register import API_REGISTER
from django.http import JsonResponse


def get_query_result(request):
    query_name = request.GET.get('query_name')
    query = request.GET.get('query')
    # get the query function
    query_function = API_REGISTER().get(query_name)
    
    # get the result
    try:
        options = query_function(query)
        result = []
        for option in options:
            result.append({'id': option.id, 'text': option.string})
        
    except Exception as e:
        result = {"error": str(e)}
        
    # return the result
    return JsonResponse(result, safe=False)
