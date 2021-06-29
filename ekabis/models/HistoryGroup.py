from django.contrib.auth.models import Group, User
from django.db import models


class HistoryGroup(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, db_column='grup')
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='user')

    def __str__(self):
        return '%s %s %s' % (self.user.first_name, self.user.last_name, self.group)
