import datetime
import traceback
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import redirect
from django.urls import resolve
from django.utils.safestring import mark_safe

from ekabis.models import Notification, NotificationUser, Permission, YekaCompetition
from ekabis.models.YekaCompetitionPerson import YekaCompetitionPerson
from ekabis.services.services import YekaCompetitionGetService, YekaCompetitionPersonService




def notification(request, html,uuid,type):
    try:
        with transaction.atomic():
            notification = Notification()
            notification.not_description = mark_safe(html)
            url_name = resolve(request.path_info).url_name
            title = Permission.objects.get(codename=url_name)
            notification.title = title.name
            notification.save()
            if type =='yeka_competition':
                filter = {
                    'uuid': uuid
                }
                competition = YekaCompetitionGetService(request, filter)
                filter = {
                    'competition':competition
                }
                yeka_persons = YekaCompetitionPersonService(request, filter)
                for yeka_person in yeka_persons:
                    user_not = NotificationUser()
                    user_not.notification = notification
                    user_not.user = yeka_person.employee.person.user
                    user_not.save()

            admins = User.objects.filter(groups__name='Admin')
            for user in admins:
                user_not_admin = NotificationUser()
                user_not_admin.notification = notification
                user_not_admin.user = user
                user_not_admin.save()

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')



def notification_eskalasyon(html,uuid,type):
    try:
        with transaction.atomic():
            notification = Notification()
            notification.not_description = mark_safe(html)
            title = 'ESKALASYON HESABI - ' + str(datetime.datetime.now())
            notification.title = title
            notification.save()


    except Exception as e:
        traceback.print_exc()
        pass
