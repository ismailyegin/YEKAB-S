from itertools import combinations

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from sbs.Forms.CompetitionForm import CompetitionForm
from sbs.Forms.CompetitionSearchForm import CompetitionSearchForm
from django.db.models import Q
from sbs.models import SportClubUser, SportsClub, Competition, Athlete, CompAthlete, Weight
from sbs.models.SimpleCategory import SimpleCategory
from sbs.models.EnumFields import EnumFields
from sbs.services import general_methods
from sbs.Forms.SimplecategoryForm import SimplecategoryForm
from sbs.models.Activity import Activity
from sbs.Forms.ActivityForm import ActivityForm

from datetime import date, datetime
from django.utils import timezone



@login_required
def return_activity(request):

    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    comquery = CompetitionSearchForm()
    activity = Activity.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        startDate = request.POST.get('startDate')
        compType = request.POST.get('compType')
        compGeneralType = request.POST.get('compGeneralType')
        if name or startDate or compType or compGeneralType:
            query = Q()
            if name:
                query &= Q(name__icontains=name)
            if startDate:
                query &= Q(startDate__year=int(startDate))

            activity = Activity.objects.filter(query).distinct()
        else:
            activity = Activity.objects.all()
    return render(request, 'faliyet/faaliyetler.html', {'activity': activity, 'query': comquery})


@login_required
def faliyet_ekle(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    competition_form = ActivityForm()
    if request.method == 'POST':
        competition_form = ActivityForm(request.POST)
        if competition_form.is_valid():
            competition_form.save()
            log = str(request.POST.get('name')) + " faliyeti sisteme ekledi"
            log = general_methods.logwrite(request, request.user, log)

            messages.success(request, 'Faaliyet Başarıyla Kaydedilmiştir.')

            return redirect('sbs:faaliyet')
        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'faliyet/faliyet-ekle.html',
                  {'competition_form': competition_form})


@login_required
def faaliyet_sil(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = Activity.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Competition.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def faliyet_duzenle(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    activity = Activity.objects.get(pk=pk)
    competition_form = ActivityForm(request.POST or None, instance=activity)
    if request.method == 'POST':

        if competition_form.is_valid():
            competition_form.save()

            log = str(request.POST.get('name')) + " faliyeti guncelledi"
            log = general_methods.logwrite(request, request.user, log)

            messages.success(request, 'Faaliyet Başarıyla Güncellenmiştir.')

            return redirect('sbs:faaliyet')
        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'faliyet/faaliyet-guncelle.html',
                  {'competition_form': competition_form, 'competition': activity})
