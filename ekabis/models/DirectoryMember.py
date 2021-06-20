from django.contrib.auth.models import User
from django.db import models

from sbs.models.DirectoryCommission import DirectoryCommission
from sbs.models.DirectoryMemberRole import DirectoryMemberRole
from sbs.models.Person import Person
from sbs.models.Communication import Communication


class DirectoryMember(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    communication = models.OneToOneField(Communication, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)
    role = models.ForeignKey(DirectoryMemberRole, on_delete=models.CASCADE, verbose_name='Üye Rolü')
    commission = models.ForeignKey(DirectoryCommission, on_delete=models.DO_NOTHING, verbose_name='Kurulu')

    oldpk = models.IntegerField(null=True, blank=True)

    # class Meta:
    #     default_permissions = ()
