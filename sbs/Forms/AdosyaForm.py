from sbs.models import Abirim
from sbs.models.Adosya import Adosya
from django import forms
from django.forms import ModelForm
from sbs.models.AdosyaParametre import AdosyaParametre
from sbs.models.AbirimParametre import AbirimParametre
from sbs.models.Aklasor import Aklasor




class AdosyaForm(ModelForm):
    klasor=None
    class Meta:
        model = Adosya
        fields = ('sirano',)
        labels = {'sirano': 'Sıra No',}
        widgets = {
            'sirano': forms.TextInput(
                attrs={'class': 'form-control ', 'required': 'required'}),
        }
    def __init__(self,pk, *args, **kwargs):
        super(AdosyaForm, self).__init__(*args, **kwargs)
        # print(birim)
        klasor=Aklasor.objects.get(pk=pk)
        parametre=AbirimParametre.objects.filter(birim=klasor.birim)
        for item in parametre:
            if item.type == 'string':
                self.fields[item.title] = forms.CharField(max_length=250)
                self.fields[item.title].widget.attrs['class'] = 'form-control'

            elif item.type == 'date':
                self.fields[item.title] = forms.CharField(max_length=50)
                self.fields[item.title].widget.attrs['class'] = 'form-control  datepicker6'

            elif item.type == 'number':

                self.fields[item.title] =forms.CharField(max_length=50)
                self.fields[item.title].widget.attrs['class'] = 'form-control'
                self.fields[item.title].widget.attrs['onkeypress'] = 'validate(event)'
            elif item.type == 'year':

                self.fields[item.title] = forms.CharField(max_length=50)
                self.fields[item.title].widget.attrs['class'] = 'form-control  dateyear'

        # for visible in self.visible_fields():
        #     visible.field.widget.attrs['class'] = 'form-control'

    def save(self,pk):
        klasor=Aklasor.objects.get(pk=pk)
        parametre = AbirimParametre.objects.filter(birim=klasor.birim)
        dosya=Adosya(
            sirano=self.data['sirano'],
                     klasor_id=pk,
                    )
        dosya.save()

        for item in parametre:
            dosyaParametre = AdosyaParametre(
                value= str(self.data[item.title]),
                dosya=dosya,
            )
            dosyaParametre.parametre=item
            dosyaParametre.save()
        return dosya.pk
    def update(self,pk):
        dosya=Adosya.objects.get(pk=pk)
        parametre = AbirimParametre.objects.filter(birim=dosya.klasor.birim)

        for item in parametre:
            test=AdosyaParametre.objects.filter(dosya=dosya,parametre=item)[0]
            test.value=str(self.data[item.title])
            test.save()
        return dosya.pk
