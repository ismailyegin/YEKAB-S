from django.db import models
from sbs.models.Category import Category
from sbs.models.Judge import Judge
from sbs.models.CompetitionAges import CompetitionAges

class Competition(models.Model):
    TURKEY = 0
    WORLD = 1
    OLYMPIAD = 2
    EUROPE = 3

    COMPGENERALTYPE = (
        (TURKEY, 'Türkiye'),
        (WORLD, 'Dünya'),
        (OLYMPIAD, 'Olimpiyat'),
        (EUROPE, 'Avrupa')
    )

    INTERUNIVERSITY = 0
    INTERSCHOOL = 1
    PERSONAL = 2
    COMPTYPE = (
        (INTERUNIVERSITY, 'Üniversiteler Arası'),
        (INTERSCHOOL, 'Okullar Arası'),
        (PERSONAL, 'Ferdi'),
    )
    compType = models.IntegerField(db_column='compType', blank=True, null=True,
                                   choices=COMPTYPE)  # Field name made lowercase.
    creationDate = models.DateTimeField(db_column='creationDate', blank=True, null=True, auto_now_add=True)
    # Field name made lowercase.
    operationDate = models.DateTimeField(db_column='operationDate', blank=True, null=True,
                                         auto_now_add=True)  # Field name made lowercase.

    finishDate = models.DateTimeField(db_column='finishDate', blank=True, null=True)  # Field name made lowercase.
    startDate = models.DateTimeField(db_column='startDate', blank=True, null=True)  # Field name made lowercase.

    registerStartDate = models.DateTimeField(db_column='registerStartDate', blank=True,
                                             null=True)  # Field name made lowercase.
    registerFinishDate = models.DateTimeField(db_column='registerFinishDate', blank=True,
                                              null=True)  # Field name made lowercase.
    name = models.CharField(max_length=255, blank=True, null=True)
    eventPlace = models.CharField(db_column='eventPlace', max_length=45, blank=True,
                                  null=True)  # Field name made lowercase.
    eskimi = models.BooleanField(default=True)
    explanation = models.CharField(max_length=20, blank=True, null=True)
    compGeneralType = models.IntegerField(db_column='compGeneralType', blank=True, null=True, choices=COMPGENERALTYPE)

    categoryies = models.ManyToManyField(Category)
    ages = models.ManyToManyField(CompetitionAges)
    judges = models.ManyToManyField(Judge)


    def __str__(self):
        return '%s ' % self.name

    # class Meta:
    #     default_permissions = ()
