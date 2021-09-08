from django.contrib.auth.models import User
from django.db import models

from ekabis.models.Person import Person
from ekabis.models.Communication import Communication
from ekabis.models.BaseModel import BaseModel


class CompanyUser(BaseModel):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, null=True, blank=True)
    communication = models.OneToOneField(Communication, on_delete=models.CASCADE, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    authorization_period_start = models.DateField(blank=True, null=True)
    authorization_period_finish = models.DateField(blank=True, null=True)

    class Meta:
        default_permissions = ()

    def __str__(self):
        return '%s ' % self.person.user.get_full_name()
