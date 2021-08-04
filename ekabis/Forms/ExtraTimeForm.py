from django import forms
from ekabis.models.ExtraTime import ExtraTime

CHOICES = (('is_gunu', 'İş Günü'), ('takvim_gunu', 'Takvim Günü'),)


class ExtraTimeForm(forms.ModelForm):
    class Meta:
        model = ExtraTime
        fields = ('time', 'time_type')
        labels = {'time': 'Ek Süre', 'time_type': 'Süre Türü'}
        widgets = {
            'time': forms.TextInput(
                attrs={'class': 'form-control ', 'onkeypress': 'validate(event)'}),
            'time_type': forms.Select(choices=CHOICES, attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                              'style': 'width: 100%; ', }),
        }
