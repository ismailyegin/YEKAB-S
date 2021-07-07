from django import forms

from ekabis.models.Settings import Settings


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ('key', 'value', 'is_active')

        labels = {'key': 'İsim ', 'value': 'Değer', 'is_active': 'Aktif?'}
        widgets = {
            'value': forms.TextInput(attrs={'class': 'form-control '}),
            'key': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'iCheck-helper'}),

        }
