import traceback
from idlelib.help import HelpText

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Sum, Count, Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import resolve
from django.utils.safestring import mark_safe

from ekabis.models import ConnectionRegion, Permission, City, YekaCompetition, HelpMenu, YekaAccept, Yeka, \
    YekaCompetitionEskalasyon_eskalasyon, YekaCompetitionEskalasyon
from ekabis.models.VacationDay import VacationDay
from ekabis.models.YekaContract import YekaContract
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
    yekas = YekaService(request, None).order_by('-date')
    comp_array = []


    days = VacationDayService(request, None)

    res_count = yekas.filter(type='Rüzgar').count()
    ges_count = yekas.filter(type='Güneş').count()
    biyo_count = yekas.filter(type='Biyokütle').count()
    jeo_count = yekas.filter(type='Jeotermal').count()
    user = request.user
    person_filter = {
        'person__user': user,
    }

    employee = EmployeeGetService(request, person_filter)
    competition_filter = {
        'employee': employee,
    }
    competition_array=[]
    all_yeka=[]
    competitions = YekaCompetitionPersonService(request, competition_filter)
    for competition in  competitions:
        competition_array.append(competition.competition.pk)
    for yeka in yekas:
        yeka_dict = dict()
        yeka_all_dict = dict()
        regions = yeka.connection_region.filter(isDeleted=False).filter(yekacompetition__pk__in=competition_array)
        region_all = yeka.connection_region.filter(isDeleted=False)
        if regions:
            yeka_dict['yeka'] = yeka
            yeka_dict['regions'] = regions
            comp_array.append(yeka_dict)
        yeka_all_dict['yeka'] = yeka
        yeka_all_dict['regions'] = region_all
        all_yeka.append(yeka_all_dict)

    return render(request, 'anasayfa/personel.html',
                  {'res_count': res_count, 'yeka': yekas, 'vacation_days': days,
                   'ges_count': ges_count,'comp_array':comp_array,'all_yeka':all_yeka,
                   'jeo_count': jeo_count, 'biyo_count': biyo_count,'person_comp':competition_array,
                   'calendarNames': calendarNames, 'person_competitions': competitions,
                   })
@login_required
def return_yonetici_dashboard(request):
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
    yekas = YekaService(request, None).order_by('-date')
    comp_array = []

    for yeka in yekas:
        yeka_dict = dict()
        competitions = []
        regions = yeka.connection_region.filter(isDeleted=False)
        for region in regions:
            for comp in region.yekacompetition.filter(isDeleted=False):
                competitions.append(comp)
        yeka_dict['yeka'] = yeka
        yeka_dict['regions'] = regions
        comp_array.append(yeka_dict)
    days = VacationDayService(request, None)

    res_count = yekas.filter(type='Rüzgar').count()
    ges_count = yekas.filter(type='Güneş').count()
    biyo_count = yekas.filter(type='Biyokütle').count()
    jeo_count = yekas.filter(type='Jeotermal').count()
    user = request.user
    person_filter = {
        'person__user': user,
    }

    employee = EmployeeGetService(request, person_filter)
    competition_filter = {
        'employee': employee,
    }
    competitions = YekaCompetitionPersonService(request, competition_filter)

    return render(request, 'anasayfa/yonetici-anasayfa.html',
                  {'res_count': res_count, 'yeka': yekas, 'vacation_days': days,
                   'ges_count': ges_count,'yekas':comp_array,
                   'jeo_count': jeo_count, 'biyo_count': biyo_count,
                   'calendarNames': calendarNames, 'person_competitions': competitions,
                   })

@login_required
def return_admin_dashboard(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)

    yekas = YekaService(request, None).order_by('-date')
    comp_array = []

    for yeka in yekas:
        yeka_dict = dict()
        competitions = []
        regions = yeka.connection_region.filter(isDeleted=False)
        for region in regions:
            for comp in region.yekacompetition.filter(isDeleted=False):
                competitions.append(comp)
        yeka_dict['yeka'] = yeka
        yeka_dict['regions'] = regions
        comp_array.append(yeka_dict)
    res_count = yekas.filter(type='Rüzgar').count()
    ges_count = yekas.filter(type='Güneş').count()
    biyo_count = yekas.filter(type='Biyokütle').count()
    jeo_count = yekas.filter(type='Jeotermal').count()

    regions = ConnectionRegionService(request, None)
    days = VacationDayService(request, None)

    # region_json = serializers.serialize("json", ConnectionRegion.objects.all(), cls=DjangoJSONEncoder)
    # yeka_json = serializers.serialize("json",yeka, cls=DjangoJSONEncoder)
    # list_yeka=list(yeka)

    yeka_acccepts = YekaAccept.objects.filter(isDeleted=False)

    installedPower_array = []
    currentPower_array = []
    yeka_capacity_array = []
    company_array = []

    calendar_filter = {
        'isDeleted': False,
        'user': request.user
    }
    total_capacity = 0
    calendarNames = CalendarNameService(request, calendar_filter)
    # for yeka_accept in yeka_acccepts:
    #     accept_dict = dict()
    #     currentPower_dict = dict()
    #     yeka_capacity_dict = dict()
    #     company_dict = dict()
    #     competition = YekaCompetition.objects.get(business=yeka_accept.business)
    #     accept_dict['label'] = competition.name
    #     total = yeka_accept.accept.filter(isDeleted=False).aggregate(Sum('installedPower'))
    #     currentPower = yeka_accept.accept.filter(isDeleted=False).aggregate(Sum('currentPower'))
    #     if total['installedPower__sum'] is None:
    #         total['installedPower__sum'] = 0
    #     if currentPower['currentPower__sum'] is None:
    #         currentPower['currentPower__sum'] = 0
    #     accept_dict['power'] = total['installedPower__sum']
    #     currentPower_dict['power'] = currentPower['currentPower__sum']
    #     currentPower_dict['label'] = competition.name
    #     if total['installedPower__sum'] != None:
    #         total_capacity += float(total['installedPower__sum'])
    #     if currentPower['currentPower__sum'] != None:
    #         total_capacity += float(currentPower['currentPower__sum'])
    #
    #     if Yeka.objects.filter(connection_region__yekacompetition=competition):
    #         current_yeka = Yeka.objects.get(connection_region__yekacompetition=competition)
    #         yeka_capacity_dict['label'] = current_yeka.definition
    #         yeka_capacity_dict['remaining_capacity'] = current_yeka.capacity - total_capacity
    #         yeka_capacity_dict['total'] = current_yeka.capacity
    #         yeka_capacity_dict['capacity'] = total_capacity
    #         yeka_capacity_array.append(yeka_capacity_dict)
    #     currentPower_array.append(currentPower_dict)
    #     installedPower_array.append(accept_dict)
    #     accept_company = competition.company
    #     company_dict['electrical_power'] = currentPower['currentPower__sum']
    #     contract = YekaContract.objects.filter(business=competition.business)
    #     if contract:
    #         if contract[0].company:
    #             company_dict['contract'] = YekaContract.objects.get(business=competition.business)
    #         else:
    #             company_dict['contract'] = None
    #     else:
    #         company_dict['contract'] = None
    #     company_dict['mechanical_power'] = total['installedPower__sum']
    #     company_dict['competition'] = competition
    #     if YekaCompetitionEskalasyon.objects.filter(competition=competition):
    #         company_dict['price'] = YekaCompetitionEskalasyon.objects.get(competition=competition)
    #     else:
    #         company_dict['price'] = None
    #     company_array.append(company_dict)

    return render(request, 'anasayfa/admin.html', {
        'yeka': yekas,
        # 'region_json': region_json,'yeka_json':yeka_json,
        'regions': regions, 'vacation_days': days,
        'res_count': res_count, 'accepts': installedPower_array, 'yeka_capacity': yeka_capacity_array,
        'ges_count': ges_count, 'current_power': currentPower_array,'yekas':comp_array,
        'jeo_count': jeo_count, 'calendarNames': calendarNames, 'company_accepts': company_array,
        'biyo_count': biyo_count, 'urls': urls, 'current_url': current_url, 'url_name': url_name
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
                    name = calender_form.save(request, commit=False)
                    name.user = request.user
                    name.save()
            calenders = CalendarName.objects.filter(isDeleted=False)
            return render(request, 'anasayfa/CalendarNameAdd.html',
                          {
                              'calender_form': calender_form,
                              'calanders': calenders, 'urls': urls,
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
                array = []
                yeka = YekaGetService(request, yekafilter)
                cities = City.objects.filter(connectionregion__id__in=yeka.connection_region.all().values_list('pk'))
                cities = serializers.serialize("json", cities, cls=DjangoJSONEncoder)
                regions = serializers.serialize("json", yeka.connection_region.all(), cls=DjangoJSONEncoder)
                array.append(cities)
                array.append(regions)
                return JsonResponse({'status': 'Success', 'msg': 'İşlem Başarılı', 'cities': array})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def api_yeka_by_type(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                type = request.POST['type']

                regions = ConnectionRegion.objects.filter(yeka__type=type).values('cities__plateNo').annotate(
                    count=Count('cities__id'))
                array = []
                for region in regions:
                    yeka_dict = dict()
                    yeka_dict['city'] = region['cities__plateNo']
                    yeka_dict['count'] = region['count']
                    array.append(yeka_dict)

                return JsonResponse({'status': 'Success', 'msg': 'İşlem Başarılı', 'yeka_type_cities': array})
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
                yeka = None
                competitions = {}

                if request.POST['uuid']:
                    uuid = request.POST['uuid']
                    yekafilter = {
                        'uuid': uuid
                    }
                    yeka = YekaGetService(request, yekafilter)
                if request.POST['plateNo']:
                    if City.objects.filter(plateNo=request.POST['plateNo']):
                        city = City.objects.get(plateNo=request.POST['plateNo'])
                        if yeka:
                            regions = yeka.connection_region.filter(cities=city,
                                                                    isDeleted=False).distinct().values_list('id',
                                                                                                            flat=True)
                        else:
                            regions = ConnectionRegion.objects.filter(cities=city,
                                                                      isDeleted=False).distinct().values_list('id',
                                                                                                              flat=True)
                        competitions = YekaCompetition.objects.filter(competition_regions__id__in=regions,
                                                                      isDeleted=False).distinct()

                competitions = serializers.serialize("json", competitions, cls=DjangoJSONEncoder)
                return JsonResponse({'status': 'Success', 'msg': 'İşlem Başarılı', 'competitions': competitions})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


def success_initial_data(request):
    return render(request, 'anasayfa/initial_data_success.html')


def error_initial_data(request):
    return render(request, 'anasayfa/initial_data_error.html')
