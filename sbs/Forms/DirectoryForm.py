from django.forms import ModelForm
from django import forms

from sbs.models import DirectoryMember


class DirectoryForm(ModelForm):
    class Meta:
        model = DirectoryMember
        fields = (
            'role', 'commission')
        labels = {'role': 'Üye Rolü', 'commission': 'Kurulu'}
        widgets = {

            'role': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;', 'required': 'required'}),

            'commission': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                              'style': 'width: 100%;', 'required': 'required'}),

        }
