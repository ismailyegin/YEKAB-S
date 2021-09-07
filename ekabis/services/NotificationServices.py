import traceback
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import redirect
from django.utils.safestring import mark_safe

from ekabis.models import Notification, NotificationUser
from ekabis.services.services import YekaGetService


def yeka_added(request, id):
    try:
        with transaction.atomic():
            filter = {
                'pk': id
            }
            yeka = YekaGetService(request, filter)
            notification = Notification()
            url = redirect('ekabis:view_yeka_detail', yeka.uuid).url
            html = '<a style="color:black;" href="' + url + '">' + str(id) + '</a> id li  YEKA  eklenmiştir.'
            notification.description = mark_safe(html)
            notification.title = 'YEKA Ekleme'
            notification.save()

            admins = User.objects.filter(groups__name='Admin')
            for user in admins:
                user_not = NotificationUser()
                user_not.notification = notification
                user_not.user = user
                user_not.save()

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')



