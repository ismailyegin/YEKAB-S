import traceback

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db import transaction
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import resolve

from ekabis.Forms.AcceptForm import AcceptForm
from ekabis.models import YekaBusiness, YekaCompetition, Permission, YekaAccept, Accept, Logs
from ekabis.models.Yeka import Yeka
from ekabis.models.YekaBusinessBlog import YekaBusinessBlog
from ekabis.services import general_methods
from ekabis.services.NotificationServices import notification
from ekabis.services.general_methods import get_error_messages, get_client_ip
from ekabis.services.services import last_urls, YekaCompetitionGetService


@login_required
def view_yeka_accept(request, business, businessblog):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        total_mwe = 0
        total_mwm = 0
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)

        yekabusiness = YekaBusiness.objects.get(uuid=business)
        yekabussinessblog = YekaBusinessBlog.objects.get(uuid=businessblog)
        name = general_methods.yekaname(yekabusiness)

        if not YekaAccept.objects.filter(business=yekabusiness):
            accept = YekaAccept()
            accept.yekabusinessblog = yekabussinessblog
            accept.business = yekabusiness
            accept.save()
            accept_accepts=accept.accept.filter(isDeleted=False)
        else:
            accept = YekaAccept.objects.get(business=yekabusiness,isDeleted=False)
            accept_accepts=accept.accept.filter(isDeleted=False).order_by('date')



            # total_mwm=accept_accepts.aggregate(Sum('installedPower'))['installedPower__sum']
            # total_mwe=accept_accepts.aggregate(Sum('currentPower'))['currentPower__sum']
            # if total_mwm:
            #     total_mwm = round(float("{:.5f}".format(total_mwm)), 5)
            # if total_mwe:
            #     total_mwe=round(float("{:.5f}".format(total_mwe)), 5)


        return render(request, 'Accept/view_accept.html',
                      {'yekabussinessblog': yekabussinessblog, 'urls': urls, 'current_url': current_url,
                       'url_name': url_name, 'name': name, 'accept_all': accept_accepts,'accept':accept
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
    filter={
        'business':yeka_accept.business
    }
    competition=YekaCompetitionGetService(request,filter)
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)

        name = general_methods.yekaname(yeka_accept.business)

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
                    url = redirect('ekabis:view_yeka_competition_detail', competition.uuid).url
                    html = '<a style="" href="' + url + '"> ' + str(
                        competition.pk) + ' - ' + str(
                        competition.name) + '</a> adlı YEKA yarışmasına ' +str(yeka_accept.pk)+' id li kabul eklendi.'
                    notification(request, html, competition.uuid, 'yeka_competition')
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
    filter = {
        'business': yeka_accept.business
    }
    competition = YekaCompetitionGetService(request, filter)
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
                    url = redirect('ekabis:view_yeka_competition_detail', competition.uuid).url
                    html = '<a style="" href="' + url + '"> ' + str(
                        competition.pk) + ' - ' + str(
                        competition.name) + '</a> adlı YEKA yarışmasına ait ' + str(
                        yeka_accept.pk) + ' id li kabul güncellendi.'
                    notification(request, html, competition.uuid, 'yeka_competition')
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
                obj.isDeleted = True
                obj.save()
                yeka_accept = YekaAccept.objects.get(accept=obj)
                competition=YekaCompetition.objects.get(business=yeka_accept.business)

                log = str(obj.pk)+' id li kabul silindi.'
                logs = Logs(user=request.user, subject=log, previousData=pre, ip=get_client_ip(request))
                logs.save()
                url = redirect('ekabis:view_yeka_competition_detail', competition.uuid).url
                html = '<a style="" href="' + url + '"> ' + str(obj.pk)+'</a> id li kabul silindi.'
                notification(request, html, competition.uuid, 'yeka_competition')
                return JsonResponse({'status': 'Success', 'msg': 'save successfully'})

            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})
