import traceback

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect
from ekabis.Forms.GroupForm import GroupForm
from ekabis.models.PermissionGroup import PermissionGroup
from ekabis.services import general_methods
from ekabis.services.general_methods import get_error_messages
from ekabis.services.services import GroupService, PermissionService, PermissionGroupService, GroupGetService


@login_required
def add_group(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    group_form = GroupForm()
    try:
        with transaction.atomic():
            if request.method == 'POST':
                group_form = GroupForm(request.POST)
                if group_form.is_valid():
                    group = group_form.save(commit=False)
                    group.save()

                    for item in PermissionService(request, None):
                        permissionGroupfilter = {
                            'group': group,
                            'permissions': item
                        }
                        if not (PermissionGroupService(request, permissionGroupfilter)):
                            perm = PermissionGroup(group=group, permissions=item, is_active=False)
                            perm.save()

                    log = group.name + ' Grubunu Kaydetti'
                    log = general_methods.logwrite(request, request.user, log)
                    messages.success(request, 'Grup Kayıt Edilmiştir.')
                    return redirect('ekabis:view_group')
                else:
                    error_messages = get_error_messages(group_form)
                    return render(request, 'Group/GrupEkle.html',
                                  {'group_form': group_form, 'error_messages': error_messages, })
            return render(request, 'Group/GrupEkle.html',
                          {'group_form': group_form, 'error_messages': ''})
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')


@login_required
def return_list_group(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    groups = GroupService(request, None)
    return render(request, 'Group/GrupListe.html',
                  {'groups': groups})


@login_required
def return_update_group(request, pk):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        groupfilter = {
            'pk': pk
        }
        groups = GroupGetService(request, groupfilter)
        group_form = GroupForm(request.POST or None, instance=groups)
        with transaction.atomic():
            if request.method == 'POST':
                if group_form.is_valid():
                    group_form.save()
                    messages.success(request, 'Grup Güncellenmiştir.')
                    return redirect('ekabis:view_group')

                else:
                    error_messages = get_error_messages(group_form)
                    return render(request, 'Group/grupGuncelle.html',
                                  {'group_form': group_form, 'error_messages': error_messages
                                   })

            return render(request, 'Group/grupGuncelle.html',
                          {'group_form': group_form, 'error_messages': ''
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
def change_groupPermission(request, pk):
    perm = general_methods.control_access(request)
    active = general_methods.controlGroup(request)
    if not perm:
        print('ex')
        # logout(request)
        # return redirect('accounts:login')
    groupfilter = {
        'group__pk' : pk
    }
    permGroup = PermissionGroupService(request,groupfilter)
    try:
        with transaction.atomic():
            if request.method == 'POST':
                for item in permGroup:
                    if request.POST.get(str(item.pk)):
                        item.is_active = True
                    else:
                        item.is_active = False
                    item.save()
            return render(request, 'Group/GrupizinEkle.html',
                          {'permGroup': permGroup})
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
