import traceback

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from ekabis.Forms.CommunicationForm import CommunicationForm
from ekabis.Forms.CompanyForm import CompanyForm
from ekabis.services import general_methods
from ekabis.services.services import CategoryItemService, CompanyService


@login_required
def return_add_Company(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    company_form = CompanyForm()
    communication_form = CommunicationForm()
    try:
        with transaction.atomic():
            if request.method == 'POST':

                company_form = CompanyForm(request.POST, request.FILES)
                communication_form = CommunicationForm(request.POST, request.FILES)
                if company_form.is_valid():
                    communication = communication_form.save(commit=False)
                    communication.save()
                    company = company_form.save(commit=False)
                    company.communication = communication
                    company.save()
                    messages.success(request, 'Firma Kayıt Edilmiştir.')
                    return redirect('ekabis:view_company')
                else:
                    messages.warning(request, 'Alanları Kontrol Ediniz')

            return render(request, 'Company/Company.html',
                          {'company_form': company_form, 'communication_form': communication_form,
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_company')


@login_required
def delete_company(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']

                companyfilter = {
                    'uuid': uuid
                }
                obj = CompanyService(request, companyfilter).first()
                obj.delete()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})


            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def return_list_Company(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    company_form = CompanyService(request, None)
    return render(request, 'Company/Companys.html',
                  {'company_form': company_form})


@login_required
def return_update_Company(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    companyfilter = {
        'uuid': uuid

    }
    company = CompanyService(request, companyfilter).first()
    company_form = CompanyForm(request.POST or None, instance=company)
    communication_form = CommunicationForm(request.POST or None, instance=company.communication)
    try:
        with transaction.atomic():
            if request.method == 'POST':

                if company_form.is_valid():
                    communication = communication_form.save(commit=False)
                    communication.save()
                    company = company_form.save(commit=False)
                    company.communication = communication
                    company.save()

                    messages.success(request, 'Firma Güncellenmiştir.')
                else:
                    messages.warning(request, 'Alanları Kontrol Ediniz')
            return render(request, 'Company/CompanyUpdate.html',
                          {'company_form': company_form,
                           'communication_form': communication_form,
                           'company': company,

                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:change_company', uuid)
