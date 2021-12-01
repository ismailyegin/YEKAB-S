from django.db import models

from ekabis.models import Permission
from ekabis.models.BaseModel import BaseModel


class HelpMenu(BaseModel):
    text = models.CharField(max_length=250,blank=False, null=False, verbose_name='Açıklama')
    url = models.OneToOneField(Permission,verbose_name='URL', on_delete=models.DO_NOTHING)

    def __str__(self):
        return '%s ' % self.url
