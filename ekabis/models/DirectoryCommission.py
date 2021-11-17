from django.db import models
from ekabis.models.BaseModel import BaseModel

class DirectoryCommission(BaseModel):
    name = models.CharField(max_length=250,blank=False, null=False, verbose_name='Kurul Adı')

    def __str__(self):
        return '%s ' % self.name

    # class Meta:
    #     default_permissions = ()
