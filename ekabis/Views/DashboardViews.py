import traceback

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect

from ekabis.models import ConnectionRegion
from ekabis.models.VacationDay import VacationDay
from ekabis.services import general_methods
from ekabis.services.services import ActiveGroupService, GroupService, ActiveGroupGetService, GroupGetService, \
    CalendarNameService, YekaService, VacationDayService, ConnectionRegionService

from ekabis.Forms.CalendarNameForm import CalendarNameForm
from ekabis.models.CalendarName import CalendarName
from django.contrib import messages
import datetime

from ekabis.services.services import UserGetService

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



    calendar_filter={
        'isDeleted' : False,
        'user' : request.user
    }

    calendarNames=CalendarNameService(request,calendar_filter)

    return render(request, 'anasayfa/personel.html',
                  {
                      'calendarNames':calendarNames
                  })


@login_required
def return_admin_dashboard(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    yeka = YekaService(request, None)
    filter={
        'pk':1
    }
    regions = ConnectionRegionService(request,None)
    days = VacationDayService(request, filter)

    return render(request, 'anasayfa/admin.html', {
        'yeka': yeka,
        'regions': regions, 'vacation_days': days
    })


@login_required
def activeGroup(request, pk):
    activefilter={
        'user':request.user
    }
    userActive = ActiveGroupGetService(request,activefilter)
    groupfilter={
        'pk':pk
    }
    group = GroupGetService(request,groupfilter)
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
    calender_form=CalendarNameForm()

    try:
        with transaction.atomic():
            if request.method == 'POST':
                  calender_form = CalendarNameForm(request.POST)
                  if calender_form.is_valid():
                      name=calender_form.save(commit=False)
                      name.user=request.user
                      name.save()
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
    calanders=CalendarName.objects.filter(isDeleted=False)

    return render(request, 'anasayfa/CalendarNameAdd.html',
                  {
                      'calender_form':calender_form,
                      'calanders':calanders
                  })



def add_calendar(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.GET['uuid']
                date=request.GET['date']

                datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S'").date()


                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})


            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})