import traceback
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core import serializers
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import resolve
from unicode_tr import unicode_tr

from ekabis.Forms.UserFormCompany import UserFormCompany
from ekabis.Forms.CommunicationForm import CommunicationForm
from ekabis.Forms.CompanyFileNameForm import CompanyFileNameForm
from ekabis.Forms.CompanyForm import CompanyForm
from ekabis.Forms.CompanyFormDinamik import CompanyFormDinamik
from ekabis.Forms.CompanyUserForm import CompanyUserForm
from ekabis.Forms.PersonForm import PersonForm
from ekabis.Forms.UserForm import UserForm
from ekabis.models import Company, YekaCompany, ConsortiumCompany, Person, Employee, Permission, Logs
from ekabis.models.CompanyFileNames import CompanyFileNames
from ekabis.models.CompanyFiles import CompanyFiles
from ekabis.models.CompanyUser import CompanyUser
from ekabis.models.Settings import Settings
from ekabis.services import general_methods
from ekabis.services.general_methods import get_error_messages, log_model, get_client_ip
from ekabis.services.services import CompanyService, CompanyGetService, GroupService, GroupGetService, \
    CompanyFileNamesService, CompanyFileNamesGetService, YekaCompanyService, last_urls, UserService


@login_required
# Adding a new company to the system
def return_add_Company(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    company_form = CompanyFormDinamik()
    communication_form = CommunicationForm()
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        with transaction.atomic():
            if request.method == 'POST':

                company_form = CompanyFormDinamik(request.POST,
                                                  request.FILES)  # Dynamically added file form of the company
                communication_form = CommunicationForm(request.POST, request.FILES)  # Company contact information form
                if company_form.is_valid() and communication_form.is_valid():
                    communication = communication_form.save(request, commit=False)
                    communication.save()

                    company = company_form.save(request, communication)
                    company.save()

                    # if Settings.objects.filter(key='mail_companyuser'):
                    #     if Settings.objects.get(key='mail_companyuser').is_active:
                    #         general_methods.sendmail(request, user)
                    # else:
                    #     set = Settings(key='mail_companyuser')
                    #     set.is_active = False
                    #     set.save()
                    messages.success(request, 'Firma Kayıt Edilmiştir.')
                    return redirect('ekabis:view_company')
                else:
                    # Error messages returned from the form
                    error_message_company = get_error_messages(company_form)
                    error_messages_communication = get_error_messages(communication_form)

                    error_messages = error_messages_communication + error_message_company
                    return render(request, 'Company/Company.html',
                                  {'company_form': company_form, 'communication_form': communication_form,
                                   'urls': urls, 'url_name': url_name.name,
                                   'error_messages': error_messages, })

            return render(request, 'Company/Company.html',
                          {'company_form': company_form, 'communication_form': communication_form,
                           'error_messages': '', 'urls': urls, 'current_url': current_url, 'url_name': url_name.name})
    except Exception as e:
        print(e)
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_company')


@login_required
# delete the company in the system
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
                data_as_json_pre = serializers.serialize('json', Company.objects.filter(uuid=uuid))
                yeka_company = {
                    'company': obj,
                    'isDeleted': False
                }
                company = YekaCompanyService(request, yeka_company)
                if not company:
                    obj.isDeleted = True
                    obj.save()
                    log = "Firma Sil"
                    logs = Logs(user=request.user, subject=log, ip=get_client_ip(request),
                                previousData=data_as_json_pre)
                    logs.save()
                else:
                    return JsonResponse({'status': 'Fail', 'messages': 'Bu Firma Silemezsiniz'})
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})


            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
# listing companies in the system
def return_list_company(request):
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    return render(request, 'Company/Companys.html',
                  {'urls': urls, 'current_url': current_url, 'url_name': url_name.name})


@login_required
# company information whose user is known in the system
def return_user_company(request, uuid):
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    filter = {
        'uuid': uuid
    }
    company = CompanyGetService(request, filter)
    return render(request, 'Company/company_users.html',
                  {'urls': urls, 'current_url': current_url, 'url_name': url_name.name, 'company': company})


@login_required
# lists company users in the system
def company_users(request):
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)

    company = CompanyUser.objects.filter(isDeleted=False, person__user__is_active=True)
    return render(request, 'Company/view_company_user.html',
                  {'urls': urls, 'current_url': current_url, 'url_name': url_name.name, 'company': company})




@login_required
# company user is added to the system
def add_company_user(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    user_form = UserFormCompany
    person_form = PersonForm()
    communication_form = CommunicationForm()
    company_user_form = CompanyUserForm()

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        with transaction.atomic():
            if request.method == 'POST':
                user_form = UserFormCompany(request.POST)
                person_form = PersonForm(request.POST, request.FILES)
                communication_form = CommunicationForm(request.POST)
                company_user_form = CompanyUserForm(request.POST)

                if user_form.is_valid() and person_form.is_valid() and communication_form.is_valid() and company_user_form.is_valid():
                    user = User()
                    user.username = user_form.cleaned_data['email']
                    user.first_name = unicode_tr(user_form.cleaned_data['first_name']).upper()
                    user.last_name = unicode_tr(user_form.cleaned_data['last_name']).upper()
                    user.email = user_form.cleaned_data['email']
                    user.save()

                    person = person_form.save(request, commit=False)
                    communication = communication_form.save(request, commit=False)
                    person.save()
                    person.user = user
                    person.save()
                    communication.save()

                    company_user = CompanyUser(
                        person=person, communication=communication,
                        authorization_period_start=company_user_form.cleaned_data['authorization_period_start'],
                        authorization_period_finish=company_user_form.cleaned_data['authorization_period_finish']
                    )
                    company_user.save()
                    data_as_json_pre = 'Yok'
                    data_as_json_next = serializers.serialize('json', CompanyUser.objects.filter(uuid=company_user.uuid))
                    log = log_model(request, data_as_json_pre, data_as_json_next)

                    user.person.user.groups.add(Group.objects.get(name='Firma'))
                    user.save()

                    if Settings.objects.filter(key='mail_company_user'):
                        if Settings.objects.get(key='mail_company_user').value == 'True':
                            general_methods.sendmail(request, company_user.user)
                    else:
                        set = Settings(key='mail_company_user')
                        set.value = 'False'
                        set.save()

                    messages.success(request, 'Firma Kullanıcısı Başarıyla Kayıt Edilmiştir.')

                    return redirect('ekabis:view_company')

                else:

                    error_message_company = get_error_messages(user_form)
                    error_messages_person = get_error_messages(person_form)
                    error_messages_communication = get_error_messages(communication_form)
                    error_messages = error_messages_communication + error_message_company + error_messages_person

                    return render(request, 'Company/add_company_user.html',
                                  {'user_form': user_form, 'person_form': person_form,
                                   'communication_form': communication_form,
                                   'error_messages': error_messages, 'urls': urls, 'current_url': current_url,
                                   'url_name': url_name.name, 'company_user_form': company_user_form
                                   })

            return render(request, 'Company/add_company_user.html',
                          {'user_form': user_form, 'person_form': person_form, 'communication_form': communication_form,
                           'error_messages': '', 'urls': urls, 'current_url': current_url,
                           'company_user_form': company_user_form,
                           'url_name': url_name.name,
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, e)
        return redirect('ekabis:view_company')


@login_required
# user is assigned to the company in the system
def assigment_company_user(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)

    filter = {
        'uuid': uuid,

    }
    company = CompanyGetService(request, filter)

    array = []

    for company_user in company.companyuser.all():
        array.append(company_user.uuid)

    company_users = CompanyUser.objects.filter(isDeleted=False, person__user__is_active=True).exclude(
        uuid__in=array).order_by(
        '-creationDate')

    # ekstra servis yazılacak
    if request.POST:
        with transaction.atomic():
            if request.POST['company_user'] == 'add':
                companyUser = request.POST.getlist('users')
                if companyUser:
                    for id in companyUser:
                        company_user = CompanyUser.objects.get(pk=id)
                        company.companyuser.add(company_user)


            else:
                persons = request.POST.getlist('users')
                if persons:
                    for id in persons:
                        company_user = CompanyUser.objects.get(pk=id)
                        filter = {
                            'companyuser': company_user
                        }
                        current_company_user = CompanyGetService(request, filter)

                        if current_company_user:
                            current_company_user.companyuser.remove(company_user)

        return redirect('ekabis:view_company_user', company.uuid)

    return render(request, 'Company/company_user_list.html',
                  {'urls': urls, 'users': company_users,
                   'current_url': current_url, 'url_name': url_name.name, 'company': company})


@login_required
# the company in the system is updated
def change_company(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    companyfilter = {
        'uuid': uuid

    }

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        company = CompanyGetService(request, companyfilter)
        company_form = CompanyForm(request.POST or None, instance=company)
        communication_form = CommunicationForm(request.POST or None, instance=company.communication)
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
                if company_form.is_valid() and communication_form.is_valid():
                    communication = communication_form.save(request, commit=False)
                    communication.save()
                    company = company_form.save(request, commit=False)
                    company.save()
                    messages.success(request, 'Firma Güncellenmiştir.')
                else:
                    error_message_company = get_error_messages(company_form)
                    error_messages_communication = get_error_messages(communication_form)
                    error_messages = error_messages_communication + error_message_company
                    return render(request, 'Company/CompanyUpdate.html',
                                  {'company_form': company_form,
                                   'communication_form': communication_form,
                                   'company': company, 'error_messages': error_messages,
                                   'companyDocumentName': companyDocumentName, 'urls': urls, 'current_url': current_url,
                                   'url_name': url_name.name
                                   })

        return render(request, 'Company/CompanyUpdate.html',
                      {'company_form': company_form,
                       'communication_form': communication_form,
                       'company': company, 'error_messages': '',
                       'urls': urls, 'current_url': current_url,
                       'companyDocumentName': companyDocumentName, 'url_name': url_name.name

                       })

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_company')


@login_required
# company file name is added to the system
def add_company_file_name(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    company_form = CompanyFileNameForm()

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        error_messages = []
        if request.method == 'POST':
            with transaction.atomic():
                company_form = CompanyFileNameForm(request.POST)

                if company_form.is_valid():
                    company = company_form.save(request, commit=False)
                    company.save()
                    messages.success(request, 'Döküman İsim Eklenmiştir.')
                    return redirect('ekabis:view_companyfilename')
                else:
                    error_messages = get_error_messages(company_form)
                    return render(request, 'Company/CompanyFileNameAdd.html',
                                  {'company_form': company_form,
                                   'error_messages': error_messages, 'urls': urls, 'current_url': current_url,
                                   'url_name': url_name.name
                                   })

        return render(request, 'Company/CompanyFileNameAdd.html',
                      {'company_form': company_form, 'urls': urls, 'current_url': current_url,
                       'url_name': url_name.name,
                       'error_messages': error_messages,

                       })

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_company')


@login_required
# lists company file name in the system
def view_company_file_name(request):
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    companyNameList = CompanyFileNamesService(request, None)
    return render(request, 'Company/CompanyFileNameList.html',
                  {'companyNameList': companyNameList, 'urls': urls, 'current_url': current_url,
                   'url_name': url_name.name})


@login_required
# the company file name in the system is updated
def change_company_file_name(request, uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        company_name_filter = {
            'uuid': uuid
        }
        names = CompanyFileNamesGetService(request, company_name_filter)
        company_form = CompanyFileNameForm(request.POST or None, instance=names)
        if request.method == 'POST':
            with transaction.atomic():

                if company_form.is_valid():
                    company = company_form.save(request, commit=False)
                    company.save()
                    messages.success(request, 'Döküman İsim Eklenmiştir.')
                    return redirect('ekabis:view_companyfilename')
                else:
                    error_messages = get_error_messages(company_form)
                    return render(request, 'Company/CompanyFileNameUpdate.html',
                                  {'company_form': company_form,
                                   'error_messages': error_messages, 'urls': urls, 'current_url': current_url,
                                   'url_name': url_name.name
                                   })

        return render(request, 'Company/CompanyFileNameUpdate.html',
                      {'company_form': company_form, 'urls': urls, 'current_url': current_url, 'url_name': url_name.name
                       })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_companyfilename')


@login_required
# delete the company file name in the system
def delete_company_file_name(request):
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
                data_as_json_pre = serializers.serialize('json', CompanyFileNames.objects.filter(uuid=uuid))
                obj.isDeleted = True
                obj.save()
                log = "Firma Dosya İsmi Sil"
                logs = Logs(user=request.user, subject=log, ip=get_client_ip(request), previousData=data_as_json_pre)
                logs.save()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


    except Exception as e:

        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')

        return redirect('ekabis:view_companyfilename')


@login_required
# consortium is added in the system
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
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        with transaction.atomic():
            if request.method == 'POST':

                company_form = CompanyFormDinamik(request.POST, request.FILES)
                communication_form = CommunicationForm(request.POST, request.FILES)

                if company_form.is_valid() and communication_form:
                    communication = communication_form.save(request, commit=False)
                    communication.save()

                    company = company_form.save(request, communication)
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
                                   'error_messages': error_messages, 'urls': urls, 'current_url': current_url,
                                   'url_name': url_name.name})

            return render(request, 'Company/AddConsortiumCompany.html',
                          {'company_form': company_form, 'communication_form': communication_form,
                           'form': company_form, 'companies': companies, 'urls': urls, 'current_url': current_url,
                           'url_name': url_name.name,
                           'error_messages': ''})
    except Exception as e:
        print(e)
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_consortium')


@login_required
# lists consortium in the system
def view_consortium(request):
    try:

        company = {
            'is_consortium': 'True'
        }
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        consortium = CompanyService(request, company)

        return render(request, 'Company/ConsortiumList.html',
                      {'companies': consortium, 'urls': urls, 'current_url': current_url, 'url_name': url_name.name})

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')


@login_required
# the consortium in the system is updated
def change_consortium(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    companyfilter = {
        'uuid': uuid,
        'isDeleted': False

    }

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        company = CompanyGetService(request, companyfilter)
        filter = {
            'isDeleted': False,
            'is_consortium': False

        }
        consortium = ConsortiumCompany.objects.filter(isDeleted=False, company=company)
        company_exc = ConsortiumCompany.objects.filter(isDeleted=False, company=company).values_list('consortium__id')

        companies = CompanyService(request, filter).exclude(pk__in=company_exc)
        company_form = CompanyForm(request.POST or None, instance=company)
        communication_form = CommunicationForm(request.POST or None, instance=company.communication)
        companyDocumentName = CompanyFileNames.objects.all()
        employess = CompanyUser.objects.filter(isDeleted=False)

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
                    communication = communication_form.save(request, commit=False)
                    communication.save()
                    company = company_form.save(request, commit=False)
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
                                   'consortium': consortium, 'employess': employess, 'urls': urls,
                                   'current_url': current_url, 'url_name': url_name.name
                                   })

        return render(request, 'Company/UpdateConsortium.html',
                      {'company_form': company_form,
                       'communication_form': communication_form,
                       'company': company, 'error_messages': '',
                       'companies': companies, 'employess': employess,
                       'companyDocumentName': companyDocumentName, 'consortium': consortium, 'urls': urls,
                       'current_url': current_url, 'url_name': url_name.name

                       })

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_consortium')
