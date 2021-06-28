from django.db import models
from django.contrib.auth.models import auth, Permission
from ekabis.models.BaseModel import BaseModel
class Menu(BaseModel):

    name = models.CharField(max_length=120, null=True)
    url = models.CharField(max_length=120, null=True, blank=True)
    is_parent = models.BooleanField(default=True)
    is_show = models.BooleanField(default=True)
    fa_icon = models.CharField(max_length=120, null=True , blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    sorting=models.IntegerField()


    # class Meta:
    #     default_permissions = ()
