from django import forms
from django.contrib.auth.models import Permission


class PermForm(forms.Form):
    left = forms.ModelMultipleChoiceField(queryset=Permission.objects.none())
    right = forms.ModelMultipleChoiceField(queryset=Permission.objects.none())

    def __init__(self, *args, **kwargs):
        qs = kwargs.pop('left')
        qs1 = kwargs.pop('right')
        super(PermForm, self).__init__(*args, **kwargs)
        self.fields['left'].queryset = qs
        self.fields['right'].queryset = qs1

