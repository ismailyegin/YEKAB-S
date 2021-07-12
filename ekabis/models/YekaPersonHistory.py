from django.db import models

from ekabis.models import Yeka, Employee
from ekabis.models.BaseModel import BaseModel


class YekaPersonHistory(BaseModel):
    yeka = models.ForeignKey(Yeka, on_delete=models.CASCADE, verbose_name='aktifYeka')
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, verbose_name='aktifPerson')
    is_active = models.BooleanField(default=False)
