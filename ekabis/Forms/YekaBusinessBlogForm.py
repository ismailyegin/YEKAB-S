from django import forms
from django.forms import ModelForm

from ekabis.models.BusinessBlog import BusinessBlog
from ekabis.models.YekaBusinessBlog import YekaBusinessBlog
from ekabis.models.YekaBusinessBlogParemetre import YekaBusinessBlogParemetre
from ekabis.services.services import BusinessBlogGetService


class YekaBusinessBlogForm(ModelForm):
    class Meta:
        model = YekaBusinessBlog
        fields = (
            'indefinite','startDate','businessTime', 'finisDate',  'status',)
        labels = {'startDate': 'Başlama Tarihi',
                  'finisDate': 'Bitiş Tarihi',
                  'businessTime': 'Süresi',
                  'status': 'Durumu',
                  'indefinite':'Süre durumu'}
        widgets = {
            'businessTime': forms.TextInput(
                attrs={'class': 'form-control ', 'onkeypress': 'validate(event)'}),

            'status': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; '}),
            'indefinite': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; '}),
            'startDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datepicker6', 'autocomplete': 'off',
                       'onkeydown': 'return false', 'required': 'required'}),
            'finisDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datepicker6', 'autocomplete': 'off',
                       'onkeydown': 'return false', 'required': 'required'}),

        }

    def __init__(self, business,yekabussiness, *args, **kwargs):
        super(YekaBusinessBlogForm, self).__init__(*args, **kwargs)
        business_filter={
            'pk':business
        }
        tbussiness = BusinessBlogGetService(self,business_filter)
        for item in tbussiness.parametre.filter(isDeleted=False):
            if item.companynecessary:
                print('bu alan bütün firmalar icin olmalı')
                if yekabussiness.companys.all():
                    print('firma bilgisi var ')
                    for company in yekabussiness.companys.filter(isDeleted=False):
                        print(company.name)
                        title=str(item.title)+"-"+str(company.pk)


                        if item.type == 'string':
                            self.fields[title] = forms.CharField(max_length=250)
                            if item.necessary:
                                self.fields[title].widget.attrs = {'required': 'required','class': 'form-control'}
                            else:
                                self.fields[title].widget.attrs = {'class': 'form-control', }

                        elif item.type == 'date':
                            self.fields[title] = forms.CharField(max_length=50)
                            if item.necessary:
                                self.fields[title].widget.attrs = {'required': 'required','class': 'form-control', }
                            else:
                                self.fields[title].widget.attrs = {'class': 'form-control', }

                        elif item.type == 'number':

                            self.fields[title] = forms.CharField(max_length=50)
                            self.fields[title].widget.attrs['onkeypress'] = 'validate(event)'
                            if item.necessary:
                                self.fields[title].widget.attrs = {'required': 'required','class': 'form-control', }
                            else:
                                self.fields[title].widget.attrs = {'class': 'form-control', }
                        elif item.type == 'year':
                            self.fields[title] = forms.CharField(max_length=50)
                            if item.necessary:
                                self.fields[title].widget.attrs = {'required': 'required','class': 'form-control', }
                            else:
                                self.fields[title].widget.attrs = {'class': 'form-control', }
                        elif item.type == 'file':
                            self.fields[title] = forms.FileField(required=False)
                            if item.necessary:
                                self.fields[title].widget.attrs = {'required': 'required','class': 'form-control', }
                            else:
                                self.fields[title].widget.attrs = {'class': 'form-control', }
                        self.fields[title].label = str(item.title) + "-" + str(company.name)

            else:
                if item.type == 'string':
                    self.fields[item.title] = forms.CharField(max_length=250)
                    if item.necessary:
                        self.fields[item.title].widget.attrs = {'required': 'required', 'class': 'form-control', }
                    else:
                        self.fields[item.title].widget.attrs = {'class': 'form-control', }
                elif item.type == 'date':
                    self.fields[item.title] = forms.CharField(max_length=50)
                    if item.necessary:
                        self.fields[item.title].widget.attrs = {'required': 'required', 'class': 'form-control', }
                    else:
                        self.fields[item.title].widget.attrs = {'class': 'form-control', }

                elif item.type == 'number':

                    self.fields[item.title] = forms.CharField(max_length=50)
                    self.fields[item.title].widget.attrs['onkeypress'] = 'validate(event)'
                    if item.necessary:
                        self.fields[item.title].widget.attrs = {'required': 'required', 'class': 'form-control', }
                    else:
                        self.fields[item.title].widget.attrs = {'class': 'form-control', }
                elif item.type == 'year':
                    self.fields[item.title] = forms.CharField(max_length=50)
                    if item.necessary:
                        self.fields[item.title].widget.attrs = {'required': 'required', 'class': 'form-control', }
                    else:
                        self.fields[item.title].widget.attrs = {'class': 'form-control', }
                elif item.type == 'file':
                    self.fields[item.title] = forms.FileField(required=False)
                    if item.necessary:
                        self.fields[item.title].widget.attrs = {'required': 'required', 'class': 'form-control', }
                    else:
                        self.fields[item.title].widget.attrs = {'class': 'form-control', }


    def save(self, yekabusiness, business,*args, **kwargs):
        tbussiness = BusinessBlog.objects.get(pk=business)
        tyekabusinessblog = YekaBusinessBlog.objects.get(pk=yekabusiness)
        for item in tbussiness.parametre.filter(isDeleted=False):
            if item.companynecessary:
                for company in tyekabusinessblog.companys.all():
                    title = str(item.title) + "-" + str(company.pk)
                    print(title)
                    if item.type == 'file':
                        if tyekabusinessblog.paremetre.filter(parametre=item, isDeleted=False,company=company):
                            try:
                                if self.files[title]:
                                    bValue = tyekabusinessblog.paremetre.get(parametre=item)
                                    bValue.file = self.files[title]
                                    bValue.company=company
                                    bValue.save()
                            except:
                                print('deger yok ')
                                pass

                        else:
                            try:
                                if self.files[title]:
                                    parametre = YekaBusinessBlogParemetre(
                                        file=self.files[title],
                                        company=company,
                                    )
                                    parametre.parametre = item
                                    parametre.save()
                                    tyekabusinessblog.paremetre.add(parametre)
                                    tyekabusinessblog.save()
                            except:
                                print('deger yok ')
                                pass

            else:
                if item.type == 'file':
                    if tyekabusinessblog.paremetre.filter(parametre=item,isDeleted=False):
                        try:
                            if self.files[item.title]:
                                bValue = tyekabusinessblog.paremetre.get(parametre=item)
                                bValue.file = self.files[item.title]
                                bValue.save()
                        except:
                            print('deger yok ')
                            pass

                    else:
                        try:
                            if self.files[item.title]:
                                parametre = YekaBusinessBlogParemetre(
                                    file=self.files[item.title],
                                )
                                parametre.parametre = item
                                parametre.save()
                                tyekabusinessblog.paremetre.add(parametre)
                                tyekabusinessblog.save()
                        except:
                            print('deger yok ')
                            pass
                else:
                    if tyekabusinessblog.paremetre.filter(parametre=item):
                        bValue = tyekabusinessblog.paremetre.get(parametre=item)
                        bValue.value = str(self.data[item.title])
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
