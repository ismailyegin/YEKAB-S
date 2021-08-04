from django import forms
from django.forms import ModelForm

from ekabis.models.BusinessBlog import BusinessBlog


class BusinessBlogForm(ModelForm):
    class Meta:
        model = BusinessBlog
        fields = ('name',
                  'start_notification',
                  'finish_notification',)
        labels = {'name': 'Tanımı',
                  'start_notification':'Başlangıçtan İtibaren Gün',
                  'finish_notification':'Süre Bitiminden Önce Gün'
                  }

        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required'}),
            'start_notification':forms.TextInput(attrs={'class': 'form-control ', 'required': 'required','onkeypress':'validate(event)'}),
            'finish_notification':forms.TextInput(attrs={'class': 'form-control ', 'required': 'required','onkeypress':'validate(event)'}),





        }