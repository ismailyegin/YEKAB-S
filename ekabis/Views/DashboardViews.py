import traceback

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect

from ekabis.services import general_methods
from ekabis.services.services import ActiveGroupService, GroupService


@login_required
def return_directory_dashboard(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    return render(request, 'anasayfa/federasyon.html',
                  {

                  })


@login_required
def return_personel_dashboard(request):
    active = general_methods.controlGroup(request)
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    return render(request, 'anasayfa/personel.html',
                  {})


@login_required
def return_admin_dashboard(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    return render(request, 'anasayfa/admin.html',
                  {

                  })


@login_required
def activeGroup(request, pk):
    try:
        with transaction.atomic():
            activefilter = {
                'user': request.user
            }
            userActive = ActiveGroupService(request, activefilter)
            groupfilter = {
                'pk': pk
            }
            group = GroupService(request, groupfilter).first()
            userActive.group = group
            userActive.save()
            if group.name == "Admin":
                return redirect('ekabis:view_admin')
        activefilter={
        'user':request.user
        }
        userActive = ActiveGroupService(request,activefilter)
        groupfilter={
        'pk':pk
        }
        group = GroupService(request,groupfilter)[0]
        userActive.group = group
        userActive.save()
        if group.name == "Admin":
            return redirect('ekabis:view_admin')

        elif group.name == 'Yonetim':
                return redirect('ekabis:view_federasyon')

        elif group.name == 'Personel':
                return redirect('ekabis:view_personel')
        else:
                return {}
    except Exception as e:
        traceback.print_exc()
