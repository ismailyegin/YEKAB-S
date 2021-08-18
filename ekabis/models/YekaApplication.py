
from django.db import models
from ekabis.models.YekaCompany import YekaCompany
from ekabis.models.BaseModel import BaseModel
from ekabis.models.YekaBussiness import YekaBusiness
from ekabis.models.YekaBusinessBlog import YekaBusinessBlog
from ekabis.models.YekaApplicationFile import YekaApplicationFile
from ekabis.models.YekaApplicationFileName import YekaApplicationFileName

class YekaApplication(BaseModel):

    necesssary_choices = (
        (True, 'Evet '),
        (False, 'Hayır')
    )
    business = models.OneToOneField(YekaBusiness, on_delete=models.CASCADE)
    yekabusinessblog = models.ForeignKey(YekaBusinessBlog, on_delete=models.CASCADE)

    startDate=models.DateField(null=True, blank=True)
    finishDate=models.DateField(null=True,blank=True)
    preRegistration=models.BooleanField(choices=necesssary_choices,default=False)

    necessary=models.ManyToManyField(YekaApplicationFileName)
    companys=models.ManyToManyField(YekaCompany)