from django.db import models
from ekabis.models.City import City
from ekabis.models.Country import Country
from ekabis.models.BaseModel import BaseModel


class Communication(BaseModel):
    postalCode = models.CharField(max_length=120, null=True, blank=True)
    phoneNumber = models.CharField(max_length=11, null=False, blank=False)
    phoneNumber2 = models.CharField(max_length=11, null=True, blank=True)
    phoneHome = models.CharField(max_length=120, null=True, blank=True)
    phoneJop = models.CharField(max_length=120, null=True, blank=True)
    address = models.TextField(blank=True, null=True, verbose_name='Adres')
    addressHome = models.TextField(blank=True, null=True, verbose_name='AdresHome')
    addressJop = models.TextField(blank=True, null=True, verbose_name='AdresJop')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='İl', db_column='city', null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Ülke', db_column='country', null=True,
                                blank=True)

    town = models.CharField(max_length=120, null=True, blank=True)
    neighborhood = models.CharField(max_length=120, null=True, blank=True)


