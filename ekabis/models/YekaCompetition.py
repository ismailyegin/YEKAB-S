from django.db import models

from ekabis.models import Company
from ekabis.models.City import City
from ekabis.models.YekaBussiness import YekaBusiness
from ekabis.models.BaseModel import BaseModel
class YekaCompetition(BaseModel):
    name = models.TextField(blank=False, null=False, verbose_name='Yeka Yarışması')
    capacity = models.IntegerField(null=False, blank=False, verbose_name='Kapasite')
    date = models.DateField(blank=True, null=True)
    city = models.ManyToManyField(City)
    business = models.OneToOneField(YekaBusiness, on_delete=models.CASCADE,null=True,blank=True)
    company=models.ForeignKey(Company,on_delete=models.DO_NOTHING,null=True,blank=True)

    def __str__(self):
        return '%s ' % self.name

    class Meta:
        default_permissions = ()
