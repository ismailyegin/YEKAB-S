from django import forms
from django.forms import ModelForm

from ekabis.models.Company import Company
from ekabis.models.CompanyFileNames import CompanyFileNames
from ekabis.models.CompanyFiles import CompanyFiles
class CompanyFormDinamik(ModelForm):
    class Meta:
        model = Company
        fields = (
            'name',
            'degree',
            'taxOffice',
            'taxnumber',
            'mail',
        )
        labels = {'name': 'Firma İsmi *',
                  'degree': 'Unvan',
                  'taxOffice': 'Vergi Dairesi ',
                  'taxnumber': 'Vergi Numarası ',
                  'mail': 'Mail Adresi ',
                  }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),
            'degree': forms.TextInput(attrs={'class': 'form-control '}),
            'taxOffice': forms.TextInput(attrs={'class': 'form-control '}),
            'taxnumber': forms.TextInput(attrs={'class': 'form-control ','onkeypress': 'validate(event)'}),
            #'taxnumber': forms.TextInput(attrs={'class': 'form-control ','pattern':'^\$\d{1.}(.\d{3})*(\,\d+)?$','data-type':'currency'}),
            'mail': forms.EmailInput(attrs={'class': 'form-control '}),
        }

    def __init__(self, *args, **kwargs):
        super(CompanyFormDinamik, self).__init__(*args, **kwargs)
        parametre = CompanyFileNames.objects.all()
        for item in parametre:
            self.fields['file'+str(item.pk)] = forms.FileField()

            if item.is_active:
                self.fields['file' + str(item.pk)].required = True
                self.fields['file' + str(item.pk)].label = item.name +" (Zorunlu Alan)"
            else:
                self.fields['file' + str(item.pk)].required = False



    def save(self,communication):
        parametre = CompanyFileNames.objects.filter(is_active=True)
        company=Company(
            name = self.data['name'],
            degree = self.data['degree'],
            taxOffice = self.data['taxOffice'],
            taxnumber = self.data['taxnumber'],
            mail = self.data['mail'],
            communication=communication,
                    )
        company.save()
        for item in parametre:
            companyfile = CompanyFiles(
               filename=item,
               file=self.files['file'+str(item.pk)]
            )
            companyfile.save()
            company.files.add(companyfile)
            company.save()
        return company