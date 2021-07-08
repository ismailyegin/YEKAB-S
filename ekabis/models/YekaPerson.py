from django.db import models

from ekabis.models.Person import Person
from ekabis.models.BaseModel import BaseModel
from ekabis.models.Yeka import Yeka


class YekaPerson(BaseModel):
    person = models.ForeignKey(Person, null=True, blank=True, on_delete=models.DO_NOTHING)
    yeka = models.ForeignKey(Yeka, on_delete=models.DO_NOTHING, null=True, blank=True)
