from django.db import models
from ekabis.models import  Employee, YekaCompetition
from ekabis.models.BaseModel import BaseModel


class YekaCompetitionPersonHistory(BaseModel):

    competition = models.ForeignKey(YekaCompetition, on_delete=models.DO_NOTHING, verbose_name='competition')
    person = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, verbose_name='personel')
    is_active = models.BooleanField(default=False)