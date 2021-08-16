from django import forms
from ekabis.models.Settings import Settings
class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ( 'value','label','explanation')
        labels = { 'value': 'Value','label':'label','explanation':'explanation' }
        widgets = {
            'value': forms.TextInput(attrs={'class': 'form-control '}),
            'label': forms.TextInput(attrs={'class': 'form-control '}),
            'explanation': forms.TextInput(attrs={'class': 'form-control ','row':2}),
        }
