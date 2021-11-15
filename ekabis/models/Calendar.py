from django.contrib.auth.models import User, Group
from django.db import models
from ekabis.models.BaseModel import BaseModel
from ekabis.models.CalendarName import CalendarName


class Calendar(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    calendarName =models.ForeignKey(CalendarName,on_delete=models.CASCADE)
    startDate=models.DateTimeField(blank=True, null=True,)
    finishDate=models.DateTimeField(blank=True, null=True,)
    color=models.CharField(blank=True, null=True, max_length=100)
    is_active=models.BooleanField(default=True)


