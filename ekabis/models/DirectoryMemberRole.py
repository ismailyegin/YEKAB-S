from django.db import models
from ekabis.models.BaseModel import BaseModel

class DirectoryMemberRole(BaseModel):
    name = models.TextField(blank=False, null=False, verbose_name='Üye Rolü')

    def __str__(self):
        return '%s ' % self.name

    class Meta:
        default_permissions = ()
