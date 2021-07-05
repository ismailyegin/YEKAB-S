import traceback

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from ekabis.Forms.CommunicationForm import CommunicationForm
from ekabis.Forms.DirectoryCommissionForm import DirectoryCommissionForm
from ekabis.Forms.DirectoryForm import DirectoryForm
from ekabis.Forms.DirectoryMemberRoleForm import DirectoryMemberRoleForm
from ekabis.Forms.DisabledCommunicationForm import DisabledCommunicationForm
from ekabis.Forms.DisabledDirectoryForm import DisabledDirectoryForm
from ekabis.Forms.DisabledPersonForm import DisabledPersonForm

from ekabis.Forms.DisabledUserForm import DisabledUserForm
from ekabis.Forms.UserForm import UserForm
from ekabis.Forms.PersonForm import PersonForm
from ekabis.Forms.UserSearchForm import UserSearchForm
from ekabis.models.DirectoryCommission import DirectoryCommission
from ekabis.models.DirectoryMember import DirectoryMember
from ekabis.models.DirectoryMemberRole import DirectoryMemberRole
from ekabis.services import general_methods

from zeep import Client
from unicode_tr import unicode_tr

from ekabis.services.general_methods import get_error_messages
from ekabis.services.services import PersonService, UserService, GroupService, DirectoryMemberService, \
    DirectoryMemberRoleService, DirectoryCommissionService


@login_required
def add_directory_member(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user_form = UserForm()
    person_form = PersonForm()
    communication_form = CommunicationForm()
    member_form = DirectoryForm()

    if request.method == 'POST':

        user_form = UserForm(request.POST)
        person_form = PersonForm(request.POST, request.FILES)
        communication_form = CommunicationForm(request.POST)
        member_form = DirectoryForm(request.POST)

        # controller tc email

        mail = request.POST.get('email')
        userfilter = {
            'mail': mail
        }
        if UserService(request, userfilter):
            messages.warning(request, 'Mail adresi başka bir kullanici tarafından kullanilmaktadir.')
            return render(request, 'yonetim/kurul-uyesi-ekle.html',
                          {'user_form': user_form, 'person_form': person_form,
                           'communication_form': communication_form,
                           'member_form': member_form})

        tc = request.POST.get('tc')
        personfilter = {
            'tc': tc
        }
        if PersonService(request, personfilter):
            messages.warning(request, 'Tc kimlik numarasi sistemde kayıtlıdır. ')
            return render(request, 'yonetim/kurul-uyesi-ekle.html',
                          {'user_form': user_form, 'person_form': person_form,
                           'communication_form': communication_form,
                           'member_form': member_form})

        name = request.POST.get('first_name')
        surname = request.POST.get('last_name')
        year = request.POST.get('birthDate')
        year = year.split('/')

        # client = Client('https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL')
        # if not (client.service.TCKimlikNoDogrula(tc, name, surname, year[2])):
        #     messages.warning(request,
        #                      'Tc kimlik numarasi ile isim  soyisim dogum yılı  bilgileri uyuşmamaktadır. ')
        #     return render(request, 'yonetim/kurul-uyesi-ekle.html',
        #                   {'user_form': user_form, 'person_form': person_form,
        #                    'communication_form': communication_form,
        #                    'member_form': member_form})

        if user_form.is_valid() and person_form.is_valid() and communication_form.is_valid() and member_form.is_valid():
            user = User()
            user.username = user_form.cleaned_data['email']
            user.first_name = unicode_tr(user_form.cleaned_data['first_name']).upper()
            user.last_name = unicode_tr(user_form.cleaned_data['last_name']).upper()
            user.email = user_form.cleaned_data['email']
            groupfilter = {
                'name': 'Yonetim'
            }
            group = GroupService(request, groupfilter).first()
            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()
            user.groups.add(group)
            user.save()

            person = person_form.save(commit=False)
            communication = communication_form.save(commit=False)
            person.save()
            communication.save()

            directoryMember = DirectoryMember(user=user, person=person, communication=communication)
            directoryMember.role = member_form.cleaned_data['role']
            directoryMember.commission = member_form.cleaned_data['commission']
            directoryMember.save()
            log = str(user.get_full_name()) + " Kurul Uyesi kaydedildi"
            log = general_methods.logwrite(request, request.user, log)

            messages.success(request, 'Kurul Üyesi Başarıyla Kayıt Edilmiştir.')

            return redirect('ekabis:change_directorymember', directoryMember.uuid)

        else:

            for x in user_form.errors.as_data():
                messages.warning(request, user_form.errors[x].first())

            error_message_company = get_error_messages(user_form)
            error_messages_person = get_error_messages(person_form)
            error_messages_communication = get_error_messages(communication_form)
            error_messages_member = get_error_messages(member_form)
            error_messages = error_messages_communication + error_message_company + error_messages_person + error_messages_member
            return render(request, 'yonetim/kurul-uyesi-ekle.html',
                          {'user_form': user_form, 'person_form': person_form, 'communication_form': communication_form,
                           'member_form': member_form, 'error_messages': error_messages})

    return render(request, 'yonetim/kurul-uyesi-ekle.html',
                  {'user_form': user_form, 'person_form': person_form, 'communication_form': communication_form,
                   'member_form': member_form})


@login_required
def return_directory_members(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    members = None
    user_form = UserSearchForm()
    try:
        with transaction.atomic():
            if request.method == 'POST':

                user_form = UserSearchForm(request.POST)
                if user_form.is_valid():
                    firstName = unicode_tr(user_form.cleaned_data['first_name']).upper()
                    lastName = unicode_tr(user_form.cleaned_data['last_name']).upper()
                    email = user_form.cleaned_data.get('email')
                    if not (firstName or lastName or email):
                        members = DirectoryMemberService(request, None)
                    else:
                        query = Q()
                        if lastName:
                            query &= Q(user__last_name__icontains=lastName)
                        if firstName:
                            query &= Q(user__first_name__icontains=firstName)
                        if email:
                            query &= Q(user__email__icontains=email)
                        members = DirectoryMemberService(request, query)

            return render(request, 'yonetim/kurul-uyeleri.html', {'members': members, 'user_form': user_form})

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')


@login_required
def delete_directory_member(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']
                memberfilter = {
                    'uuid': uuid
                }
                obj = DirectoryMemberService(request, memberfilter)[0]

                log = str(obj.user.get_full_name()) + " kurul uyesi silindi"
                log = general_methods.logwrite(request, request.user, log)

                obj.delete()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

    except DirectoryMember.DoesNotExist:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def update_directory_member(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    memberfilter = {
        'uuid': uuid
    }
    member = DirectoryMemberService(request, memberfilter).first()
    if not member.user.groups.all():
        groupfilter = {
            'name': 'Yonetim'
        }
        member.user.groups.add(GroupService(request, groupfilter).first())
        member.save()
    groups = GroupService(request, None)

    user = member.user
    person = member.person
    communication = member.communication

    user_form = UserForm(request.POST or None, instance=user)
    person_form = PersonForm(request.POST or None, request.FILES or None, instance=person)
    member_form = DirectoryForm(request.POST or None, instance=member)
    communication_form = CommunicationForm(request.POST or None, instance=communication)
    try:
        with transaction.atomic():
            if request.method == 'POST':

                mail = request.POST.get('email')
                if user.email != mail:
                    emailfilter = {
                        'email': mail
                    }
                    if UserService(request, emailfilter):
                        messages.warning(request, 'Mail adresi başka bir kullanici tarafından kullanilmaktadir.')
                        return render(request, 'yonetim/kurul-uyesi-duzenle.html',
                                      {'user_form': user_form, 'communication_form': communication_form,
                                       'member': member,
                                       'person_form': person_form, 'member_form': member_form, 'groups': groups,

                                       })
                tc = request.POST.get('tc')

                if person.tc != tc:
                    personfilter = {
                        'tc': tc
                    }
                    if PersonService(request, personfilter):
                        messages.warning(request, 'Tc kimlik numarasi sistemde kayıtlıdır. ')
                        return render(request, 'yonetim/kurul-uyesi-duzenle.html',
                                      {'user_form': user_form, 'communication_form': communication_form,
                                       'member': member,
                                       'person_form': person_form, 'member_form': member_form, 'groups': groups,

                                       })

                name = request.POST.get('first_name')
                surname = request.POST.get('last_name')
                year = request.POST.get('birthDate')
                year = year.split('/')

                client = Client('https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL')
                if not (client.service.TCKimlikNoDogrula(tc, name, surname, year[2])):
                    messages.warning(request,
                                     'Tc kimlik numarasi ile isim  soyisim dogum yılı  bilgileri uyuşmamaktadır. ')
                    return render(request, 'yonetim/kurul-uyesi-duzenle.html',
                                  {'user_form': user_form, 'communication_form': communication_form, 'member': member,
                                   'person_form': person_form, 'member_form': member_form, 'groups': groups,

                                   })

                if user_form.is_valid() and person_form.is_valid() and communication_form.is_valid() and member_form.is_valid():

                    user_form.save()
                    person_form.save()
                    communication_form.save()
                    member_form.save()

                    log = str(user.get_full_name()) + " Kurul uyesi guncellendi"
                    log = general_methods.logwrite(request, request.user, log)

                    messages.success(request, 'Kurul Üyesi Başarıyla Güncellendi')
                else:
                    error_message_company = get_error_messages(user_form)
                    error_messages_person = get_error_messages(person_form)
                    error_messages_communication = get_error_messages(communication_form)
                    error_messages_member = get_error_messages(member_form)
                    error_messages = error_messages_communication + error_message_company + error_messages_person + error_messages_member
                    return render(request, 'yonetim/kurul-uyesi-duzenle.html',
                                  {'user_form': user_form, 'communication_form': communication_form, 'member': member,
                                   'person_form': person_form, 'member_form': member_form, 'groups': groups,
                                   'error_messages': error_messages
                                   })
            return render(request, 'yonetim/kurul-uyesi-duzenle.html',
                          {'user_form': user_form, 'communication_form': communication_form, 'member': member,
                           'person_form': person_form, 'member_form': member_form, 'groups': groups,
                           'error_messages': ''

                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')


@login_required
def return_member_roles(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    member_role_form = DirectoryMemberRoleForm()
    try:
        with transaction.atomic():
            if request.method == 'POST':

                member_role_form = DirectoryMemberRoleForm(request.POST)

                if member_role_form.is_valid():

                    memberRole = DirectoryMemberRole(name=member_role_form.cleaned_data['name'])
                    memberRole.save()
                    messages.success(request, 'Kurul Üye Rolü Başarıyla Kayıt Edilmiştir.')
                    return redirect('ekabis:view_directorymemberrole')

                else:
                    error_messages = get_error_messages(member_role_form)
                    memberRoles = DirectoryMemberRoleService(request, None)
                    return render(request, 'yonetim/kurul-uye-rolleri.html',
                                  {'member_role_form': member_role_form, 'memberRoles': memberRoles,
                                   'error_messages': error_messages})
            memberRoles = DirectoryMemberRoleService(request, None)
            return render(request, 'yonetim/kurul-uye-rolleri.html',
                          {'member_role_form': member_role_form, 'memberRoles': memberRoles, 'error_messages': ''})
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')


@login_required
def delete_member_role(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']
                memberrolefilter = {
                    'uuid': uuid
                }
                obj = DirectoryMemberRoleService(request, memberrolefilter).first()
                obj.delete()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except DirectoryMemberRole.DoesNotExist:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def update_member_role(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    memberrolefilter = {
        'uuid': uuid
    }

    memberRole = DirectoryMemberRoleService(request, memberrolefilter).first()
    member_role_form = DirectoryMemberRoleForm(request.POST or None, instance=memberRole)
    try:
        with transaction.atomic():
            if request.method == 'POST':

                if member_role_form.is_valid():
                    member_role_form.save()
                    messages.success(request, 'Başarıyla Güncellendi')
                    return redirect('ekabis:view_directorymemberrole')
                else:
                    messages.warning(request, 'Alanları Kontrol Ediniz')

            return render(request, 'yonetim/kurul-uye-rol-duzenle.html',
                          {'member_role_form': member_role_form})
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')


@login_required
def return_commissions(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    commission_form = DirectoryCommissionForm()

    try:
        with transaction.atomic():
            if request.method == 'POST':

                commission_form = DirectoryCommissionForm(request.POST)

                if commission_form.is_valid():

                    commission = DirectoryCommission(name=commission_form.cleaned_data['name'])
                    commission.save()

                    log = " Kurul eklendi"
                    log = general_methods.logwrite(request, request.user, log)
                    messages.success(request, 'Kurul Başarıyla Kayıt Edilmiştir.')
                    return redirect('ekabis:view_directorycommission')

                else:

                    messages.warning(request, 'Alanları Kontrol Ediniz')

            commissions = DirectoryCommissionService(request, None)
            return render(request, 'yonetim/kurullar.html',
                          {'commission_form': commission_form, 'commissions': commissions})

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')


@login_required
def delete_commission(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']
                commissonfilter = {
                    'uuid': uuid
                }
                obj = DirectoryCommissionService(request, commissonfilter).first()
                log = str(obj.name) + " kurul silindi"
                log = general_methods.logwrite(request, request.user, log)
                obj.delete()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})


            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

    except DirectoryCommission.DoesNotExist:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def update_commission(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    commissonfilter = {
        'uuid': pk
    }
    commission = DirectoryCommissionService(request, commissonfilter).first()
    commission_form = DirectoryCommissionForm(request.POST or None, instance=commission)
    try:
        with transaction.atomic():
            if request.method == 'POST':

                if commission_form.is_valid():
                    commission_form.save()
                    messages.success(request, 'Başarıyla Güncellendi')

                    log = str(commission.name) + " kurul guncellendi"
                    log = general_methods.logwrite(request, request.user, log)

                    return redirect('ekabis:view_directorycommission')
                else:
                    messages.warning(request, 'Alanları Kontrol Ediniz')

            return render(request, 'yonetim/kurul-duzenle.html',
                          {'commission_form': commission_form})
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')


@login_required
def updateDirectoryProfile(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    user = request.user
    memberfilter = {
        'user': user
    }
    member = DirectoryMemberService(request, memberfilter).first()
    person = member.person
    communication = member.communication
    user_form = DisabledUserForm(request.POST or None, instance=user)
    person_form = DisabledPersonForm(request.POST or None, instance=person)
    communication_form = DisabledCommunicationForm(request.POST or None, instance=communication)
    member_form = DisabledDirectoryForm(request.POST or None, instance=request.user)
    password_form = SetPasswordForm(request.user, request.POST)
    try:
        with transaction.atomic():
            if request.method == 'POST':

                if user_form.is_valid() and communication_form.is_valid() and person_form.is_valid() and member_form.is_valid() and password_form.is_valid():

                    user.username = user_form.cleaned_data['email']
                    user.first_name = unicode_tr(user_form.cleaned_data['first_name']).upper()
                    user.last_name = unicode_tr(user_form.cleaned_data['last_name']).upper()
                    user.email = user_form.cleaned_data['email']
                    user.set_password(password_form.cleaned_data['new_password1'])
                    user.save()

                    person_form.save()
                    communication_form.save()
                    member_form.save()
                    password_form.save()

                    messages.success(request, 'Yönetim Kurul Üyesi Başarıyla Güncellenmiştir.')

                    log = str(user.get_full_name()) + " yönetim kurulu guncellendi"
                    log = general_methods.logwrite(request, request.user, log)

                else:

                    error_message_password = get_error_messages(password_form)
                    error_messages_communication = get_error_messages(communication_form)
                    error_messages_person = get_error_messages(person_form)
                    error_messages_member = get_error_messages(member_form)
                    error_messages_user = get_error_messages(user_form)

                    error_messages = error_messages_user + error_message_password + error_messages_communication + error_messages_person + error_messages_member
                    return render(request, 'yonetim/yonetim-kurul-profil-guncelle.html',
                                  {'user_form': user_form, 'communication_form': communication_form,
                                   'person_form': person_form, 'password_form': password_form,
                                   'member_form': member_form,
                                   'error_messages': error_messages})

            return render(request, 'yonetim/yonetim-kurul-profil-guncelle.html',
                          {'user_form': user_form, 'communication_form': communication_form,
                           'person_form': person_form, 'password_form': password_form, 'member_form': member_form,
                           'error_messages': ''})
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
