from django.db import models

from ekabis.models import Permission
from ekabis.models.BaseModel import BaseModel


class HelpMenu(BaseModel):
    text = models.TextField(blank=False, null=False, verbose_name='Açıklama')
    url = models.ForeignKey(Permission,verbose_name='URL', on_delete=models.CASCADE)

    def __str__(self):
        return '%s ' % self.url
