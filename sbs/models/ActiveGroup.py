from random import choices

from django.contrib.auth.models import User, Group
from django.db import models


class ActiveGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='aktivUser')
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, verbose_name='aktivGroup')

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)
