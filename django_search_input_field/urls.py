# urls.py

from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .apis import get_query_result


urlpatterns = [
    path('api/query_search_input/', csrf_exempt(get_query_result), name='get_search_input_query_result'),
]