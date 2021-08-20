from django.db import models
from ekabis.models.BaseModel import BaseModel
from ekabis.models.Company import Company


class CompetitionCompany(BaseModel):

    price=models.DecimalField(null=True,blank=True,max_digits=20,decimal_places=2)
    company=models.ForeignKey(Company,on_delete=models.CASCADE,null=False,blank=False)
