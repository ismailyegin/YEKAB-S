import traceback
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import resolve
from unicode_tr import unicode_tr
from ekabis.Forms.CommunicationForm import CommunicationForm
from ekabis.Forms.CompanyFileNameForm import CompanyFileNameForm
from ekabis.Forms.CompanyForm import CompanyForm
from ekabis.Forms.CompanyFormDinamik import CompanyFormDinamik
from ekabis.Forms.PersonForm import PersonForm
from ekabis.Forms.UserForm import UserForm
from ekabis.models import Company, YekaCompany, ConsortiumCompany, Person, Employee
from ekabis.models.CompanyFileNames import CompanyFileNames
from ekabis.models.CompanyFiles import CompanyFiles
from ekabis.models.CompanyUser import CompanyUser
from ekabis.services import general_methods
from ekabis.services.general_methods import get_error_messages
from ekabis.services.services import CompanyService, CompanyGetService, GroupService, GroupGetService, \
    CompanyFileNamesService, CompanyFileNamesGetService, YekaCompanyService, last_urls


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

                    company_user.save()
                    company = company_form.save(communication, company_user)
                    company.save()

                    # kullanici kayıt olunca gruba eklenmesi yoksa  açılmasi gerekli
                    groupfilter = {
                        'name': 'Firma'
                    }

                    if GroupService(request, groupfilter):
                        group = GroupGetService(request, groupfilter)
                        user.groups.add(group)
                        user.save()
                    else:
                        group = Group(
                            name='firma'
                        )
                        group.save()
                        user.groups.add(group)
                        user.save()
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
                obj = CompanyGetService(request, companyfilter)
                yeka_company = {
                    'company': obj,
                    'isDeleted': False
                }
                company = YekaCompanyService(request, yeka_company)
                if not company:
                    obj.isDeleted = True
                    obj.save()
                else:
                    return JsonResponse({'status': 'Fail', 'messages': 'Bu Firma Silemezsiniz'})
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})


            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def return_list_Company(request):
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    return render(request, 'Company/Companys.html', {'urls': urls, 'current_url': current_url, })


@login_required
def return_update_Company(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    companyfilter = {
        'uuid': uuid

    }
    urls = last_urls(request)
    current_url = resolve(request.path_info)

    try:
        company = CompanyGetService(request, companyfilter)
        company_form = CompanyForm(request.POST or None, instance=company)
        communication_form = CommunicationForm(request.POST or None, instance=company.communication)
        person_form = PersonForm(request.POST or None, request.FILES or None, instance=company.companyuser.person)
        user_form = UserForm(request.POST or None, instance=company.companyuser.user)
        companyDocumentName = CompanyFileNames.objects.all()
        with transaction.atomic():
            if request.method == 'POST':

                if request.FILES.get('documanfile') and request.POST.get('documanname'):
                    companyfile = CompanyFiles(
                        file=request.FILES.get('documanfile'),
                        filename_id=request.POST.get('documanname')
                    )
                    companyfile.save()
                    company.files.add(companyfile)
                    company.save()
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
                                   'person_form': person_form, 'user_form': user_form,
                                   'companyDocumentName': companyDocumentName, 'urls': urls,
                                   })

        return render(request, 'Company/CompanyUpdate.html',
                      {'company_form': company_form,
                       'communication_form': communication_form,
                       'company': company, 'error_messages': '',
                       'person_form': person_form,
                       'user_form': user_form, 'urls': urls, 'current_url': current_url,
                       'companyDocumentName': companyDocumentName

                       })

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_company')


@login_required
def add_companyfilename(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    company_form = CompanyFileNameForm()

    try:
        if request.method == 'POST':
            with transaction.atomic():
                company_form = CompanyFileNameForm(request.POST)

                if company_form.is_valid():
                    company_form.save()
                    messages.success(request, 'Döküman İsim Eklenmiştir.')
                    return redirect('ekabis:view_companyfilename')
                else:
                    error_messages = get_error_messages(company_form)
                    return render(request, 'Company/CompanyFileNameAdd.html',
                                  {'company_form': company_form,
                                   'error_messages': error_messages
                                   })

        return render(request, 'Company/CompanyFileNameAdd.html',
                      {'company_form': company_form,

                       })

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_company')
    return render(request, 'Company/CompanyFileNameAdd.html')


@login_required
def view_companyfilename(request):
    companyNameList = CompanyFileNamesService(request, None)
    return render(request, 'Company/CompanyFileNameList.html', {'companyNameList': companyNameList})


@login_required
def change_companyfilename(request, uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        company_name_filter = {
            'uuid': uuid
        }
        names = CompanyFileNamesGetService(request, company_name_filter)
        company_form = CompanyFileNameForm(request.POST or None, instance=names)
        if request.method == 'POST':
            with transaction.atomic():

                if company_form.is_valid():
                    company_form.save()
                    messages.success(request, 'Döküman İsim Eklenmiştir.')
                    return redirect('ekabis:view_companyfilename')
                else:
                    error_messages = get_error_messages(company_form)
                    return render(request, 'Company/CompanyFileNameUpdate.html',
                                  {'company_form': company_form,
                                   'error_messages': error_messages
                                   })

        return render(request, 'Company/CompanyFileNameUpdate.html',
                      {'company_form': company_form,
                       })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_companyfilename')


@login_required
def delete_companyfilename(request, uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']
                company_name_filter = {
                    'uuid': uuid
                }
                obj = CompanyFileNamesGetService(request, company_name_filter)
                log = str(obj.name) + " firma dokuman  silindi"
                log = general_methods.logwrite(request, request.user, log)

                obj.isDeleted = True
                obj.save()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


    except Exception as e:

        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')

        return redirect('ekabis:view_companyfilename')


@login_required
def add_consortium(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    company_form = CompanyFormDinamik()
    communication_form = CommunicationForm()

    company = {
        'isDeleted': False
    }
    companies = CompanyService(request, company)
    try:
        with transaction.atomic():
            if request.method == 'POST':

                company_form = CompanyFormDinamik(request.POST, request.FILES)
                communication_form = CommunicationForm(request.POST, request.FILES)

                if company_form.is_valid() and communication_form:
                    communication = communication_form.save(commit=False)
                    communication.save()

                    company = company_form.save(communication, None)
                    company.save()
                    company.is_consortium = True
                    company.save()

                    messages.success(request, 'Konsorsiyum Kayıt Edilmiştir.')
                    return redirect('ekabis:view_consortium')
                else:
                    error_message_company = get_error_messages(company_form)
                    error_messages_communication = get_error_messages(communication_form)

                    error_messages = error_messages_communication + error_message_company
                    return render(request, 'Company/AddConsortiumCompany.html',
                                  {'company_form': company_form, 'communication_form': communication_form,
                                   'error_messages': error_messages, })

            return render(request, 'Company/AddConsortiumCompany.html',
                          {'company_form': company_form, 'communication_form': communication_form,
                           'form': company_form, 'companies': companies,
                           'error_messages': ''})
    except Exception as e:
        print(e)
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_consortium')


@login_required
def view_consortium(request):
    company = {
        'is_consortium': 'True'
    }
    consortium = CompanyService(request, company)
    return render(request, 'Company/ConsortiumList.html', {'companies': consortium})


@login_required
def return_update_consortium(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    companyfilter = {
        'uuid': uuid,
        'isDeleted': False

    }

    try:
        company = CompanyGetService(request, companyfilter)
        filter = {
            'isDeleted': False,

        }
        consortium = ConsortiumCompany.objects.filter(isDeleted=False, company=company)
        companies = CompanyService(request, filter)
        company_form = CompanyForm(request.POST or None, instance=company)
        communication_form = CommunicationForm(request.POST or None, instance=company.communication)
        companyDocumentName = CompanyFileNames.objects.all()
        employess = Employee.objects.filter(user__groups__name='firma', isDeleted=False)
        with transaction.atomic():
            if request.method == 'POST':

                list = request.POST['consortium_list']
                consortium_list = list.split(',')
                for list in consortium_list:
                    consortium_id = list.split('&')[0]
                    consortium_percent = list.split('&')[1]
                    filter = {
                        'uuid': consortium_id
                    }
                    new = ConsortiumCompany(consortium=CompanyGetService(request, filter), company=company,
                                            percent=int(consortium_percent))
                    new.save()

                if request.FILES.get('documanfile') and request.POST.get('documanname'):
                    companyfile = CompanyFiles(
                        file=request.FILES.get('documanfile'),
                        filename_id=request.POST.get('documanname')
                    )
                    companyfile.save()
                    company.files.add(companyfile)
                    company.save()
                if company_form.is_valid() and communication_form.is_valid():
                    communication = communication_form.save(commit=False)
                    communication.save()
                    company = company_form.save(commit=False)
                    company.communication = communication
                    company.save()

                    messages.success(request, 'Firma Güncellenmiştir.')

                else:
                    error_message_company = get_error_messages(company_form)
                    error_messages_communication = get_error_messages(communication_form)
                    error_messages = error_messages_communication + error_message_company
                    return render(request, 'Company/UpdateConsortium.html',
                                  {'company_form': company_form,
                                   'communication_form': communication_form,
                                   'company': company, 'error_messages': error_messages,
                                   'companyDocumentName': companyDocumentName, 'companies': companies,
                                   'consortium': consortium, 'employess': employess,
                                   })

        return render(request, 'Company/UpdateConsortium.html',
                      {'company_form': company_form,
                       'communication_form': communication_form,
                       'company': company, 'error_messages': '',
                       'companies': companies, 'employess': employess,
                       'companyDocumentName': companyDocumentName, 'consortium': consortium,

                       })

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_consortium')
