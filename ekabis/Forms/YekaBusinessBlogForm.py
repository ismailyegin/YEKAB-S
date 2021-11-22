from datetime import timedelta

from django import forms
from django.forms import ModelForm

from ekabis.models.BusinessBlog import BusinessBlog
from ekabis.models.YekaBusinessBlog import YekaBusinessBlog
from ekabis.models.YekaBusinessBlogParemetre import YekaBusinessBlogParemetre
from ekabis.services.services import BusinessBlogGetService
from datetime import datetime
from django.utils import formats
import datetime

CHOICES = (('is_gunu', 'İş Günü'), ('takvim_gunu', 'Takvim Günü'),)
TRUE_FALSE_CHOICES = (
    ('4', 'Başlanmadı'),
    ('3', 'Devam Ediyor'),
    ('1', 'Tamamlandı'),
    ('2', 'Tamamlanmadı'),

)


class YekaBusinessBlogForm(ModelForm):
    class Meta:
        model = YekaBusinessBlog
        fields = (
            'indefinite',

            'dependence_parent',
            'child_block',
            'time_type',
            'businessTime',
            'startDate',
            'explanation',
            'status',
            'completion_date',

        )
        labels = {
            'startDate': 'İşin Yapılma Tarihi',
            # 'finisDate': 'Bitiş Tarihi',
            'businessTime': 'Süresi(Gün)',
            'status': 'Durumu',
            'indefinite': 'Süre Durumu',
            'time_type': 'Süre Türü',
            'dependence_parent': 'Bir Önceki İş Bloğu',
            'child_block': 'Bir Sonraki İş Bloğu',
            'explanation': 'Açıklama ',
        }
        widgets = {
            'businessTime': forms.TextInput(
                attrs={'class': 'form-control ', 'onkeypress': 'validate(event)'}),
            'time_type': forms.Select(choices=CHOICES, attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                              'style': 'width: 100%; ', }),

            'status': forms.Select(choices=TRUE_FALSE_CHOICES,
                                   attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%;', 'value': ''}),
            'indefinite': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                              'style': 'width: 100%; '}),
            'startDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right ', 'id': 'datepicker4', 'autocomplete': 'off',
                       'onkeydown': 'return true', "data-inputmask-alias": "datetime",
                       "data-inputmask-inputformat": "dd/mm/yyyy", "data-mask": "", "inputmode": "numeric"}),
            'completion_date': forms.DateInput(
                attrs={'class': 'form-control  pull-right datepicker6', 'id': 'datepicker', 'autocomplete': 'off',
                       'onkeydown': 'return true', "data-inputmask-alias": "datetime",
                       "data-inputmask-inputformat": "dd/mm/yyyy", "data-mask": "", "inputmode": "numeric"}),
            'explanation': forms.TextInput(
                attrs={'class': 'form-control', 'rows': '3'}),
            'dependence_parent': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                     'style': 'width: 100%; '}),
            'child_block': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                               'style': 'width: 100%; '}),
            # 'finisDate': forms.DateInput(
            #     attrs={'class': 'form-control  pull-right datepicker6', 'autocomplete': 'off',
            #            'onkeydown': 'return false', 'required': 'required'}),

        }

    def __init__(self, business, yekabussiness, *args, **kwargs):
        super(YekaBusinessBlogForm, self).__init__(*args, **kwargs)
        # if yekabussiness.parent:
        #     if yekabussiness.parent.finisDate:
        #         self.fields['startDate'].label = 'İşin Yapılma Tarihi   (' + str(
        #             yekabussiness.parent.businessblog.name) + ' bitiş Tarihi:' + str(
        #             yekabussiness.parent.finisDate.strftime("%d-%m-%Y")) + ')'
        business_filter = {
            'pk': business
        }
        tbussiness = BusinessBlogGetService(self, business_filter)



        for item in tbussiness.parametre.filter(isDeleted=False):
            if item.type == 'string':
                self.fields[item.title] = forms.CharField(max_length=250)
                if item.necessary:
                    self.fields[item.title].widget.attrs = {'required': 'required', 'class': 'form-control', }
                else:
                    self.fields[item.title].widget.attrs = {'class': 'form-control', }
            elif item.type == 'date':
                self.fields[item.title] = forms.CharField(max_length=50)
                if item.necessary:
                    self.fields[item.title].widget.attrs = {'required': 'required',
                                                            'class': 'form-control datepicker6', }
                else:
                    self.fields[item.title].widget.attrs = {'class': 'form-control datepicker6', }

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
                    self.fields[item.title].widget.attrs = {'required': 'required', 'class': 'form-control dateyear', }
                else:
                    self.fields[item.title].widget.attrs = {'class': 'form-control dateyear', }
            elif item.type == 'file':
                self.fields[item.title] = forms.FileField(required=False)
                if item.necessary:
                    self.fields[item.title].widget.attrs = {'required': 'required', 'class': 'form-control', }
                else:
                    self.fields[item.title].widget.attrs = {'class': 'form-control', }

    def save(self, yekabusiness, business, *args, **kwargs):

        tbussiness = BusinessBlog.objects.get(pk=business)
        tyekabusinessblog = YekaBusinessBlog.objects.get(pk=yekabusiness)

        for item in tbussiness.parametre.filter(isDeleted=False):
            if item.type == 'file':
                if tyekabusinessblog.parameter.filter(parametre=item, isDeleted=False):
                    try:
                        if self.files[item.title]:
                            bValue = tyekabusinessblog.parameter.get(parametre=item)
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
                            tyekabusinessblog.parameter.add(parametre)
                            tyekabusinessblog.save()
                    except:
                        print('deger yok ')
                        pass
            else:
                if tyekabusinessblog.parameter.filter(parametre=item):
                    bValue = tyekabusinessblog.parameter.get(parametre=item)
                    bValue.value = str(self.data[item.title])
                    bValue.save()
                else:
                    parametre = YekaBusinessBlogParemetre(
                        value=str(self.data[item.title]),
                    )
                    parametre.parametre = item
                    parametre.save()
                    tyekabusinessblog.parameter.add(parametre)
                    tyekabusinessblog.save()

        super().save(*args, **kwargs)
        return


def update(self, yekabusiness, business, *args, **kwargs):
    tbussiness = BusinessBlog.objects.get(pk=business)
    tyekabusinessblog = YekaBusinessBlog.objects.get(pk=yekabusiness)
    for item in tyekabusinessblog.parametre.all():
        test = tbussiness.filter(parametre=item)
        test.value = str(self.data[item.title])
        test.save()
    return
