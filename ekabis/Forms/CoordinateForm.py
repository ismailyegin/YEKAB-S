from django import forms

from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.ConnectionUnit import ConnectionUnit
from ekabis.models.Coordinate import Coordinate


class CoordinateForm(BaseForm):
    class Meta:
        model = Coordinate
        fields = ('x', 'y')

        labels = {'x': 'X KoordinatÄ± ', 'y': 'Y KoordinatÄ±'}
        widgets = {
            'x': forms.NumberInput(attrs={'class': 'form-control ', 'required': 'required'}),
            'y': forms.NumberInput(attrs={'class': 'form-control ', 'required': 'required'}),

        }
