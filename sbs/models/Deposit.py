from django.db import models
from sbs.models.Products import Products
from sbs.models.SportsClub import SportsClub


class Deposit(models.Model):
    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)

    date = models.DateTimeField()
    description = models.CharField(max_length=300, null=True, blank=True)
    count = models.IntegerField(null=True, blank=True)
    delivery = models.CharField(max_length=300, null=True, blank=True)

    club = models.ForeignKey(SportsClub, on_delete=models.SET_NULL, verbose_name='Emanet Kulup', blank=True, null=True)
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, verbose_name='Emanet Malzeme', blank=True,
                                null=True)
