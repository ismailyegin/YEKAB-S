from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from ekabis.Forms.CommunicationForm import CommunicationForm
from ekabis.Forms.GroupForm import GroupForm

from ekabis.services import general_methods

from django.contrib.auth.models import Group, Permission, User


@login_required
def add_group(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    group_form = GroupForm()

    if request.method == 'POST':
        company_form = GroupForm(request.POST, request.FILES)
        communication_form = CommunicationForm(request.POST, request.FILES)
        if company_form.is_valid():
            communication = communication_form.save(commit=False)
            communication.save()
            company = company_form.save(commit=False)
            company.communication = communication
            company.save()

            messages.success(request, 'Grup Kayıt Edilmiştir.')
            return redirect('ekabis:group-list')
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')
    return render(request, 'Group/GrupEkle.html',
                  {'group_form': group_form, })


@login_required
def return_list_group(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    groups = Group.objects.all()
    return render(request, 'Group/GrupListe.html',
                  {'groups': groups})









@login_required
def return_update_group(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    groups = Group.objects.get(pk=pk)
    group_form = GroupForm(request.POST or None, instance=groups)
    if request.method == 'POST':
        if group_form.is_valid():
            group_form.save()
            messages.success(request, 'Grup Güncellenmiştir.')
            return redirect('ekabis:view_group')

        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'Group/grupGuncelle.html',
                  {'group_form': group_form,
                   })
