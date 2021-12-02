import datetime
import traceback

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import resolve

from ekabis.models import NotificationUser, Permission, Notification
from ekabis.serializers.NotificationUserSerializers import NotificationUserSerializer
from ekabis.services import general_methods
from ekabis.services.services import last_urls


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

def read_notification_all(request):
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        user = request.user
        notifications = NotificationUser.objects.filter(is_read=False, user=user).order_by('-creationDate')
        for notification in notifications:
            notification.is_read = True
            notification.read_date = datetime.date.today()
            notification.save()
        return redirect('ekabis:bildirimler')
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


def view_notification(request):
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        user = request.user
        notifications = NotificationUser.objects.filter(user=user).order_by('-creationDate')
        return render(request, 'notification/notification.html', {'notification_all': notifications, 'urls': urls, 'current_url': current_url, 'url_name': url_name.name})
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


@login_required
def make_is_read(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                id = request.POST['id']
                obj = NotificationUser.objects.get(pk=int(id))
                obj.is_read=True
                obj.read_date = datetime.date.today()
                obj.save()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

    except obj.DoesNotExist:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})
