from builtins import print, set, property, int
from datetime import timedelta, datetime
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

from ekabis.Forms.UserSearchForm import UserSearchForm
from ekabis.services import general_methods
from ekabis.models.Logs import Logs



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