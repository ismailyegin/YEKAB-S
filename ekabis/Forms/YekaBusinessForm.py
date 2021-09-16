from django import forms

from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.YekaBussiness import YekaBusiness

class YekaBusinessForm(BaseForm):
    class Meta:
        model = YekaBusiness
        fields = ('name', )

        labels = {'Name': 'Tanım ', }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),

        }