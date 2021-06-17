from django.contrib.auth.models import User
from django.db import models


class Logs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Üye Rolü', db_column='user')
    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=150, null=True)
    ip = models.CharField(max_length=20, null=True)

    def __str__(self):
        return '%s ' % self.user.get_full_name()

    # class Meta:
    #     default_permissions = ()
