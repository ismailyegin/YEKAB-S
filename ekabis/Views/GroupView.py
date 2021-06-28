import traceback

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect
from ekabis.Forms.GroupForm import GroupForm
from ekabis.services import general_methods
from ekabis.services.services import GroupService


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
                    log = group.name + ' Grubunu Kaydetti'
                    log = general_methods.logwrite(request, request.user, log)
                    messages.success(request, 'Grup Kayıt Edilmiştir.')
                    return redirect('ekabis:view_group')
                else:
                    messages.warning(request, 'Alanları Kontrol Ediniz')
                return render(request, 'Group/GrupEkle.html',
                              {'group_form': group_form, })
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
    groupfilter = {
        'pk': pk
    }
    groups = GroupService(request, groupfilter).first()
    group_form = GroupForm(request.POST or None, instance=groups)
    try:
        if request.method == 'POST':
            if group_form.is_valid():
                group_form.save()
                messages.success(request, 'Grup Güncellenmiştir.')
                return redirect('ekabis:view_group')

            else:
                messages.warning(request, 'Alanları Kontrol Ediniz')

        return render(request, 'Group/grupGuncelle.html',
                      {'group_form': group_form,
                       })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
