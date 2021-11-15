from django.db import models

from ekabis.models.Company import Company
from ekabis.models.BaseModel import BaseModel


class ConsortiumCompany(BaseModel):
    percent = models.IntegerField(null=True, blank=True, verbose_name='Yüzde')
    consortium = models.ForeignKey(Company, on_delete=models.DO_NOTHING, related_name='Firma', null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, related_name='Konsorsiyum', null=True, blank=True)

    def __str__(self):
        return '%s ' % self.consortium.name
