from django.db import models

from ekabis.models.BaseModel import BaseModel


class VacationDay(BaseModel):
    definition = models.CharField(blank=True, null=True, max_length=100)
    date = models.DateTimeField(blank=True, null=True,verbose_name='Tatil Günü')

    def __str__(self):
        return '%s' % self.definition
    class Meta:
        verbose_name = "VacationDay"


