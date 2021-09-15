from django.db import models

from ekabis.models import YekaCompetition
from ekabis.models.ConnectionRegion import ConnectionRegion
from ekabis.models.Yeka import Yeka
from ekabis.models.Company import Company
from ekabis.models.BaseModel import BaseModel
from ekabis.models.CompetitionApplication import CompetitionApplication
from ekabis.models.YekaApplicationFile import YekaApplicationFile


class YekaCompany(BaseModel):
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(null=True, blank=True, default=True)
    files = models.ManyToManyField(YekaApplicationFile)
    # price=models.DecimalField(null=True,blank=True,max_digits=20,decimal_places=2)
    yeka = models.ForeignKey(Yeka, on_delete=models.CASCADE, null=True, blank=True)
    connection_region = models.ForeignKey(ConnectionRegion, on_delete=models.CASCADE, null=True, blank=True)
    competition = models.ForeignKey(YekaCompetition, on_delete=models.CASCADE, null=True, blank=True)
    application = models.ForeignKey(CompetitionApplication, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '%s ' % self.company.name
