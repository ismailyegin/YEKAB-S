from django import forms

from ekabis.Forms.BaseForm import BaseForm
from ekabis.models import Company, Person, Employee
from ekabis.models.Yeka import Yeka

STATUS_CHOICES = (
    (("Güneş"), ("Güneş")),
    (("Rüzgar"), ("Rüzgar")),
    (("Biyokütle"), ("Biyokütle")),
    (("Jeotermal"), ("Jeotermal")),
    (("Hibrit"), ("Hibrit")),

)


class YekaForm(BaseForm):
    class Meta:
        model = Yeka

        fields = ('date', 'definition', 'capacity', 'type')

        labels = {'definition': 'Tanım * ', 'date': 'Resmi Gazetede İlan Tarihi  *', 'capacity': 'Kapasite (MWe)',
                  'type': 'Kaynak Türü *'}
        widgets = {
            'definition': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),

            'date': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker', 'autocomplete': 'off',
                       'onkeydown': 'return false', 'required': 'required'}),
            'capacity': forms.TextInput(attrs={'class': 'form-control ', 'onkeypress': 'validate(event)'}),
            'type': forms.Select(choices=STATUS_CHOICES,
                                 attrs={'class': 'form-control select2 select2-hidden-accessible',
                                        'style': 'width: 100%;', 'required': 'required'}),

        }
