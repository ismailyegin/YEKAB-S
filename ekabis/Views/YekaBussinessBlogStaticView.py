import traceback

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import resolve

from ekabis.Forms.CoordinateForm import CoordinateForm
from ekabis.Forms.LocationForm import LocationForm
from ekabis.models.Coordinate import Coordinate
from ekabis.models.Location import Location

from ekabis.Forms.CompetitionCompanyForm import CompetitionCompanyForm
from ekabis.Forms.CompetitionForm import CompetitionForm
from ekabis.Forms.InstitutionForm import InstitutionForm
from ekabis.Forms.NewspaperForm import NewspaperForm
from ekabis.Forms.ProposalForm import ProposalForm
from ekabis.Forms.YekaApplicationFileForm import YekaApplicationFileForm
from ekabis.Forms.YekaApplicationFileNameForm import YekaApplicationFileName, YekaApplicationFileNameForm
from ekabis.Forms.YekaApplicationForm import YekaApplicationForm
from ekabis.Forms.YekaContractForm import YekaContract, YekaContractForm
from ekabis.models import YekaBusiness, YekaCompetition, Permission, Company, Logs, CompanyUser, ConnectionRegion, \
    YekaCompany
from ekabis.models.Competition import Competition
from ekabis.models.CompetitionCompany import CompetitionCompany
from ekabis.models.Institution import Institution
from ekabis.models.Newspaper import Newspaper
from ekabis.models.Proposal import Proposal
from ekabis.models.ProposalActive import ProposalActive
from ekabis.models.Proposalnstitution import ProposalInstitution
from ekabis.models.Yeka import Yeka
# test amaclı yazıldı silinecek
from ekabis.models.CompetitionApplication import CompetitionApplication
from ekabis.models.YekaBusinessBlog import YekaBusinessBlog
from ekabis.models.YekaProposal import YekaProposal
from ekabis.services import general_methods
from ekabis.services.general_methods import get_client_ip
from ekabis.services.general_methods import get_error_messages
from ekabis.services.services import last_urls, \
    NewspaperGetService, NewspaperService, YekaApplicationFileNameService, YekaApplicationFileNameGetService, \
    YekaApplicationGetService, YekaApplicationService, YekaBusinessGetService, \
    YekaBusinessBlogGetService, YekaApplicationFileGetService
from ekabis.models.YekaUser import YekaUser
from ekabis.Forms.YekaUserForm import YekaUserForm
from ekabis.models.YekaCompanyUser import YekaCompanyUser

from ekabis.Forms.ProposalInstitutionForm import ProposalInstitutionForm


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

        name = general_methods.yekaname(yekabusiness)

        newspaper_form = NewspaperForm()
        newspaper_filter = {
            'business': yekabusiness

        }
        newspapers = NewspaperService(request, newspaper_filter)
        with transaction.atomic():
            if request.method == 'POST':
                newspaper_form = NewspaperForm(request.POST, request.FILES)
                if newspaper_form.is_valid():

                    newspaper = newspaper_form.save(commit=False)
                    newspaper.yekabusinessblog = yekabussinessblog
                    newspaper.business = yekabusiness
                    newspaper.save()
                    messages.success(request, 'Resmi Gazete Eklenmiştir Edilmiştir.')
                    return redirect('ekabis:add_newspaper', business, businessblog)
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
        return redirect('ekabis:view_yekabusinessBlog', yekabusiness.uuid)


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
    name = general_methods.yekaname(newspaper.business)

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        with transaction.atomic():
            if request.method == 'POST':
                if newspaper_form.is_valid():
                    newspaper_form.save(request)
                    messages.success(request, 'Resmi Gazete Güncellenmiştir')
                    return redirect('ekabis:add_newspaper', newspaper.business.uuid, newspaper.yekabusinessblog.uuid)
                else:
                    error_messages = get_error_messages(newspaper_form)
                    return render(request, 'Newspaper/change_newspaper.html',
                                  {'newspaper_form': newspaper_form,
                                   'error_messages': error_messages, 'urls': urls, 'current_url': current_url,
                                   'url_name': url_name, 'name': name

                                   })

            return render(request, 'Newspaper/change_newspaper.html',
                          {'newspaper_form': newspaper_form, 'urls': urls, 'current_url': current_url,
                           'url_name': url_name, 'name': name

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
                data_as_json_pre = serializers.serialize('json', Newspaper.objects.filter(uuid=uuid))
                obj.isDeleted = True
                obj.save()
                log = str(obj.file) + " - gazete silindi."
                logs = Logs(user=request.user, subject=log, ip=get_client_ip(request), previousData=data_as_json_pre)
                logs.save()
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

        filenames = YekaApplicationFileNameService(request, None)
        with transaction.atomic():
            if request.method == 'POST':
                filename_form = YekaApplicationFileNameForm(request.POST, request.FILES)
                if filename_form.is_valid():
                    filename = filename_form.save(request, commit=False)
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
    filenames = YekaApplicationFileNameService(request, ExtraTimefilter).order_by('-creationDate')

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
                    filename_form.save(request)
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
                data_as_json_pre = serializers.serialize('json', Newspaper.objects.filter(uuid=uuid))
                obj.isDeleted = True
                obj.save()
                log = str(obj.filename) + " - doküman ismi silindi."
                logs = Logs(user=request.user, subject=log, ip=get_client_ip(request), previousData=data_as_json_pre)
                logs.save()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})


            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


# basvuru ayarları

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
        filter = {
            'business': yekabusiness
        }
        if YekaApplicationService(request, filter):
            return redirect('ekabis:change_yekaapplication', YekaApplicationGetService(request, filter).uuid)
        yekabussinessblog = YekaBusinessBlog.objects.get(uuid=businessblog)
        name = general_methods.yekaname(yekabusiness)

        application_form = YekaApplicationForm()
        files = YekaApplicationFileNameService(request, None)
        with transaction.atomic():
            if request.method == 'POST':
                application_form = YekaApplicationForm(request.POST, request.FILES)
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
                    return redirect('ekabis:change_yekaapplication', application.uuid)
                else:
                    error_messages = get_error_messages(application_form)
                    return render(request, 'Application/add_application.html',
                                  {'application_form': application_form,
                                   'error_messages': error_messages, 'urls': urls, 'current_url': current_url,
                                   'url_name': url_name, 'name': name, 'files': files
                                   })

            return render(request, 'Application/add_application.html',
                          {'application_form': application_form,
                           'business': business,
                           'yekabussinessblog': yekabussinessblog, 'urls': urls, 'current_url': current_url,
                           'url_name': url_name, 'name': name, 'files': files
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka', )


@login_required
def change_yekaapplication(request, uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        filter = {
            'uuid': uuid
        }
        application = YekaApplicationGetService(request, filter)
        yekabusiness = application.business
        yekabussinessblog = application.yekabusinessblog

        name = general_methods.yekaname(yekabusiness)

        application_form = YekaApplicationForm(request.POST or None, instance=application)
        file = []
        for item in application.necessary.all():
            file.append(item.pk)
        files = YekaApplicationFileName.objects.exclude(pk__in=file, isDeleted=False)
        with transaction.atomic():
            if request.method == 'POST':
                if application_form.is_valid():
                    app = application_form.save(commit=False)
                    app.yekabusinessblog = yekabussinessblog
                    app.business = yekabusiness
                    app.save()
                    for item in YekaApplicationFileNameService(request, None):
                        try:
                            if request.POST.get(str(item.pk)):
                                if app.necessary.filter(uuid=item.uuid, isDeleted=False) != None:
                                    app.necessary.add(item)
                                    app.save()
                            else:
                                if app.necessary.filter(uuid=item.uuid, isDeleted=False) != None:
                                    app.necessary.remove(item)
                                    app.save()

                        except Exception as e:
                            print(e)
                            traceback.print_exc()

                    messages.success(request, 'Basarıyla Güncellenmistir.')
                    return redirect('ekabis:change_yekaapplication', app.uuid)
                else:
                    error_messages = get_error_messages(application_form)
                    return render(request, 'Application/change_application.html',
                                  {'application_form': application_form,
                                   'error_messages': error_messages, 'urls': urls, 'current_url': current_url,
                                   'url_name': url_name, 'name': name, 'files': files, 'application': application
                                   })

            return render(request, 'Application/change_application.html',
                          {'application_form': application_form,
                           'yekabussinessblog': yekabussinessblog, 'urls': urls, 'current_url': current_url,
                           'url_name': url_name, 'name': name, 'files': files, 'application': application
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka', )


# basvurular

@login_required
def view_application(request, business, businessblog):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
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
    if YekaApplicationService(request, filter):
        application = YekaApplicationGetService(request, filter)

        name = general_methods.yekaname(yekabusiness)
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)

        return render(request, 'Application/view_application.html',
                      {'application': application, 'urls': urls, 'current_url': current_url, 'url_name': url_name,
                       'name': name})
    else:
        return redirect('ekabis:add_yekaapplication', yekabusiness.uuid, businessblog.uuid)


@login_required
def view_applicationfile(request, business, businessblog, applicationfile):
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
        filename_form = YekaApplicationFileForm(request.POST or None, request.FILES or None, instance=applicationfile)
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        with transaction.atomic():
            if request.method == 'POST':
                if filename_form.is_valid():
                    filename_form.save(request)
                    messages.success(request, 'Dosya Güncellenmiştir')
                    return redirect('ekabis:view_application', yekabusiness.uuid, businessblog.uuid)
                else:
                    error_messages = get_error_messages(filename_form)
                    return render(request, 'Application/view_applicationfile.html',
                                  {'application': application,
                                   'urls': urls,
                                   'current_url': current_url,
                                   'url_name': url_name,
                                   'error_messages': error_messages,
                                   'filename_form': filename_form
                                   })
            return render(request, 'Application/view_applicationfile.html',
                          {'application': application, 'urls': urls,
                           'current_url': current_url, 'url_name': url_name,
                           'filename_form': filename_form
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


# yarisma ayarları

@login_required
def change_competition(request, business, businessblog):
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
        yekabusinessblog = YekaBusinessBlogGetService(request, filter)

        if not Competition.objects.filter(business=yekabusiness):
            competition = Competition(
                business=yekabusiness,
                yekabusinessblog=yekabusinessblog,
            )
            competition.save()
        else:
            competition = Competition.objects.get(business=yekabusiness)
        competition_form = CompetitionForm(request.POST or None, request.FILES or None, instance=competition)
        name = general_methods.yekaname(yekabusiness)

        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)

        with transaction.atomic():
            if request.method == 'POST':
                if competition_form.is_valid():
                    competition_form.save(request)
                    messages.success(request, 'Yarışma Güncellenmiştir')
                    return redirect('ekabis:change_competition', competition.business.uuid,
                                    competition.yekabusinessblog.uuid)
                else:
                    error_messages = get_error_messages(competition_form)
                    return render(request, 'Competition/change_competition.html',
                                  {'competition_form': competition_form,
                                   'competition': competition,
                                   'urls': urls, 'current_url': current_url,
                                   'url_name': url_name, 'name': name,
                                   'error_messages': error_messages})

            return render(request, 'Competition/change_competition.html',
                          {'competition_form': competition_form,
                           'competition': competition,
                           'urls': urls, 'current_url': current_url,
                           'url_name': url_name, 'name': name})
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required
def add_competition_company(request, competition):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:

        competition = Competition.objects.get(uuid=competition)

        company_form = CompetitionCompanyForm()
        array_exclude = []
        for item in competition.company.all():
            array_exclude.append(item.company.pk)
        # basvurular varsa oradan alınacak yoksa bütün firmalarda alınacak
        if CompetitionApplication.objects.filter(business=competition.business):
            application = CompetitionApplication.objects.get(business=competition.business)
            array = []
            for item in application.companys.all():
                array.append(item.company.pk)
            company_form.fields['company'].queryset = Company.objects.filter(id__in=array).exclude(id__in=array_exclude)
        else:
            company_form.fields['company'].queryset = Company.objects.exclude(id__in=array_exclude)
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        name = general_methods.yekaname(competition.business)

        with transaction.atomic():

            if request.method == 'POST':
                company_form = CompetitionCompanyForm(request.POST or None)
                if company_form.is_valid():
                    company = company_form.save(request, commit=False)
                    company.save()
                    competition.company.add(company)
                    competition.save()
                    messages.success(request, 'Firma  Eklenmistir')
                    return redirect('ekabis:change_competition', competition.business.uuid,
                                    competition.yekabusinessblog.uuid)
                else:
                    error_messages = get_error_messages(company_form)
                    return render(request, 'Competition/add_competition_company.html',
                                  {
                                      'urls': urls,
                                      'current_url': current_url,
                                      'url_name': url_name,
                                      'error_messages': error_messages,
                                      'company_form': company_form, 'name': name
                                  })
            return render(request, 'Competition/add_competition_company.html',
                          {'urls': urls,
                           'current_url': current_url, 'url_name': url_name, 'name': name,
                           'company_form': company_form
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required
def delete_competition_company(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']

                pre = serializers.serialize('json', CompetitionCompany.objects.filter(uuid=uuid))
                obj = CompetitionCompany.objects.get(uuid=uuid)
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


@login_required
def change_competition_company(request, competition, uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        competition = Competition.objects.get(uuid=competition)

        comp_company = CompetitionCompany.objects.get(uuid=uuid)

        company_form = CompetitionCompanyForm(request.POST or None, instance=comp_company)
        array_exclude = []
        for item in competition.company.all():
            if item.company != comp_company.company:
                array_exclude.append(item.company.pk)
        # basvurular varsa oradan alınacak yoksa bütün firmalarda alınacak
        if CompetitionApplication.objects.filter(business=competition.business):
            application = CompetitionApplication.objects.get(business=competition.business)
            array = []
            for item in application.companys.all():
                array.append(item.company.pk)
            company_form.fields['company'].queryset = Company.objects.filter(id__in=array).exclude(id__in=array_exclude)
        else:
            company_form.fields['company'].queryset = Company.objects.exclude(id__in=array_exclude)

        company_form.fields['company'].initial = comp_company.company

        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        with transaction.atomic():
            if request.method == 'POST':
                if company_form.is_valid():
                    company = company_form.save(request, commit=False)
                    company.save()
                    messages.success(request, 'Firma  Güncellenmistir')
                    return redirect('ekabis:change_competition', competition.business.uuid,
                                    competition.yekabusinessblog.uuid)
                else:
                    error_messages = get_error_messages(company_form)
                    return render(request, 'Competition/change_competition_company.html',
                                  {
                                      'urls': urls,
                                      'current_url': current_url,
                                      'url_name': url_name,
                                      'error_messages': error_messages,
                                      'company_form': company_form
                                  })
            return render(request, 'Competition/change_competition_company.html',
                          {'urls': urls,
                           'current_url': current_url, 'url_name': url_name,
                           'company_form': company_form
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


#
# sözleşma alanı


@login_required
def change_yekacontract(request, business, businessblog):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)

        yekabussinessblog = YekaBusinessBlog.objects.get(uuid=businessblog)
        yekabusiness = YekaBusiness.objects.get(uuid=business)
        filter = {
            'business': yekabusiness
        }

        contract = None
        if YekaContract.objects.filter(business=yekabusiness):
            contract = YekaContract.objects.get(business=yekabusiness)
        else:
            contract = YekaContract(
                yekabusinessblog=yekabussinessblog,
                business=yekabusiness
            )
            contract.save()
        contract_form = YekaContractForm(request.POST or None, request.FILES or None, instance=contract)
        name = general_methods.yekaname(yekabusiness)
        with transaction.atomic():
            if request.method == 'POST':
                if contract_form.is_valid():
                    contract = contract_form.save(request, commit=False)
                    contract.save()
                    yekabusiness.company = contract.company
                    yekabusiness.save()
                    messages.success(request, 'Basarıyla Eklenmiştir.')
                    redirect('ekabis:change_yekacontract', contract.business.uuid, contract.yekabusinessblog.uuid)
                else:
                    error_messages = get_error_messages(contract_form)
                    return render(request, 'Contract/change_yekacontract.html',
                                  {'contract_form': contract_form,
                                   'error_messages': error_messages, 'urls': urls, 'current_url': current_url,
                                   'url_name': url_name, 'name': name,
                                   })

            return render(request, 'Contract/change_yekacontract.html',
                          {'contract_form': contract_form,
                           'business': business,
                           'yekabussinessblog': yekabussinessblog, 'urls': urls, 'current_url': current_url,
                           'url_name': url_name, 'name': name,
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka', )


#
# aday yeka


@login_required
def change_yekaproposal(request, business, businessblog):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)

        yekabussinessblog = YekaBusinessBlog.objects.get(uuid=businessblog)
        yekabusiness = YekaBusiness.objects.get(uuid=business)

        yekaproposal = None
        if YekaProposal.objects.filter(business=yekabusiness):
            yekaproposal = YekaProposal.objects.get(business=yekabusiness)
        else:
            yekaproposal = YekaProposal(
                yekabusinessblog=yekabussinessblog,
                business=yekabusiness
            )
            yekaproposal.save()

        name = general_methods.yekaname(yekabusiness)

        return render(request, 'Proposal/change_yekaproposal.html',
                      {'yekaproposal': yekaproposal,
                       'business': business,
                       'yekabussinessblog': yekabussinessblog, 'urls': urls, 'current_url': current_url,
                       'url_name': url_name, 'name': name,
                       })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka', )


# Aday yeka ekle


@login_required
def add_proposal(request, uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:

        yeka_proposal = YekaProposal.objects.get(uuid=uuid)

        proposal_form = ProposalForm()

        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        name = general_methods.yekaname(yeka_proposal.business)

        with transaction.atomic():

            if request.method == 'POST':
                proposal_form = ProposalForm(request.POST or None, request.FILES or None)
                if proposal_form.is_valid():
                    company = proposal_form.save(request, commit=False)
                    company.save()
                    yeka_proposal.proposal.add(company)
                    yeka_proposal.save()
                    messages.success(request, 'Aday Yeka  Eklenmistir')
                    return redirect('ekabis:change_yekaproposal', yeka_proposal.business.uuid,
                                    yeka_proposal.yekabusinessblog.uuid)
                else:
                    error_messages = get_error_messages(proposal_form)
                    return render(request, 'Proposal/add_proposal.html',
                                  {
                                      'urls': urls,
                                      'current_url': current_url,
                                      'url_name': url_name,
                                      'error_messages': error_messages,
                                      'proposal_form': proposal_form, 'name': name,
                                  })
            return render(request, 'Proposal/add_proposal.html',
                          {'urls': urls,
                           'current_url': current_url, 'url_name': url_name,
                           'proposal_form': proposal_form, 'name': name,
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required
def change_proposal(request, uuid, proposal):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:

        yeka_proposal = YekaProposal.objects.get(uuid=uuid)
        proposal = Proposal.objects.get(uuid=proposal)
        proposal_form = ProposalForm(request.POST or None, request.FILES or None, instance=proposal)

        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        with transaction.atomic():

            if request.method == 'POST':

                if proposal_form.is_valid():
                    company = proposal_form.save(request, commit=False)
                    company.save()

                    messages.success(request, 'Aday Yeka Güncellenmiştir.')
                    return redirect('ekabis:change_yekaproposal', yeka_proposal.business.uuid,
                                    yeka_proposal.yekabusinessblog.uuid)
                else:
                    error_messages = get_error_messages(proposal_form)
                    return render(request, 'Proposal/change_proposal.html',
                                  {
                                      'urls': urls,
                                      'current_url': current_url,
                                      'url_name': url_name,
                                      'error_messages': error_messages,
                                      'proposal_form': proposal_form
                                  })
            return render(request, 'Proposal/change_proposal.html',
                          {'urls': urls,
                           'current_url': current_url, 'url_name': url_name,
                           'proposal_form': proposal_form
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required
def delete_proposal(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']
                obj = Proposal.objects.get(uuid=uuid)
                data_as_json_pre = serializers.serialize('json', Proposal.objects.filter(uuid=uuid))

                obj.isDeleted = True
                obj.save()
                log = str(obj.pk) + " - aday yeka silindi."
                logs = Logs(user=request.user, subject=log, ip=get_client_ip(request), previousData=data_as_json_pre)
                logs.save()

                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})


            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


# kurum görüşlerinim alınması


@login_required
def change_proposal_active(request, business, businessblog):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)

        yekabussinessblog = YekaBusinessBlog.objects.get(uuid=businessblog)
        yekabusiness = YekaBusiness.objects.get(uuid=business)

        pro_active = ProposalActive.objects.filter(business=yekabusiness)
        #
        # olmayanların eklemesini yaptık
        array = []
        for item in pro_active:
            array.append(item.institution.pk)

        for item in Institution.objects.exclude(id__in=array).filter(isDeleted=False):
            active = ProposalActive(
                business=yekabusiness,
                institution=item
            )
            active.save()
        pro_active = ProposalActive.objects.filter(business=yekabusiness)
        name = general_methods.yekaname(yekabusiness)

        with transaction.atomic():

            if request.method == 'POST':
                for item in pro_active:
                    try:
                        if request.POST.get(str(item.pk)):
                            if ProposalActive.objects.filter(uuid=item.uuid, isDeleted=False) != None:
                                pro = ProposalActive.objects.get(uuid=item.uuid)
                                pro.is_active = True
                                pro.save()

                        else:
                            if ProposalActive.objects.filter(uuid=item.uuid, isDeleted=False) != None:
                                pro = ProposalActive.objects.get(uuid=item.uuid)
                                pro.is_active = False
                                pro.save()
                    except Exception as e:
                        print(e)
                        traceback.print_exc()
                pro_active = ProposalActive.objects.filter(business=yekabusiness)

            return render(request, 'Proposal/change_proposal_active.html',
                          {'pro_active': pro_active,
                           'yekabusiness': yekabusiness,
                           'yekabussinessblog': yekabussinessblog, 'urls': urls, 'current_url': current_url,
                           'url_name': url_name, 'name': name,
                           })



    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka', )


@login_required
def view_institution(request, business, businessblog):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        yekabussinessblog = YekaBusinessBlog.objects.get(uuid=businessblog)
        yekabusiness = YekaBusiness.objects.get(uuid=business)
        institutions = Institution.objects.filter(isDeleted=False)
        institution_form = InstitutionForm()
        name = general_methods.yekaname(yekabusiness)
        with transaction.atomic():

            if request.method == 'POST':
                institution_form = InstitutionForm(request.POST or None)
                if institution_form.is_valid():
                    ins = institution_form.save(request, commit=False)
                    ins.save()
                    messages.success(request, 'Kurum Eklenmistir')
                    return redirect('ekabis:view_institution', yekabusiness.uuid, yekabussinessblog.uuid)
                else:
                    error_messages = get_error_messages(institution_form)
                    return render(request, 'Proposal/view_institution.html',
                                  {'institutions': institutions,
                                   'business': business,
                                   'yekabussinessblog': yekabussinessblog,
                                   'urls': urls, 'current_url': current_url,
                                   'url_name': url_name, 'name': name,
                                   'institution_form': institution_form,
                                   'error_messages': error_messages,
                                   })

            return render(request, 'Proposal/view_institution.html',
                          {'institutions': institutions,
                           'business': business,
                           'yekabussinessblog': yekabussinessblog,
                           'urls': urls, 'current_url': current_url,
                           'url_name': url_name, 'name': name,
                           'institution_form': institution_form
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka', )


@login_required
def change_institution(request, business, businessblog, uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)

        yekabussinessblog = YekaBusinessBlog.objects.get(uuid=businessblog)
        yekabusiness = YekaBusiness.objects.get(uuid=business)

        institutions = Institution.objects.filter(isDeleted=False)
        institution = Institution.objects.get(uuid=uuid)
        institution_form = InstitutionForm(request.FILES or None, request.POST or None, instance=institution)
        name = general_methods.yekaname(yekabusiness)

        with transaction.atomic():

            if request.method == 'POST':
                if institution_form.is_valid():
                    ins = institution_form.save(request, commit=False)
                    ins.save()
                    messages.success(request, 'Kurum Eklenmistir')
                    return redirect('ekabis:view_institution', yekabusiness.uuid, yekabussinessblog.uuid)
                else:
                    error_messages = get_error_messages(institution_form)
                    return render(request, 'Proposal/view_institution.html',
                                  {'institutions': institutions,
                                   'yekabusiness': yekabusiness,
                                   'yekabussinessblog': yekabussinessblog,
                                   'urls': urls, 'current_url': current_url,
                                   'url_name': url_name, 'name': name,
                                   'institution_form': institution_form,
                                   'error_messages': error_messages,
                                   })

            return render(request, 'Proposal/view_institution.html',
                          {'institutions': institutions,
                           'business': business,
                           'yekabussinessblog': yekabussinessblog,
                           'urls': urls, 'current_url': current_url,
                           'url_name': url_name, 'name': name,
                           'institution_form': institution_form
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka', )


@login_required
def delete_institution(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']
                obj = Institution.objects.get(uuid=uuid)
                obj.isDeleted = True
                obj.save()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def view_proposal_institution(request, yekaproposal, uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)

        yekaproposal = YekaProposal.objects.get(uuid=yekaproposal)
        proposal = Proposal.objects.get(uuid=uuid)

        yekabussinessblog = yekaproposal.yekabusinessblog
        yekabusiness = yekaproposal.business

        name = general_methods.yekaname(yekabusiness)

        # olmayan kurumların eklemesini yaptık
        for item in ProposalActive.objects.filter(business=yekabusiness):
            if not proposal.institution.filter(institution=item.institution):
                pro_institution = ProposalInstitution(
                    institution=item.institution,
                )
                pro_institution.save()
                proposal.institution.add(pro_institution)
                proposal.save()

        proposal_institution = proposal.institution.filter(isDeleted=False)
        with transaction.atomic():
            return render(request, 'Proposal/view_proposal_institution.html',
                          {'proposal_institution': proposal_institution,
                           'yekabusiness': yekabusiness,
                           'yekabussinessblog': yekabussinessblog,
                           'urls': urls, 'current_url': current_url,
                           'url_name': url_name, 'name': name,
                           'proposal': proposal,
                           'yekaproposal': yekaproposal
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka', )


@login_required
def change_proposal_institution(request, yekaproposal, proposal, uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)

        yekaproposal = YekaProposal.objects.get(uuid=yekaproposal)
        proposal = Proposal.objects.get(uuid=proposal)
        pro_institution = ProposalInstitution.objects.get(uuid=uuid)

        proposal_form = ProposalInstitutionForm(request.POST or None, request.FILES or None, instance=pro_institution)
        yekabussinessblog = yekaproposal.yekabusinessblog
        yekabusiness = yekaproposal.business
        name = general_methods.yekaname(yekabusiness)
        with transaction.atomic():

            if request.method == 'POST':
                if proposal_form.is_valid():
                    ins = proposal_form.save(request, commit=False)
                    ins.save()
                    messages.success(request, 'Öneri güncellenmisştir.')
                    return redirect('ekabis:view_proposal_institution', yekaproposal.uuid, proposal.uuid)
                else:
                    error_messages = get_error_messages(proposal_form)
                    return render(request, 'Proposal/change_propsal_institution.html',
                                  {'proposal_form': proposal_form,
                                   'yekabusiness': yekabusiness,
                                   'yekabussinessblog': yekabussinessblog,
                                   'urls': urls, 'current_url': current_url,
                                   'url_name': url_name, 'name': name,
                                   'error_messages': error_messages,
                                   })

            return render(request, 'Proposal/change_propsal_institution.html',
                          {'proposal_form': proposal_form,
                           'yekabusiness': yekabusiness,
                           'yekabussinessblog': yekabussinessblog,
                           'urls': urls, 'current_url': current_url,
                           'url_name': url_name, 'name': name,
                           'proposal': proposal
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka', )


@login_required
def delete_proposal_institution(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']
                obj = ProposalInstitution.objects.get(uuid=uuid)
                obj.isDeleted = True
                obj.save()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def view_yeka_user(request, business, businessblog):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)

        yekabussinessblog = YekaBusinessBlog.objects.get(uuid=businessblog)
        yekabusiness = YekaBusiness.objects.get(uuid=business)

        name = general_methods.yekaname(yekabusiness)
        yekacompany = None
        # eklemsini yaptık
        if not YekaCompanyUser.objects.filter(business=yekabusiness):
            yekacompany = YekaCompanyUser(
                business=yekabusiness,
                yekabusinessblog=yekabussinessblog,
            )
            yekacompany.save()
        else:
            yekacompany = YekaCompanyUser.objects.get(business=yekabusiness)
        if not yekabusiness.company:
            messages.warning(request, 'Sözleşme İmzanmadan firma Kullanıcı atanamaz.')
            test = request.META.get('HTTP_REFERER')
            # önceki sayfaya yönlendirilecek
        company_user = yekacompany.companyuser.filter(isDeleted=False)
        with transaction.atomic():
            return render(request, 'CompanyUser/view_companyuser.html',
                          {'company_user': company_user,
                           'yekabusiness': yekabusiness,
                           'yekabussinessblog': yekabussinessblog,
                           'urls': urls, 'current_url': current_url,
                           'url_name': url_name, 'name': name,
                           'yekacompany': yekacompany
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka', )


@login_required
def add_yeka_user(request, yekacompany):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:

        yeka_company = YekaCompanyUser.objects.get(uuid=yekacompany)
        company_form = YekaUserForm()

        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        name = general_methods.yekaname(yeka_company.business)
        with transaction.atomic():
            if request.method == 'POST':
                company_form = YekaUserForm(request.POST or None, request.FILES or None)
                if company_form.is_valid():
                    company = company_form.save(request, commit=False)
                    company.save()
                    yeka_company.companyuser.add(company)
                    yeka_company.save()
                    messages.success(request, 'Firma Kullanıcısı Eklenmistir')
                    return redirect('ekabis:view_yeka_user', yeka_company.business.uuid,
                                    yeka_company.yekabusinessblog.uuid)
                else:
                    error_messages = get_error_messages(company_form)
                    return render(request, 'CompanyUser/add_company_user.html',
                                  {
                                      'urls': urls, 'name': name,
                                      'current_url': current_url,
                                      'url_name': url_name,
                                      'error_messages': error_messages,
                                      'company_form': company_form
                                  })
            return render(request, 'CompanyUser/add_company_user.html',
                          {'urls': urls,
                           'current_url': current_url, 'url_name': url_name,
                           'company_form': company_form, 'name': name,
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required
def change_yeka_user(request, yekacompany, companyuser):
    test = change_yeka_user
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:

        yeka_company = YekaCompanyUser.objects.get(uuid=yekacompany)
        yeka_user = YekaUser.objects.get(uuid=companyuser)
        company_form = YekaUserForm(request.POST or None, request.FILES or None, instance=yeka_user)
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        name = general_methods.yekaname(yeka_company.business)

        with transaction.atomic():
            if request.method == 'POST':
                if company_form.is_valid():
                    company = company_form.save(request, commit=False)
                    company.save()
                    messages.success(request, 'Firma Kullanıcısı Güncellenmiştir.')
                    return redirect('ekabis:view_yeka_user', yeka_company.business.uuid,
                                    yeka_company.yekabusinessblog.uuid)
                else:
                    error_messages = get_error_messages(company_form)
                    return render(request, 'CompanyUser/change_company_user.html',
                                  {
                                      'urls': urls,
                                      'current_url': current_url,
                                      'url_name': url_name, 'name': name,
                                      'error_messages': error_messages,
                                      'company_form': company_form
                                  })
            return render(request, 'CompanyUser/change_company_user.html',
                          {'urls': urls,
                           'current_url': current_url, 'url_name': url_name,
                           'company_form': company_form, 'name': name,
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required
def delete_yeka_user(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']
                obj = CompanyUser.objects.get(uuid=uuid)
                obj.isDeleted = True
                obj.save()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def add_coordinate(request, uuid, yeka_proposal_uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:

        proposal = Proposal.objects.get(uuid=uuid)
        yeka_proposal = YekaProposal.objects.get(uuid=yeka_proposal_uuid)
        coordinate_form = CoordinateForm()
        name = general_methods.yekaname(yeka_proposal.business)
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        coordinates = proposal.coordinate.filter(isDeleted=False)
        with transaction.atomic():

            if request.method == 'POST':
                coordinate_form = CoordinateForm(request.POST or None, request.FILES or None)
                if coordinate_form.is_valid():
                    coordinate = coordinate_form.save(request, commit=False)
                    coordinate.save()
                    proposal.coordinate.add(coordinate)
                    proposal.save()
                    messages.success(request, 'Koordinat  Eklenmiştir')
                    return redirect('ekabis:add_coordinate', uuid, yeka_proposal_uuid)
                else:
                    error_messages = get_error_messages(coordinate_form)
                    return render(request, 'Proposal/add_coordinate.html',
                                  {'name': name,
                                   'urls': urls, 'coordinates': coordinates,
                                   'current_url': current_url,
                                   'url_name': url_name, 'yeka_proposal': yeka_proposal,
                                   'error_messages': error_messages,
                                   'coordinate_form': coordinate_form
                                   })
            return render(request, 'Proposal/add_coordinate.html',
                          {'urls': urls, 'name': name, 'coordinates': coordinates,
                           'current_url': current_url, 'url_name': url_name,
                           'coordinate_form': coordinate_form, 'yeka_proposal': yeka_proposal,
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required
def change_coordinate(request, uuid, yeka_proposal_uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:

        coordinate = Coordinate.objects.get(uuid=uuid)
        yeka_proposal = YekaProposal.objects.get(uuid=yeka_proposal_uuid)
        coordinate_form = CoordinateForm(request.POST or None, request.FILES or None, instance=coordinate)
        name = general_methods.yekaname(yeka_proposal.business)
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        with transaction.atomic():

            if request.method == 'POST':
                if coordinate_form.is_valid():
                    form = coordinate_form.save(request, commit=False)
                    form.save()
                    messages.success(request, 'Koordinat  güncellenmiştir.')
                    return redirect('ekabis:change_yekaproposal', yeka_proposal.business.uuid,
                                    yeka_proposal.yekabusinessblog.uuid)
                else:
                    error_messages = get_error_messages(coordinate_form)
                    return render(request, 'Proposal/change_coordinate.html',
                                  {'name': name,
                                   'urls': urls, 'coordinate': coordinate,
                                   'current_url': current_url,
                                   'url_name': url_name,
                                   'error_messages': error_messages,
                                   'coordinate_form': coordinate_form
                                   })
            return render(request, 'Proposal/change_coordinate.html',
                          {'urls': urls, 'name': name, 'coordinate': coordinate,
                           'current_url': current_url, 'url_name': url_name,
                           'coordinate_form': coordinate_form
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required
def delete_coordinate(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']
                obj = Coordinate.objects.get(uuid=uuid)
                obj.isDeleted = True
                obj.save()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def add_location(request, uuid, yeka_proposal_uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:

        proposal = Proposal.objects.get(uuid=uuid)
        yeka_proposal = YekaProposal.objects.get(uuid=yeka_proposal_uuid)
        location_form = LocationForm()
        name = general_methods.yekaname(yeka_proposal.business)
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        locations = proposal.location.filter(isDeleted=False)
        with transaction.atomic():

            if request.method == 'POST':
                location_form = LocationForm(request.POST or None, request.FILES or None)
                if location_form.is_valid():
                    location = location_form.save(request, commit=False)
                    location.save()
                    proposal.location.add(location)
                    proposal.save()
                    messages.success(request, 'Konum Bilgisi  Eklenmiştir')
                    return redirect('ekabis:add_location', uuid, yeka_proposal_uuid)
                else:
                    error_messages = get_error_messages(location_form)
                    return render(request, 'Proposal/add_location.html',
                                  {'name': name, 'proposal': proposal,
                                   'urls': urls, 'locations': locations,
                                   'current_url': current_url,
                                   'url_name': url_name, 'yeka_proposal': yeka_proposal,
                                   'error_messages': error_messages,
                                   'location_form': location_form
                                   })
            return render(request, 'Proposal/add_location.html',
                          {'urls': urls, 'name': name, 'locations': locations,
                           'current_url': current_url, 'url_name': url_name, 'proposal': proposal,
                           'location_form': location_form, 'yeka_proposal': yeka_proposal,
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required
def change_location(request, uuid, yeka_proposal_uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:

        location = Location.objects.get(uuid=uuid)
        yeka_proposal = YekaProposal.objects.get(uuid=yeka_proposal_uuid)
        name = general_methods.yekaname(yeka_proposal.business)
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        location_form = LocationForm(request.POST or None, request.FILES or None, instance=location)

        with transaction.atomic():

            if request.method == 'POST':
                if location_form.is_valid():
                    location = location_form.save(request, commit=False)
                    location.save()
                    messages.success(request, 'Konum Bilgisi Güncellenmiştir')
                    return redirect('ekabis:change_yekaproposal', yeka_proposal.business.uuid,
                                    yeka_proposal.yekabusinessblog.uuid)
                else:
                    error_messages = get_error_messages(location_form)
                    return render(request, 'Proposal/change_location.html',
                                  {'name': name,
                                   'urls': urls,
                                   'current_url': current_url,
                                   'url_name': url_name, 'yeka_proposal': yeka_proposal,
                                   'error_messages': error_messages,
                                   'location_form': location_form
                                   })
            return render(request, 'Proposal/change_location.html',
                          {'urls': urls, 'name': name,
                           'current_url': current_url, 'url_name': url_name,
                           'location_form': location_form, 'yeka_proposal': yeka_proposal,
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required
def delete_location(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']
                obj = Location.objects.get(uuid=uuid)
                obj.isDeleted = True
                obj.save()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def add_competition_company_select(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:

        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)

        yekas = serializers.serialize("json", Yeka.objects.filter(isDeleted=False), cls=DjangoJSONEncoder)
        regions = serializers.serialize("json", ConnectionRegion.objects.filter(isDeleted=False), cls=DjangoJSONEncoder)
        competitions = serializers.serialize("json", YekaCompetition.objects.filter(isDeleted=False),
                                             cls=DjangoJSONEncoder)

        with transaction.atomic():

            if request.method == 'POST':
                competition = YekaCompetition.objects.get(pk=request.POST.get('select_competition'))
                company = Company.objects.get(pk=request.POST.get('select_company'))
                yeka_application = CompetitionApplication.objects.get(business=competition.business)
                yeka_company = YekaCompany(
                    company=company
                )
                yeka_company.save()
                yeka_application.companys.add(yeka_company)
                yeka_application.save()
            return render(request, 'Application/add_competitions_company_select.html',
                          {'urls': urls,
                           'current_url': current_url, 'url_name': url_name,
                           'yekas': yekas,
                           'regions': regions,
                           'competitions': competitions
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required
def add_competition_company_select_api(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                id = request.POST['id']
                competitions = YekaCompetition.objects.filter(pk=id)
                if competitions.filter(business__businessblogs__businessblog__name="Başvurunun Alınması"):
                    competition = YekaCompetition.objects.get(pk=id)
                    if CompetitionApplication.objects.filter(business=competition.business):
                        yeka_application = CompetitionApplication.objects.get(business=competition.business)
                    else:
                        yeka_business_blog = competition.business.businessblogs.filter(
                            businessblog__name="Başvurunun Alınması")
                        yeka_application = CompetitionApplication(
                            business=competition.business,
                            yekabusinessblog=yeka_business_blog[0],
                        )
                        yeka_application.save()

                    ex_company = yeka_application.companys.all().values_list('id')
                    comp = Company.objects.exclude(pk__in=ex_company)

                    company = serializers.serialize("json", comp, cls=DjangoJSONEncoder)

                    return JsonResponse({'status': 'Success', 'msg': 'İşlem Başarılı', 'company': company})

                else:
                    return JsonResponse({'status': 'Fail', 'msg': 'Başvuruların alınması iş Blogu yok'})

                return JsonResponse({'status': 'Success', 'msg': 'İşlem Başarılı'})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


def proposal_add_sub_yeka(request, yeka_business, yeka_business_block):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)

        yeka_bussiness_block = YekaBusinessBlog.objects.get(uuid=yeka_business_block)
        yeka_business = YekaBusiness.objects.get(uuid=yeka_business)

        yekaproposal = None
        if YekaProposal.objects.filter(business=yeka_business):
            yekaproposal = YekaProposal.objects.get(business=yeka_business)
        else:
            yekaproposal = YekaProposal(
                yekabusinessblog=yeka_bussiness_block,
                business=yeka_business
            )
            yekaproposal.save()

        name = general_methods.yekaname(yeka_business)
        competition=None
        if YekaCompetition.objects.filter(business=yeka_business):
            competition = YekaCompetition.objects.get(business=yeka_business)

        return render(request, 'Proposal/proposal_sub_yeka_list.html',
                      {'yekaproposal': yekaproposal,
                       'business': yeka_business,'competition':competition,
                       'yekabussinessblog': yeka_bussiness_block, 'urls': urls, 'current_url': current_url,
                       'url_name': url_name, 'name': name,
                       })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')
