from django.contrib.auth.models import User
from django.db import models

from ekabis.models.Person import Person
from ekabis.models.Communication import Communication
from ekabis.models.BaseModel import BaseModel


class CompanyUser(BaseModel):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    communication = models.OneToOneField(Communication, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    class Meta:
        default_permissions = ()
