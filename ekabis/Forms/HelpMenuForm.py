from django import forms

from ekabis.models.HelpMenu import HelpMenu


class HelpMenuForm(forms.ModelForm):
    class Meta:
        model = HelpMenu
        fields = ('text',)

        labels = {'text': 'Açıklama *', }
        widgets = {
            'text': forms.Textarea(
                attrs={'class': 'form-control textarea', 'id': 'summernote', 'name': 'summernote',
                       'placeholder': 'Mesaj',
                       'columns': 10}),

        }
