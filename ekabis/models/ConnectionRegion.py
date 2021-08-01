from django.db import models

from ekabis.models.BaseModel import BaseModel
from ekabis.models.YekaCompetition import YekaCompetition
from ekabis.models.City import City

class ConnectionRegion(BaseModel):
    name = models.TextField(blank=False, null=False, verbose_name='Bağlantı Bölgesi')
    capacity = models.IntegerField(null=False, blank=False, verbose_name='Kapasite')
    cities=models.ManyToManyField(City)
    yekacompetition=models.ManyToManyField(YekaCompetition)
    def __str__(self):
        return '%s ' % self.name

    class Meta:
        default_permissions = ()
