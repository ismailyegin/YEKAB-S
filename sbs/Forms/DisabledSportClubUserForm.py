from django import forms
from django.forms import ModelForm

from sbs.models import SportClubUser


class DisabledSportClubUserForm(ModelForm):
    class Meta:
        model = SportClubUser

        fields = (
            'role',)
        labels = {'role': 'Kulüp Rolü'}

        widgets = {

            'role': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%; ', 'disabled': 'disabled'}),

        }
