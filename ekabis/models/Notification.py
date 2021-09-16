from django.contrib.auth.models import User
from django.db import models
from ekabis.models.BaseModel import BaseModel


class Notification(BaseModel):
    description = models.CharField(blank=True, null=True, max_length=200, verbose_name='İçerik')
    title = models.CharField(blank=True, null=True, max_length=200, verbose_name='Başlık')

    def __str__(self):
        return '%s ' % self.description
