from django.db import models
from ekabis.models.BaseModel import BaseModel


class Country(BaseModel):
    name = models.TextField(blank=True, null=True, verbose_name='Ülke')

    def __str__(self):
        return '%s ' % self.name


    class Meta:
        default_permissions = ()

