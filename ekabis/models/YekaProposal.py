
from django.db import models
from ekabis.models.Proposal import Proposal
from ekabis.models.BaseModel import BaseModel
from ekabis.models.YekaBussiness import YekaBusiness
from ekabis.models.YekaBusinessBlog import YekaBusinessBlog



class YekaProposal(BaseModel):

    business = models.OneToOneField(YekaBusiness, on_delete=models.CASCADE)
    yekabusinessblog = models.ForeignKey(YekaBusinessBlog, on_delete=models.CASCADE)
    proposal=models.ManyToManyField(Proposal)



    # startDate=models.DateField(null=True, blank=True)
    # finishDate=models.DateField(null=True,blank=True)
    # preRegistration=models.BooleanField(choices=necesssary_choices,default=False)
    #
    # necessary=models.ManyToManyField(YekaApplicationFileName)
    # companys=models.ManyToManyField(YekaCompany)