import traceback

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render

from ekabis.Forms.YekaBusinessBlogForm import YekaBusinessBlogForm
from ekabis.Forms.YekaConnectionRegionForm import YekaConnectionRegionForm
from ekabis.Forms.YekaForm import YekaForm
from ekabis.models import YekaCompanyHistory, YekaConnectionRegion, ConnectionRegion, YekaBusiness, ExtraTime
from ekabis.models.Company import Company
from ekabis.models.Employee import Employee
from ekabis.models.Yeka import Yeka
from ekabis.models.YekaBusinessBlog import YekaBusinessBlog
from ekabis.models.YekaCompany import YekaCompany
from ekabis.models.YekaPerson import YekaPerson
from ekabis.models.YekaPersonHistory import YekaPersonHistory
from ekabis.services import general_methods
from ekabis.services.general_methods import get_error_messages
from ekabis.services.services import YekaService, CompanyService, YekaConnectionRegionService, YekaGetService, \
    YekaConnectionRegionGetService, YekaPersonService, \
    EmployeeGetService, YekaCompanyService, CompanyGetService, ExtraTimeService, YekaBusinessBlogGetService, \
    BusinessBlogGetService, ConnectionRegionService
import datetime
@login_required
def return_yeka(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    yeka_form = YekaForm()
    try:
        with transaction.atomic():
            return render(request, 'Yeka/view_yeka.html',
                          {'yeka_form': yeka_form, 'error_messages': '', })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')
@login_required
def add_yeka(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        yeka_form = YekaForm()
        if request.method == 'POST':
            with transaction.atomic():
                yeka_form = YekaForm(request.POST)
                if yeka_form.is_valid():
                    yeka=yeka_form.save(commit=False)
                    yeka.save()

                    log = "Yeka eklendi"
                    log = general_methods.logwrite(request, request.user, log)
                    messages.success(request, 'Yeka Başarıyla Kayıt Edilmiştir.')
                    return redirect('ekabis:view_yeka')

                else:
                    error_message_unit = get_error_messages(yeka_form)

                    return render(request, 'Yeka/add_yeka.html',
                                  {'yeka_form': yeka_form, 'error_messages': error_message_unit,
                                   })

        return render(request, 'Yeka/add_yeka.html',
                      {'yeka_form': yeka_form, 'error_messages': ''})

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


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
                    obj.isDeleted = True
                    obj.save()
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

                    yeka.definition = yeka_form.cleaned_data['definition']
                    yeka.date = yeka_form.cleaned_data['date']
                    yeka.save()

                    new_regions = request.POST.getlist('region')
                    current = []
                    for region in new_regions:
                        current.append(ConnectionRegion.objects.get(uuid=region))
                    capacity = 0
                    for region in current:
                        capacity = capacity + region.value
                        if not region in yeka_regions:
                            new = YekaConnectionRegion(yeka=yeka, connectionRegion=region)
                            new.save()

                    sub_yeka = Yeka.objects.filter(Q(yekaParent=yeka) & Q(isDeleted=False))
                    if sub_yeka:
                        sub_capacity = 0
                        for sub in sub_yeka:
                            sub_capacity = sub_capacity + sub.capacity
                        if capacity >= sub_capacity:
                            yeka.capacity = capacity
                            yeka.save()
                        else:
                            error_message_unit = get_error_messages(yeka_form)
                            return render(request, 'Yeka/change_yeka.html',
                                          {'yeka_form': yeka_form, 'error_messages': error_message_unit,
                                           'yeka_connections': yeka_regions, 'connection_regions': connection_regions
                                           })

                    else:
                        yeka.capacity = capacity
                        yeka.save()

                    delete_yeka = list(set(yeka_regions) - set(current))

                    for delete_yeka in delete_yeka:
                        delete = YekaConnectionRegion.objects.get(
                            Q(connectionRegion__uuid=delete_yeka.uuid) & Q(yeka=yeka))
                        delete.delete()

                    messages.success(request, 'Yeka Başarıyla Güncellendi')
                    return redirect('ekabis:view_yeka')
                else:
                    error_message_unit = get_error_messages(yeka_form)
                    return render(request, 'Yeka/change_yeka.html',
                                  {'yeka_form': yeka_form, 'error_messages': error_message_unit,
                                   'yeka_connections': yeka_regions, 'connection_regions': connection_regions
                                   })

            return render(request, 'Yeka/change_yeka.html',
                          {'yeka_form': yeka_form, 'error_messages': '', 'yeka_connections': yeka_regions,
                           'connection_regions': connection_regions
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


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

    yeka_filter = {
        'uuid': uuid,

    }
    yeka = YekaGetService(request, yeka_filter)
    yeka_person_filter = {
        'yeka': yeka,
        'isDeleted': False,
        'is_active':True
    }

    yeka_person = YekaPersonService(request, yeka_person_filter).order_by('-creationDate')
    array = []
    for person in yeka_person:
        array.append(person.employee.uuid)

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
                        person = EmployeeGetService(request, person_filter)
                        person_yeka = YekaPerson(yeka=yeka, employee=person, is_active=True)
                        person_yeka.save()

                        personHistory = YekaPersonHistory(yeka=yeka, person=person, is_active=True)
                        personHistory.save()

                        log = str(yeka.definition) + ' adlı yekaya - ' + str(
                            person.user.get_full_name()) + " adlı personel atandı."
                        log = general_methods.logwrite(request, request.user, log)
            else:
                persons = request.POST.getlist('sub_employee')
                if persons:
                    for person_id in persons:
                        person_filter = {
                            'pk': person_id
                        }
                        person = EmployeeGetService(request, person_filter)
                        yeka_person = YekaPerson.objects.get(
                            Q(isDeleted=False) & Q(yeka__uuid=uuid) & Q(employee__uuid=person.uuid))

                        yeka_person.isDeleted = True
                        yeka_person.is_active = False
                        yeka_person.save()

                        personHistory = YekaPersonHistory(yeka=yeka_person.yeka, person=person, is_active=False)
                        personHistory.save()

                        log = str(yeka_person.yeka.definition) + ' adlı yekadan -' + str(
                            person.user.get_full_name()) + " personeli çıkarıldı."
                        log = general_methods.logwrite(request, request.user, log)


        return redirect('ekabis:view_yeka_personel', uuid)

    return render(request, 'Yeka/yekaPersonList.html',
                  {'persons': persons, 'yeka_persons': yeka_person, 'yeka_uuid': uuid})




def yeka_company_list(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    yeka_filter = {
        'uuid': uuid
    }

    yeka = YekaGetService(request, yeka_filter)
    yeka_company_filter = {
        'yeka': yeka,
        'isDeleted': False,
        'is_active': True

    }
    url = general_methods.yeka_control(request, yeka)
    if url and url != 'view_yeka_company':
        return redirect('ekabis:' + url, yeka.uuid)

    yeka_company = YekaCompanyService(request, yeka_company_filter).order_by('-creationDate')
    array = []
    for company_yeka in yeka_company:
        array.append(company_yeka.company.uuid)

    companies = Company.objects.filter(isDeleted=False).exclude(uuid__in=array)
    if request.POST:
        with transaction.atomic():
            if request.POST['yeka'] =='add':
                companies = request.POST.getlist('company')
                if companies:
                    for company_id in companies:
                        company = Company.objects.get(pk=company_id)
                        yeka_company = YekaCompany(yeka=yeka, company=company, is_active=True)
                        yeka_company.save()
                        log = str(yeka.definition) + ' adlı yekaya -' + str(company.name) + " adlı firma atandı."
                        log = general_methods.logwrite(request, request.user, log)
            else:
                companies = request.POST.getlist('company')
                if companies:
                    for company_id in companies:
                        company = Company.objects.get(pk=company_id)

                        yeka_company = YekaCompany.objects.get(
                            Q(yeka__uuid=uuid) & Q(company=company) & Q(isDeleted=False))

                        if yeka_company:
                            yeka_company.isDeleted = True
                            yeka_company.is_active = False
                            yeka_company.save()

                        companyHistory = YekaCompanyHistory(yeka=yeka_company.yeka, company=company, is_active=False)
                        companyHistory.save()

                        log = str(yeka_company.yeka.definition) + '-' + str(
                            yeka_company.company.name) + " adlı firma çıkarıldı."
                        log = general_methods.logwrite(request, request.user, log)
        return redirect('ekabis:view_yeka_company', yeka.uuid)

    return render(request, 'Yeka/yeka_company_list.html',
                  {'companies': companies, 'yeka_companies': yeka_company, 'yeka_uuid': uuid})


def yeka_company_assignment(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                company_uuid = request.POST['company_uuid']
                yeka_uuid = request.POST['yeka_uuid']

                yeka_filter = {
                    'uuid': yeka_uuid
                }

                yeka = YekaGetService(request, yeka_filter)
                company_filter = {
                    'uuid': company_uuid
                }
                company = CompanyGetService(request, company_filter)

                yeka_company = YekaCompany(yeka=yeka, company=company, is_active=True)
                yeka_company.save()

                log = str(yeka.definition) + ' adlı yekaya -' + str(company.name) + " adlı firma atandı."
                log = general_methods.logwrite(request, request.user, log)

                return JsonResponse({'status': 'Success', 'msg': 'save successfully'})

            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


def yeka_company_remove(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']
                company = Company.objects.get(uuid=uuid)

                yeka_company = YekaCompany.objects.get(
                    Q(yeka__uuid=request.POST['yeka_uuid']) & Q(company__uuid=uuid) & Q(isDeleted=False))

                if yeka_company:
                    yeka_company.isDeleted = True
                    yeka_company.is_active = False
                    yeka_company.save()

                companyHistory = YekaCompanyHistory(yeka=yeka_company.yeka, company=company, is_active=False)
                companyHistory.save()

                log = str(yeka_company.yeka.definition) + '-' + str(
                    yeka_company.company.name) + " adlı firma çıkarıldı."
                log = general_methods.logwrite(request, request.user, log)

                return JsonResponse({'status': 'Success', 'msg': 'save successfully'})

            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required()
def view_yekabusinessBlog(request, uuid):
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
        return render(request, 'Yeka/timeline.html',
                      {'yekabusinessbloks': yekabusinessbloks,
                       'yeka': yeka,
                       'ekstratimes': ekstratimes
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
        yekaBusinessBlogo_form = YekaBusinessBlogForm(business.pk,yekabussiness, instance=yekabussiness)
        for item in yekabussiness.paremetre.all():

            if item.company:
                title=item.parametre.title +"-" + str(item.company.pk)
                if item.parametre.type == 'file':
                    yekaBusinessBlogo_form.fields[title].initial = item.file
                    yekaBusinessBlogo_form.fields[title].hidden_widget.template_name = "django/forms/widgets/clearable_file_input.html"
                    # yekaBusinessBlogo_form.fields[item.parametre.title].widget.clear_checkbox_label = ""
                    # yekaBusinessBlogo_form.fields[item.parametre.title].widget.initial_text = ""
                    # yekaBusinessBlogo_form.fields[item.parametre.title].widget.input_text = ""

                else:
                    yekaBusinessBlogo_form.fields[title].initial = item.value
            else:
                if item.parametre.type == 'file':
                    yekaBusinessBlogo_form.fields[item.parametre.title].initial = item.file
                    yekaBusinessBlogo_form.fields[
                        item.parametre.title].hidden_widget.template_name = "django/forms/widgets/clearable_file_input.html"
                    # yekaBusinessBlogo_form.fields[item.parametre.title].widget.clear_checkbox_label = ""
                    # yekaBusinessBlogo_form.fields[item.parametre.title].widget.initial_text = ""
                    # yekaBusinessBlogo_form.fields[item.parametre.title].widget.input_text = ""

                else:
                    yekaBusinessBlogo_form.fields[item.parametre.title].initial = item.value




        if request.POST:
            yekaBusinessBlogo_form = YekaBusinessBlogForm(business.pk,yekabussiness, request.POST or None, request.FILES or None,
                                                          instance=yekabussiness)
            if yekaBusinessBlogo_form.is_valid():
                if not   yekaBusinessBlogo_form.cleaned_data['indefinite']:
                    startDate = yekaBusinessBlogo_form.cleaned_data['startDate']
                    finishDate = startDate + datetime.timedelta(days=int(yekaBusinessBlogo_form.cleaned_data['businessTime']))
                    yekabussiness.finisDate = finishDate
                    yekabussiness.save()
                else:
                    yekabussiness.businessTime=0
                    yekabussiness.save()
                yekaBusinessBlogo_form.save(yekabussiness.pk, business.pk)
                return redirect('ekabis:view_yekabusinessBlog', yeka.uuid)
        return render(request, 'Yeka/YekabussinesBlogUpdate.html',
                      {
                          'yekaBusinessBlogo_form': yekaBusinessBlogo_form,
                          'yeka': yeka
                      })
    except Exception as e:

        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


def add_yekabusinessblog_company(request, yeka, yekabusinessblog):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:

        yeka_filter = {
            'uuid': yeka
        }

        yeka = YekaGetService(request, yeka_filter)
        yeka_yekabusiness_filter = {
            'uuid': yekabusinessblog
        }

        yeka = YekaGetService(request, yeka_filter)
        yekabussinessblog = YekaBusinessBlogGetService(request, yeka_yekabusiness_filter)


        yeka = YekaGetService(request,yeka_filter)
        yekabussinessblog = YekaBusinessBlogGetService(request,yeka_yekabusiness_filter)

        company_list=YekaCompany.objects.filter(isDeleted=False,yeka=yeka)


        if request.POST:
            with transaction.atomic():
                companyies = request.POST.getlist('company')
                if companyies:
                    for item in companyies:
                        if not yekabussinessblog.companys.filter(pk=item) and Company.objects.filter(pk=item):
                            yekabussinessblog.companys.add(Company.objects.get(pk=item))
                            yekabussinessblog.save()

                return redirect('ekabis:view_yekabusinessBlog', yeka.uuid)
        return render(request, 'Yeka/add_yekabusinessblog_company.html',
                      {
                          'company_list': company_list,
                          'yeka': yeka
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
        yeka_filter = {
            'uuid': uuid
        }
        yeka = YekaGetService(request, yeka_filter)

        url = general_methods.yeka_control(request, yeka)
        if url and url != 'view_yekabusinessBlog':
            return redirect('ekabis:' + url, yeka.uuid)
        yekabusinessbloks = None

        extratime_filter = {
            'yeka': yeka,
            'isDeleted' : False,
        }
        ekstratimes = ExtraTimeService(request, extratime_filter)
        extratime=[]
        endDate=None
        for item in ekstratimes:
            if ExtraTime.objects.filter(yekabusinessblog=item.yekabusinessblog).count()>1:
                extra=ExtraTime.objects.filter(yekabusinessblog=item.yekabusinessblog).order_by('-creationDate')
                date=None
                ex=None
                for busines in range(len(extra)):

                    if busines==0:
                        if extra[busines]==item:
                            endDate=item.yekabusinessblog.finisDate
                            ex=item.yekabusinessblog.creationDate

                        else:
                            date=extra[busines].yekabusinessblog.finisDate
                    else:
                        if extra[busines]==item:
                            endDate=date+datetime.timedelta(days=item.time)
                            ex = item.yekabusinessblog.creationDate
                        else:
                            date=extra[busines].yekabusinessblog.finisDate+datetime.timedelta(days=item.time)
                beka = {
                    'uuid': item.uuid,
                    'content': item.yekabusinessblog.businessblog.name + " Ek Süre"+ str(ex),
                    'start': endDate,
                    'finish': endDate+datetime.timedelta(days=item.time),
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
                       'ekstratimes': extratime
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

        url=general_methods.yeka_control(request, yeka)
        if url and url !='view_yekabusinessBlog':
            return redirect('ekabis:'+url ,yeka.uuid)
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
        yeka_filter = {
            'uuid': yeka
        }

        yeka = YekaGetService(request, yeka_filter)
        yeka_yekabusiness_filter_ = {
            'uuid': yekabusiness
        }

        yekabussiness = YekaBusinessBlogGetService(request, yeka_yekabusiness_filter_)
        extrafilter={
            'yekabusinessblog':yekabussiness
        }
        extratime=ExtraTimeService(request,extrafilter)

        return render(request, 'Yeka/yekabussinessblog_detail.html',
                      {
                          'yeka': yeka,
                          'yekabusinessblok':yekabussiness,
                          'ekstratimes':extratime,
                      })
    except Exception as e:

        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


