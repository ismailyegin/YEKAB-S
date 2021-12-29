from django import forms
from django.forms import ModelForm

from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.Claim import Claim


class ClaimForm(BaseForm):
    class Meta:
        model = Claim

        fields = (
            'title',  'definition', 'importanceSort')

        labels = {
                  'title': 'Başlık ',
                  'status': 'Durumu ',
                  'definition': 'Açıklama ',
                  'importanceSort': 'Önem Durumu',
                }

        widgets = {

            'importanceSort': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                  'style': 'width: 100%; '}),

            'title': forms.TextInput(attrs={'class': 'form-control', "style": "text-transform:uppercase"}),
            'definition': forms.Textarea(attrs={'class': 'form-control','rows': '6'}),


        }
