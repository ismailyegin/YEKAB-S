from django.db import models

from ekabis.models import YekaCompetition
from ekabis.models.ProgressReport import ProgressReport
from ekabis.models.BaseModel import BaseModel



class YekaProgressReport(BaseModel):
    competition = models.OneToOneField(YekaCompetition, on_delete=models.DO_NOTHING)
    progressReport = models.ManyToManyField(ProgressReport)
