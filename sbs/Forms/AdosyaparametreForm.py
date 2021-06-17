from django.forms import ModelForm

from sbs.models.AdosyaParametre import AdosyaParametre


class AdosyaparametreForm(ModelForm):
    class Meta:
        model = AdosyaParametre
        fields =('value','parametre')
    def __init__(self, *args, **kwargs):
        super(AdosyaparametreForm,self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'