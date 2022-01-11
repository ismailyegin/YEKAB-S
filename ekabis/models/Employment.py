from django.db import models
from ekabis.models.BaseModel import BaseModel


class Employment(BaseModel):
    employmentDate = models.DateField(null=True, blank=True, verbose_name='Tarihi')
    employmentFile = models.FileField(upload_to='istihdam/', null=True, blank=True, verbose_name=' İstihdam Dokümanı')
