from django import forms
from ekabis.models.Permission import Permission


class PermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ('name', 'codename','model','codeurl','parent','group')
        labels = {
            'name': 'İsim',
            'codename': 'Kod İsmi',
            'codeurl': 'Kod Url',
            'parent':'Menu de ki üst url',
            'group': 'Grup',
            'model':'Model'
        }
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control '}),
            'codename': forms.TextInput(attrs={'class': 'form-control '}),
            'codeurl': forms.TextInput(attrs={'class': 'form-control '}),
            'model': forms.TextInput(attrs={'class': 'form-control '}),
            'parent':forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                              'style': 'width: 100%; '}),
            'group':forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                              'style': 'width: 100%; '}),



        }
