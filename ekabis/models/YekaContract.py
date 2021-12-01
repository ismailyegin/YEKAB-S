
from django.db import models

from ekabis.models import ConnectionUnit, Company, Yeka, YekaCompetition
from ekabis.models.YekaCompany import YekaCompany
from ekabis.models.BaseModel import BaseModel
from ekabis.models.YekaBussiness import YekaBusiness
from ekabis.models.YekaBusinessBlog import YekaBusinessBlog
from ekabis.models.YekaApplicationFile import YekaApplicationFile
from ekabis.models.YekaApplicationFileName import YekaApplicationFileName

class YekaContract(BaseModel):

    necesssary_choices = (
        (True, 'Evet '),
        (False, 'Hayır')
    )
    business = models.OneToOneField(YekaBusiness, on_delete=models.DO_NOTHING)
    yekabusinessblog = models.ForeignKey(YekaBusinessBlog, on_delete=models.DO_NOTHING)
    contract=models.FileField(null=True,blank=True)
    price=models.DecimalField(null=True,blank=True,max_digits=20,decimal_places=2)
    unit=models.ForeignKey(ConnectionUnit,on_delete=models.DO_NOTHING,null=True,blank=True)
    company=models.ForeignKey(Company,on_delete=models.DO_NOTHING, null=True,blank=True)

