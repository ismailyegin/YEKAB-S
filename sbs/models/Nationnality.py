from django.contrib.auth.models import User
from django.db import models


class Nationnality(models.Model):
    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=150, null=True)

    def __str__(self):
        return '%s ' % self.name

    # class Meta:
    #     default_permissions = ()
