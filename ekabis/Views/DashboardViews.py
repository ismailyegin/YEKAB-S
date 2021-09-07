import traceback

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import resolve
from django.utils.safestring import mark_safe

from ekabis.models import ConnectionRegion, Permission, City, YekaCompetition
from ekabis.models.VacationDay import VacationDay
from ekabis.serializers.YekaSerializer import YekaSerializer
from ekabis.services import general_methods
from ekabis.services.services import ActiveGroupService, GroupService, ActiveGroupGetService, GroupGetService, \
    CalendarNameService, YekaService, VacationDayService, ConnectionRegionService, last_urls, EmployeeGetService, \
    YekaCompetitionService, YekaCompetitionPersonService, YekaGetService

from ekabis.Forms.CalendarNameForm import CalendarNameForm
from ekabis.models.CalendarName import CalendarName
from django.contrib import messages
import datetime

from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from rest_framework.response import Response
from ekabis.services.services import UserGetService


from ekabis.models.BlockEnumField import BlockEnumFields


@login_required
def return_directory_dashboard(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    return render(request, 'anasayfa/federasyon.html',
                  {

                  })


@login_required
def return_personel_dashboard(request):
    active = general_methods.controlGroup(request)
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    calendar_filter = {
        'isDeleted': False,
        'user': request.user
    }

    calendarNames = CalendarNameService(request, calendar_filter)

    user = request.user
    person_filter = {
        'user': user,
    }

    employee = EmployeeGetService(request, person_filter)
    competition_filter = {
        'employee': employee,
    }
    competitions = YekaCompetitionPersonService(request, competition_filter)

    return render(request, 'anasayfa/personel.html',
                  {
                      'calendarNames': calendarNames,'person_competitions':competitions,
                  })


@login_required
def return_admin_dashboard(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    yeka = YekaService(request, None).order_by('-date')
    regions = ConnectionRegionService(request, None)
    days = VacationDayService(request, None)
    # region_json = serializers.serialize("json", ConnectionRegion.objects.all(), cls=DjangoJSONEncoder)
    # yeka_json = serializers.serialize("json",yeka, cls=DjangoJSONEncoder)
    # list_yeka=list(yeka)

    return render(request, 'anasayfa/admin.html', {
        'yeka': yeka,
        # 'region_json': region_json,'yeka_json':yeka_json,
        'regions': regions, 'vacation_days': days,
    })
@login_required
def activeGroup(request, pk):
    activefilter = {
        'user': request.user
    }
    userActive = ActiveGroupGetService(request, activefilter)
    groupfilter = {
        'pk': pk
    }
    group = GroupGetService(request, groupfilter)
    userActive.group = group
    userActive.save()
    if group.name == "Admin":
        return redirect('ekabis:view_admin')

    elif group.name == 'Yonetim':
        return redirect('ekabis:view_federasyon')

    elif group.name == 'Personel':
        return redirect('ekabis:view_personel')
    else:
        return redirect('ekabis:view_admin')


@login_required()
def add_calendarName(request):
    calender_form = CalendarNameForm()

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        with transaction.atomic():
            if request.method == 'POST':
                calender_form = CalendarNameForm(request.POST)
                if calender_form.is_valid():
                    name = calender_form.save(commit=False)
                    name.user = request.user
                    name.save()
            calanders = CalendarName.objects.filter(isDeleted=False)
            return render(request, 'anasayfa/CalendarNameAdd.html',
                          {
                              'calender_form': calender_form,
                              'calanders': calanders, 'urls': urls,
                              'current_url': current_url, 'url_name': url_name
                          })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')


def add_calendar(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.GET['uuid']
                date = request.GET['date']

                datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S'").date()

                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})


            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})
@login_required
def api_connection_region_cities(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']
                yekafilter = {
                    'uuid': uuid
                }
                yeka = YekaGetService(request, yekafilter)
                cities=City.objects.filter(connectionregion__id__in=yeka.connection_region.all().values_list('pk'))
                cities = serializers.serialize("json", cities, cls=DjangoJSONEncoder)
                return JsonResponse({'status': 'Success', 'msg': 'İşlem Başarılı', 'cities': cities})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})




@login_required
def api_connection_region_competitions(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                yeka=None
                competitions= {}

                if request.POST['uuid']:
                    uuid = request.POST['uuid']
                    yekafilter = {
                    'uuid': uuid
                    }
                    yeka = YekaGetService(request, yekafilter)
                if request.POST['plateNo']:
                    if City.objects.filter(plateNo=request.POST['plateNo']):
                        city=City.objects.get(plateNo=request.POST['plateNo'])
                        if yeka:
                            regions=yeka.connection_region.filter(cities=city,isDeleted=False).distinct().values_list('id', flat=True)
                        else:
                            regions=ConnectionRegion.objects.filter(cities=city,isDeleted=False).distinct().values_list('id', flat=True)
                        competitions=YekaCompetition.objects.filter(connectionregion__id__in=regions,isDeleted=False).distinct()

                competitions = serializers.serialize("json", competitions, cls=DjangoJSONEncoder)
                return JsonResponse({'status': 'Success', 'msg': 'İşlem Başarılı', 'competitions': competitions})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})