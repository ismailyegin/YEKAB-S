from django import forms
from django.forms import ModelForm
from ekabis.models.BusinessBlogParametreType import BusinessBlogParametreType
class BusinessBlogParametreForm(ModelForm):
    class Meta:
        model = BusinessBlogParametreType
        fields = ('title','type')
        labels = {'title': 'Tanımı','type':'Türü'}
        widgets = {
            'title':  forms.TextInput(attrs={'class': 'form-control ','required': 'required'}),
            'type': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%;', 'required': 'required'}),
        }