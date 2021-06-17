from django.db import models


class Category(models.Model):
    kategoriid = models.IntegerField(primary_key=True)
    kategoriadi = models.CharField(max_length=20, blank=True, null=True)
    erkek = models.IntegerField(blank=True, null=True)
    bayan = models.IntegerField(blank=True, null=True)
    sayi = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '%s ' % self.kategoriadi
