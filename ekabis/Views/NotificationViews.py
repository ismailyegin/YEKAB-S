import datetime
import traceback

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render

from ekabis.models import NotificationUser
from ekabis.serializers.NotificationUserSerializers import NotificationUserSerializer


def get_notification(request):
    try:

        user = request.user
        notifications = NotificationUser.objects.filter(is_seen=False, user=user)

        for notification in notifications:
            notification.is_seen = True
            notification.save()

        data = NotificationUserSerializer(notifications, many=True)

        responseData = dict()
        responseData['notifications'] = data.data

        return JsonResponse(responseData, safe=True)

    except Exception as e:

        return JsonResponse({'status': 'Fail', 'msg': e})


def view_notification(request):
    try:

        user = request.user
        notifications = NotificationUser.objects.filter(user=user).order_by('-creationDate')
        return render(request, 'notification/notification.html', {'notifications': notifications})
    except Exception as e:

        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


def is_read(request,id):
    notification = NotificationUser.objects.get(pk=id)
    if not notification.is_read:
        notification.is_read = True
        notification.read_date=datetime.date.today()
        notification.save()
    return redirect('ekabis:bildirimler')