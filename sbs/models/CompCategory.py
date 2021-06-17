from django.db import models

from sbs.models.GrupForReport import GrupForReport
from sbs.models.Competition import Competition


class CompCategory(models.Model):
    athletegroup = models.CharField(db_column='athleteGroup', max_length=255, blank=True,
                                    null=True)  # Field name made lowercase.
    creationdate = models.DateTimeField(db_column='creationDate', blank=True, null=True)  # Field name made lowercase.
    kobilid = models.IntegerField(db_column='kobilId')  # Field name made lowercase.
    operationdate = models.DateTimeField(db_column='operationDate', blank=True, null=True)  # Field name made lowercase.
    sex = models.IntegerField(blank=True, null=True)
    competition = models.ForeignKey(Competition, models.SET_NULL, db_column='competition', blank=True, null=True)
    startdate = models.CharField(db_column='startDate', max_length=45, blank=True,
                                 null=True)  # Field name made lowercase.
    name = models.CharField(max_length=45, blank=True, null=True)
    starttime = models.CharField(db_column='startTime', max_length=45, blank=True,
                                 null=True)  # Field name made lowercase.
    grupforreport = models.ForeignKey(GrupForReport, models.DO_NOTHING, db_column='grupForReport', blank=True,
                                      null=True)  # Field name made lowercase.

    def __str__(self):
        return '%s' % (self.name)
    # class Meta:
    #     db_table = 'compcategory'
    #     managed = False
