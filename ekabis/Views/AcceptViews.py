import traceback

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import resolve

from ekabis.Forms.AcceptForm import AcceptForm
from ekabis.models import YekaBusiness, YekaCompetition, Permission, YekaAccept, Accept, Logs
from ekabis.models.Yeka import Yeka
from ekabis.models.YekaBusinessBlog import YekaBusinessBlog
from ekabis.services import general_methods
from ekabis.services.general_methods import get_error_messages, get_client_ip
from ekabis.services.services import last_urls


@login_required
def view_yeka_accept(request, business, businessblog):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)

        yekabusiness = YekaBusiness.objects.get(uuid=business)
        yekabussinessblog = YekaBusinessBlog.objects.get(uuid=businessblog)
        name = ''
        if Yeka.objects.filter(business=yekabusiness):
            name = Yeka.objects.get(business=yekabusiness).definition
        elif YekaCompetition.objects.filter(business=yekabusiness):
            name = YekaCompetition.objects.get(business=yekabusiness).name

        if not YekaAccept.objects.filter(yekabusinessblog=yekabussinessblog):
            accept = YekaAccept()
            accept.yekabusinessblog = yekabussinessblog
            accept.business = yekabusiness
            accept.save()
        else:
            accept = YekaAccept.objects.get(yekabusinessblog=yekabussinessblog)

        return render(request, 'Accept/view_accept.html',
                      {'yekabussinessblog': yekabussinessblog, 'urls': urls, 'current_url': current_url,
                       'url_name': url_name, 'name': name, 'accept': accept
                       })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required
def add_yeka_accept(request, uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    yeka_accept = YekaAccept.objects.get(uuid=uuid)
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)

        name = ''

        if Yeka.objects.filter(business=yeka_accept.business):
            name = Yeka.objects.get(business=yeka_accept.business).definition
        elif YekaCompetition.objects.filter(business=yeka_accept.business):
            name = YekaCompetition.objects.get(business=yeka_accept.business).name

        with transaction.atomic():
            accept_form = AcceptForm()

            if request.method == 'POST':
                accept_form = AcceptForm(request.POST or None, request.FILES or None)
                if accept_form.is_valid():
                    form = accept_form.save(request, commit=False)
                    form.save()
                    yeka_accept.accept.add(form)
                    yeka_accept.save()
                    messages.success(request, 'Kabul kayıt edildi.')
                    return redirect('ekabis:view_yeka_accept', yeka_accept.business.uuid,
                                    yeka_accept.yekabusinessblog.uuid)
                else:
                    error_messages = get_error_messages(accept_form)
                    return render(request, 'Accept/add_accept.html',
                                  {'accept_form': accept_form,
                                   'error_messages': error_messages, 'urls': urls, 'current_url': current_url,
                                   'url_name': url_name, 'name': name,
                                   })

            return render(request, 'Accept/add_accept.html',
                          {'accept_form': accept_form,
                           'business': yeka_accept.business,
                           'yekabussinessblog': yeka_accept.yekabusinessblog, 'urls': urls, 'current_url': current_url,
                           'url_name': url_name, 'name': name
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka_accept', yeka_accept.business.uuid, yeka_accept.yekabusinessblog.uuid)


@login_required
def change_accept(request, uuid, accept_uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    accept = Accept.objects.get(uuid=uuid)
    yeka_accept = YekaAccept.objects.get(uuid=accept_uuid)
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)

        name = ''

        if Yeka.objects.filter(business=yeka_accept.business):
            name = Yeka.objects.get(business=yeka_accept.business).definition
        elif YekaCompetition.objects.filter(business=yeka_accept.business):
            name = YekaCompetition.objects.get(business=yeka_accept.business).name
        accept_form = AcceptForm(request.POST or None, request.FILES or None, instance=accept)

        with transaction.atomic():
            if request.method == 'POST':
                if accept_form.is_valid():
                    form = accept_form.save(request, commit=False)
                    form.save()
                    messages.success(request, 'Kabul kayıt güncellendi.')
                    return redirect('ekabis:view_yeka_accept', yeka_accept.business.uuid,
                                    yeka_accept.yekabusinessblog.uuid)
                else:
                    error_messages = get_error_messages(accept_form)
                    return render(request, 'Accept/change_accept.html',
                                  {'accept_form': accept_form,
                                   'error_messages': error_messages, 'urls': urls, 'current_url': current_url,
                                   'url_name': url_name, 'name': name,
                                   })

            return render(request, 'Accept/change_accept.html',
                          {'accept_form': accept_form,
                           'business': yeka_accept.business,
                           'yekabussinessblog': yeka_accept.yekabusinessblog, 'urls': urls, 'current_url': current_url,
                           'url_name': url_name, 'name': name
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka_accept', yeka_accept.business.uuid, yeka_accept.yekabusinessblog.uuid)


@login_required
def delete_accept(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']

                pre = serializers.serialize('json', Accept.objects.filter(uuid=uuid))
                obj = Accept.objects.get(uuid=uuid)
                obj.isDeleted = False
                obj.save()

                log = ' adlı kabul silindi.'
                logs = Logs(user=request.user, subject=log, previousData=pre, ip=get_client_ip(request))
                logs.save()
                return JsonResponse({'status': 'Success', 'msg': 'save successfully'})

            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})
