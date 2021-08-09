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
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='user', null=False, blank=False)
    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)
    workDefinition = models.ForeignKey(CategoryItem, on_delete=models.DO_NOTHING, null=True, blank=True)
    is_yekaPersonel = models.BooleanField(default=False)

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

    class Meta:
        ordering = ['pk']
        default_permissions = ()
