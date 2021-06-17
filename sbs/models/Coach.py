from django.contrib.auth.models import User
from django.db import models

from sbs.models.Level import Level
from sbs.models.Communication import Communication
from sbs.models.Person import Person


class Coach(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    communication = models.OneToOneField(Communication, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grades = models.ManyToManyField(Level, related_name='CoachGrades')
    visa = models.ManyToManyField(Level, related_name='CoachVisa')
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)
    iban = models.CharField(max_length=120, null=True, blank=True, verbose_name='İban Adresi')

    oldpk = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

    # class Meta:
    #     ordering = ['pk']
    #     default_permissions = ()
