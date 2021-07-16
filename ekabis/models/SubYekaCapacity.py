from django.db import models

from ekabis.models.ConnectionCapacity import ConnectionCapacity
from ekabis.models.BaseModel import BaseModel
from ekabis.models.Yeka import Yeka


class SubYekaCapacity(BaseModel):
    capacity = models.ForeignKey(ConnectionCapacity, null=True, blank=True, on_delete=models.DO_NOTHING)
    yeka = models.ForeignKey(Yeka, on_delete=models.DO_NOTHING, null=True, blank=True)
