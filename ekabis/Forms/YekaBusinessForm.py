from django import forms
from ekabis.models.YekaBussiness import YekaBusiness

class YekaBusinessForm(forms.ModelForm):
    class Meta:
        model = YekaBusiness
        fields = ('name', )

        labels = {'Name': 'Tanım ', }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),

        }