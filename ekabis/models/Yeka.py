from django.db import models


from ekabis.models.ConnectionUnit import ConnectionUnit
from ekabis.models.BaseModel import BaseModel
from ekabis.models.YekaBussiness import YekaBusiness

class Yeka(BaseModel):
    definition = models.CharField(blank=True, null=True, max_length=250)
    date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    capacity = models.IntegerField(blank=True, null=True)
    yekaParent = models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)
    unit = models.ForeignKey(ConnectionUnit, on_delete=models.DO_NOTHING, null=True, blank=True)
    is_parent = models.BooleanField(default=False, null=True, blank=True)
    business = models.ForeignKey(YekaBusiness, on_delete=models.CASCADE,null=True,blank=True)
