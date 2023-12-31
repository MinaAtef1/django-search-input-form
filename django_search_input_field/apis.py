

import traceback
from .query_function_register import API_REGISTER
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from uuid import uuid4

@login_required
def get_query_result(request):
    query_name = request.GET.get('query_name')
    query = request.GET.get('q')
    # get the query function
    query_function = API_REGISTER().get(query_name)
    
    # get the result
    try:
        options = query_function(search_query=query)
        result = []
        for option in options:
            result.append({'id': option.id, 'text': option.string})
        
    except Exception as e:
        uuid = uuid4()
        print(uuid, "ERROR: ", e, traceback.format_exc())
        result = {"error": f"An error occurred. Please contact the administrator. The error id is {uuid}"}
        
    # return the result
    return JsonResponse(result, safe=False)
