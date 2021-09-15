from django.db import models

from ekabis.models.Proposal import Proposal
from ekabis.models.YekaCompetition import YekaCompetition
from ekabis.models.BaseModel import BaseModel

#Aday Yekaya ait alt yeka belirlenmesi
class ProposalSubYeka(BaseModel):
    sub_yeka = models.OneToOneField(YekaCompetition, on_delete=models.DO_NOTHING, null=True, blank=True)
    proposal = models.OneToOneField(Proposal, on_delete=models.DO_NOTHING, null=True, blank=True)
