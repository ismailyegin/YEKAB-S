from django.db import models
from ekabis.models.AssociateDegreeFile import AssociateDegreeFile
from ekabis.models.BaseModel import BaseModel
from ekabis.models.YekaBussiness import YekaBusiness
from ekabis.models.YekaBusinessBlog import YekaBusinessBlog


class YekaAssociateDegree(BaseModel):
    business = models.OneToOneField(YekaBusiness, on_delete=models.CASCADE)
    yekabusinessblog = models.ForeignKey(YekaBusinessBlog, on_delete=models.CASCADE)
    associateDegree = models.ManyToManyField(AssociateDegreeFile)
