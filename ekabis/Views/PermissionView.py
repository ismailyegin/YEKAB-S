import traceback
from datetime import datetime

import requests
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import resolve

from ekabis.Forms.PermissionForm import PermissionForm
from ekabis.Forms.UserSearchForm import UserSearchForm
from ekabis.models import Permission
from ekabis.services import general_methods
from ekabis.services.general_methods import get_error_messages
from ekabis.services.services import LogsService, last_urls
import inspect
@login_required
def view_permission(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)

        permissions=Permission.objects.all()
        return render(request, 'Permission/view_permission.html', {'permissions':permissions,'urls': urls, 'current_url': current_url, 'url_name': url_name})
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')

@login_required
def change_permission(request,uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:

        permission=Permission.objects.get(uuid=uuid)
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        permission_form=PermissionForm(request.POST or None,instance=permission)
        # code name alanından fonksiyona ulaşılacak
        code = inspect.getsource(change_permission)
        with transaction.atomic():
            if request.method == 'POST':
                if permission_form.is_valid():
                    perm=permission_form.save(request,commit=False)
                    perm.save()
                    messages.success(request, 'Firma Kullanıcısı Güncellenmiştir.')
                    return redirect('ekabis:view_permission')
                else:
                    error_messages = get_error_messages(permission_form)
                    return render(request, 'Permission/change_permission.html',
                                  {
                                   'urls': urls,
                                   'current_url': current_url,
                                   'url_name': url_name,
                                   'error_messages': error_messages,
                                   'permission_form':permission_form,
                                      'code':code
                                   })
            return render(request, 'Permission/change_permission.html',
                          { 'urls': urls,
                           'current_url': current_url, 'url_name': url_name,
                           'permission_form':permission_form,
                            'code': code
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')