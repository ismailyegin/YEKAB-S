from django.db import models

from sbs.models.Competition import Competition
from sbs.models.Category import Category
from sbs.models.CompCategory import CompCategory
from sbs.models.Athlete import Athlete


class CompAthlete(models.Model):
    creationdate = models.DateTimeField(db_column='creationDate', blank=True, null=True)  # Field name made lowercase.
    operationdate = models.DateTimeField(db_column='operationDate', blank=True, null=True)  # Field name made lowercase.
    degree = models.IntegerField(default=0)

    lotno = models.IntegerField(db_column='lotNo', default=0)  # Field name made lowercase.

    sessionno = models.IntegerField(db_column='sessionNo', default=0)  # Field name made lowercase.

    athlete = models.ForeignKey(Athlete, models.DO_NOTHING, db_column='athlete', blank=True, null=True)
    compcategory = models.ForeignKey(CompCategory, models.DO_NOTHING, db_column='compCategory', blank=True,
                                     null=True)  # Field name made lowercase.
    category = models.ForeignKey(Category, models.DO_NOTHING, db_column='category', blank=True, null=True)
    competition = models.ForeignKey(Competition, models.DO_NOTHING, db_column='competition', blank=True, null=True)

    # class Meta:
    #     db_table = 'compathlete'
    #     managed = False
