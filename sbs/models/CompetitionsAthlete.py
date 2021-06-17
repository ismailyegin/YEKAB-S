import enum

from django.db import models

from sbs.models.Category import Category
from sbs.models.Coach import Coach
from sbs.models.Athlete import Athlete
from sbs.models.SportsClub import SportsClub
from sbs.models.Competition import Competition


class CompetitionsAthlete(models.Model):
    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)

    coach = models.ForeignKey(Coach, on_delete=models.SET_NULL, null=True)
    athlete = models.ForeignKey(Athlete, on_delete=models.SET_NULL, related_name='athlete',null=True)
    athleteTwo = models.ForeignKey(Athlete, on_delete=models.SET_NULL, related_name='athlete2' , null=True)
    club = models.ForeignKey(SportsClub, on_delete=models.SET_NULL, null=True)
    competition = models.ForeignKey(Competition, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    degree = models.IntegerField(default=0)

    sira = models.IntegerField(blank=True, null=True)
    grupid = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '%s ' % self.coach

    # class Meta:
    #     default_permissions = ()
