from django.db import models
from ekabis.models.BaseModel import BaseModel


class Country(BaseModel):
    name = models.CharField(max_length=250,blank=True, null=True, verbose_name='Ülke')

    def __str__(self):
        return '%s ' % self.name


    class Meta:
        default_permissions = ()

