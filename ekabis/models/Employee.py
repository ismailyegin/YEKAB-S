from random import choices

from django.contrib.auth.models import User
from django.db import models
from ekabis.models.BaseModel import BaseModel

from ekabis.models.Person import Person
from ekabis.models.Communication import Communication
from ekabis.models.CategoryItem import CategoryItem


class Employee(BaseModel):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, db_column='person', null=False, blank=False)
    communication = models.OneToOneField(Communication, on_delete=models.CASCADE, db_column='communication')

    def __str__(self):
        return '%s' % self.person.user.get_full_name()

    class Meta:
        ordering = ['pk']
        default_permissions = ()
