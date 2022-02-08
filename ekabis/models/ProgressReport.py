from django.db import models
from ekabis.models.BaseModel import BaseModel


class ProgressReport(BaseModel):
    definition = models.CharField(null=True, blank=True, verbose_name='Açıklama' ,max_length=250)
    reportFile = models.FileField(upload_to='ilerleme-raporu/', null=True, blank=True, verbose_name='İlerleme Raporu')

    def __str__(self):
        return '%s' % self.definition