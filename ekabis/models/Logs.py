from django.contrib.auth.models import User
from django.db import models
from ekabis.models.BaseModel import BaseModel

class Logs(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Üye Rolü', db_column='user')
    subject = models.CharField(max_length=150, null=True)
    ip = models.CharField(max_length=20, null=True)
    previousData = models.TextField(null=True, blank=True, verbose_name='Önceki Değer')
    nextData = models.TextField(null=True, blank=True, verbose_name='Sonraki Değer')
    status=models.BooleanField(default=False)

    def __str__(self):
        return '%s ' % self.user.get_full_name()

