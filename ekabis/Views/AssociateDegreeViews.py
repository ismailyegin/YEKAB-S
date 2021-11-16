import traceback

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import resolve

from ekabis.Forms.AssociateFileForm import AssociateFileForm
from ekabis.Forms.AssociateFileNameForm import AssociateFileNameForm
from ekabis.Forms.FactoryFileNameForm import FactoryFileNameForm
from ekabis.models import Permission, Logs, YekaBusiness, YekaBusinessBlog, Yeka, YekaCompetition
from ekabis.models.AssociateDegreeFile import AssociateDegreeFile
from ekabis.models.AssociateDegreeFileName import AssociateDegreeFileName
from ekabis.models.YekaAssociateDegree import YekaAssociateDegree

from ekabis.services import general_methods
from ekabis.services.general_methods import get_error_messages, get_client_ip
from ekabis.services.services import last_urls, AssociateFileNameService, AssociateFileNameGetService, \
    AssociateFileGetService

# Adding the document name of the associate degree business plan
@login_required
def add_associate_file_name(request):
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
                file_name_form = AssociateFileNameForm(request.POST or None)
                if file_name_form.is_valid():
                    form = file_name_form.save(request, commit=False)
                    form.save()
                    messages.success(request, 'Döküman isim eklenmiştir.')
                    return redirect('ekabis:view_associate_file_name')
                else:
                    error_messages = get_error_messages(file_name_form)
                    return render(request, 'AssociateDegree/add_associate_degree_filename.html',
                                  {'file_name_form': file_name_form,
                                   'error_messages': error_messages, 'urls': urls, 'current_url': current_url,
                                   'url_name': url_name.name
                                   })

        return render(request, 'AssociateDegree/add_associate_degree_filename.html',
                      {'file_name_form': file_name_form, 'urls': urls, 'current_url': current_url, 'url_name': url_name.name

                       })

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_associate_file_name')

# Listing the document name of the associate degree business plan
@login_required
def view_associate_file_name(request):
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    file_names = AssociateFileNameService(request, None)
    return render(request, 'AssociateDegree/view_associate_filename.html',
                  {'file_names': file_names, 'urls': urls, 'current_url': current_url, 'url_name': url_name.name})
# update document name of factory business block
@login_required
def change_factory_file_name(request, uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    filter = {
        'uuid': uuid
    }
    file = AssociateFileNameGetService(request, filter)
    file_name_form = AssociateFileNameForm(request.POST or None, instance=file)

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        if request.method == 'POST':
            with transaction.atomic():
                if file_name_form.is_valid():
                    form = file_name_form.save(request, commit=False)
                    form.save()
                    messages.success(request, 'Döküman ismi güncellenmiştir.')
                    return redirect('ekabis:view_associate_file_name')
                else:
                    error_messages = get_error_messages(file_name_form)
                    return render(request, 'AssociateDegree/change_associate_filename.html',
                                  {'file_name_form': file_name_form,
                                   'error_messages': error_messages, 'urls': urls, 'current_url': current_url,
                                   'url_name': url_name.name
                                   })

        return render(request, 'AssociateDegree/change_associate_filename.html',
                      {'file_name_form': file_name_form, 'urls': urls, 'current_url': current_url, 'url_name': url_name.name,
                       'error_messages': '',
                       })

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_associate_file_name')

# deleting the document name of the associate degree business plan
@login_required
def delete_associate_file_name(request):
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

                data_as_json_pre = serializers.serialize('json', AssociateDegreeFileName.objects.filter(uuid=uuid))
                obj = AssociateFileNameGetService(request, filter)
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

        return redirect('ekabis:view_associate_file_name')

# YEKA's associate degree work block information
@login_required
def view_yeka_associate_degree(request, business, businessblog):
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
        name = general_methods.yekaname(yekabusiness)

        if not YekaAssociateDegree.objects.filter(business=yekabusiness):
            associate = YekaAssociateDegree()
            associate.yekabusinessblog = yekabussinessblog
            associate.business = yekabusiness
            associate.save()
            files = associate.associateDegree.filter(isDeleted=False)

        else:
            associate = YekaAssociateDegree.objects.get(business=yekabusiness)
            files = associate.associateDegree.filter(isDeleted=False)

        return render(request, 'AssociateDegree/view_yeka_associate_file.html',
                      {'yekabussinessblog': yekabussinessblog, 'urls': urls, 'current_url': current_url,
                       'url_name': url_name.name, 'name': name, 'associate': associate, 'files': files,
                       })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')

# add document to associate degree business block
@login_required
def add_associate_file(request, uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    yeka_associate = YekaAssociateDegree.objects.get(business__uuid=uuid)
    associate = yeka_associate.associateDegree
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)

        name = general_methods.yekaname(yeka_associate.business)

        with transaction.atomic():
            associate_file_form = AssociateFileForm()

            if request.method == 'POST':
                associate_file_form = AssociateFileForm(request.POST or None, request.FILES or None)
                if associate_file_form.is_valid():
                    form = associate_file_form.save(request, commit=False)
                    form.save()
                    yeka_associate.associateDegree.add(form)
                    yeka_associate.save()
                    messages.success(request, 'Doküman kayıt edildi.')
                    return redirect('ekabis:view_yeka_associate_degree_file', yeka_associate.business.uuid,
                                    yeka_associate.yekabusinessblog.uuid)
                else:
                    error_messages = get_error_messages(associate_file_form)
                    return render(request, 'AssociateDegree/add_associate_file.html',
                                  {'associate_file_form': associate_file_form, 'business': yeka_associate.business,
                                   'yekabussinessblog': yeka_associate.yekabusinessblog,
                                   'error_messages': error_messages, 'urls': urls, 'current_url': current_url,
                                   'url_name': url_name.name, 'name': name,
                                   })

            return render(request, 'AssociateDegree/add_associate_file.html',
                          {'associate_file_form': associate_file_form,
                           'business': yeka_associate.business,
                           'yekabussinessblog': yeka_associate.yekabusinessblog, 'urls': urls,
                           'current_url': current_url,
                           'url_name': url_name.name, 'name': name
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka_associate_degree_file', yeka_associate.business.uuid,
                        yeka_associate.yekabusinessblog.uuid)

# change document to associate degree business block
@login_required
def change_associate_file(request, uuid, yeka_associate):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    associate_file = AssociateDegreeFile.objects.get(uuid=uuid)
    yeka_associate = YekaAssociateDegree.objects.get(uuid=yeka_associate)
    associate_file_form = AssociateFileForm(request.POST or None, request.FILES or None, instance=associate_file)

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)

        with transaction.atomic():

            if request.method == 'POST':
                if associate_file_form.is_valid():
                    form = associate_file_form.save(request, commit=False)
                    form.save()
                    messages.success(request, 'Doküman güncellendi.')
                    return redirect('ekabis:view_yeka_associate_degree_file', yeka_associate.business.uuid,
                                    yeka_associate.yekabusinessblog.uuid)
                else:
                    error_messages = get_error_messages(associate_file_form)
                    return render(request, 'AssociateDegree/add_associate_file.html',
                                  {'associate_file_form': associate_file_form, 'business': yeka_associate.business,
                                   'yekabussinessblog': yeka_associate.yekabusinessblog,
                                   'error_messages': error_messages, 'urls': urls, 'current_url': current_url,
                                   'url_name': url_name.name,
                                   })

            return render(request, 'AssociateDegree/add_associate_file.html',
                          {'associate_file_form': associate_file_form,
                           'business': yeka_associate.business,
                           'yekabussinessblog': yeka_associate.yekabusinessblog, 'urls': urls,
                           'current_url': current_url,
                           'url_name': url_name.name,
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka_associate_degree_file', yeka_associate.business.uuid,
                        yeka_associate.yekabusinessblog.uuid)

# delete document to associate degree business block
@login_required
def delete_associate_file(request):
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

                data_as_json_pre = serializers.serialize('json', AssociateDegreeFile.objects.filter(uuid=uuid))
                obj = AssociateFileGetService(request, filter)
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

        return redirect('ekabis:view_associate_file_name')
