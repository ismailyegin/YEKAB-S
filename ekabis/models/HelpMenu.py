from django.db import models
from ekabis.models.BaseModel import BaseModel


class HelpMenu(BaseModel):
    text = models.TextField(blank=False, null=False, verbose_name='Açıklama')
    url = models.CharField(max_length=300, blank=False, null=False, verbose_name='URL')

    def __str__(self):
        return '%s ' % self.url
