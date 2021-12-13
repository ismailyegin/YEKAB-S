import traceback

from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect
from ekabis.Forms.DisabledUserForm import DisabledUserForm
from ekabis.services import general_methods
from ekabis.models import DirectoryMember, Employee
from ekabis.services.services import CategoryItemService, DirectoryCommissionService, DirectoryMemberRoleService, \
    GroupGetService, \
    CommunicationGetService, PersonGetService, UserGetService




@login_required
def activeGroup(request, pk):
    try:
        gropfilter = {
            'name': request.GET.get('group')
        }
        group = GroupGetService(request, gropfilter)
        communicationfilter = {
            'pk': request.GET.get('communication')
        }
        communication = CommunicationGetService(request, communicationfilter)
        personfilter = {
            'pk': request.GET.get('person')
        }
        person = PersonGetService(request, personfilter)
        userfilter = {
            'pk': request.GET.get('user')
        }
        user = UserGetService(request, userfilter)
        if group.name == "Admin":
            user.groups.add(group)
            user.is_superuser = True
            user.is_staff = True
            user.is_active = True
            user.save()
            log = str(user.get_full_name()) + " grubu " + str(group.name)+" olarak güncellendi"
            log = general_methods.logwrite(request, request.user, log)
            return redirect('ekabis:view_admin')
        elif group.name == "Personel":
            employe = Employee(person=person,
                               communication=communication,
                               user=user,
                               workDefinition=CategoryItemService(request, None)
                               )
            employe.save()
            user.groups.add(group)
            user.save()
            log = str(user.get_full_name()) + " grubu " + str(group.name)+" olarak güncellendi"
            log = general_methods.logwrite(request, request.user, log)
            return redirect('ekabis:view_personel', pk=employe.pk)

        elif group.name == "Yonetim":
            member = DirectoryMember(person=person, communication=communication, user=user,
                                     role=DirectoryMemberRoleService(request, None).first(),
                                     commission=DirectoryCommissionService(request, None).first())
            member.save()
            user.groups.add(group)
            user.save()
            log = str(user.get_full_name()) + " grubu " + str(group.name) + " olarak güncellendi"
            log = general_methods.logwrite(request, request.user, log)
            return redirect('ekabis:view_directoryMember', pk=member.pk)
        return {}
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')


def viewRepairPage(request):
    return render(request, 'maintenancePage.html')
