from random import choices
from django.contrib.auth.models import  Group
from django.db import models
from ekabis.models.BaseModel import BaseModel
from ekabis.models.Permission import Permission
class PermissionGroup(BaseModel):
    permissions = models.ForeignKey(Permission,verbose_name='permissions',blank=True,on_delete=models.CASCADE)
    group=models.ForeignKey(Group,verbose_name='group',blank=True,on_delete=models.CASCADE)
    is_active=models.BooleanField(default=False)
