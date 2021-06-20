from django.db import models

from sbs.models.City import City
from sbs.models.Country import Country


class Communication(models.Model):
    postalCode = models.CharField(max_length=120, null=True, blank=True)
    phoneNumber = models.CharField(max_length=120, null=True, blank=True)
    phoneNumber2 = models.CharField(max_length=120, null=True, blank=True)
    address = models.TextField(blank=True, null=True, verbose_name='Adres')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='İl', db_column='city')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Ülke', db_column='country')
    kobilid = models.IntegerField(null=True, blank=True, default=1)

    class Meta:
        default_permissions = ()
        db_table = 'communication'
        managed = False

