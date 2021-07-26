from django.db import models




from ekabis.models.Employee import Employee

from ekabis.models.BaseModel import BaseModel
from ekabis.models.Yeka import Yeka


class YekaPerson(BaseModel):
    employee = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.DO_NOTHING)
    yeka = models.ForeignKey(Yeka, on_delete=models.DO_NOTHING, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return '%s ' % self.employee.user.get_full_name()

    task_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return '%s %s %s %s' % (
            self.employee.user.first_name, self.employee.user.last_name, ' - ', self.yeka.definition)

