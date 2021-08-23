from django import forms
from django.forms import ModelForm

from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.Location import Location



class LocationForm(BaseForm):
    class Meta:
        model = Location

        fields = ('city', 'district', 'neighborhood',)
        labels = {'city': 'Şehir * ', 'district': 'İlçe * ', 'neighborhood': 'Mahalle * '}
        widgets = {
            'city': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible',
                       'style': 'width: 100%; ', "onChange": 'ilceGetir()', 'name': "city", 'id': "id_city"}),
            'district': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                            'style': 'width: 100%; ', 'id': 'ilce_id', "onChange": 'mahalleGetir()',
                                            }),
            'neighborhood': forms.Select(
                attrs={'class': 'form-control select2 select2-hidden-accessible ',
                       'style': 'width: 100%; ',
                       'placeholder': 'Mahalle', 'id': 'neighborhood_id',
                       }),

        }
