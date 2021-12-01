from django.db import models
from django.contrib.auth.models import auth, Permission
from ekabis.models.BaseModel import BaseModel


class Menu(BaseModel):
    name = models.CharField(max_length=120, null=True)
    url = models.CharField(max_length=120, null=True, blank=True)
    is_parent = models.BooleanField()
    is_show = models.BooleanField(default=True)
    fa_icon = models.CharField(max_length=120, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True)
    sorting = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '%s ' % self.name

    class Meta:
        ordering = ['sorting']
        default_permissions = ()
