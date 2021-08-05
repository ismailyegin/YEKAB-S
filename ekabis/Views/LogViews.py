import traceback
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import resolve

from ekabis.Forms.UserSearchForm import UserSearchForm
from ekabis.models import Permission
from ekabis.services import general_methods
from ekabis.services.services import LogsService, last_urls


@login_required
def return_log(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    logs = None
    user_form = UserSearchForm()
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        with transaction.atomic():
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
                    logs = LogsService(request, None).order_by('-id')
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

                    logs = LogsService(request, query).order_by('-id')

            return render(request, 'Log/Logs.html', {'logs': logs, 'user_form': user_form,'urls': urls, 'current_url': current_url, 'url_name': url_name})
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
