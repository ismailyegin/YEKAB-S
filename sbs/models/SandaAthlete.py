
from django.db import models

from sbs.models.Athlete import Athlete
from sbs.models.Competition import Competition


class SandaAthlete(models.Model):
    athlete = models.OneToOneField(Athlete, on_delete=models.CASCADE)
    competition = models.OneToOneField(Competition, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' % (self.athlete.user.first_name, self.athlete.user.last_name)

    # class Meta:
    #     default_permissions = ()
