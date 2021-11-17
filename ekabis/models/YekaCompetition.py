from django.db import models
from unicode_tr import unicode_tr

from ekabis.models import Company
from ekabis.models.City import City
from ekabis.models.YekaBussiness import YekaBusiness
from ekabis.models.BaseModel import BaseModel


class YekaCompetition(BaseModel):
    name = models.CharField(max_length=250,blank=False, null=False, verbose_name='Yeka Yarışması')
    capacity = models.IntegerField(null=False, blank=False, verbose_name='Kapasite')
    date = models.DateField(blank=True, null=True)
    city = models.ManyToManyField(City)
    business = models.OneToOneField(YekaBusiness, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)
    eskalasyon_first_date = models.CharField(null=True, blank=True,max_length=100)
    is_calculation = models.BooleanField(null=True, blank=True, default=True)

    def __str__(self):
        return '%s ' % self.name

    def save(self, force_insert=False, force_update=False):
         if self.name:
                self.name = unicode_tr(self.name).upper()

         super(YekaCompetition, self).save(force_insert, force_update)
