from builtins import print, set, property, int
from datetime import timedelta, datetime
from operator import attrgetter
from os import name

from django.db.models.functions import Lower

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

from sbs.Forms.BeltForm import BeltForm
from sbs.Forms.CategoryItemForm import CategoryItemForm
from sbs.Forms.CommunicationForm import CommunicationForm
from sbs.Forms.DisabledCommunicationForm import DisabledCommunicationForm
from sbs.Forms.DisabledPersonForm import DisabledPersonForm
from sbs.Forms.DisabledUserForm import DisabledUserForm
from sbs.Forms.LicenseForm import LicenseForm
from sbs.Forms.LicenseFormAntrenor import LicenseFormAntrenor
from sbs.Forms.UserForm import UserForm
from sbs.Forms.PersonForm import PersonForm
from sbs.Forms.UserSearchForm import UserSearchForm
from sbs.Forms.SearchClupForm import SearchClupForm
from sbs.models import Athlete, CategoryItem, Person, Communication, License, SportClubUser, SportsClub, City, Country, \
    Coach, CompAthlete, Competition
from sbs.models.EnumFields import EnumFields
from sbs.models.Level import Level
from sbs.services import general_methods

from sbs.models.Logs import Logs

from accounts.models import Forgot

# page
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# from sbs.models.simplecategory import simlecategory

from sbs.models.PreRegistration import PreRegistration
from sbs.models.ReferenceReferee import ReferenceReferee
from sbs.models.ReferenceCoach import ReferenceCoach


@login_required
def return_log(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    logs = Logs.objects.none()
    user_form = UserSearchForm()
    if request.method == 'POST':

        user_form = UserSearchForm(request.POST)
        firstName = request.POST.get('first_name')
        lastName = request.POST.get('last_name')
        email = request.POST.get('email')
        playDate = request.POST.get('playDate')
        finishDate = request.POST.get('finishDate')

        if playDate:
            playDate = datetime.strptime(playDate, '%d/%m/%Y').date()

        if finishDate:
            finishDate = datetime.strptime(finishDate, "%d/%m/%Y").date()

        if not (firstName or lastName or email or playDate or finishDate):
            logs = Logs.objects.all().order_by('-creationDate')

        else:
            query = Q()
            if lastName:
                query &= Q(user__last_name__icontains=lastName)
            if firstName:
                query &= Q(user__first_name__icontains=firstName)
            if email:
                query &= Q(user__email__icontains=email)
            if playDate:
                query &= Q(creationDate__gte=playDate)
            if finishDate:
                query &= Q(creationDate__lt=finishDate)

            logs = Logs.objects.filter(query).order_by('-creationDate')

    return render(request, 'Log/Logs.html', {'logs': logs, 'user_form': user_form})