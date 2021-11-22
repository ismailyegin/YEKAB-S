import datetime
import traceback
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import resolve

from ekabis.Forms.ExtraTimeFileForm import ExtraTimeFileForm
from ekabis.Forms.ExtraTimeForm import ExtraTimeForm
from ekabis.Views.VacationDayViews import is_vacation_day
from ekabis.models import YekaBusiness, YekaCompetition, Permission, Logs
from ekabis.models.ExtraTime import ExtraTime
from ekabis.models.VacationDay import VacationDay
from ekabis.models.Yeka import Yeka
from ekabis.models.YekaBusinessBlog import YekaBusinessBlog
from ekabis.services import general_methods
from ekabis.services.general_methods import get_error_messages, get_client_ip
from ekabis.services.services import ExtraTimeService, ExtraTimeGetService, ExtraTimeFileGetService, last_urls, \
    YekaCompetitionGetService


@login_required
def return_add_extra_time(request, business, businessblog):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        yekabusiness = YekaBusiness.objects.get(uuid=business)
        yekabussinessblog = YekaBusinessBlog.objects.get(uuid=businessblog)

        competition = YekaCompetition.objects.get(business=yekabusiness)


        name = ''
        if Yeka.objects.filter(business=yekabusiness):
            name = Yeka.objects.get(business=yekabusiness).definition
        elif YekaCompetition.objects.filter(business=yekabusiness):
            name = YekaCompetition.objects.get(business=yekabusiness).name
        name = general_methods.yekaname(competition.business)
        # if ExtraTime.objects.filter(yekabusinessblog=yekabussinessblog):
        #      return redirect('ekabis:change_extratime', ExtraTime.objects.get(yekabusinessblog=yekabussinessblog).uuid)
        extratime_form = ExtraTimeForm()
        extra_times = ExtraTime.objects.filter(yekabusinessblog=yekabussinessblog)
        with transaction.atomic():
            if request.method == 'POST':

                extratime = ExtraTime(user=request.user, time=1, business=yekabusiness,
                                      yekabusinessblog=yekabussinessblog)
                extratime.save()
                extratime_form = ExtraTimeForm(request.POST,instance=extratime)
                if extratime_form.is_valid():
                    extratime = extratime_form.save(request, commit=False)
                    extratime.user = request.user
                    extratime.yekabusinessblog = yekabussinessblog
                    extratime.business = yekabusiness
                    extratime.save()
                    main = yekabussinessblog

                    dependence_blocks = YekaBusinessBlog.objects.filter(dependence_parent=yekabussinessblog)
                    for dependence_block in dependence_blocks:
                            add_time_next(yekabussinessblog.pk, dependence_block.pk, competition,extratime.time,yekabussinessblog)
                    messages.success(request, 'Ek Süre Kayıt Edilmiştir.')
                    return redirect('ekabis:view_yeka_competition_detail',competition.uuid)
                else:
                    error_messages = get_error_messages(extratime_form)
                    return render(request, 'ExtraTime/add_extratime.html',
                                  {'extratime_form': extratime_form,
                                   'error_messages': error_messages, 'urls': urls, 'current_url': current_url,
                                   'url_name': url_name, 'name': name,
                                   })

            return render(request, 'ExtraTime/add_extratime.html',
                          {'extratime_form': extratime_form,
                           'business': business, 'extra_times': extra_times,
                           'yekabussinessblog': yekabussinessblog, 'urls': urls, 'current_url': current_url,
                           'url_name': url_name, 'name': name
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yekabusinessBlog', business.uuid)

def add_time_next(parent_id, current_id, yeka,time,sabit):
    parent_block = YekaBusinessBlog.objects.get(pk=parent_id)
    current_block = YekaBusinessBlog.objects.get(pk=current_id)

    start_date = parent_block.startDate
    if parent_block.businessTime:
        if sabit.pk==current_block.pk:
            time = parent_block.businessTime + int(time)
        else:
            time = int(time)
    else:
        return redirect('ekabis:view_yeka_competition_detail', yeka.uuid)
    time_type = parent_block.time_type
    if time_type == 'is_gunu':
        add_time = time
        count = 0
        while add_time > 1:
            start_date = start_date + datetime.timedelta(days=1)
            count = count + 1
            is_vacation = is_vacation_day(start_date)
            if not is_vacation:
                add_time = add_time - 1
    else:
        start_date = start_date + datetime.timedelta(days=time) - datetime.timedelta(days=1)
    current_block.startDate = start_date
    current_block.save()
    dependence_blocks = YekaBusinessBlog.objects.filter(dependence_parent=current_block)
    for dependence_block in dependence_blocks:
        add_time_next(current_block.pk, dependence_block.pk, yeka,time,sabit)

@login_required
def return_list_extra_time(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    ExtraTimefilter = {
        'isDeleted': False

    }
    ekstratime = []
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    for item in ExtraTimeService(request, ExtraTimefilter).order_by('-creationDate'):
        if Yeka.objects.filter(business=item.business):
            time = {
                'yeka': Yeka.objects.get(business=item.business).definition,
                'blogname': item.yekabusinessblog.businessblog.name,
                'time': item.time,
                'uuid': item.uuid,

            }


        elif YekaCompetition.objects.filter(business=item.business):
            time = {
                'yeka': YekaCompetition.objects.get(business=item.business).name,
                'blogname': item.yekabusinessblog.businessblog.name,
                'time': item.time,
                'uuid': item.uuid,

            }
        else:
            time = {
                'yeka': None,
                'blogname': item.yekabusinessblog.businessblog.name,
                'time': item.time,
                'uuid': item.uuid,
            }
        ekstratime.append(time)
    return render(request, 'ExtraTime/view_extratime.html',
                  {'ekstratime': ekstratime, 'urls': urls, 'current_url': current_url, 'url_name': url_name})


@login_required
def return_update_extra_time(request, uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    extra_time_filter = {
        'uuid': uuid
    }
    extratime = ExtraTimeGetService(request, extra_time_filter)

    extratime_form = ExtraTimeForm(request.POST or None, instance=extratime)
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        with transaction.atomic():
            if request.method == 'POST':
                if extratime_form.is_valid():
                    extra = extratime_form.save(request, commit=False)
                    extra.save()
                    messages.success(request, 'Ek Süre Güncellenmiştir')
                    return redirect('ekabis:view_extratime')
                else:
                    error_messages = get_error_messages(extratime_form)
                    return render(request, 'ExtraTime/change_extratime.html',
                                  {'extratime_form': extratime_form,
                                   'error_messages': error_messages, 'urls': urls, 'current_url': current_url,
                                   'url_name': url_name

                                   })

            return render(request, 'ExtraTime/change_extratime.html',
                          {'extratime_form': extratime_form, 'urls': urls, 'current_url': current_url,
                           'url_name': url_name

                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required
def delete_extra_time(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']

                extra_time_filter = {
                    'uuid': uuid
                }
                obj = ExtraTimeGetService(request, extra_time_filter)
                times = ExtraTime.objects.filter(yekabusinessblog=obj.yekabusinessblog).order_by('-creationDate')
                if times:
                    time = times[0]
                main = obj.yekabusinessblog
                while main != None:
                    if YekaBusinessBlog.objects.filter(parent=main, isDeleted=False):
                        parent = YekaBusinessBlog.objects.get(parent=main, isDeleted=False)
                        if not parent.indefinite:

                            if time.time_type == 'is_gunu':
                                after_day = (parent.startDate.date() + datetime.timedelta(days=obj.time)).strftime(
                                    "%d/%m/%Y")

                                delete_time = time.time
                                start_date = parent.startDate.date()
                                finish_date = parent.finisDate.date() - timedelta(days=time.time)
                                finish_time = time.time
                                count = 0
                                while delete_time > 0:
                                    start_date = start_date + datetime.timedelta(days=-1)
                                    count = count + 1
                                    is_vacation = is_vacation_day(start_date)
                                    if not is_vacation:
                                        delete_time = delete_time - 1
                                while is_vacation_day(finish_date) == True:
                                    finish_date = finish_date - datetime.timedelta(days=-1)

                                parent.startDate = start_date
                                parent.finisDate = finish_date
                                parent.save()
                                main = parent
                            else:
                                parent.startDate = parent.startDate.date() - timedelta(days=time.time)
                                parent.finisDate = parent.finisDate.date() - timedelta(days=time.time)
                                parent.save()
                                main = parent
                        else:
                            # süresiz ise işlem yapılmayacaktır.
                            main = None
                    else:
                        main = None

                obj.isDeleted = True
                obj.save()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})


            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def add_extratimefile(request, uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        extra_filter = {
            'uuid': uuid
        }
        extratime = ExtraTimeGetService(request, extra_filter)
        extratime_form = ExtraTimeFileForm()
        if Yeka.objects.filter(business=extratime.business):
            yeka = Yeka.objects.get(business=extratime.business)
        elif YekaCompetition.objects.filter(business=extratime.business):
            yeka = YekaCompetition.objects.get(business=extratime.business)

        else:
            yeka = None
        with transaction.atomic():
            if request.method == 'POST':
                extratime_form = ExtraTimeFileForm(request.POST, request.FILES)
                if extratime_form.is_valid():
                    time = extratime_form.save(request,commit=False)
                    time.save()
                    extratime.files.add(time)
                    extratime.save()

                    messages.success(request, 'Ek Süreye Dosya  Kayıt Edilmiştir.')
                    return redirect('ekabis:view_extratime')
                else:
                    error_messages = get_error_messages(extratime_form)
                    return render(request, 'ExtraTime/add_extratimefile.html',
                                  {'extratime_form': extratime_form,
                                   'error_messages': error_messages,
                                   'extratime': extratime,
                                   'yeka': yeka, 'urls': urls, 'current_url': current_url, 'url_name': url_name
                                   })

            return render(request, 'ExtraTime/add_extratimefile.html',
                          {
                              'extratime_form': extratime_form,
                              'extratime': extratime, 'urls': urls, 'current_url': current_url, 'url_name': url_name,
                              'yeka': yeka,

                          })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')


@login_required
def change_extratimefile(request, uuid, time):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        extra_filter = {
            'uuid': time
        }
        extratime = ExtraTimeGetService(request, extra_filter)
        if Yeka.objects.filter(business=extratime.business):
            yeka = Yeka.objects.get(business=extratime.business)
        elif YekaCompetition.objects.filter(business=extratime.business):
            yeka = YekaCompetition.objects.get(business=extratime.business)
        else:
            yeka = None
        extratimefile_filter = {
            'uuid': uuid
        }
        extratimefile = ExtraTimeFileGetService(request, extratimefile_filter)
        extratime_form = ExtraTimeFileForm(request.POST or None, request.FILES or None, instance=extratimefile)
        with transaction.atomic():
            if request.method == 'POST':
                if extratime_form.is_valid():
                    time = extratime_form.save(request,commit=False)
                    time.save()
                    extratime.files.add(time)
                    extratime.save()
                    messages.success(request, 'Ek Süreye Dosya  Kayıt Edilmiştir.')
                    return redirect('ekabis:view_extratime')
                else:
                    error_messages = get_error_messages(extratime_form)
                    return render(request, 'ExtraTime/change_extratimefile.html',
                                  {'extratime_form': extratime_form,
                                   'error_messages': error_messages,
                                   'extratime': extratime,
                                   'yeka': yeka, 'urls': urls, 'current_url': current_url, 'url_name': url_name
                                   })

            return render(request, 'ExtraTime/change_extratimefile.html',
                          {
                              'extratime_form': extratime_form,
                              'extratime': extratime,
                              'yeka': yeka, 'urls': urls, 'current_url': current_url, 'url_name': url_name
                          })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')


@login_required
def delete_extratimefile(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']

                extra_time_filter = {
                    'uuid': uuid
                }
                data_as_json_pre = serializers.serialize('json', ExtraTime.objects.filter(uuid=uuid))
                obj = ExtraTimeFileGetService(request, extra_time_filter)
                obj.isDeleted = True
                obj.save()
                log = "Ek süre silindi."
                logs = Logs(user=request.user, subject=log, ip=get_client_ip(request), previousData=data_as_json_pre)
                logs.save()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})
