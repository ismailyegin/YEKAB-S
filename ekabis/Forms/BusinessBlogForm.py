from django import forms
from django.forms import ModelForm

from ekabis.models.BusinessBlog import BusinessBlog


class BusinessBlogForm(ModelForm):
    class Meta:
        model = BusinessBlog
        fields = ('name',)
        labels = {'name': 'Tanımı',}
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required'}),

        }