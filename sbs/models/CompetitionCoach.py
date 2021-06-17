from django.db import models

from sbs.models.Coach import Coach
from sbs.models.Athlete import Athlete
from sbs.models.Competition import Competition


class CompetitionCoach(models.Model):
    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)

    coach = models.ForeignKey(Coach, on_delete=models.SET_NULL, null=True)
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)

    sira = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '%s ' % self.coach

    # class Meta:
    #     default_permissions = ()
