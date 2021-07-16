from django import forms
from ekabis.models.ExtraTime import ExtraTime

class ExtraTimeForm(forms.ModelForm):
    class Meta:
        model = ExtraTime
        fields = ('time',)
        labels = {'time': 'Eksta Eklenecek zaman '}
        widgets = {
            'time': forms.TextInput(
                attrs={'class': 'form-control ', 'onkeypress': 'validate(event)'}),
        }