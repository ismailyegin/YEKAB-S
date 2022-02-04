from django.contrib.auth.models import User, Group
from django.db import models

from ekabis.models import YekaCompetition
from ekabis.models.BaseModel import BaseModel
from ekabis.models.CalendarName import CalendarName


class CalendarYeka(BaseModel):
    calendarName =models.ForeignKey(CalendarName,on_delete=models.DO_NOTHING)
    startDate=models.DateTimeField(blank=True, null=True,)
    finishDate=models.DateTimeField(blank=True, null=True,)
    is_active=models.BooleanField(default=True)
    competition=models.ForeignKey(YekaCompetition,on_delete=models.CASCADE,null=True,blank=True)
