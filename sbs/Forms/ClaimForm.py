from django import forms
from django.forms import ModelForm

from sbs.models.Claim import Claim


class ClaimForm(ModelForm):
    class Meta:
        model = Claim

        fields = (
            'title', 'project', 'status', 'definition', 'importanceSort', 'pay')

        labels = {'pay': 'Ücret ',
                  'title': 'Başlık ',
                  'status': 'Durumu ',
                  'definition': 'Açıklama ',
                  'importanceSort': 'Önem Durumu',
                  'project': 'Proje Seçiniz', }

        widgets = {
            'status': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; '}),
            'importanceSort': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                  'style': 'width: 100%; '}),
            'project': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                           'style': 'width: 100%; '}),
            'title': forms.TextInput(attrs={'class': 'form-control', "style": "text-transform:uppercase"}),
            'definition': forms.Textarea(attrs={'class': 'form-control','rows': '2'}),


            'pay': forms.NumberInput(attrs={'class': 'form-control', 'onkeypress': 'validate(event)'}),

        }
