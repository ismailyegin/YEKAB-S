from django.db import models
from unicode_tr import unicode_tr

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

    def save(self, force_insert=False, force_update=False):
        if self.name:
            self.name = unicode_tr(self.name).upper()

        super(ConnectionRegion, self).save(force_insert, force_update)
