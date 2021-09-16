
from django.contrib.auth.models import User, Group
from django.db import models

from ekabis.models.Employee import Employee
from ekabis.models.Yeka import Yeka

from django.db import models
from ekabis.models import Yeka, Employee
from ekabis.models.BaseModel import BaseModel


class YekaPersonHistory(BaseModel):

    yeka = models.ForeignKey(Yeka, on_delete=models.CASCADE, verbose_name='yeka')
    person = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, verbose_name='personel')
    is_active = models.BooleanField(default=False)
