from django.contrib.auth.models import User
from django.db import models

from ekabis.models.DirectoryCommission import DirectoryCommission
from ekabis.models.DirectoryMemberRole import DirectoryMemberRole
from ekabis.models.Person import Person
from ekabis.models.Communication import Communication
from ekabis.models.BaseModel import BaseModel


class DirectoryMember(BaseModel):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    communication = models.OneToOneField(Communication, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)
    role = models.ForeignKey(DirectoryMemberRole, on_delete=models.CASCADE, verbose_name='Üye Rolü')
    commission = models.ForeignKey(DirectoryCommission, on_delete=models.DO_NOTHING, verbose_name='Kurulu')


    class Meta:
        default_permissions = ()
