from django.db import models

from ekabis.models.ConnectionRegion import ConnectionRegion
from ekabis.models.BaseModel import BaseModel
from ekabis.models.Yeka import Yeka


class YekaConnectionRegion(BaseModel):
    connectionRegion = models.ForeignKey(ConnectionRegion, null=True, blank=True, on_delete=models.DO_NOTHING)
    yeka = models.ForeignKey(Yeka, on_delete=models.DO_NOTHING, null=True, blank=True)
