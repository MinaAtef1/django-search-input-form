```
# Django Search Input Field

The Django Search Input Field package simplifies the process of integrating Ajax searchable input fields into Django forms. This package provides flexibility for searching model fields or any custom data, enhancing the user experience and improving search functionality within your Django applications.

## Installation

You can install the package via pip:

```shell
pip install django-search-input
```

Once installed, add the app to your `INSTALLED_APPS` in your Django settings:

```python
INSTALLED_APPS = [
    ...
    "django_search_input_field"
]
```

Finally, include the package's URLs in your project's URL configuration:

```python
urlpatterns = [
    path('django_search_filters/', include('django_search_input_field.urls')),
]
```

## Model Fields Search

To perform model field search, you can utilize the `SearchFieldModelOptions` provided by the package. Here's an example:

```python
from django_search_input_field.options import SearchFieldModelOptions
from django import forms

class EntryFieldsSearch(SearchFieldModelOptions):
    model = Subjects
    query_function_name = 'search_subjects'

    def get_permissions(self, request):
        return True

class SubjectFormAllFieldsSearch(forms.Form):
    name = SelectSearchCharField(query_function_name='search_subjects', field='name')
    description = forms.CharField(widget=forms.Textarea)
```

## Custom Data Search

For custom data search, you can use the `SearchFieldOptions` along with custom filtering logic. Here's an example:

```python
from django_search_input_field.options import SearchFieldOptions
from django_search_input_field.field import SelectSearchCharField
from django_search_input_field.data_structures import DictOption
from django import forms

class SubjectNameSearch(SearchFieldOptions):
    query_function_name = 'subject_name_search'
    
    def get_permissions(self, request):
        return request.user.is_staff

    def get_filtered_options(self, function_filters, search_key):
        # Custom filtering logic goes here
        return [DictOption(id=subject['id'], string=subject['name'], json=subject['additional_data']) for subject in subjects ]

class SubjectFormJsons(forms.Form):
    name = SelectSearchCharField(query_function_name='subject_name_search', field='name')
    description = forms.CharField(widget=forms.Textarea)
```


## Custom Data Search with Related Fields

For custom data search with related fields handling, you can use the `SearchFieldOptions` along with custom filtering logic. Here's an example:

```python
from django_search_input_field.field import SelectSearchCharField, CharModelRelatedField
from django_search_input_field.options import SearchFieldOptions, DictOption
from django_search_input_field.form import RelatedFillForm
from django import forms

class SubjectNameSearch(SearchFieldOptions):
    query_function_name = 'subject_name_search'
    
    def get_permissions(self, request):
        return request.user.is_staff

    def get_filtered_options(self, function_filters, search_key):
        subjects = [{'id':'math', 'name': 'Math', "additional_data": {"year": 2021, "semester": 1}},
                    {'id':'science', 'name': 'Science', "additional_data": {"year": 2021, "semester": 1}},
                    {'id':'english', 'name': 'English', "additional_data": {"year": 2021, "semester": 1}}]
                    
        return [DictOption(id=subject['id'], string=subject['name'], json=subject['additional_data']) for subject in subjects ]

class SubjectFormJsons(RelatedFillForm):
    name = SelectSearchCharField(query_function_name='subject_name_search', field='name')
    year = CharModelRelatedField(related_search_input='name', related_field='additional_data.year')
    semester = CharModelRelatedField(related_search_input='name', related_field='additional_data.semester')
```

In this example, `SubjectNameSearch` defines custom permissions and custom filtering logic for searching subjects. 

`SubjectFormJsons` inherits from `RelatedFillForm`, allowing for automatic filling of related fields based on the selected subject name. The `year` and `semester` fields are populated based on the additional data associated with the selected subject.


## Contributing

Contributions are welcome! If you have any improvements or bug fixes, feel free to submit a pull request. For major changes, please open an issue first to discuss the proposed changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```
