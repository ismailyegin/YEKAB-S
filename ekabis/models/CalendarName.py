from django.contrib.auth.models import User, Group
from django.db import models
from ekabis.models.BaseModel import BaseModel


class CalendarName(BaseModel):
    name = models.CharField(blank=False, null=False, max_length=255)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    color = models.CharField(blank=False, null=False, max_length=100)
