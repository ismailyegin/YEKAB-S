from django.contrib.auth.models import User
from django.db import models
from ekabis.models.Communication import Communication
from ekabis.models.CategoryItem import CategoryItem

from ekabis.models.BaseModel import BaseModel


class Company(BaseModel):
    IsFormal = (
        (True, 'Bireysel'),
        (False, 'Kurumsal'),
    )
    name = models.CharField(blank=False, null=False, max_length=120, verbose_name='İsim')
    communication = models.OneToOneField(Communication, on_delete=models.CASCADE, db_column='communication')
    sorumlu = models.CharField(blank=True, null=True, max_length=120, verbose_name='Sorumlu')
    isFormal = models.BooleanField(default=False, choices=IsFormal)
    degree = models.CharField(blank=True, null=True, max_length=120, verbose_name='Unvan')
    taxOffice = models.CharField(blank=True, null=True, max_length=120, verbose_name='Vergi Dairesi ')
    taxnumber = models.CharField(null=True, blank=True, max_length=120, verbose_name='Vergi Numarasi  ')
    mail = models.CharField(blank=True, null=True, max_length=120, verbose_name='mail')
    JopDescription = models.ManyToManyField(CategoryItem)
    kobilid = models.IntegerField(null=True, blank=True, default=1)

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        ordering = ['pk']
