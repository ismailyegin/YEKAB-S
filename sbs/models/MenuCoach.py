from django.db import models
from django.contrib.auth.models import auth, Permission, User


class MenuCoach(models.Model):
    name = models.CharField(max_length=120, null=True)
    url = models.CharField(max_length=120, null=True, blank=True)
    permission = models.ManyToManyField(User)
    is_parent = models.BooleanField(default=True)
    is_show = models.BooleanField(default=True)
    fa_icon = models.CharField(max_length=120, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    sorting = models.IntegerField(null=True, blank=True)

    # class Meta:
    #     default_permissions = ()
