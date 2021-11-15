from django import forms

from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.HelpMenu import HelpMenu


class HelpMenuForm(BaseForm):
    class Meta:
        model = HelpMenu
        fields = ('text','url',)

        labels = {'text': 'Açıklama *', 'url *':'Sayfa URL'}
        widgets = {
            'text': forms.Textarea(
                attrs={'class': 'form-control textarea', 'id': 'summernote', 'name': 'summernote',
                       'placeholder': 'Mesaj',
                       'columns': 10}),
            'url': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%;', 'required': 'required'}),

        }
