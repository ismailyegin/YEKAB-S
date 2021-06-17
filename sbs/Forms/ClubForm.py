from django import forms
from django.forms import ModelForm

from sbs.models import SportsClub


class ClubForm(ModelForm):
    class Meta:
        model = SportsClub

        fields = (
            'name', 'shortName', 'foundingDate', 'logo', 'clubMail', 'isFormal', 'petition')
        labels = {
            'name': 'Adı',
            'shortName': 'Kısa Adı',
            'foundingDate': 'Kuruluş Tarihi',
            'clubMail': 'Email',
            'isFormal': 'Kulüp Türü',
            'petition': 'Yetki Belgesi'

        }
        widgets = {
            'isFormal': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                            'style': 'width: 100%; '}),

            'name': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required', "style": "text-transform:uppercase"}),

            'shortName': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),

            'clubMail': forms.TextInput(attrs={'class': 'form-control'}),

            'foundingDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask', 'id': 'datepicker2', 'autocomplete': 'off',
                        'required': 'required'}),

        }
