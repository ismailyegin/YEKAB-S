from django.db import models

from sbs.models.Competition import Competition


class GrupForReport(models.Model):
    centerreferee = models.CharField(db_column='centerReferee', max_length=255, blank=True,
                                     null=True)  # Field name made lowercase.
    compdoctor = models.CharField(db_column='compDoctor', max_length=255, blank=True,
                                  null=True)  # Field name made lowercase.
    creationdate = models.DateTimeField(db_column='creationDate', blank=True, null=True)  # Field name made lowercase.
    jurymemberfour = models.CharField(db_column='juryMemberFour', max_length=255, blank=True,
                                      null=True)  # Field name made lowercase.
    jurymemberone = models.CharField(db_column='juryMemberOne', max_length=255, blank=True,
                                     null=True)  # Field name made lowercase.
    jurymemberthree = models.CharField(db_column='juryMemberThree', max_length=255, blank=True,
                                       null=True)  # Field name made lowercase.
    jurymembertwo = models.CharField(db_column='juryMemberTwo', max_length=255, blank=True,
                                     null=True)  # Field name made lowercase.
    jurypresident = models.CharField(db_column='juryPresident', max_length=255, blank=True,
                                     null=True)  # Field name made lowercase.
    kobilid = models.IntegerField(db_column='kobilId')  # Field name made lowercase.
    marshallone = models.CharField(db_column='marshallOne', max_length=255, blank=True,
                                   null=True)  # Field name made lowercase.
    marshalltwo = models.CharField(db_column='marshallTwo', max_length=255, blank=True,
                                   null=True)  # Field name made lowercase.
    name = models.CharField(max_length=255, blank=True, null=True)
    operationdate = models.DateTimeField(db_column='operationDate', blank=True, null=True)  # Field name made lowercase.
    refereeone = models.CharField(db_column='refereeOne', max_length=255, blank=True,
                                  null=True)  # Field name made lowercase.
    refereetwo = models.CharField(db_column='refereeTwo', max_length=255, blank=True,
                                  null=True)  # Field name made lowercase.
    speaker = models.CharField(max_length=255, blank=True, null=True)
    techcontrollerone = models.CharField(db_column='techControllerOne', max_length=255, blank=True,
                                         null=True)  # Field name made lowercase.
    techcontrollertwo = models.CharField(db_column='techControllerTwo', max_length=255, blank=True,
                                         null=True)  # Field name made lowercase.
    timekeeper = models.CharField(db_column='timeKeeper', max_length=255, blank=True,
                                  null=True)  # Field name made lowercase.
    competition = models.ForeignKey(Competition, on_delete=models.DO_NOTHING, db_column='competition', blank=True,
                                    null=True)

    # class Meta:
    #     db_table = 'grupforreport'
