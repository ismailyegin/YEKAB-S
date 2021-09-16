from django.db import models
from ekabis.models.BaseModel import BaseModel
from ekabis.models.YekaBussiness import YekaBusiness
from ekabis.models.YekaBusinessBlog import YekaBusinessBlog
from ekabis.models.YekaApplicationFileName import YekaApplicationFileName


class CompetitionApplication(BaseModel):
    necesssary_choices = (
        (True, 'Evet '),
        (False, 'Hayır')
    )
    business = models.OneToOneField(YekaBusiness, on_delete=models.CASCADE)
    yekabusinessblog = models.ForeignKey(YekaBusinessBlog, on_delete=models.CASCADE,null=True,blank=True)
    startDate = models.DateField(null=True, blank=True)
    finishDate = models.DateField(null=True, blank=True)
    preRegistration = models.BooleanField(choices=necesssary_choices, default=False)
    necessary = models.ManyToManyField(YekaApplicationFileName)

