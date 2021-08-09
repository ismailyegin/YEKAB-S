from django.contrib.auth.models import User
from django.db import models
from ekabis.models.Communication import Communication
from ekabis.models.CategoryItem import CategoryItem
from ekabis.models.CompanyFiles import CompanyFiles
from ekabis.models.CompanyUser import CompanyUser

from ekabis.models.BaseModel import BaseModel


class Company(BaseModel):
    name = models.CharField(blank=False, null=False, max_length=120, verbose_name='İsim')
    communication = models.OneToOneField(Communication, on_delete=models.CASCADE, db_column='communication', null=True,
                                         blank=True)
    sorumlu = models.CharField(blank=True, null=True, max_length=120, verbose_name='Sorumlu')
    isFormal = models.BooleanField(default=False)
    degree = models.CharField(blank=True, null=True, max_length=120, verbose_name='Unvan')
    taxOffice = models.CharField(blank=True, null=True, max_length=120, verbose_name='Vergi Dairesi ')
    taxnumber = models.CharField(null=True, blank=True, max_length=120, verbose_name='Vergi Numarasi  ')
    mail = models.CharField(blank=True, null=True, max_length=120, verbose_name='mail')
    JopDescription = models.ManyToManyField(CategoryItem)
    kobilid = models.IntegerField(null=True, blank=True, default=1)
    files = models.ManyToManyField(CompanyFiles)
    companyuser = models.ManyToManyField(CompanyUser, null=True, blank=True)
    is_consortium = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        ordering = ['pk']
