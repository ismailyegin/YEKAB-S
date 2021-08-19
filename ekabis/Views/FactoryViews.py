import traceback

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import resolve

from ekabis.Forms.FactoryFileForm import FactoryFileForm
from ekabis.Forms.FactoryFileNameForm import FactoryFileNameForm
from ekabis.Forms.FactoryForm import FactoryForm
from ekabis.models import Permission, Logs, YekaBusiness, YekaBusinessBlog, Yeka, YekaCompetition, FactoryFile
from ekabis.models.Factory import Factory
from ekabis.models.FactoryFileName import FactoryFileName
from ekabis.models.YekaFactory import YekaFactory
from ekabis.services import general_methods
from ekabis.services.general_methods import get_error_messages, get_client_ip
from ekabis.services.services import last_urls, FactoryFileNameService, FactoryFileNameGetService, FactoryGetService, \
    FactoryFileGetService


@login_required
def add_factory_file_name(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    file_name_form = FactoryFileNameForm()
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        if request.method == 'POST':
            with transaction.atomic():
                file_name_form = FactoryFileNameForm(request.POST)

                if file_name_form.is_valid():
                    company = file_name_form.save(request, commit=False)
                    company.save()
                    messages.success(request, 'Döküman isim eklenmiştir.')
                    return redirect('ekabis:views_factory_file_name')
                else:
                    error_messages = get_error_messages(file_name_form)
                    return render(request, 'Factory/add_factory_file_name.html',
                                  {'file_name_form': file_name_form,
                                   'error_messages': error_messages, 'urls': urls, 'current_url': current_url,
                                   'url_name': url_name
                                   })

        return render(request, 'Factory/add_factory_file_name.html',
                      {'file_name_form': file_name_form, 'urls': urls, 'current_url': current_url, 'url_name': url_name

                       })

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:views_factory_file_name')


@login_required
def view_factory_file_name(request):
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    file_names = FactoryFileNameService(request, None)
    return render(request, 'Factory/view_factory_file_name.html',
                  {'file_names': file_names, 'urls': urls, 'current_url': current_url, 'url_name': url_name})


@login_required
def change_factory_file_name(request, uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    filter = {
        'uuid': uuid
    }
    file_name = FactoryFileNameGetService(request, filter)
    file_name_form = FactoryFileNameForm(request.POST or None, instance=file_name)
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        if request.method == 'POST':
            with transaction.atomic():

                if file_name_form.is_valid():
                    company = file_name_form.save(request, commit=False)
                    company.save()
                    messages.success(request, 'Doküman ismi güncellenmiştir.')
                    return redirect('ekabis:views_factory_file_name')
                else:
                    error_messages = get_error_messages(file_name_form)
                    return render(request, 'Factory/update_factory_file_name.html',
                                  {'file_name_form': file_name_form,
                                   'error_messages': error_messages, 'urls': urls, 'current_url': current_url,
                                   'url_name': url_name
                                   })

        return render(request, 'Factory/update_factory_file_name.html',
                      {'file_name_form': file_name_form, 'urls': urls, 'current_url': current_url,
                       'url_name': url_name})

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:views_factory_file_name')


@login_required
def delete_factory_file_name(request):
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

                data_as_json_pre = serializers.serialize('json', FactoryFileName.objects.filter(uuid=uuid))
                obj = FactoryFileNameGetService(request, company_name_filter)
                log = str(obj.name) + " - doküman ismi silindi."
                logs = Logs(user=request.user, subject=log, ip=get_client_ip(request), previousData=data_as_json_pre)
                logs.save()
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
def view_yeka_factory(request, business, businessblog):
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

        if not YekaFactory.objects.filter(yekabusinessblog=yekabussinessblog):
            factory = YekaFactory()
            factory.yekabusinessblog = yekabussinessblog
            factory.business = yekabusiness
            factory.save()
        else:
            factory = YekaFactory.objects.get(yekabusinessblog=yekabussinessblog)

        return render(request, 'Factory/view_yeka_factory.html',
                      {'yekabussinessblog': yekabussinessblog, 'urls': urls, 'current_url': current_url,
                       'url_name': url_name, 'name': name, 'factory': factory
                       })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required
def add_yeka_factory(request, uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    yeka_factory = YekaFactory.objects.get(uuid=uuid)
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)

        name = ''

        if Yeka.objects.filter(business=yeka_factory.business):
            name = Yeka.objects.get(business=yeka_factory.business).definition
        elif YekaCompetition.objects.filter(business=yeka_factory.business):
            name = YekaCompetition.objects.get(business=yeka_factory.business).name

        with transaction.atomic():
            factory_form = FactoryForm()

            if request.method == 'POST':
                factory_form = FactoryForm(request.POST or None, request.FILES or None)
                if factory_form.is_valid():
                    form = factory_form.save(request, commit=False)
                    form.save()
                    yeka_factory.factory.add(form)
                    yeka_factory.save()
                    messages.success(request, 'Fabrika kayıt edildi.')
                    return redirect('ekabis:update_factory', form.uuid)
                else:
                    error_messages = get_error_messages(factory_form)
                    return render(request, 'Factory/add_yeka_factory.html',
                                  {'factory_form': factory_form, 'yeka_factory': yeka_factory,
                                   'error_messages': error_messages, 'urls': urls, 'current_url': current_url,
                                   'url_name': url_name, 'name': name,
                                   })

            return render(request, 'Factory/add_yeka_factory.html',
                          {'factory_form': factory_form, 'yeka_factory': yeka_factory,
                           'business': yeka_factory.business,
                           'yekabussinessblog': yeka_factory.yekabusinessblog, 'urls': urls, 'current_url': current_url,
                           'url_name': url_name, 'name': name
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka_factory', yeka_factory.business.uuid, yeka_factory.yekabusinessblog.uuid)


@login_required
def update_yeka_factory(request, uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    factory = Factory.objects.get(uuid=uuid)
    yeka_factory = YekaFactory.objects.get(factory=factory)

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)

        name = ''
        if Yeka.objects.filter(business=yeka_factory.business):
            name = Yeka.objects.get(business=yeka_factory.business).definition
        elif YekaCompetition.objects.filter(business=yeka_factory.business):
            name = YekaCompetition.objects.get(business=yeka_factory.business).name

        with transaction.atomic():
            factory_form = FactoryForm(request.POST or None, request.FILES or None, instance=factory)

            if request.method == 'POST':
                if factory_form.is_valid():
                    form = factory_form.save(request, commit=False)
                    form.save()
                    yeka_factory.factory.add(form)
                    yeka_factory.save()
                    messages.success(request, 'Fabrika kayıt edildi.')
                    return redirect('ekabis:view_yeka_factory', yeka_factory.business.uuid,
                                    yeka_factory.yekabusinessblog.uuid)
                else:
                    error_messages = get_error_messages(factory_form)
                    return render(request, 'Factory/update_yeka_factory.html',
                                  {'factory_form': factory_form, 'yeka_factory': yeka_factory,'factory':factory,
                                   'error_messages': error_messages, 'urls': urls, 'current_url': current_url,
                                   'url_name': url_name, 'name': name,
                                   })

            return render(request, 'Factory/update_yeka_factory.html',
                          {'factory_form': factory_form, 'yeka_factory': yeka_factory,
                           'business': yeka_factory.business,'factory':factory,
                           'yekabussinessblog': yeka_factory.yekabusinessblog, 'urls': urls, 'current_url': current_url,
                           'url_name': url_name, 'name': name
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka_factory', yeka_factory.business.uuid, yeka_factory.yekabusinessblog.uuid)


@login_required
def add_factory_file(request, uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    factory = Factory.objects.get(uuid=uuid)
    yeka_factory = YekaFactory.objects.get(factory=factory)

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)

        name = ''

        if Yeka.objects.filter(business=yeka_factory.business):
            name = Yeka.objects.get(business=yeka_factory.business).definition
        elif YekaCompetition.objects.filter(business=yeka_factory.business):
            name = YekaCompetition.objects.get(business=yeka_factory.business).name

        with transaction.atomic():
            factory_form = FactoryFileForm()

            if request.method == 'POST':
                factory_form = FactoryFileForm(request.POST or None, request.FILES or None)
                if factory_form.is_valid():
                    form = factory_form.save(request, commit=False)
                    form.save()
                    factory.file.add(form)
                    factory.save()
                    messages.success(request, 'Doküman kayıt edildi.')
                    return redirect('ekabis:update_factory', uuid)
                else:
                    error_messages = get_error_messages(factory_form)
                    return render(request, 'Factory/add_factory_file.html',
                                  {'factory_form': factory_form, 'yeka_factory': yeka_factory,'factory':factory,
                                   'error_messages': error_messages, 'urls': urls, 'current_url': current_url,
                                   'url_name': url_name, 'name': name,
                                   })

            return render(request, 'Factory/add_factory_file.html',
                          {'factory_form': factory_form, 'yeka_factory': yeka_factory,
                           'business': yeka_factory.business,'factory':factory,
                           'yekabussinessblog': yeka_factory.yekabusinessblog, 'urls': urls, 'current_url': current_url,
                           'url_name': url_name, 'name': name
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka_factory', yeka_factory.business.uuid, yeka_factory.yekabusinessblog.uuid)



@login_required
def update_factory_file(request, uuid,factory_uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    file = FactoryFile.objects.get(uuid=uuid)
    factory=Factory.objects.get(uuid=factory_uuid)
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)

        factory_form = FactoryFileForm(request.POST or None, request.FILES or None,instance=file)

        with transaction.atomic():

            if request.method == 'POST':
                if factory_form.is_valid():
                    form = factory_form.save(request, commit=False)
                    form.save()
                    messages.success(request, 'Doküman güncellendi.')
                    return redirect('ekabis:update_factory', factory_uuid)
                else:
                    error_messages = get_error_messages(factory_form)
                    return render(request, 'Factory/update_factory_file.html',
                                  {'factory_form': factory_form, 'factory':factory,
                                   'error_messages': error_messages, 'urls': urls, 'current_url': current_url,
                                   'url_name': url_name,
                                   })

            return render(request, 'Factory/update_factory_file.html',
                          {'factory_form': factory_form,
                           'factory':factory,
                            'urls': urls, 'current_url': current_url,
                           'url_name': url_name,
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:update_factory', factory_uuid)

@login_required
def delete_factory(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']
                filter = {
                    'uuid': uuid
                }

                data_as_json_pre = serializers.serialize('json', Factory.objects.filter(uuid=uuid))
                obj = FactoryGetService(request, filter)
                log = str(obj.name) + " - fabrika silindi."
                logs = Logs(user=request.user, subject=log, ip=get_client_ip(request), previousData=data_as_json_pre)
                logs.save()
                obj.isDeleted = True
                obj.save()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')

@login_required
def delete_factory_file(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']
                filter = {
                    'uuid': uuid
                }

                data_as_json_pre = serializers.serialize('json', Factory.objects.filter(uuid=uuid))
                obj = FactoryFileGetService(request, filter)
                log = str(obj.name) + " - doküman silindi."
                logs = Logs(user=request.user, subject=log, ip=get_client_ip(request), previousData=data_as_json_pre)
                logs.save()
                obj.isDeleted = True
                obj.save()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')
