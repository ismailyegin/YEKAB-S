from django.db import models
from ekabis.models.BaseModel import BaseModel
from ekabis.models.Company import Company


class CompetitionCompany(BaseModel):
    price=models.DecimalField(null=True,blank=True)
    company=models.ManyToManyField(Company)
