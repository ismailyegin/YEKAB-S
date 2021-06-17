from django.db import models


class Weight(models.Model):
    creationdate = models.DateTimeField(db_column='creationDate', blank=True, null=True)  # Field name made lowercase.
    kobilid = models.IntegerField(db_column='kobilId')  # Field name made lowercase.
    operationdate = models.DateTimeField(db_column='operationDate', blank=True, null=True)  # Field name made lowercase.
    weight = models.CharField(max_length=255, blank=True, null=True)

    # class Meta:
    #     db_table = 'weight'
