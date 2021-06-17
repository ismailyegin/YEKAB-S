from django.db import models
from django.template.defaultfilters import default

from sbs.models.SportClubUser import SportClubUser
from sbs.models.Coach import Coach
from sbs.models.Communication import Communication


class SportsClub(models.Model):
    IsFormal = (
        (True, 'Spor Kulubü'),
        (False, 'Diger(Özel Salon-Dojo-Sportif Dernek)'),
    )

    name = models.CharField(blank=True, null=True, max_length=120)
    shortName = models.CharField(blank=True, null=True, max_length=120)
    foundingDate = models.CharField(blank=True, null=True, max_length=120)
    clubMail = models.CharField(blank=True, null=True, max_length=120)
    logo = models.ImageField(upload_to='club/', null=True, blank=True, verbose_name='Kulüp Logo')
    communication = models.OneToOneField(Communication, on_delete=models.CASCADE, db_column='communication', null=True,
                                         blank=True)
    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)
    coachs = models.ManyToManyField(Coach)
    isFormal = models.BooleanField(default=True, choices=IsFormal)
    clubUser = models.ManyToManyField(SportClubUser)
    dataAccessControl = models.BooleanField(blank=True, null=True, default=False)
    password = models.CharField(blank=True, null=True, max_length=120)
    username = models.CharField(blank=True, null=True, max_length=120)
    isRegister = models.BooleanField(default=False)
    petition = models.FileField(upload_to='club/', null=True, blank=True, verbose_name='Yetki Belgesi ')

    def __str__(self):
        return '%s' % (self.name)

    # class Meta:
    #     default_permissions = ()
    #     db_table = 'sportclub'
    #     managed = False
