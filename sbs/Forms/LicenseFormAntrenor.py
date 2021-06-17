from django import forms
from django.forms import ModelForm

from sbs.models import License
from sbs.models.SportsClub import SportsClub


class LicenseFormAntrenor(ModelForm):
    sportsClub = forms.ModelChoiceField(queryset=SportsClub.objects.all(),
                                        to_field_name='name',
                                        empty_label="Seçiniz",
                                        label="Kulübü",
                                        required=True,
                                        widget=forms.Select(
                                            attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                   'style': 'width: 100%; '}))

    class Meta:
        model = License

        fields = (
            'startDate', 'branch', 'sportsClub', 'licenseNo', 'cityHeadShip', 'expireDate', 'lisansPhoto')

        labels = {'startDate': 'Başlangıç Tarihi', 'branch': 'Branş',
                  'licenseNo': 'Lisans No', 'cityHeadShip': 'Verildiği İl', 'expireDate': ' Bitiş Tarihi',
                  'lisansPhoto': 'Lisans Foto'}

        widgets = {

            'startDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask', 'id': 'datepicker2', 'autocomplete': 'on',
                        }),

            'expireDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask', 'id': 'datepicker4', 'autocomplete': 'on',
                       }),

            'branch': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; '}),

            'licenseNo': forms.TextInput(
                attrs={'class': 'form-control', 'required': 'required', 'onkeypress': 'validate(event)'}),

            'cityHeadShip': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                'style': 'width: 100%;', 'required': 'required'}),

        }
