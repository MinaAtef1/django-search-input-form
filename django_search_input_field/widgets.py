from django import forms

class SelectSearchTextInput(forms.widgets.TextInput):
    template_name = 'select_search_text_input.html'


    