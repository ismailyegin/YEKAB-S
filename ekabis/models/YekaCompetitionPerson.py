from django.db import models

from ekabis.models import YekaCompetition
from ekabis.models.Employee import Employee

from ekabis.models.BaseModel import BaseModel
from ekabis.models.Yeka import Yeka


class YekaCompetitionPerson(BaseModel):
    employee = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.DO_NOTHING)
    competition = models.ForeignKey(YekaCompetition, on_delete=models.DO_NOTHING, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    task_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return '%s %s %s ' % (
            self.employee.person.user.first_name, self.employee.person.user.last_name, ' - ')