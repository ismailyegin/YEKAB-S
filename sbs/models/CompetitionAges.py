from django.db import models


class CompetitionAges(models.Model):
    year = models.IntegerField(blank=False, null=False)
    def __str__(self):
        return '%s ' % self.year