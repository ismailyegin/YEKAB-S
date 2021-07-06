import json
import traceback

from django.core import serializers
from builtins import classmethod

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

from ekabis.Forms.ClaimForm import ClaimForm
from ekabis.services import general_methods
from ekabis.models.Claim import Claim

from ekabis.Forms.DestekSearchForm import DestekSearchform
from unicode_tr import unicode_tr
from ekabis.Forms.UserSearchForm import UserSearchForm
from ekabis.services.general_methods import get_error_messages
from ekabis.services.services import ClaimService


@login_required
def return_claim(request):
    perm = general_methods.control_access(request)
    active = general_methods.controlGroup(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    destek_form = DestekSearchform()
    destek = None
    user_form = UserSearchForm()
    try:
        with transaction.atomic():
            if request.method == 'POST':

                destek_form = DestekSearchform(request.POST or None)
                status = request.POST.get('status')
                importanceSort = request.POST.get('importanceSort')
                firstName = unicode_tr(request.POST.get('first_name')).upper()
                lastName = unicode_tr(request.POST.get('last_name')).upper()
                if not (status or importanceSort):
                    if active == 'Admin':
                        destek = ClaimService(request, None)
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

                    if active == 'Admin':
                        destek = ClaimService(request, query)

            return render(request, 'Destek/DestekTalepListesi.html',
                          {'claims': destek, 'destek_form': destek_form, 'user_form': user_form, })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')


@login_required
def claim_add(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    claim_form = ClaimForm()
    try:
        with transaction.atomic():
            if request.method == 'POST':

                claim_form = ClaimForm(request.POST)
                if claim_form.is_valid():
                    claimSave = claim_form.save(commit=False)
                    claimSave.user = request.user
                    claimSave.save()

                    messages.success(request, 'Destek Talep  Eklendi.')
                    return redirect('ekabis:view_claim')
                else:
                    error_messages = get_error_messages(claim_form)
                    return render(request, 'Destek/Desktek-ekle.html',
                                  {'claim_form': claim_form, 'error_messages': error_messages})
            return render(request, 'Destek/Desktek-ekle.html', {'claim_form': claim_form, 'error_messages': ''})

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')


@login_required
def claim_update(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    clain = Claim.objects.get(uuid=uuid)
    claim_form = ClaimForm(request.POST or None, instance=clain)
    try:
        with transaction.atomic():
            if request.method == 'POST':

                if claim_form.is_valid():
                    claim_form.save()
                    messages.success(request, 'Destek Talep  Güncellendi.')
                    return redirect('ekabis:view_claim')
                else:
                    error_messages = get_error_messages(claim_form)
                    return render(request, 'Destek/Desktek-ekle.html',
                                  {'claim_form': claim_form, 'error_messages': error_messages})

            return render(request, 'Destek/Desktek-ekle.html', {'claim_form': claim_form, 'error_messages': ''})
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')

@login_required
def delete_claim(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']

                claimfilter = {
                    'uuid': uuid
                }
                obj = ClaimService(request, claimfilter).first()
                obj.delete()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})


            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

