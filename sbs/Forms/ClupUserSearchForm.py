from urllib import request

from django import forms
from django.forms import ModelForm
from sbs.models import SportsClub
from sbs.models import SportClubUser
from sbs.models import City


class ClubSearchForm(ModelForm):
    kisi = forms.ModelChoiceField(queryset=SportClubUser.objects.all().distinct(),
                                  to_field_name='user',
                                  empty_label="Seçiniz",
                                  label="Kulüp Yöneticisi",
                                  required=False,
                                  widget=forms.Select(
                                      attrs={'class': 'form-control select2 select2-hidden-accessible',
                                             'style': 'width: 100%; '}))
    city = forms.ModelChoiceField(queryset=City.objects.all().distinct(),
                                  to_field_name='name',
                                  empty_label="Seçiniz",
                                  label="Şehir",
                                  required=False,
                                  widget=forms.Select(
                                      attrs={'class': 'form-control select2 select2-hidden-accessible',
                                             'style': 'width: 100%; '}))

    class Meta:
        model = SportsClub

        fields = (
            'name', 'shortName', 'clubMail',)

        labels = {
            'name': 'Kulüp Adı',
            'shortName': 'Kulüp Kısa Adı',
            'clubMail': 'Kulüp Email',
            # 'isFormal' : 'Kulüp Türü'

        }
        widgets = {
            # 'isFormal': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
            #                                 'style': 'width: 100%; '}),

            'name': forms.TextInput(attrs={'class': 'form-control ', "style": "text-transform:uppercase"}),

            'shortName': forms.TextInput(attrs={'class': 'form-control'}),

            'clubMail': forms.TextInput(attrs={'class': 'form-control'}),

        }
