import traceback

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from unicode_tr import unicode_tr

from ekabis.Forms.CommunicationForm import CommunicationForm
from ekabis.Forms.CompanyForm import CompanyForm
from ekabis.Forms.CompanyFormDinamik import CompanyFormDinamik
from ekabis.Forms.PersonForm import PersonForm
from ekabis.Forms.UserForm import UserForm
from ekabis.models.CompanyUser import CompanyUser
from ekabis.services import general_methods
from ekabis.services.general_methods import get_error_messages
from ekabis.services.services import CompanyService


@login_required
def return_add_Company(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    company_form = CompanyFormDinamik()
    communication_form = CommunicationForm()
    user_form = UserForm()
    person_form = PersonForm()
    try:
        with transaction.atomic():
            if request.method == 'POST':

                company_form = CompanyFormDinamik(request.POST, request.FILES)
                communication_form = CommunicationForm(request.POST, request.FILES)
                person_form = PersonForm(request.POST, request.FILES)
                user_form = UserForm(request.POST)
                if company_form.is_valid() and communication_form and user_form and person_form:
                    communication = communication_form.save(commit=False)
                    communication.save()

                    user = User()
                    user.username = request.POST.get('email')
                    user.first_name = unicode_tr(request.POST.get('first_name')).upper()
                    user.last_name = unicode_tr(request.POST.get('last_name')).upper()
                    user.email = request.POST.get('email')
                    user.save()

                    person = person_form.save(commit=False)
                    person.save()
                    company_user = CompanyUser(
                        person=person,
                        user=user,
                        communication=communication,
                    )
                    # kullanici kayıt olunca gruba eklenmesi yoksa  açılmasi gerekli

                    company_user.save()
                    company = company_form.save(communication, company_user)
                    company.save()

                    messages.success(request, 'Firma ve Kullanici Kayıt Edilmiştir.')
                    return redirect('ekabis:view_company')
                else:
                    error_message_company = get_error_messages(company_form)
                    error_messages_communication = get_error_messages(communication_form)
                    error_messages_person = get_error_messages(person_form)
                    error_messages_user = get_error_messages(user_form)
                    error_messages = error_messages_communication + error_message_company + error_messages_person + error_messages_user
                    return render(request, 'Company/Company.html',
                                  {'company_form': company_form, 'communication_form': communication_form,
                                   'error_messages': error_messages, })

            return render(request, 'Company/Company.html',
                          {'company_form': company_form, 'communication_form': communication_form, 'form': company_form,
                           'error_messages': '', 'user_form': user_form, 'person_form': person_form})
    except Exception as e:
        print(e)
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
                obj.isDeleted = True
                obj.save()
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
    companyfilter = {
        'isDeleted': False

    }
    company_form = CompanyService(request, companyfilter)
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
    company = CompanyService(request, companyfilter)[0]
    company_form = CompanyForm(request.POST or None, instance=company)
    communication_form = CommunicationForm(request.POST or None, instance=company.communication)
    person_form = PersonForm(request.POST or None,request.FILES or None,  instance=company.companyuser.person)
    user_form = UserForm(request.POST or None, instance=company.companyuser.user)
    try:
        with transaction.atomic():
            if request.method == 'POST':

                if company_form.is_valid() and communication_form.is_valid() and user_form and person_form:
                    communication = communication_form.save(commit=False)
                    communication.save()
                    company = company_form.save(commit=False)
                    company.communication = communication
                    company.save()
                    user_form.save()
                    person_form.save()

                    messages.success(request, 'Firma Güncellenmiştir.')
                else:
                    error_message_company = get_error_messages(company_form)
                    error_messages_communication = get_error_messages(communication_form)
                    error_messages = error_messages_communication + error_message_company
                    return render(request, 'Company/CompanyUpdate.html',
                                  {'company_form': company_form,
                                   'communication_form': communication_form,
                                   'company': company, 'error_messages': error_messages,
                                   'person_form': person_form, 'user_form': user_form
                                   })

        return render(request, 'Company/CompanyUpdate.html',
                      {'company_form': company_form,
                       'communication_form': communication_form,
                       'company': company, 'error_messages': '',
                       'person_form': person_form,
                       'user_form': user_form

                       })

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_company')



@login_required
def add_companyfilename(request):
    return render(request, 'Company/CompanyUpdate.html')

@login_required
def view_companyfilename(request):
    return render(request, 'Company/CompanyUpdate.html')
@login_required
def change_companyfilename(request):
    return render(request, 'Company/CompanyUpdate.html')