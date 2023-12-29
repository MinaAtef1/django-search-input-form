from django import forms

class SearchTextInput(forms.widgets.TextInput):
    template_name = 'search_text_input.html'

    