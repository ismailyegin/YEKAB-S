
from django.db import models

from sbs.models.Athlete import Athlete
from sbs.models.Competition import Competition
from sbs.models.SimpleCategory import SimpleCategory

class TaoluAthlete(models.Model):
    athlete = models.OneToOneField(Athlete, on_delete=models.CASCADE)
    competition = models.OneToOneField(Competition, on_delete=models.CASCADE)
    categori = models.ManyToManyField(SimpleCategory)

    def __str__(self):
        return '%s %s' % (self.athlete.user.first_name, self.athlete.user.last_name)

    # class Meta:
    #     default_permissions = ()
