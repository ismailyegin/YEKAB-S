from django.db import models

from ekabis.models.Company import Company
from ekabis.models.BaseModel import BaseModel
from ekabis.models.YekaApplicationFile import YekaApplicationFile

class YekaCompany(BaseModel):
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(null=True,blank=True,default=True)
    files = models.ManyToManyField(YekaApplicationFile)
    price=models.DecimalField(null=True,blank=True,max_digits=20,decimal_places=2)
    def __str__(self):
        return '%s ' % self.company.name
