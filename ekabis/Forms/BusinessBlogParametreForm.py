from django import forms
from django.forms import ModelForm

from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.BusinessBlogParametreType import BusinessBlogParametreType


class BusinessBlogParametreForm(BaseForm):
    class Meta:
        model = BusinessBlogParametreType
        fields = ('title', 'type', 'necessary', 'companynecessary', 'is_change', 'visibility_in_yeka')
        labels = {'title': 'Tanımı',
                  'type': 'Türü',
                  'necessary': 'Zorunlu ',
                  'companynecessary': 'Firma Müdahale Edebilir Mi?', 'is_change': 'Düzenlenebilir mi?',
                  'visibility_in_yeka': 'Yeka İş Bloğunda Görünmeli Mi?'}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),
            'type': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;', 'required': 'required'}),
            'necessary': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                             'style': 'width: 100%;', 'required': 'required'}),
            'companynecessary': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                    'style': 'width: 100%;', 'required': 'required'}),
            'is_change': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                             'style': 'width: 100%;', 'required': 'required'}),
            'visibility_in_yeka': forms.CheckboxInput(attrs={'class': 'form-check-input'})

        }
