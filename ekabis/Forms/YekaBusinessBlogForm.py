from django import forms
from django.forms import ModelForm

from ekabis.models.BusinessBlog import BusinessBlog
from ekabis.models.YekaBusinessBlog import YekaBusinessBlog
from ekabis.models.YekaBusinessBlogParemetre import YekaBusinessBlogParemetre


class YekaBusinessBlogForm(ModelForm):
    class Meta:
        model = YekaBusinessBlog

        fields = (
            'startDate', 'finisDate', 'businessTime', 'status')
        labels = {'startDate': 'Başlama Tarihi', 'finisDate': 'Bitiş Tarihi', 'businessTime': 'Süresi',
                  'status': 'Durumu'}

        widgets = {
            'businessTime': forms.TextInput(
                attrs={'class': 'form-control ', 'onkeypress': 'validate(event)'}),

            'status': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; '}),
            'startDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datepicker6', 'autocomplete': 'off',
                       'onkeydown': 'return false', 'required': 'required'}),
            'finisDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datepicker6', 'autocomplete': 'off',
                       'onkeydown': 'return false', 'required': 'required'}),

        }

    def __init__(self, business, *args, **kwargs):
        super(YekaBusinessBlogForm, self).__init__(*args, **kwargs)
        tbussiness = BusinessBlog.objects.get(pk=business)
        for item in tbussiness.parametre.all():
            if item.type == 'string':
                self.fields[item.title] = forms.CharField(max_length=250)
                self.fields[item.title].widget.attrs['class'] = 'form-control'

            elif item.type == 'date':
                self.fields[item.title] = forms.CharField(max_length=50)
                self.fields[item.title].widget.attrs['class'] = 'form-control  datepicker6'

            elif item.type == 'number':

                self.fields[item.title] = forms.CharField(max_length=50)
                self.fields[item.title].widget.attrs['class'] = 'form-control'
                self.fields[item.title].widget.attrs['onkeypress'] = 'validate(event)'
            elif item.type == 'year':

                self.fields[item.title] = forms.CharField(max_length=50)
                self.fields[item.title].widget.attrs['class'] = 'form-control  dateyear'
            elif item.type == 'file':
                self.fields[item.title] = forms.FileField(required=False)

    def save(self, yekabusiness, business,*args, **kwargs):
        tbussiness = BusinessBlog.objects.get(pk=business)
        tyekabusinessblog = YekaBusinessBlog.objects.get(pk=yekabusiness)
        for item in tbussiness.parametre.all():
            if item.type == 'file':

                if tyekabusinessblog.paremetre.filter(parametre=item):
                    try:
                        if self.files[item.title]:
                            bValue = tyekabusinessblog.paremetre.get(parametre=item)
                            bValue.file = self.files[item.title]
                            bValue.save()
                    except:
                        print('deger yok')
                        pass


                else:
                    parametre = YekaBusinessBlogParemetre(
                        file=self.files[item.title],
                    )
                    parametre.parametre = item
                    parametre.save()
                    tyekabusinessblog.paremetre.add(parametre)
                    tyekabusinessblog.save()



            else:
                if tyekabusinessblog.paremetre.filter(parametre=item):
                    bValue=tyekabusinessblog.paremetre.get(parametre=item)
                    bValue.value=str(self.data[item.title])
                    bValue.save()
                else:
                    parametre = YekaBusinessBlogParemetre(
                        value=str(self.data[item.title]),
                    )
                    parametre.parametre = item
                    parametre.save()
                    tyekabusinessblog.paremetre.add(parametre)
                    tyekabusinessblog.save()

        super().save(*args, **kwargs)

        return

def update(self,yekabusiness, business,*args, **kwargs):
    tbussiness = BusinessBlog.objects.get(pk=business)
    tyekabusinessblog = YekaBusinessBlog.objects.get(pk=yekabusiness)
    for item in tyekabusinessblog.parametre.all():
        test = tbussiness.filter(parametre=item)
        test.value = str(self.data[item.title])
        test.save()
    return
