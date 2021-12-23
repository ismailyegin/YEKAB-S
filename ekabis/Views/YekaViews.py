import json
import time
import traceback

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, Http404, HttpResponse, FileResponse
from django.shortcuts import redirect, render
from django.urls import resolve
# from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ekabis.Forms.YekaBusinessBlogForm import YekaBusinessBlogForm
from ekabis.Forms.YekaCompanyForm import YekaCompanyForm
from ekabis.Forms.YekaForm import YekaForm
from ekabis.Forms.YekaHoldingCompetitionForm import YekaHoldingCompetitionForm
from ekabis.Views.VacationDayViews import is_vacation_day
from ekabis.models import ExtraTime, \
    Permission, Logs, ConnectionRegion, YekaCompetition, FileExtension, YekaCompetitionEskalasyon, YekaBusiness, \
    YekaBusinessBlogParemetre, YekaHoldingCompetition, ConnectionUnit

from ekabis.models.Company import Company
from ekabis.models.Employee import Employee
from ekabis.models.LogAPIObject import LogAPIObject
from ekabis.models.Yeka import Yeka
from ekabis.models.CompetitionApplication import CompetitionApplication
from ekabis.models.YekaApplicationFile import YekaApplicationFile
from ekabis.models.YekaApplicationFileName import YekaApplicationFileName
from ekabis.models.YekaBusinessBlog import YekaBusinessBlog
from ekabis.models.YekaCompany import YekaCompany
from ekabis.models.YekaCompetitionPerson import YekaCompetitionPerson
from ekabis.models.YekaContract import YekaContract
from ekabis.models.YekaPerson import YekaPerson
from ekabis.models.YekaPersonHistory import YekaPersonHistory
from ekabis.models.YekaProposal import YekaProposal
from ekabis.serializers import CompanySerializers
from ekabis.serializers.CompanySerializers import CompanySerializer
from ekabis.serializers.CompetitionSerializers import YekaCompetitionSerializer
from ekabis.serializers.ConnectionRegionSerializer import ConnectionRegionSerializer
from ekabis.serializers.YekaCompanySerializers import YekaCompanySerializer
from ekabis.serializers.YekaCompetitionEskalasyonSerializers import YekaCompetitionEskalasyonSerializer
from ekabis.serializers.YekaProposalSerializers import ProposalSerializer, ProposalResponseSerializer
from ekabis.serializers.YekaSerializer import YekaSerializer
from ekabis.services import general_methods
from ekabis.services.NotificationServices import notification
from ekabis.services.general_methods import get_error_messages, get_client_ip
from ekabis.services.services import YekaService, YekaConnectionRegionService, YekaGetService, \
    YekaPersonService, \
    EmployeeGetService, ExtraTimeService, YekaBusinessBlogGetService, \
    BusinessBlogGetService, ConnectionRegionService, last_urls, YekaCompetitionGetService, \
    YekaBusinessGetService
import datetime

from ekabis.models.CompetitionApplication import CompetitionApplication
from ekabis.models.YekaApplicationFile import YekaApplicationFile
import base64

from django.core.files.base import ContentFile


@login_required
def return_yeka(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    yeka_form = YekaForm()
    try:
        print(datetime.datetime.now())
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        with transaction.atomic():
            return render(request, 'Yeka/view_yeka.html',
                          {'yeka_form': yeka_form, 'error_messages': '', 'urls': urls, 'current_url': current_url,
                           'url_name': url_name})
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, e)
        return redirect('ekabis:view_yeka')


@login_required
def add_yeka(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        yeka_form = YekaForm()
        if request.method == 'POST':
            with transaction.atomic():
                yeka_form = YekaForm(request.POST)
                if yeka_form.is_valid():
                    yeka = yeka_form.save(request, commit=False)
                    yeka.save()
                    url = redirect('ekabis:view_yeka_detail', yeka.uuid).url
                    html = '<a style="" href="' + url + '">ID: ' + str(
                        yeka.pk) + ' - ' + yeka.definition + '</a> YEKA eklendi.'
                    notification(request, html, yeka.uuid, 'yeka')

                    messages.success(request, 'Yeka Başarıyla Kayıt Edilmiştir.')
                    return redirect('ekabis:view_yeka_detail', yeka.uuid)

                else:
                    error_message_unit = get_error_messages(yeka_form)

                    return render(request, 'Yeka/add_yeka.html',
                                  {'yeka_form': yeka_form, 'error_messages': error_message_unit,
                                   })
        return render(request, 'Yeka/add_yeka.html',
                      {'yeka_form': yeka_form, 'error_messages': '', 'urls': urls, 'current_url': current_url,
                       'url_name': url_name})

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        raise Http404()


@login_required
def return_sub_yeka(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        yeka_filter = {
            'uuid': uuid
        }
        yeka = YekaGetService(request, yeka_filter)

        alt_yeka_filter = {
            'yekaParent': yeka,
            'isDeleted': False
        }
        alt_yekalar = YekaService(request, alt_yeka_filter)
        yekalar = dict()
        sub_yekalar = []
        # if alt_yekalar:
        #     for alt_yeka in alt_yekalar:
        #         capacities = SubYekaCapacity.objects.filter(yeka=alt_yeka)
        #         yekalar['yeka'] = alt_yeka
        #         yekalar['capacities'] = capacities
        #         sub_yekalar.append(yekalar)
        return render(request, 'Yeka/view_sub_yeka.html',
                      {'alt_yekalar': sub_yekalar, 'yeka': uuid, })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required
def delete_yeka(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']
                yekafilter = {
                    'uuid': uuid
                }
                obj = YekaService(request, yekafilter).first()

                parent_filter = {
                    'isDeleted': False,
                    'yekaParent__uuid': obj.uuid
                }
                parent = YekaService(request, parent_filter)
                if parent:
                    return JsonResponse({'status': 'Fail', 'msg': 'Yeka silinemez.Alt Yekalar bulunmaktadır.'})
                else:
                    data_as_json_pre = serializers.serialize('json', Yeka.objects.filter(uuid=uuid))
                    obj.isDeleted = True
                    obj.save()

                    url = redirect('ekabis:view_yeka').url
                    html = '<a style="" href="' + url + '">ID: ' + str(
                        obj.pk) + ' - ' + obj.definition + '</a> YEKA  silindi.'
                    notification(request, html, obj.uuid, 'yeka')
                    log = str(obj.definition) + " - Yeka silindi."
                    logs = Logs(user=request.user, subject=log, ip=get_client_ip(request),
                                previousData=data_as_json_pre)
                    logs.save()
                    return JsonResponse({'status': 'Success', 'msg': 'save successfully'})

            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def update_yeka(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        yeka_filter = {
            'uuid': uuid
        }
        yeka = YekaGetService(request, yeka_filter)
        yeka_form = YekaForm(request.POST or None, instance=yeka)
        alt_yeka_filter = {
            'isDeleted': False,
            'yekaParent__uuid': uuid

        }

        alt_yekalar = YekaService(request, alt_yeka_filter)
        yeka_connections_filter = {
            'isDeleted': False,
            'yeka': yeka
        }
        yeka_connections = YekaConnectionRegionService(request, yeka_connections_filter)
        yeka_regions = []

        for yeka_connection in yeka_connections:
            yeka_regions.append(yeka_connection.connectionRegion)

        connection_regions_filter = {
            'isDeleted': False,

        }
        connection_regions = ConnectionRegionService(request, connection_regions_filter)
        with transaction.atomic():
            if request.method == 'POST':

                if yeka_form.is_valid():
                    yeka = yeka_form.save(request, commit=False)
                    yeka.definition = yeka_form.cleaned_data['definition']
                    yeka.date = yeka_form.cleaned_data['date']
                    yeka.capacity = yeka_form.cleaned_data['capacity']
                    yeka.type = yeka_form.cleaned_data['type']
                    yeka.save()
                    url = redirect('ekabis:view_yeka_detail', yeka.uuid).url
                    html = '<a style="" href="' + url + '">ID: ' + str(
                        yeka.pk) + ' - ' + yeka.definition + '</a> YEKA güncellendi.'
                    notification(request, html, yeka.uuid, 'yeka')
                    messages.success(request, 'Yeka Başarıyla Güncellendi')
                    return redirect('ekabis:view_yeka_detail', yeka.uuid)
                else:
                    error_message_unit = get_error_messages(yeka_form)
                    return render(request, 'Yeka/change_yeka.html',
                                  {'yeka_form': yeka_form, 'error_messages': error_message_unit, 'yeka': yeka,
                                   'yeka_connections': yeka_regions, 'connection_regions': connection_regions,
                                   'urls': urls, 'current_url': current_url, 'url_name': url_name,
                                   })

            return render(request, 'Yeka/change_yeka.html',
                          {'yeka_form': yeka_form, 'error_messages': '', 'yeka_connections': yeka_regions,
                           'connection_regions': connection_regions, 'urls': urls, 'current_url': current_url,
                           'url_name': url_name, 'yeka': yeka,
                           })
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(status=500)


@login_required
def alt_yeka_ekle(request, uuid):
    # try:
    #     yeka_form = YekaForm()
    #     yeka_filter = {
    #         'uuid': uuid
    #     }
    #     yeka = YekaGetService(request, yeka_filter)
    #
    #     url = general_methods.yeka_control(request, yeka)
    #     if url:
    #         return redirect('ekabis:' + url, yeka.uuid)
    #
    #     alt_yeka_filter = {
    #         'yekaParent': yeka,
    #         'isDeleted': False
    #
    #     }
    #     alt_yekalar = YekaService(request, alt_yeka_filter)
    #     yeka_connection_region_filter = {
    #         'yeka': yeka
    #     }
    #     yeka_connection = YekaConnectionRegionGetService(request, yeka_connection_region_filter)
    #     capacity_filter = {
    #         'isDeleted': False,
    #         'connection_region': yeka_connection.connectionRegion
    #     }
    #     yeka_connection_capacities = ConnectionCapacityService(request, capacity_filter)
    #     with transaction.atomic():
    #         if request.method == 'POST':
    #
    #             yeka_form = YekaForm(request.POST)
    #             yeka_connection_form = YekaConnectionRegionForm(request.POST)
    #
    #             if yeka_form.is_valid():
    #                 total_capacity = 0
    #                 array_capacity = []
    #                 for region_capacity in request.POST.getlist('region_capacity'):
    #                     capacity = ConnectionCapacity.objects.get(uuid=region_capacity)
    #                     array_capacity.append(capacity)
    #                     total_capacity = total_capacity + capacity.value
    #
    #                 if yeka.capacity >= total_capacity:
    #                     new_yeka = Yeka(definition=yeka_form.cleaned_data['definition'],
    #                                     date=yeka_form.cleaned_data['date']
    #                                     )
    #                     new_yeka.save()
    #                     new_yeka.yekaParent = yeka
    #                     yeka_business = YekaBusiness(name=yeka.business.name)
    #                     yeka_business.save()
    #                     if yeka.business.businessblogs.all():
    #                         parent_yeka_business_blog = YekaBusinessBlog.objects.none()
    #                         for item in yeka.business.businessblogs.all().order_by('sorting'):
    #
    #                             if item.sorting == 1:
    #                                 yeka_businessblog = YekaBusinessBlog(
    #                                     finisDate=item.finisDate,
    #                                     startDate=item.startDate,
    #                                     sorting=item.sorting,
    #                                     businessTime=item.businessTime,
    #                                     status=item.status,
    #                                     businessblog=item.businessblog
    #
    #                                 )
    #                                 parent_yeka_business_blog = yeka_businessblog
    #                                 yeka_businessblog.save()
    #
    #                             else:
    #                                 yeka_businessblog = YekaBusinessBlog(parent=parent_yeka_business_blog,
    #                                                                      finisDate=item.finisDate,
    #                                                                      businessblog=item.businessblog,
    #                                                                      sorting=item.sorting,
    #                                                                      businessTime=item.businessTime,
    #                                                                      status=item.status,
    #                                                                      )
    #                                 yeka_businessblog.save()
    #                                 parent_yeka_business_blog = yeka_businessblog
    #                             if item.companys.all():
    #                                 for company in item.companys.all():
    #                                     yeka_businessblog.companys.add(company)
    #                                     yeka_businessblog.save()
    #
    #                             yeka_business.save()
    #                             yeka_business.businessblogs.add(yeka_businessblog)
    #                             yeka_business.save()
    #
    #                     new_yeka.business = yeka_business
    #                     new_yeka.save()
    #
    #                     for new_capacity in array_capacity:
    #                         yeka_region_capacity = SubYekaCapacity(yeka=new_yeka, capacity=new_capacity)
    #                         yeka_region_capacity.save()
    #
    #                     new_yeka.capacity = total_capacity
    #                     new_yeka.unit = array_capacity[0].unit
    #                     new_yeka.save()
    #                 else:
    #                     messages.warning(request,
    #                                      'Alt Yeka Toplam Kapasitesi Üst Yeka Toplam Kapasitesinden Büyük Olamaz.')
    #                     return render(request, 'Yeka/add_sub_yeka.html',
    #                                   {'yeka_form': yeka_form, 'error_messages': '', 'alt_yekalar': alt_yekalar,
    #                                    'yeka_connection_capacity': yeka_connection_capacities, 'yeka': uuid
    #                                    })
    #
    #                 log = "Alt Yeka eklendi"
    #                 log = general_methods.logwrite(request, request.user, log)
    #                 messages.success(request, 'Alt Yeka Başarıyla Kayıt Edilmiştir.')
    #                 return redirect('ekabis:view_yeka')
    #
    #             else:
    #                 error_message_unit = get_error_messages(yeka_form)
    #                 return render(request, 'Yeka/add_sub_yeka.html',
    #                               {'yeka_form': yeka_form, 'error_messages': error_message_unit,
    #                                'alt_yekalar': alt_yekalar, 'yeka_connection_capacity': yeka_connection_capacities,
    #                                'yeka': uuid
    #                                })
    #
    #         return render(request, 'Yeka/add_sub_yeka.html',
    #                       {'yeka_form': yeka_form, 'error_messages': '', 'alt_yekalar': alt_yekalar,
    #                        'yeka_connection_capacity': yeka_connection_capacities, 'yeka': uuid
    #                        })
    #
    # except Exception as e:
    #     traceback.print_exc()
    #     messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
    #     return redirect('ekabis:view_yeka')
    return


@login_required
def update_sub_yeka(request, uuid):
    # try:
    #     yeka_filter = {
    #         'uuid': uuid
    #     }
    #     yeka = YekaGetService(request, yeka_filter)
    #     alt_yeka_filter = {
    #         'yekaParent': yeka,
    #         'isDeleted': False
    #
    #     }
    #     alt_yekalar = YekaService(request, alt_yeka_filter)
    #     yeka_connection_region_filter = {
    #         'yeka': yeka.yekaParent
    #     }
    #     yeka_connection = YekaConnectionRegionGetService(request, yeka_connection_region_filter)
    #     yeka_connection_capacities = []
    #     if yeka_connection:
    #         capacity_filter = {
    #             'isDeleted': False,
    #             'connection_region': yeka_connection.connectionRegion
    #         }
    #         yeka_connection_capacities = ConnectionCapacityService(request, capacity_filter)
    #     yeka_form = YekaForm(request.POST or None, instance=yeka)
    #
    #     subyeka_filter = {
    #         'yeka': yeka,
    #         'isDeleted': False
    #     }
    #
    #     current_capacities = SubYekaCapacityService(request, subyeka_filter)
    #     sub_capacities = []
    #     for sub in current_capacities:
    #         sub_capacities.append(sub.capacity)
    #
    #     with transaction.atomic():
    #
    #         if request.method == 'POST':
    #
    #             if yeka_form.is_valid():
    #                 total_capacity = 0
    #                 array_capacity = []
    #                 for region_capacity in request.POST.getlist('region_capacity'):
    #                     capacity = ConnectionCapacity.objects.get(uuid=region_capacity)
    #                     array_capacity.append(capacity)
    #                     total_capacity = total_capacity + capacity.value
    #
    #                 if yeka.capacity >= total_capacity:
    #                     yeka.definition = yeka_form.cleaned_data['definition']
    #                     yeka.date = yeka_form.cleaned_data['date']
    #                     yeka.save()
    #
    #                     for new_capacity in array_capacity:
    #                         if not new_capacity in sub_capacities:
    #                             yeka_region_capacity = SubYekaCapacity(yeka=yeka, capacity=new_capacity)
    #                             yeka_region_capacity.save()
    #
    #                     yeka.capacity = total_capacity
    #                     yeka.unit = array_capacity[0].unit
    #                     yeka.save()
    #
    #                     delete_yeka = list(set(current_capacities) - set(array_capacity))
    #
    #                     for remove_yeka in delete_yeka:
    #                         if not remove_yeka in current_capacities:
    #                             delete = SubYekaCapacity.objects.get(
    #                                 Q(uuid=remove_yeka.uuid) & Q(yeka=yeka))
    #                             delete.delete()
    #                 else:
    #                     messages.warning(request,
    #                                      'Alt Yeka Toplam Kapasitesi Üst Yeka Toplam Kapasitesinden Büyük Olamaz.')
    #                     return render(request, 'Yeka/update_sub_yeka.html',
    #                                   {'yeka_form': yeka_form, 'error_messages': '', 'alt_yekalar': alt_yekalar,
    #                                    'yeka_connection_capacity': yeka_connection_capacities, 'yeka': uuid,
    #                                    'current_capacities': sub_capacities
    #                                    })
    #
    #                 log = "Alt Yeka güncellendi"
    #                 log = general_methods.logwrite(request, request.user, log)
    #                 messages.success(request, 'Alt Yeka Başarıyla Kayıt Edilmiştir.')
    #                 return redirect('ekabis:view_yeka')
    #
    #             else:
    #                 error_message_unit = get_error_messages(yeka_form)
    #                 return render(request, 'Yeka/update_sub_yeka.html',
    #                               {'yeka_form': yeka_form, 'error_messages': error_message_unit,
    #                                'alt_yekalar': alt_yekalar, 'yeka_connection_capacity': yeka_connection_capacities,
    #                                'yeka': uuid, 'current_capacities': sub_capacities
    #                                })
    #
    #         return render(request, 'Yeka/update_sub_yeka.html',
    #                       {'yeka_form': yeka_form, 'error_messages': '', 'alt_yekalar': alt_yekalar,
    #                        'yeka_connection_capacity': yeka_connection_capacities, 'yeka': uuid,
    #                        'current_capacities': sub_capacities
    #                        })
    #
    # except Exception as e:
    #     traceback.print_exc()
    #     messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
    #     return redirect('ekabis:change_sub_yeka', uuid)
    return


def yeka_person_list(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:

        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)

        yeka_filter = {
            'uuid': uuid,

        }
        yeka = YekaGetService(request, yeka_filter)
        yeka_person_filter = {
            'yeka': yeka,
            'isDeleted': False,
            'is_active': True
        }

        yeka_person = YekaPersonService(request, yeka_person_filter).order_by('-creationDate')
        array = []
        for person in yeka_person:
            array.append(person.employee.uuid)
        name = ''
        if yeka.business:
            name = general_methods.yekaname(yeka.business)
        # ekstra servis yazılacak
        persons = Employee.objects.filter(isDeleted=False).exclude(uuid__in=array).order_by('-creationDate')
        if request.POST:
            with transaction.atomic():
                if request.POST['yeka'] == 'add':
                    persons = request.POST.getlist('employee')
                    if persons:
                        for person_id in persons:
                            person_filter = {
                                'pk': person_id
                            }
                            employee = EmployeeGetService(request, person_filter)
                            person_yeka = YekaPerson(yeka=yeka, employee=employee, is_active=True)
                            person_yeka.save()

                            personHistory = YekaPersonHistory(yeka=yeka, person=employee, is_active=True)
                            personHistory.save()

                            log = str(yeka.definition) + ' adlı yekaya - ' + str(
                                employee.person.user.get_full_name()) + " adlı personel atandı."
                            log = general_methods.logwrite(request, request.user, log)
                            url = redirect('ekabis:view_yeka_detail', yeka.uuid).url
                            html = '<a style="color:black;" href="' + url + '">' + str(
                                id) + str(yeka.definition) + ' </a> adlı yekaya - ' + str(
                                employee.person.user.get_full_name()) + ' adlı personel atandı.'
                            notification(request, html, yeka.uuid, 'yeka')
                else:
                    persons = request.POST.getlist('sub_employee')
                    if persons:
                        for person_id in persons:
                            person_filter = {
                                'pk': person_id
                            }
                            employee = EmployeeGetService(request, person_filter)
                            yeka_person = YekaPerson.objects.get(
                                Q(isDeleted=False) & Q(yeka__uuid=uuid) & Q(employee__uuid=employee.uuid))

                            yeka_person.isDeleted = True
                            yeka_person.is_active = False
                            yeka_person.save()

                            personHistory = YekaPersonHistory(yeka=yeka_person.yeka, person=employee, is_active=False)
                            personHistory.save()

                            log = str(yeka_person.yeka.definition) + ' adlı yekadan -' + str(
                                employee.person.user.get_full_name()) + " personeli çıkarıldı."
                            log = general_methods.logwrite(request, request.user, log)
                            url = redirect('ekabis:view_yeka_detail', yeka.uuid).url
                            html = '<a style="" href="' + url + '">' + str(
                                id) + str(yeka.definition) + ' </a> adlı yekaya - ' + str(
                                employee.person.user.get_full_name()) + ' adlı personel çıkarıldı.'
                            notification(request, html, yeka.uuid, 'yeka')

            return redirect('ekabis:view_yeka_detail', yeka.uuid)
        return render(request, 'Yeka/yekaPersonList.html',
                      {'persons': persons, 'yeka_persons': yeka_person, 'yeka_uuid': uuid, 'urls': urls,
                       'current_url': current_url, 'url_name': url_name, 'yeka': yeka, 'name': name})
    except Exception as e:

        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


# yeka firma atama
# def yeka_company_list(request, uuid):
#     perm = general_methods.control_access(request)
#
#     if not perm:
#         logout(request)
#         return redirect('accounts:login')
#     urls = last_urls(request)
#     current_url = resolve(request.path_info)
#     url_name = Permission.objects.get(codename=current_url.url_name)
#     yeka_filter = {
#         'uuid': uuid
#     }
#
#     yeka = YekaGetService(request, yeka_filter)
#     yeka_company_filter = {
#         'yeka': yeka,
#         'isDeleted': False,
#         'is_active': True
#
#     }
#     url = general_methods.yeka_control(request, yeka)
#     if url and url != 'view_yeka_company':
#         return redirect('ekabis:' + url, yeka.uuid)
#
#     yeka_company = YekaCompanyService(request, yeka_company_filter).order_by('-creationDate')
#     array = []
#     for company_yeka in yeka_company:
#         array.append(company_yeka.company.uuid)
#
#     companies = Company.objects.filter(isDeleted=False).exclude(uuid__in=array)
#     if request.POST:
#         with transaction.atomic():
#             if request.POST['yeka'] == 'add':
#                 companies = request.POST.getlist('company')
#                 if companies:
#                     for company_id in companies:
#                         company = Company.objects.get(pk=company_id)
#                         yeka_company = YekaCompany(yeka=yeka, company=company, is_active=True)
#                         yeka_company.save()
#                         log = str(yeka.definition) + ' adlı yekaya -' + str(company.name) + " adlı firma atandı."
#                         log = general_methods.logwrite(request, request.user, log)
#             else:
#                 companies = request.POST.getlist('company')
#                 if companies:
#                     for company_id in companies:
#                         company = Company.objects.get(pk=company_id)
#
#                         yeka_company = YekaCompany.objects.get(
#                             Q(yeka__uuid=uuid) & Q(company=company) & Q(isDeleted=False))
#
#                         if yeka_company:
#                             yeka_company.isDeleted = True
#                             yeka_company.is_active = False
#                             yeka_company.save()
#
#                         companyHistory = YekaCompanyHistory(yeka=yeka_company.yeka, company=company, is_active=False)
#                         companyHistory.save()
#
#                         log = str(yeka_company.yeka.definition) + '-' + str(
#                             yeka_company.company.name) + " adlı firma çıkarıldı."
#                         log = general_methods.logwrite(request, request.user, log)
#         return redirect('ekabis:view_yeka_company', yeka.uuid)
#
#     return render(request, 'Yeka/yeka_company_list.html',
#                   {'companies': companies, 'yeka_companies': yeka_company, 'yeka_uuid': uuid, 'urls': urls,
#                    'current_url': current_url, 'url_name': url_name})
#
# yeka firma güncelleme
# def yeka_company_assignment(request):
#     perm = general_methods.control_access(request)
#     if not perm:
#         logout(request)
#         return redirect('accounts:login')
#     try:
#         with transaction.atomic():
#             if request.method == 'POST' and request.is_ajax():
#                 company_uuid = request.POST['company_uuid']
#                 yeka_uuid = request.POST['yeka_uuid']
#
#                 yeka_filter = {
#                     'uuid': yeka_uuid
#                 }
#
#                 yeka = YekaGetService(request, yeka_filter)
#                 company_filter = {
#                     'uuid': company_uuid
#                 }
#                 company = CompanyGetService(request, company_filter)
#
#                 yeka_company = YekaCompany(yeka=yeka, company=company, is_active=True)
#                 yeka_company.save()
#
#                 log = str(yeka.definition) + ' adlı yekaya -' + str(company.name) + " adlı firma atandı."
#                 log = general_methods.logwrite(request, request.user, log)
#
#                 return JsonResponse({'status': 'Success', 'msg': 'save successfully'})
#
#             else:
#                 return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
#     except:
#         traceback.print_exc()
#         return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})
#
# yeka firma silme
# def yeka_company_remove(request):
#     perm = general_methods.control_access(request)
#     if not perm:
#         logout(request)
#         return redirect('accounts:login')
#     try:
#         with transaction.atomic():
#             if request.method == 'POST' and request.is_ajax():
#                 uuid = request.POST['uuid']
#                 company = Company.objects.get(uuid=uuid)
#
#                 yeka_company = YekaCompany.objects.get(
#                     Q(yeka__uuid=request.POST['yeka_uuid']) & Q(company__uuid=uuid) & Q(isDeleted=False))
#
#                 if yeka_company:
#                     yeka_company.isDeleted = True
#                     yeka_company.is_active = False
#                     yeka_company.save()
#
#                 companyHistory = YekaCompanyHistory(yeka=yeka_company.yeka, company=company, is_active=False)
#                 companyHistory.save()
#
#                 log = str(yeka_company.yeka.definition) + '-' + str(
#                     yeka_company.company.name) + " adlı firma çıkarıldı."
#                 log = general_methods.logwrite(request, request.user, log)
#
#                 return JsonResponse({'status': 'Success', 'msg': 'save successfully'})
#
#             else:
#                 return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
#     except:
#         traceback.print_exc()
#         return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required()
def view_yekabusinessBlog(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        yeka_filter = {
            'uuid': uuid
        }
        yeka = YekaGetService(request, yeka_filter)
        url = general_methods.yeka_control(request, yeka)
        if url and url != 'view_yekabusinessBlog':
            return redirect('ekabis:' + url, yeka.uuid)
        yekabusinessbloks = None

        if yeka.business:
            yekabusiness = yeka.business
            yekabusinessbloks = yekabusiness.businessblogs.filter(isDeleted=False).order_by('sorting')

        return render(request, 'Yeka/timeline.html',
                      {'yekabusinessbloks': yekabusinessbloks,
                       'yeka': yeka,
                       'urls': urls, 'current_url': current_url,
                       'url_name': url_name,

                       })

    except Exception as e:

        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required()
def change_yekabusinessBlog(request, yeka, yekabusiness, business):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        yeka_filter = {
            'uuid': yeka
        }

        yeka = YekaGetService(request, yeka_filter)
        yeka_yekabusiness_filter_ = {
            'uuid': yekabusiness
        }

        yekabussiness = YekaBusinessBlogGetService(request, yeka_yekabusiness_filter_)
        yeka_business_filter_ = {
            'uuid': business
        }
        business = BusinessBlogGetService(request, yeka_business_filter_)
        yekaBusinessBlogo_form = YekaBusinessBlogForm(business.pk, yekabussiness, request.POST or None,
                                                      request.FILES or None,
                                                      instance=yekabussiness)
        yekaBusinessBlogo_form.fields['dependence_parent'].queryset = yeka.business.businessblogs.exclude(
            uuid=yekabussiness.uuid).filter(isDeleted=False)
        yekaBusinessBlogo_form.fields['child_block'].queryset = yeka.business.businessblogs.exclude(
            uuid=yekabussiness.uuid).filter(isDeleted=False)

        # if yekaBusinessBlogo_form['dependence_parent'].initial != None:
        #     yekaBusinessBlogo_form.fields['startDate'].widget.attrs['disabled'] = True
        # yekaBusinessBlogo_form.fields['status'].widget.attrs['disabled'] = True
        name = general_methods.yekaname(yeka.business)
        holding_competition_form = None
        if business.name == 'Yarışmanın Yapılması':

            if YekaHoldingCompetition.objects.filter(business=yeka.business):
                holding_competition = YekaHoldingCompetition.objects.get(business=yeka.business)
            else:
                holding_competition = YekaHoldingCompetition(
                    yekabusinessblog=yekabussiness,
                    business=yeka.business
                )
                holding_competition.save()
            holding_competition_form = YekaHoldingCompetitionForm(request.POST or None,
                                                                  instance=holding_competition)

        if request.POST:

            yekaBusinessBlogo_form = YekaBusinessBlogForm(business.pk, yekabussiness, request.POST or None,
                                                          request.FILES or None,
                                                          instance=yekabussiness)
            if holding_competition_form:
                if holding_competition_form.is_valid():
                    holding_comp = holding_competition_form.save(request, commit=False)
                    holding_comp.save()
                    if YekaContract.objects.filter(business=yeka.business):
                        contract = YekaContract.objects.get(business=yeka.business)
                    else:
                        contract = YekaContract(
                            yekabusinessblog=yekabussiness,
                            business=yeka.business
                        )
                        contract.save()
                    if holding_competition_form.cleaned_data['unit'].name == 'TL':
                        contract.unit = ConnectionUnit.objects.get(name='TL')
                        contract.save()
                    elif holding_competition_form.cleaned_data['unit'].name == 'USD':
                        contract.unit = ConnectionUnit.objects.get(name='USD')
                        contract.save()
            if yekaBusinessBlogo_form.is_valid():
                if yekabussiness.indefinite:
                    yekabussiness.businessTime = None
                    yekabussiness.save()
                    yekaBusinessBlogo_form.cleaned_data['businessTime'] = None
                    yekaBusinessBlogo_form.save(yekabussiness.pk, business.pk)
                else:
                    yekaBusinessBlogo_form.save(yekabussiness.pk, business.pk)
                # if yekaBusinessBlogo_form['child_block'].data == yekaBusinessBlogo_form['dependence_parent'].data:
                #     messages.warning(request, 'Bir önceki iş bloğu ile bir sonraki iş bloğu aynı olamaz.')
                #     return render(request, 'Yeka/YekabussinesBlogUpdate.html',
                #                   {
                #                       'yekaBusinessBlogo_form': yekaBusinessBlogo_form,
                #                       'yeka': yeka, 'urls': urls, 'current_url': current_url, 'url_name': url_name,
                #                       'name': name
                #                   })

                childblock = yekabussiness.child_block
                if childblock:
                    childblock.parent = yekabussiness
                    childblock.dependence_parent = yekabussiness
                    childblock.save()
                if not yekabussiness.indefinite and yekabussiness.startDate:
                    dependence_blocks = YekaBusinessBlog.objects.filter(dependence_parent=yekabussiness)
                    for dependence_block in dependence_blocks:
                        add_time_next(yekabussiness.pk, dependence_block.pk, yeka)

                url = redirect('ekabis:view_yeka_detail', yeka.uuid).url
                html = '<a style="" href="' + url + '"> ID: ' + str(
                    yekabussiness.pk) + '-' + str(yekabussiness.businessblog.name) + ' </a> adlı iş bloğu güncellendi.'
                notification(request, html, yeka.uuid, 'yeka')
                return redirect('ekabis:view_yeka_detail', yeka.uuid)
        else:
            for item in yekabussiness.parameter.filter(isDeleted=False, parametre__visibility_in_yeka=True):
                if item.parametre.type == 'file':
                    if item.file:
                        yekaBusinessBlogo_form.fields[item.parametre.title].initial = item.file
                        yekaBusinessBlogo_form.fields[item.parametre.title].widget.attrs = {'class': 'form-control'}

                elif item.parametre.type == 'date':
                    if item.value:
                        yekaBusinessBlogo_form.fields[item.parametre.title].initial = item.value
                        yekaBusinessBlogo_form.fields[item.parametre.title].widget.attrs = {
                            'class': 'form-control datepicker6'}
                else:
                    yekaBusinessBlogo_form.fields[item.parametre.title].initial = item.value
        return render(request, 'Yeka/YekabussinesBlogUpdate.html',
                      {
                          'yekaBusinessBlogo_form': yekaBusinessBlogo_form,
                          'yeka': yeka, 'urls': urls, 'current_url': current_url, 'url_name': url_name,
                          'name': name, 'holding_competition_form': holding_competition_form
                      })
    except Exception as e:

        traceback.print_exc()
        messages.warning(request, e)
        return redirect('ekabis:view_yeka')


def add_time_next(parent_id, current_id, yeka):
    parent_block = YekaBusinessBlog.objects.get(pk=parent_id)
    current_block = YekaBusinessBlog.objects.get(pk=current_id)
    if parent_block.completion_date:
        start_date = parent_block.completion_date
    else:
        start_date = parent_block.startDate
    if parent_block.businessTime:
        time = parent_block.businessTime
    else:
        return redirect('ekabis:view_yeka_detail', yeka.uuid)
    time_type = parent_block.time_type
    if time_type == 'is_gunu':
        add_time = time
        count = 0
        while add_time > 1:
            start_date = start_date + datetime.timedelta(days=1)
            count = count + 1
            is_vacation = is_vacation_day(start_date)
            if not is_vacation:
                add_time = add_time - 1
    else:
        start_date = start_date + datetime.timedelta(days=time) - datetime.timedelta(days=1)
    current_block.startDate = start_date
    current_block.save()
    dependence_blocks = YekaBusinessBlog.objects.filter(dependence_parent=current_block)
    for dependence_block in dependence_blocks:
        add_time_next(current_block.pk, dependence_block.pk, yeka)


def add_yekabusinessblog_company(request, business, yekabusinessblog):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        yeka_filter = {
            'uuid': business
        }

        yekabusiness = YekaBusinessGetService(request, yeka_filter)
        yeka_yekabusiness_filter = {
            'uuid': yekabusinessblog
        }
        name = general_methods.yekaname(yekabusiness)

        yekabussinessblog = YekaBusinessBlogGetService(request, yeka_yekabusiness_filter)

        application = CompetitionApplication.objects.get(business=yekabusiness)
        competition = YekaCompetition.objects.get(business=yekabusiness)
        region = ConnectionRegion.objects.filter(yekacompetition=competition).first()
        yeka = Yeka.objects.filter(connection_region=region).first()
        company_list = []
        if YekaCompany.objects.filter(application=application):
            yeka_company = YekaCompany.objects.filter(application=application)
            array_company = []
            for item in yeka_company:
                array_company.append(item.company.pk)
            company_list = Company.objects.exclude(id__in=array_company).filter(isDeleted=False)
        else:
            company_list = Company.objects.all()
        if request.POST:
            with transaction.atomic():
                get_list_company = request.POST.getlist('company')

                for id in get_list_company:
                    company = Company.objects.get(uuid=id)
                    yeka_app = YekaCompany(application=application, company=company, yeka=yeka, competition=competition,
                                           connection_region=region)
                    yeka_app.save()
                    for necessary in application.necessary.all():
                        file = YekaApplicationFile(
                            filename=necessary,
                        )
                        file.save()
                        yeka_app.files.add(file)
                        yeka_app.save()
                messages.success(request, 'Firma  eklenmistir.')
                return redirect('ekabis:view_application', yekabusiness.uuid, yekabussinessblog.uuid)

        return render(request, 'Yeka/add_yekabusinessblog_company.html',
                      {
                          'name': name, 'urls': urls, 'current_url': current_url, 'url_name': url_name,
                          'companies': company_list,
                      })
    except Exception as e:

        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


def change_yekabusinessblog_company(request, uuid, business, yekabusinessblog):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        yeka_business_company = YekaCompany.objects.get(uuid=uuid)
        yeka_filter = {
            'uuid': business
        }

        yekabusiness = YekaBusinessGetService(request, yeka_filter)
        yeka_yekabusiness_filter = {
            'uuid': yekabusinessblog
        }
        name = general_methods.yekaname(yekabusiness)

        yekabussinessblog = YekaBusinessBlogGetService(request, yeka_yekabusiness_filter)
        application = CompetitionApplication.objects.get(business=yekabusiness)
        competition = YekaCompetition.objects.get(business=yekabusiness)
        region = ConnectionRegion.objects.filter(yekacompetition=competition).first()
        yeka = Yeka.objects.filter(connection_region=region).first()
        company_list = []
        if YekaCompany.objects.filter(application=application):
            yeka_company = YekaCompany.objects.filter(application=application)
            array_company = []
            for item in yeka_company:
                array_company.append(item.company.pk)
            company_list = Company.objects.exclude(id__in=array_company).filter(isDeleted=False)
            companies = company_list
        if request.POST:
            with transaction.atomic():
                new_company = request.POST('company')
                yeka_business_company.company = Company.objects.get(uuid=new_company)
                yeka_business_company.save()

        return render(request, 'Yeka/change_businessblog_company.html',
                      {
                          'name': name, 'urls': urls, 'current_url': current_url, 'url_name': url_name,
                          'companies': company_list, 'yeka_company': yeka_business_company
                      })
    except Exception as e:

        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required()
def view_yekabusiness_gant(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        yeka_filter = {
            'uuid': uuid
        }
        yeka = YekaGetService(request, yeka_filter)

        url = general_methods.yeka_control(request, yeka)
        if url and url != 'view_yekabusinessBlog':
            return redirect('ekabis:' + url, yeka.uuid)
        yekabusinessbloks = None

        extratime_filter = {
            'business': yeka.business,
            'isDeleted': False,
        }
        ekstratimes = ExtraTimeService(request, extratime_filter)
        extratime = []
        name = general_methods.yekaname(yeka.business)
        endDate = None
        for item in ekstratimes:
            if ExtraTime.objects.filter(yekabusinessblog=item.yekabusinessblog).count() > 1:
                extra = ExtraTime.objects.filter(yekabusinessblog=item.yekabusinessblog).order_by('-creationDate')
                date = None
                ex = None
                for busines in range(len(extra)):

                    if busines == 0:
                        if extra[busines] == item:
                            endDate = item.yekabusinessblog.finisDate
                            ex = item.yekabusinessblog.creationDate

                        else:
                            date = extra[busines].yekabusinessblog.finisDate
                    else:
                        if extra[busines] == item:
                            endDate = date + datetime.timedelta(days=item.time)
                            ex = item.yekabusinessblog.creationDate
                        else:
                            date = extra[busines].yekabusinessblog.finisDate + datetime.timedelta(days=item.time)
                beka = {
                    'uuid': item.uuid,
                    'content': item.yekabusinessblog.businessblog.name + " Ek Süre" + str(ex),
                    'start': endDate,
                    'finish': endDate + datetime.timedelta(days=item.time),
                    'bloguuid': item.yekabusinessblog.uuid,
                }
                extratime.append(beka)
            else:
                beka = {
                    'uuid': item.uuid,
                    'content': item.yekabusinessblog.businessblog.name + " Ek Süre",
                    'start': item.yekabusinessblog.finisDate,
                    'finish': item.yekabusinessblog.finisDate + datetime.timedelta(days=item.time),
                    'bloguuid': item.yekabusinessblog.uuid,
                }
                extratime.append(beka)

        if yeka.business:
            yekabusiness = yeka.business
            yekabusinessbloks = yekabusiness.businessblogs.exclude(businessblog__name='Fiyat Eskalasyonu').filter(
                isDeleted=False).order_by('sorting')
        return render(request, 'Yeka/gant.html',
                      {'yekabusinessbloks': yekabusinessbloks,
                       'yeka': yeka,
                       'ekstratimes': extratime, 'urls': urls,
                       'current_url': current_url, 'url_name': url_name,
                       'name': name
                       })

    except Exception as e:

        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required()
def view_yekabusiness_gant2(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        yeka_filter = {
            'uuid': uuid
        }
        yeka = YekaGetService(request, yeka_filter)

        url = general_methods.yeka_control(request, yeka)
        if url and url != 'view_yekabusinessBlog':
            return redirect('ekabis:' + url, yeka.uuid)
        yekabusinessbloks = None

        extratime_filter = {
            'yeka': yeka
        }
        ekstratimes = ExtraTimeService(request, extratime_filter)

        if yeka.business:
            yekabusiness = yeka.business
            yekabusinessbloks = yekabusiness.businessblogs.filter(isDeleted=False).order_by('sorting')
        return render(request, 'Yeka/gant.html',
                      {'yekabusinessbloks': yekabusinessbloks,
                       'yeka': yeka,
                       'ekstratimes': ekstratimes
                       })

    except Exception as e:

        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required()
def view_yekabusinessblog_gant(request, yeka, yekabusiness):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        yeka_filter = {
            'uuid': yeka
        }

        yeka_yekabusiness_filter_ = {
            'uuid': yekabusiness
        }

        yekabussiness = YekaBusinessBlogGetService(request, yeka_yekabusiness_filter_)
        yeka = YekaCompetition.objects.get(uuid=yeka)
        region = ConnectionRegion.objects.filter(yekacompetition__in=yeka)
        extrafilter = {
            'yekabusinessblog': yekabussiness
        }
        extratime = ExtraTimeService(request, extrafilter)
        # name = general_methods.yekaname(yeka.business)

        return render(request, 'Yeka/yekabussinessblog_detail.html',
                      {
                          'yeka': yeka,
                          'yekabusinessblok': yekabussiness,
                          'ekstratimes': extratime, 'urls': urls, 'current_url': current_url, 'url_name': url_name
                      })
    except Exception as e:

        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required()
def view_yekacompetition_business_gant(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        yekacompetition_filter = {
            'uuid': uuid
        }
        yeka = YekaCompetitionGetService(request, yekacompetition_filter)

        url = general_methods.competition_control(request, yeka)
        if url and url != 'view_yekacompeittion_business_gant':
            return redirect('ekabis:' + url, yeka.uuid)
        yekabusinessbloks = None

        extratime_filter = {
            'business': yeka.business,
            'isDeleted': False,
        }
        ekstratimes = ExtraTimeService(request, extratime_filter)
        extratime = []
        endDate = None
        for item in ekstratimes:
            if ExtraTime.objects.filter(yekabusinessblog=item.yekabusinessblog).count() > 1:
                extra = ExtraTime.objects.filter(yekabusinessblog=item.yekabusinessblog).order_by('-creationDate')
                date = None
                ex = None
                for busines in range(len(extra)):

                    if busines == 0:
                        if extra[busines] == item:
                            endDate = item.yekabusinessblog.finisDate
                            ex = item.yekabusinessblog.creationDate

                        else:
                            date = extra[busines].yekabusinessblog.finisDate
                    else:
                        if extra[busines] == item:
                            endDate = date + datetime.timedelta(days=item.time)
                            ex = item.yekabusinessblog.creationDate
                        else:
                            date = extra[busines].yekabusinessblog.finisDate + datetime.timedelta(days=item.time)
                beka = {
                    'uuid': item.uuid,
                    'content': item.yekabusinessblog.businessblog.name + " Ek Süre" + str(ex),
                    'start': endDate,
                    'finish': endDate + datetime.timedelta(days=item.time),
                    'bloguuid': item.yekabusinessblog.uuid,
                }
                extratime.append(beka)
            else:
                beka = {
                    'uuid': item.uuid,
                    'content': item.yekabusinessblog.businessblog.name + " Ek Süre",
                    'start': item.yekabusinessblog.finisDate,
                    'finish': item.yekabusinessblog.finisDate + datetime.timedelta(days=item.time),
                    'bloguuid': item.yekabusinessblog.uuid,
                }
                extratime.append(beka)

        if yeka.business:
            yekabusiness = yeka.business
            yekabusinessbloks = yekabusiness.businessblogs.filter(isDeleted=False).order_by('sorting')
        return render(request, 'Yeka/gant.html',
                      {'yekabusinessbloks': yekabusinessbloks,
                       'yeka': yeka,
                       'ekstratimes': extratime, 'urls': urls, 'current_url': current_url, 'url_name': url_name
                       })

    except Exception as e:

        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required()
def view_ufe(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        # data = general_methods.ufe()
        data = []

        return render(request, 'Yeka/ufe.html',
                      {'urls': urls, 'current_url': current_url, 'url_name': url_name,
                       'data': data
                       })

    except Exception as e:

        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required()
def view_kur(request, ):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        data = general_methods.kur()

        return render(request, 'Yeka/kur.html',
                      {'urls': urls, 'current_url': current_url, 'url_name': url_name,
                       'data': data
                       })

    except Exception as e:

        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


def test_yeka(request):
    table_th = []
    from collections import namedtuple
    def namedtuplefetchall(cursor):
        "Return all rows from a cursor as a namedtuple"
        desc = cursor.not_description
        for col in desc:
            table_th.append(col[0])
        nt_result = namedtuple('Result', [col[0] for col in desc])
        return [nt_result(*row) for row in cursor.fetchall()]

    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT  yeka.capacity  ,yeka.name,app.finishDate,app.preRegistration FROM ekabis_yekacompetition as yeka left JOIN ekabis_yekaapplication as app ON yeka.business_id=app.business_id")
        row = namedtuplefetchall(cursor)
    return render(request, 'Yeka/cytoscape.html', {'row': row,
                                                   'table_th': table_th})


@login_required()
def view_yeka_detail(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:

        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        yeka_filter = {
            'uuid': uuid
        }
        user = request.user
        employee = None
        yeka = YekaGetService(request, yeka_filter)

        if YekaPerson.objects.filter(employee__person__user=user, yeka=yeka, isDeleted=False):
            employee = YekaPerson.objects.get(employee__person__user=user, yeka=yeka, isDeleted=False)

        employe_filter = {
            'yeka': yeka
        }
        name = ''
        blocks = []
        indemnity_bond_file = None
        indemnity_quantity = None
        # x = yeka.business.businessblogs.filter(isDeleted=False,
        #                                        businessblog__name='YEKA Kullanım Hakkı Sözleşmesinin İmzalanması')
        # if x:
        #     block = yeka.business.businessblogs.get(isDeleted=False,
        #                                             businessblog__name='YEKA Kullanım Hakkı Sözleşmesinin İmzalanması')
        #     if block.parameter.filter(isDeleted=False).filter(parametre__title='Teminat Mektubu'):
        #         indemnity_bond_file = block.parameter.get(isDeleted=False, parametre__title='Teminat Mektubu').file
        #     if block.parameter.filter(isDeleted=False).filter(parametre__title='Teminat Miktarı'):
        #         indemnity_quantity = block.parameter.get(isDeleted=False, parametre__title='Teminat Miktarı').value
        yekabusinessbloks = None
        if yeka.business:
            name = general_methods.yekaname(yeka.business)  # Yeka Adı
            yekabusiness = yeka.business
            yekabusinessbloks = yekabusiness.businessblogs.filter(isDeleted=False).order_by('sorting')
            for blok in yekabusinessbloks:  # Yekaya Ait İş planı
                bloc_dict = {}

                bloc_dict['yekabusinessblog'] = blok
                bloc_dict['businessblog'] = blok.businessblog.uuid
                bloc_dict['yeka'] = yeka.uuid
                blocks.append(bloc_dict)
        connection_regions = yeka.connection_region.filter(isDeleted=False).order_by('name')
        employees = YekaPersonService(request, employe_filter)
        return render(request, 'Yeka/yekaDetail.html',
                      {'urls': urls, 'current_url': current_url, 'employee': employee,
                       'url_name': url_name, 'name': name, 'blocks': blocks, 'user': user,
                       'yeka': yeka, 'yekabusinessbloks': yekabusinessbloks, 'indemnity_quantity': indemnity_quantity,
                       'indemnity_file': indemnity_bond_file,
                       'employees': employees, 'connection_regions': connection_regions
                       })
    except Exception as e:

        traceback.print_exc()
        messages.warning(request, e)
        return redirect('ekabis:view_yeka')


@login_required()
def test(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:

        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        yeka_filter = {
            'uuid': uuid
        }
        yeka = YekaGetService(request, yeka_filter)
        name = general_methods.yekaname(yeka.business)
        yekabusinessbloks = None
        if yeka.business:
            yekabusiness = yeka.business
            yekabusinessbloks = yekabusiness.businessblogs.filter(isDeleted=False).order_by('sorting')

        employe_filter = {
            'yeka': yeka
        }

        employees = YekaPersonService(request, employe_filter)

        return render(request, 'test.html',
                      {'urls': urls, 'current_url': current_url,
                       'url_name': url_name, 'name': name,
                       'yeka': yeka, 'yekabusinessbloks': yekabusinessbloks,
                       'employees': employees,

                       })

    except Exception as e:

        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required
def view_dependence(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                pk = request.POST['pk']
                business = request.POST['business']
                blog = YekaBusinessBlog.objects.get(pk=pk)

                if blog.finisDate:
                    return JsonResponse({'status': 'Success', 'msg': 'save successfully',
                                         'finishdate': blog.finisDate.strftime("%d/%m/%Y")})
                else:

                    return JsonResponse({'status': 'Success', 'msg': 'save successfully', 'finishdate': None})






            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def select_report(request):
    # from weasyprint import HTML,CSS
    try:
        print('TR')
        # html = HTML(string='''
        #     <!DOCTYPE html>
        # <html class="no-js" lang="tr">
        # <head>
        #     <style> table{border: 1px solid black;}</style>
        #     <meta charset="utf-8" />
        # </head>
        # <div class="header">
        #     <img class="logo"  src="'''  '''">
        # </div>
        # <div class="section-header">Servis Bilgileri</div>
        # <div class="container">
        #     <div class="row">
        #         <div class="row col-6 entry"><h3 class="col-4">Müşteri:</h3><p>''' '''</p></div>
        #         <div class="row col-6 entry"><h3 class="col-5">Servise Getiren:</h3><p>'''  '''</p></div>
        #     </div>
        #     <div class="row">
        #         <div class="row col-3 entry"><h3>Plaka:</h3><p>'''  '''</p></div>
        #         <div class="row col-5 entry"><h3>Marka/Model:</h3><p>'''  '''/'''  '''</p></div>
        #         <div class="row col-4 entry"><h3>Kilometre:</h3><p>'''  ''' KM</p></div>
        #     </div>
        #     <div class="row">
        #         <div class="row col-3 entry"><h3>Usta:</h3><p>''' '''</p></div>
        #         <div class="row col-5 entry"><h3>Giriş zamanı:</h3><p>'''  '''</p></div>
        #         <div class="row col-4 entry"><h3>Teslim Alan:</h3><p>'''  '''</p></div>
        #
        #
        #     </div>
        # <div>
        # <div class="desc-header">Şikayet:</div>
        # <div class="description">'''  '''</div>
        # <div class="desc-header">Tespit:</div>
        # <div class="description">'''  '''</div>
        # <table>
        # <caption>Servis  Ürün Listesi</caption>
        # <tr>
        #     <th>Barkod</th>
        #     <th>Ürün Adı</th>
        #     <th>Marka</th>
        #     <th>Adet</th>
        #     <th>Net Fiyat</th>
        #     <th>KDV</th>
        #     <th>Toplam Fiyat</th>
        # </tr>'''  '''
        # <tr class="footer">
        #     <th></th>
        #     <th></th>
        #     <th></th>
        #     <th>Net: </th><td class="last-td">'''  ''' ₺</td>
        #     <th>Toplam: </th><td class="last-td">''' ''' ₺</td>
        # </tr>
        # </table>
        # <div>
        #     <div class="section-header" style="page-break-before: always"> Araç Fotoğrafları </div>
        #     '''
        #
        #                    '''
        #                </div>
        #                </html>
        #
        #                ''')
        # css = CSS(string='''
        # .bordered{border-bottom: 10000000px solid black;}
        # .last-td{
        #     border:0px !important;
        # }
        # .container{
        #     display: block;
        # }
        # .row{
        #     display: flex;
        #     float:center;
        #     padding-top: 7px;
        #     padding-bottom: 7px;
        # }
        # .col-6{
        #     width: 50%;
        #     padding: 0px;
        #     margin: 0px;
        # }
        # .col-5{
        #     width: 40%;
        #     padding: 0px;
        #     margin: 0px;
        # }
        # .col-4{
        #     width: 33%;
        #     margin: 0px;
        #     padding: 0px;
        # }
        # .col-3{
        #     width: 25%;
        #     margin: 0px;
        #     padding: 0px;
        # }
        # .col-2{
        #     width: 16%;
        #     margin: 0px;
        #     padding: 0px;
        # }
        # .entry h3{
        #     font-size: 12px;
        #     margin-top:auto;
        #     margin-bottom:auto;
        # }
        # .entry p{
        #     font-size: 10px;
        #     margin-top:auto;
        #     margin-bottom:auto;
        #     padding-left: 5px;
        # }
        # .logo{
        #     height:70px;
        # }
        # .car-image{
        #     height:225px;
        #     width:300px;
        # }
        # .header{
        #     padding-bottom:20px;
        # }
        # .footer{
        #     align-items: right;
        #     text-align: right;
        # }
        # table caption{
        #     font-weight: bold;
        #     font-size: 16px;
        #     color: #fff;
        #     padding-top: 3px;
        #     padding-bottom: 2px;
        #     background-color: #3c4b64;
        # }
        # .car-image{
        #     padding-top: 5px;
        #     padding-bottom: 5px;
        #     padding-right: 5px;
        #     padding-left: 5px;
        # }
        # .section-header{
        #     padding-top: 5px;
        #     padding-bottom: 4px;
        #     background-color: #3c4b64;
        #     font-weight: bold;
        #     font-size: 16px;
        #     color: #fff;
        # }
        # table {
        #
        #     width: 100%;
        #     position: relative;
        # }
        # table * {
        #     position: relative;
        # }
        # table thead tr {
        #     height: 20px;
        #     background: #36304a;
        # }
        # table tbody tr {
        #     border: 1px solid black !important;
        #     height: 20px;
        # }
        # table td.c,
        # table th.c {
        #     text-align: center;
        # }
        # table td.r,
        # table th.r {
        #     text-align: center;
        # }
        # tbody tr {
        #     border: 1px solid black !important;
        #     font-size: 10px;
        #     color: #020203;
        #     line-height: 1.2;
        #     font-weight: unset;
        # }
        # .description {
        #     padding-top: 10px;
        #     padding-bottom: 10px;
        #     font-size: 12px;
        # }
        # .desc-header {
        #     padding-top: 10px;
        #     font-size: 14px;
        #     font-weight: bold;
        # }
        # ''')
        # html.write_pdf(
        #     'report.pdf', stylesheets=[css])
        # return FileResponse(open('report.pdf', 'rb'), status=status.HTTP_200_OK,
        #                     content_type='application/pdf')
    except:
        raise Exception("Error While creating service detail pdf")


def view_yeka_by_type(request, type):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        with transaction.atomic():
            urls = last_urls(request)
            current_url = resolve(request.path_info)
            url_name = Permission.objects.get(codename=current_url.url_name)
            filter = {'type': type}
            yeka = YekaService(request, filter)

            return render(request, 'Yeka/view_yeka_by_type.html',
                          {'error_messages': '', 'urls': urls, 'current_url': current_url, 'yeka': yeka, 'type': type,
                           'url_name': url_name})

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@api_view(http_method_names=['POST'])
def get_region(request):
    if request.POST:
        try:

            yeka_id = request.POST.get('yeka_id')
            yeka = Yeka.objects.get(pk=yeka_id)
            connection_region_yeka = yeka.connection_region.filter(isDeleted=False)

            data_region = ConnectionRegionSerializer(connection_region_yeka, many=True)

            responseData = dict()
            responseData['region'] = data_region.data

            return JsonResponse(responseData, safe=True)

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


@api_view(http_method_names=['POST'])
def get_yeka_company(request):
    if request.POST:
        try:

            yeka_company_id = request.POST.get('yeka_company_id')
            yeka_company = YekaCompany.objects.get(uuid=yeka_company_id)

            data_company = YekaCompanySerializer(yeka_company)

            responseData = dict()
            responseData['yeka_company'] = data_company.data

            return JsonResponse(responseData, safe=True)

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


@api_view(http_method_names=['POST'])
def get_yeka_competition(request):
    if request.POST:
        try:

            region_id = request.POST.get('region_id')
            region = ConnectionRegion.objects.get(pk=region_id)
            yeka_competition = region.yekacompetition.filter(isDeleted=False)
            company = Company.objects.filter(isDeleted=False)

            data_competition = YekaCompetitionSerializer(yeka_competition, many=True)
            data_company = CompanySerializer(company, many=True)

            responseData = dict()

            responseData['competition'] = data_competition.data
            responseData['company'] = data_company.data

            return JsonResponse(responseData, safe=True)

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


def company_application(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        with transaction.atomic():
            urls = last_urls(request)
            current_url = resolve(request.path_info)
            url_name = Permission.objects.get(codename=current_url.url_name)

            yekas = YekaService(request, None).order_by('-creationDate')

            return render(request, 'Application/make_company_application.html',
                          {'error_messages': '', 'urls': urls, 'current_url': current_url, 'yekas': yekas,
                           'url_name': url_name})

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


def save_company_app_file(request):
    if request.POST:
        try:
            name = ""
            id = request.POST['id']
            array = []
            array = json.loads(request.POST.get('files'))
            file_array = []
            for item in array:
                file = item['file']
                brc = file.split(';base64,')
                format = brc[0]
                imgstr = brc[1]
                ext = format.split('/')[-1]
                if FileExtension.objects.filter(mime_type=ext):
                    ext = FileExtension.objects.get(mime_type=ext).extension
                date = time.time() * 1000
                name = YekaApplicationFileName.objects.get(pk=item['filename']).filename
                data = ContentFile(base64.b64decode(imgstr), name=name + '_' + str(date) + '_temp.' + ext)
                x = {'name': item['filename'], 'file': data}
                file_array.append(x)
            yeka_company = YekaCompany.objects.get(uuid=id)
            if not array == None:

                for file in file_array:
                    if not \
                            yeka_company.files.filter(
                                filename=YekaApplicationFileName.objects.get(pk=int(file['name'])))[
                                0].file:

                        filename = YekaApplicationFileName.objects.get(pk=int(file['name']))
                        file_input = file['file']
                        app_file = yeka_company.files.filter(filename=filename).first()
                        app_file.file = file_input
                        app_file.save()

                    else:
                        return JsonResponse({'status': 'Fail', 'msg': "Bu dosya ismine ait dosya var."})
                url = redirect('ekabis:view_yeka_detail', yeka_company.yeka.uuid).url
                html = '<a style="" href="' + url + '"> ID: ' + str(
                    yeka_company.company.name) + ' </a> firmanın ' + name + ' belgesi  yüklendi.'
                notification(request, html, yeka_company.yeka.uuid, 'yeka')
                return JsonResponse({'status': 'Success', 'msg': "Başvuru Kayıt Edildi."})

            else:
                return JsonResponse({'status': 'Fail', 'msg': "Başvuru dosyaları kayıt edilemedi."})


        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


def make_application(request):
    if request.POST:
        try:

            competition_id = request.POST['competition_id']
            company_id = request.POST['company_id']
            yeka_id = request.POST['yeka_id']
            region_id = request.POST['region_id']

            yeka = Yeka.objects.get(pk=yeka_id)
            region = ConnectionRegion.objects.get(pk=region_id)
            competition = YekaCompetition.objects.get(pk=int(competition_id))
            company = Company.objects.get(pk=int(company_id))
            if competition.business.businessblogs.filter(businessblog__name='Başvurunun Alınması'):
                if CompetitionApplication.objects.filter(business=competition.business):
                    yeka_application = CompetitionApplication.objects.get(business=competition.business)
                else:
                    block = competition.business.businessblogs.filter(businessblog__name='Başvurunun Alınması').first()
                    yeka_application = CompetitionApplication(business=competition.business, yekabusinessblog=block)
                    yeka_application.save()

                if YekaCompany.objects.filter(company=company, competition=competition):
                    return JsonResponse({'status': 'Fail', 'msg': "Bu bilgilerde başvuru zaten var."})

                else:
                    yeka_company = YekaCompany(
                        company=company, competition=competition, connection_region=region, yeka=yeka,
                        application=yeka_application
                    )
                    yeka_company.save()
                    for necessary in yeka_application.necessary.all():
                        file = YekaApplicationFile(
                            filename=necessary,
                        )
                        file.save()
                        yeka_company.files.add(file)
                        yeka_company.save()
                url = redirect('ekabis:view_yeka_detail', yeka.uuid).url
                html = '<a style="" href="' + url + '"> ID: ' + str(
                    company.pk) + '-' + str(company.name) + ' </a> firma başvurusu oluşturuldu.'
                notification(request, html, yeka.uuid, 'yeka')
            else:
                return JsonResponse({'status': 'Fail', 'msg': "Başvuruların alınması iş bloğu mevcut değil."})

            return JsonResponse({'status': 'Success', 'msg': "Başvuru Kayıt Edildi."})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


def get_application(request):
    if request.POST:
        try:

            yeka_app = CompetitionApplication.objects.filter(isDeleted=False)
            region = None
            yeka = None
            competition = None
            applications = []
            for app in yeka_app:
                yeka = Yeka.objects.get(business=app.business)
                competition = YekaCompetition.objects.get(business=app.business)
                region = ConnectionRegion.objects.get(yekacompetition__in=competition)

                data_region = ConnectionRegionSerializer(region, many=True)
                data_competition = YekaCompetitionSerializer(competition, many=True)
                data_yeka = YekaSerializer(yeka, many=True)

                responseData = dict()

                responseData['competition'] = data_competition.data
                responseData['region'] = data_region.data
                responseData['yeka'] = data_yeka.data
                applications.append(responseData)

            return JsonResponse(applications, safe=True)

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


@login_required
def delete_yeka_company_file(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['id']
                obj = YekaApplicationFile.objects.get(uuid=uuid)
                data_as_json_pre = serializers.serialize('json', YekaApplicationFile.objects.filter(uuid=uuid))

                yeka_company = YekaCompany.objects.get(files=obj)
                file = yeka_company.files.get(file=obj.file)
                file.file.delete()
                file.save()

                log = 'Başvuru dosya ID: ' + str(obj.pk) + ' - ' + str(obj.filename.filename) + " belgesi silindi."
                logs = Logs(user=request.user, subject=log, ip=get_client_ip(request),
                            previousData=data_as_json_pre)
                logs.save()
                return JsonResponse({'status': 'Success', 'msg': 'Belge Silindi'})


    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@api_view(http_method_names=['POST'])
def get_yeka_competition_company(request):
    if request.POST:
        try:

            id = request.POST.get('competition_id')
            competition = YekaCompetition.objects.get(pk=id)
            companies = YekaCompany.objects.filter(competition=competition)

            data_companies = YekaCompanySerializer(companies, many=True)

            response = {

                'data': data_companies.data,
                'draw': int(request.POST.get('draw')),
                'recordsTotal': companies.count(),
                'recordsFiltered': companies.count(),

            }
            return JsonResponse(response)



        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


@api_view(http_method_names=['POST'])
def get_yeka_competition_proposal(request):
    if request.POST:
        try:

            id = request.POST.get('competition_id')
            competition = YekaCompetition.objects.get(pk=id)
            if YekaProposal.objects.filter(business=competition.business):
                yeka_proposal = YekaProposal.objects.get(business=competition.business)
                proposal = yeka_proposal.proposal.filter(isDeleted=False)
                data_proposal = ProposalSerializer(proposal, many=True)

                response = {

                    'data': data_proposal.data,
                    'draw': int(request.POST.get('draw')),
                    'recordsTotal': proposal.count(),
                    'recordsFiltered': proposal.count(),

                }
                return JsonResponse(response)
            else:
                response = {}
                return JsonResponse({'status': 'Fail', 'msg': 'Aday Yeka Bulunmamaktadır', 'response': response})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


@api_view(http_method_names=['POST'])
def get_yeka_competition_eskalasyon(request):
    if request.POST:
        try:

            id = request.POST.get('competition_id')
            competition = YekaCompetition.objects.get(pk=id)
            yeka_eskalasyon = YekaCompetitionEskalasyon.objects.filter(competition=competition)
            data_eskalasyon = YekaCompetitionEskalasyonSerializer(yeka_eskalasyon, many=True)

            response = {

                'data': data_eskalasyon.data,
                'draw': int(request.POST.get('draw')),
                'recordsTotal': yeka_eskalasyon.count(),
                'recordsFiltered': yeka_eskalasyon.count(),

            }
            return JsonResponse(response)

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


def yeka_report(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        with transaction.atomic():
            urls = last_urls(request)
            current_url = resolve(request.path_info)
            url_name = Permission.objects.get(codename=current_url.url_name)
            yekas = YekaService(request, None)

            return render(request, 'Yeka/rapor.html',
                          {'error_messages': '', 'urls': urls, 'current_url': current_url, 'yekas': yekas,
                           'url_name': url_name})
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


def yeka_business_time(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        yekas = Yeka.objects.filter(isDeleted=False)
        for yeka in yekas:
            for region in yeka.connection_region.filter(isDeleted=False):
                for competition in region.yekacompetition.filter(isDeleted=False):
                    for block in competition.business.businessblogs.filter(isDeleted=False):
                        if yeka.business.businessblogs.filter(businessblog__name=block.businessblog.name):
                            block.indefinite = yeka.business.businessblogs.get(
                                businessblog__name=block.businessblog.name).indefinite
                            block.time_type = yeka.business.businessblogs.get(
                                businessblog__name=block.businessblog.name).time_type
                            block.save()
                            if block.businessblog.name == 'Yarışmanın Yapılması':
                                unit = None
                                price = None
                                if YekaHoldingCompetition.objects.filter(business=competition.business):
                                    comp_holding = YekaHoldingCompetition.objects.get(business=competition.business)
                                    unit = comp_holding.unit
                                    price = comp_holding.max_price
                                if YekaContract.objects.filter(business=competition.business):
                                    contract=YekaContract.objects.get(business=competition.business)
                                    contract.unit=unit
                                    contract.save()
        return redirect('ekabis:view_yeka')

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')
