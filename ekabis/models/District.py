from django.db import models
from ekabis.models.City import City


class District(models.Model):
    name = models.CharField(max_length=250,blank=True, null=True, verbose_name='İlçe')
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return '%s ' % self.name


