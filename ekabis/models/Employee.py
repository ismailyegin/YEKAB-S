from random import choices

from django.contrib.auth.models import User
from django.db import models

from sbs.models import CategoryItem
from sbs.models.License import License
from sbs.models.Level import Level
from sbs.models.Person import Person
from sbs.models.Communication import Communication


class Employee(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, db_column='person')
    communication = models.OneToOneField(Communication, on_delete=models.CASCADE, db_column='communication')
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='user')
    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)
    workDefinition = models.ForeignKey(CategoryItem, on_delete=models.DO_NOTHING)
    kobilid = models.IntegerField(null=True, blank=True, default=1)

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

    class Meta:
        ordering = ['pk']
        default_permissions = ()
