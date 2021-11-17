import calendar
import datetime
import json
import traceback

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import resolve

from ekabis.Forms.VacationDayForm import VacationDayForm
from ekabis.Forms.VacationDayUpdateForm import VacationDayUpdateForm
from ekabis.models import Permission, Logs
from ekabis.models.VacationDay import VacationDay
from ekabis.services import general_methods
from ekabis.services.general_methods import get_error_messages, log, log_model, get_client_ip
from ekabis.services.services import VacationDayService, VacationDayGetService, last_urls


# Adding holidays to be used in the system
@login_required
def add_vacation_day(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    vacation_form = VacationDayForm()
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)

    try:

        with transaction.atomic():
            if request.method == 'POST':
                vacation_form = VacationDayForm(request.POST)

                if vacation_form.is_valid():
                    days = request.POST['reservation']
                    days = days.split('-')
                    start_date = datetime.datetime.strptime(days[0].split(' ')[0], '%d/%m/%Y')
                    end_date = datetime.datetime.strptime(days[1].split(' ')[1], '%d/%m/%Y')

                    range = (end_date - start_date).days

                    while range >= 0:
                        current = VacationDay.objects.filter(definition=vacation_form.cleaned_data['definition'],
                                                             date=start_date)
                        if not current:

                            day = VacationDay()
                            data_as_json_pre = 'Yok'
                            day.definition = vacation_form.cleaned_data['definition']
                            day.date = start_date
                            day.save()
                            data_as_json_next = serializers.serialize('json', VacationDay.objects.filter(uuid=day.uuid))
                            log = log_model(request, data_as_json_pre, data_as_json_next)
                            start_date = start_date + datetime.timedelta(days=1)
                            range = range - 1
                        else:
                            messages.warning(request, '' + str(start_date.date()) + ' tatil günü kayıtlıdır.')
                            start_date = start_date + datetime.timedelta(days=1)
                            range = range - 1

                    messages.success(request, 'Tatil Günü Başarıyla Kayıt Edilmiştir.')
                    return redirect('ekabis:vacation_days')

                else:
                    error_message_unit = get_error_messages(vacation_form)

                    return render(request, 'ExtraTime/add_vacation_day.html',
                                  {'vacation_form': vacation_form, 'error_messages': error_message_unit, 'urls': urls,
                                   'current_url': current_url, 'url_name': url_name})

            return render(request, 'ExtraTime/add_vacation_day.html',
                          {'vacation_form': vacation_form, 'error_messages': '', 'urls': urls,
                           'current_url': current_url, 'url_name': url_name,
                           })

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:vacation_days')


@login_required
def return_vacation_day(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    vacation_form = VacationDayForm()
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)

    filter = {
        'isDeleted': False
    }
    days = VacationDayService(request, filter).order_by('-id')
    return render(request, 'ExtraTime/view_vacation_day.html',
                  {'days': days, 'urls': urls, 'current_url': current_url, 'url_name': url_name})


# Added holiday deletion
@login_required
def delete_vacation_date(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']
                filter = {
                    'uuid': uuid
                }
                obj = VacationDayGetService(request, filter)
                data_as_json_pre = serializers.serialize('json', VacationDay.objects.filter(uuid=uuid))

                obj.isDeleted = True
                obj.save()
                log = str(obj.definition) + " - tatil günü silindi."
                logs = Logs(user=request.user, subject=log, ip=get_client_ip(request), previousData=data_as_json_pre)
                logs.save()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})


            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

    except obj.DoesNotExist:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


# Added holiday update
@login_required
def update_vacation_date(request, uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    filter = {
        'uuid': uuid
    }

    day = VacationDayGetService(request, filter)
    day_as_json_pre = serializers.serialize('json', VacationDay.objects.filter(uuid=uuid))

    vacation_form = VacationDayUpdateForm(request.POST or None, instance=day)

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        with transaction.atomic():
            if request.method == 'POST':

                if vacation_form.is_valid():

                    day.definition = vacation_form.cleaned_data['definition']
                    day.date = vacation_form.cleaned_data['date']
                    day.save()
                    data_as_json_next = serializers.serialize('json', VacationDay.objects.filter(pk=day.pk))
                    log = log_model(request, day_as_json_pre, data_as_json_next)
                    messages.success(request, 'Tatil Günü Güncellenmiştir')
                    return redirect('ekabis:vacation_days')
                else:
                    error_messages = get_error_messages(vacation_form)
                    return render(request, 'ExtraTime/update_vacation_date.html',
                                  {'vacation_form': vacation_form,
                                   'error_messages': error_messages, 'urls': urls, 'current_url': current_url,
                                   'url_name': url_name
                                   })

            return render(request, 'ExtraTime/update_vacation_date.html',
                          {'vacation_form': vacation_form, 'urls': urls, 'current_url': current_url,
                           'url_name': url_name, 'error_messages': ''})
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:vacation_days')


# Query whether the incoming date is a holiday
def is_vacation_day(date):
    vacation_date = VacationDay.objects.filter(isDeleted=False)
    vacation_date_array = []
    for vacation in vacation_date:
        vacation_date_array.append((vacation.date).strftime("%d/%m/%Y"))
    day = calendar.day_name[(date.weekday())]
    if day == 'Saturday' or day == 'Sunday':
        return True
    elif date.strftime("%d/%m/%Y") in vacation_date:
        return True
    else:
        return False
