
import datetime
import traceback
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import resolve

from ekabis.Forms.ExtraTimeForm import ExtraTimeForm
from ekabis.Forms.YekaApplicationForm import YekaApplicationForm
from ekabis.models import YekaBusiness, YekaCompetition, Permission
from ekabis.models.Yeka import Yeka
from ekabis.models.YekaApplicationFile import YekaApplicationFile
from ekabis.models.YekaBusinessBlog import YekaBusinessBlog
from ekabis.services import general_methods
from ekabis.services.general_methods import get_error_messages
from ekabis.services.services import ExtraTimeGetService, last_urls, \
    NewspaperGetService, NewspaperService, YekaApplicationFileNameService, YekaApplicationFileNameGetService, \
    YekaApplicationGetService, YekaApplicationService, YekaBusinessService, YekaBusinessGetService, \
    YekaBusinessBlogGetService, YekaApplicationFileGetService

from ekabis.Forms.NewspaperForm import NewspaperForm
from ekabis.Forms.YekaApplicationFileForm import YekaApplicationFileForm
# test amaclı yazıldı silinecek
from ekabis.models.YekaApplication import YekaApplication

from ekabis.Forms.YekaApplicationFileNameForm import YekaApplicationFileName, YekaApplicationFileNameForm


@login_required
def add_newspaper(request, business, businessblog):
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

        newspaper_form = NewspaperForm()

        newspapers =NewspaperService(request,None)
        with transaction.atomic():
            if request.method == 'POST':
                newspaper_form = NewspaperForm(request.POST , request.FILES)
                if newspaper_form.is_valid():
                    newspaper = newspaper_form.save(commit=False)
                    newspaper.yekabusinessblog = yekabussinessblog
                    newspaper.business = yekabusiness
                    newspaper.save()
                    messages.success(request, 'Resmi Gazete Eklenmiştir Edilmiştir.')
                    return redirect('ekabis:view_newspaper')
                else:
                    error_messages = get_error_messages(newspaper_form)
                    return render(request, 'Newspaper/add_newspaper.html',
                                  {'newspaper_formv': newspaper_form,
                                   'error_messages': error_messages, 'urls': urls, 'current_url': current_url,
                                   'url_name': url_name, 'name': name,
                                   })

            return render(request, 'Newspaper/add_newspaper.html',
                          {'newspaper_form': newspaper_form,
                           'business': business, 'newspapers': newspapers,
                           'yekabussinessblog': yekabussinessblog, 'urls': urls, 'current_url': current_url,
                           'url_name': url_name, 'name': name
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yekabusinessBlog', business.uuid)


@login_required
def view_newspaper(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    ExtraTimefilter = {
        'isDeleted': False

    }
    ekstratime = []
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    for item in NewspaperService(request, ExtraTimefilter).order_by('-creationDate'):
        if Yeka.objects.filter(business=item.business):
            time = {
                'yeka': Yeka.objects.get(business=item.business).definition,
                'blogname': item.yekabusinessblog.businessblog.name,
                'uuid': item.uuid,
                'listingDate': item.listingDate,
                'newspaperCount': item.newspaperCount,
                'newspapwerText': item.newspapwerText,
                'file': item.file,
                'creationDate': item.creationDate,

            }


        elif YekaCompetition.objects.filter(business=item.business):
            time = {
                'yeka': YekaCompetition.objects.get(business=item.business).name,
                'blogname': item.yekabusinessblog.businessblog.name,
                'uuid': item.uuid,
                'listingDate': item.listingDate,
                'newspaperCount': item.newspaperCount,
                'newspapwerText': item.newspapwerText,
                'file': item.file,
                'creationDate': item.creationDate,

            }
        else:
            time = {
                'yeka': None,
                'blogname': item.yekabusinessblog.businessblog.name,
                'time': item.time,
                'uuid': item.uuid,
                'listingDate': item.listingDate,
                'newspaperCount': item.newspaperCount,
                'newspapwerText': item.newspapwerText,
                'file': item.file,
                'creationDate': item.creationDate,
            }
        ekstratime.append(time)
    return render(request, 'Newspaper/view_newspaper.html',
                  {'ekstratime': ekstratime, 'urls': urls, 'current_url': current_url, 'url_name': url_name})


@login_required
def change_newspaper(request, uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    newspaper_filter = {
        'uuid': uuid
    }
    newspaper = NewspaperGetService(request, newspaper_filter)

    newspaper_form = NewspaperForm(request.POST or None, request.FILES or None, instance=newspaper)
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        with transaction.atomic():
            if request.method == 'POST':
                if newspaper_form.is_valid():
                    newspaper_form.save()
                    messages.success(request, 'Resmi Gazete Güncellenmiştir')
                    return redirect('ekabis:view_newspaper')
                else:
                    error_messages = get_error_messages(newspaper_form)
                    return render(request, 'Newspaper/change_newspaper.html',
                                  {'newspaper_form': newspaper_form,
                                   'error_messages': error_messages, 'urls': urls, 'current_url': current_url,
                                   'url_name': url_name

                                   })

            return render(request, 'Newspaper/change_newspaper.html',
                          {'newspaper_form': newspaper_form, 'urls': urls, 'current_url': current_url,
                           'url_name': url_name

                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required
def delete_newspaper(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']
                newspaper_filter = {
                    'uuid': uuid
                }
                obj = NewspaperGetService(request, newspaper_filter)
                obj.isDeleted = True
                obj.save()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})


            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

#
# basvuru dosya isimleri

@login_required
def add_yekaapplicationfilename(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)

        filename_form = YekaApplicationFileNameForm()

        filenames =YekaApplicationFileNameService(request,None)
        with transaction.atomic():
            if request.method == 'POST':
                filename_form = YekaApplicationFileNameForm(request.POST , request.FILES)
                if filename_form.is_valid():
                    filename= filename_form.save(commit=False)
                    filename.save()
                    messages.success(request, 'Dosya ismi  Eklenmiştir .')
                    return redirect('ekabis:view_yekaapplicationfilename')
                else:
                    error_messages = get_error_messages(filename_form)
                    return render(request, 'Application/add_applicationfilename.html',
                                  {'filename_form': filename_form,
                                   'error_messages': error_messages, 'urls': urls, 'current_url': current_url,
                                   'url_name': url_name, 'filenames': filenames,
                                   })

            return render(request, 'Application/add_applicationfilename.html',
                          {'filename_form': filename_form,
                            'filenames': filenames,
                         'urls': urls, 'current_url': current_url,
                           'url_name': url_name,
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required
def view_yekaapplicationfilename(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    ExtraTimefilter = {
        'isDeleted': False

    }
    ekstratime = []
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    filenames=YekaApplicationFileNameService(request, ExtraTimefilter).order_by('-creationDate')

    return render(request, 'Application/view_applicationfilename.html',
                  {'filenames': filenames, 'urls': urls, 'current_url': current_url, 'url_name': url_name})


@login_required
def change_yekaapplicationfilename(request, uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    filename_filter = {
        'uuid': uuid
    }
    filename = YekaApplicationFileNameGetService(request, filename_filter)

    filename_form = YekaApplicationFileNameForm(request.POST or None, instance=filename)
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        with transaction.atomic():
            if request.method == 'POST':
                if filename_form.is_valid():
                    filename_form.save()
                    messages.success(request, 'Dosya İsmi  Güncellenmiştir')
                    return redirect('ekabis:view_yekaapplicationfilename')
                else:
                    error_messages = get_error_messages(filename_form)
                    return render(request, 'Application/change_applicationfilename.html',
                                  {'filename_form': filename_form,
                                   'error_messages': error_messages, 'urls': urls, 'current_url': current_url,
                                   'url_name': url_name

                                   })

            return render(request, 'Application/change_applicationfilename.html',
                          {'filename_form': filename_form, 'urls': urls, 'current_url': current_url,
                           'url_name': url_name

                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required
def delete_yekaapplicationfilename(request):
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
                obj = YekaApplicationFileNameGetService(request, filter)
                obj.isDeleted = True
                obj.save()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})


            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})



#basvuru ayarları

@login_required
def add_yekaapplication(request, business, businessblog):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)

        yekabusiness = YekaBusiness.objects.get(uuid=business)
        filter={
            'business':yekabusiness
        }
        if YekaApplicationService(request,filter):
           return  redirect('ekabis:change_yekaapplication',YekaApplicationGetService(request,filter).uuid )
        yekabussinessblog = YekaBusinessBlog.objects.get(uuid=businessblog)
        YekaApplication
        name = ''
        if Yeka.objects.filter(business=yekabusiness):
            name = Yeka.objects.get(business=yekabusiness).definition
        elif YekaCompetition.objects.filter(business=yekabusiness):
            name = YekaCompetition.objects.get(business=yekabusiness).name

        application_form = YekaApplicationForm()
        files=YekaApplicationFileNameService(request,None)
        with transaction.atomic():
            if request.method == 'POST':
                application_form = YekaApplicationForm(request.POST , request.FILES)
                if application_form.is_valid():
                    application = application_form.save(commit=False)
                    application.yekabusinessblog = yekabussinessblog
                    application.business = yekabusiness
                    application.save()

                    for item in files:
                        if request.POST.get(str(item.pk)):
                            application.necessary.add(item)
                            application.save()


                    messages.success(request, 'Basarıyla Eklenmiştir.')
                    return redirect('ekabis:change_yekaapplication',application.uuid)
                else:
                    error_messages = get_error_messages(application_form)
                    return render(request, 'Application/add_application.html',
                                  {'application_form': application_form,
                                   'error_messages': error_messages, 'urls': urls, 'current_url': current_url,
                                   'url_name': url_name, 'name': name,'files':files
                                   })

            return render(request, 'Application/add_application.html',
                          {'application_form': application_form,
                           'business': business,
                           'yekabussinessblog': yekabussinessblog, 'urls': urls, 'current_url': current_url,
                           'url_name': url_name, 'name': name,'files':files
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka',)



@login_required
def change_yekaapplication(request,uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        filter={
            'uuid':uuid
        }
        application=YekaApplicationGetService(request,filter)
        yekabusiness = application.business
        yekabussinessblog = application.yekabusinessblog

        name = ''
        if Yeka.objects.filter(business=yekabusiness):
            name = Yeka.objects.get(business=yekabusiness).definition
        elif YekaCompetition.objects.filter(business=yekabusiness):
            name = YekaCompetition.objects.get(business=yekabusiness).name

        application_form = YekaApplicationForm(request.POST or None,instance=application)
        file=[]
        for item in application.necessary.all():
            file.append(item.pk)
        files=YekaApplicationFileName.objects.exclude(pk__in=file,isDeleted=False)
        with transaction.atomic():
            if request.method == 'POST':
                if application_form.is_valid():
                    app = application_form.save(commit=False)
                    app.yekabusinessblog = yekabussinessblog
                    app.business = yekabusiness
                    app.save()
                    for item in YekaApplicationFileNameService(request,None):
                        try:
                            if request.POST.get(str(item.pk)):
                                if app.necessary.filter(uuid=item.uuid,isDeleted=False) != None:
                                    app.necessary.add(item)
                                    app.save()
                            else:
                                if app.necessary.filter(uuid=item.uuid,isDeleted=False) != None:
                                    app.necessary.remove(item)
                                    app.save()

                        except Exception as e:
                            print(e)
                            traceback.print_exc()

                    messages.success(request, 'Basarıyla Güncellenmistir.')
                    return redirect('ekabis:change_yekaapplication',app.uuid)
                else:
                    error_messages = get_error_messages(application_form)
                    return render(request, 'Application/change_application.html',
                                  {'application_form': application_form,
                                   'error_messages': error_messages, 'urls': urls, 'current_url': current_url,
                                   'url_name': url_name, 'name': name,'files':files,'application':application
                                   })

            return render(request, 'Application/change_application.html',
                          {'application_form': application_form,
                           'yekabussinessblog': yekabussinessblog, 'urls': urls, 'current_url': current_url,
                           'url_name': url_name, 'name': name,'files':files,'application':application
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka',)

#basvurular

@login_required
def view_application(request,business,businessblog):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    filter = {
        'uuid': business
    }
    yekabusiness=YekaBusinessGetService(request,filter)
    filter={
        'uuid':businessblog
    }
    businessblog=YekaBusinessBlogGetService(request,filter)

    filter={
        'business':yekabusiness
    }
    application=YekaApplicationGetService(request,filter)


    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)

    return render(request, 'Application/view_application.html',
                  {'application': application, 'urls': urls, 'current_url': current_url, 'url_name': url_name})



@login_required
def view_applicationfile(request,business,businessblog,applicationfile):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        filter = {
            'uuid': business
        }
        yekabusiness = YekaBusinessGetService(request, filter)
        filter = {
            'uuid': businessblog
        }
        businessblog = YekaBusinessBlogGetService(request, filter)

        filter = {
            'business': yekabusiness
        }
        application = YekaApplicationGetService(request, filter)

        filter = {
            'uuid': applicationfile
        }
        applicationfile = YekaApplicationFileGetService(request, filter)
        filename_form = YekaApplicationFileForm(request.POST or None,request.FILES or None, instance=applicationfile)
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        with transaction.atomic():
            if request.method == 'POST':
                if filename_form.is_valid():
                    filename_form.save()
                    messages.success(request, 'Dosya Güncellenmiştir')
                    return redirect('ekabis:view_application',yekabusiness.uuid,businessblog.uuid)
                else:
                    error_messages = get_error_messages(filename_form)
                    return render(request, 'Application/view_applicationfile.html',
                                  {'application': application,
                                   'urls': urls,
                                   'current_url': current_url,
                                   'url_name': url_name,
                                   'error_messages': error_messages,
                                   'filename_form':filename_form
                                   })
            return render(request, 'Application/view_applicationfile.html',
                          {'application': application, 'urls': urls,
                           'current_url': current_url, 'url_name': url_name,
                           'filename_form':filename_form
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')

#yarisma

@login_required
def view_competition(request,business,businessblog):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    filter = {
        'uuid': business
    }
    yekabusiness=YekaBusinessGetService(request,filter)
    filter={
        'uuid':businessblog
    }
    businessblog=YekaBusinessBlogGetService(request,filter)

    filter={
        'business':yekabusiness
    }
    application=YekaApplicationGetService(request,filter)


    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)

    return render(request, 'Application/view_application.html',
                  {'application': application, 'urls': urls, 'current_url': current_url, 'url_name': url_name})


@login_required
def add_competition_company(request,business,businessblog,applicationfile):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        filter = {
            'uuid': business
        }
        yekabusiness = YekaBusinessGetService(request, filter)
        filter = {
            'uuid': businessblog
        }
        businessblog = YekaBusinessBlogGetService(request, filter)

        filter = {
            'business': yekabusiness
        }
        application = YekaApplicationGetService(request, filter)

        filter = {
            'uuid': applicationfile
        }
        applicationfile = YekaApplicationFileGetService(request, filter)
        filename_form = YekaApplicationFileForm(request.POST or None,request.FILES or None, instance=applicationfile)
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        with transaction.atomic():
            if request.method == 'POST':
                if filename_form.is_valid():
                    filename_form.save()
                    messages.success(request, 'Dosya Güncellenmiştir')
                    return redirect('ekabis:view_application',yekabusiness.uuid,businessblog.uuid)
                else:
                    error_messages = get_error_messages(filename_form)
                    return render(request, 'Application/view_applicationfile.html',
                                  {'application': application,
                                   'urls': urls,
                                   'current_url': current_url,
                                   'url_name': url_name,
                                   'error_messages': error_messages,
                                   'filename_form':filename_form
                                   })
            return render(request, 'Application/view_applicationfile.html',
                          {'application': application, 'urls': urls,
                           'current_url': current_url, 'url_name': url_name,
                           'filename_form':filename_form
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')
