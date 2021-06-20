from builtins import classmethod

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

from sbs.Forms.ClaimForm import ClaimForm
from sbs.services import general_methods
from sbs.models.Claim import Claim
from sbs.Forms.DestekSearchForm import DestekSearchform
from unicode_tr import unicode_tr
from sbs.Forms.UserSearchForm import UserSearchForm

from sbs.models import MenuDirectory, MenuAdmin


@login_required
def return_claim(request):
    perm = general_methods.control_access(request)
    active = general_methods.controlGroup(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    destek_form = DestekSearchform()
    destek = Claim.objects.none()
    user_form = UserSearchForm()
    if request.method == 'POST':
        destek_form = DestekSearchform(request.POST or None)
        status = request.POST.get('status')
        importanceSort = request.POST.get('importanceSort')
        firstName = unicode_tr(request.POST.get('first_name')).upper()
        lastName = unicode_tr(request.POST.get('last_name')).upper()

        if not (status or importanceSort):
            if active == 'Admin' or active == 'Arsiv':
                destek = Claim.objects.all()
        else:
            query = Q()
            if status:
                query &= Q(status=status)
            if importanceSort:
                query &= Q(importanceSort=importanceSort)
            if lastName:
                query &= Q(last_name__icontains=lastName)
            if firstName:
                query &= Q(user__first_name__icontains=firstName)

            if active == 'Admin' or active == 'Arsiv':
                destek = Claim.objects.filter(query)

    return render(request, 'Destek/DestekTalepListesi.html',
                  {'claims': destek, 'destek_form': destek_form, 'user_form': user_form, })


@login_required
def claim_add(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    claim_form = ClaimForm()

    if request.method == 'POST':
        claim_form = ClaimForm(request.POST)
        if claim_form.is_valid():
            claimSave = claim_form.save(commit=False)
            claimSave.user = request.user
            claimSave.save()

            messages.success(request, 'Destek Talep  Eklendi.')
            return redirect('sbs:destek-talep-listesi')
        else:
            messages.warning(request, 'Form Bilgilerini Kontrol Ediniz Lütfen .')

    return render(request, 'Destek/Desktek-ekle.html', {'claim_form': claim_form, })


@login_required
def claim_update(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    clain = Claim.objects.get(pk=pk)
    claim_form = ClaimForm(request.POST or None, instance=clain)

    if request.method == 'POST':
        if claim_form.is_valid():
            claim_form.save()
            messages.success(request, 'Destek Talep  Güncellendi.')
            return redirect('sbs:destek-talep-listesi')

    return render(request, 'Destek/Desktek-ekle.html', {'claim_form': claim_form, })


@login_required
def claim_delete(request, pk):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    clain = Claim.objects.get(pk=pk)
    clain.delete()

    messages.success(request, 'Destek Talep  Silindi.')

    return redirect('sbs:destek-talep-listesi')


@login_required
def menu(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    return render(request, 'Destek/Desktek-ekle.html', {})
