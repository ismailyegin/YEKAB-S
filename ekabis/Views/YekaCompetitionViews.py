import traceback

from dateutil.relativedelta import relativedelta
from django import forms
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db.models import Q
from django.urls import resolve

from ekabis.Forms.CompetitionBusinessBlockForm import CompetitionBusinessBlockForm
from ekabis.Forms.ConnectionRegionForm import ConnectionRegionForm
from ekabis.Forms.PurchaseGuaranteeForm import PurchaseGuaranteeForm
from ekabis.Forms.YekaBusinessBlogForm import YekaBusinessBlogForm
from ekabis.Forms.YekaBusinessForm import YekaBusinessForm
from ekabis.Forms.YekaCompetitionForm import YekaCompetitionForm
from ekabis.Forms.YekaContractForm import YekaContractForm
from ekabis.Forms.YekaForm import YekaForm
from ekabis.Forms.YekaHoldingCompetitionForm import YekaHoldingCompetitionForm
from ekabis.Views.VacationDayViews import is_vacation_day
from ekabis.models.Competition import Competition
from ekabis.models.Proposal import Proposal
from ekabis.models.Settings import Settings
from ekabis.models.YekaBusinessBlog import YekaBusinessBlog
from ekabis.models import YekaCompetition, YekaBusiness, BusinessBlog, Employee, YekaPerson, \
    YekaPersonHistory, Permission, ConnectionRegion, YekaPurchaseGuarantee, ProposalSubYeka, YekaCompetitionEskalasyon, \
    YekaBusinessBlogParemetre, BusinessBlogParametreType, Company, YekaHoldingCompetition, ConnectionUnit, \
    YekaGuarantee, YekaAccept, YekaCompetitionEskalasyon_eskalasyon, Calendar, CalendarYeka, YekaProgressReport
from ekabis.models.YekaCompetitionPerson import YekaCompetitionPerson
from ekabis.models.YekaCompetitionPersonHistory import YekaCompetitionPersonHistory
from ekabis.models.YekaContract import YekaContract
from ekabis.models.YekaProposal import YekaProposal
from ekabis.services import general_methods
from ekabis.services.NotificationServices import notification
from ekabis.services.general_methods import get_error_messages
from ekabis.services.services import YekaGetService, ConnectionRegionGetService, YekaCompetitionGetService, \
    YekaBusinessGetService, YekaBusinessBlogGetService, BusinessBlogGetService, YekaCompetitionPersonService, \
    EmployeeGetService, last_urls, ExtraTimeService, YekaCompetitionService, YekaService, ActiveGroupGetService, \
    YekaPersonService
import datetime
from django.db.models import Sum
from django.core import serializers

from ekabis.models.Yeka import Yeka
from oxiterp.settings.base import MEDIA_URL


@login_required
def view_competition(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    yeka_form = YekaForm()

    try:
        region_filter = {
            'uuid': uuid,
            'isDeleted': False,
        }
        region = ConnectionRegionGetService(request, region_filter)
        competitions = region.yekacompetition.filter(isDeleted=False)
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        with transaction.atomic():
            return render(request, 'YekaCompetition/view_competition.html',
                          {'region': region, 'competitions': competitions, 'yeka_form': yeka_form, 'error_messages': '',
                           'urls': urls, 'current_url': current_url, 'url_name': url_name})

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required
def add_competition(request, region):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        region_filter = {
            'uuid': region,
            'isDeleted': False,
        }
        region = ConnectionRegionGetService(request, region_filter)
        competition_form = YekaCompetitionForm()
        holding_competition = None
        if Yeka.objects.filter(connection_region=region):
            yeka = Yeka.objects.filter(connection_region=region)[0]
            competition_form = YekaCompetitionForm()  # initial={'date': yeka.date} yeka resmi gazete tarihi  miras
        with transaction.atomic():
            if request.method == 'POST':

                competition_form = YekaCompetitionForm(request.POST)

                if competition_form.is_valid():

                    competition = competition_form.save(request, commit=False)

                    total = int(
                        region.yekacompetition.filter(isDeleted=False).exclude(id=competition.id).distinct().aggregate(
                            Sum('capacity'))[
                            'capacity__sum'] or 0)
                    total += competition.capacity

                    if total > region.capacity:
                        messages.warning(request, 'Yeka Yarışmalarının Toplam Kapasitesi Bölgeden Büyük Olamaz')
                        return render(request, 'YekaCompetition/add_competition.html',
                                      {'competition_form': competition_form, 'region': region,
                                       })
                    competition.save()
                    for item in region.cities.all():
                        competition.city.add(item)
                        competition.save()
                    region.yekacompetition.add(competition)
                    region.save()
                    yeka_filter = {
                        'isDeleted': False,
                        'connection_region': region

                    }
                    yeka = YekaGetService(request, yeka_filter)

                    if yeka.business:
                        yeka_business = YekaBusiness(name=region.name)
                        yeka_business.save()
                        if yeka.business.businessblogs.all():
                            parent_yeka_business_blog = YekaBusinessBlog.objects.none()
                            for item in yeka.business.businessblogs.filter(isDeleted=False).order_by('sorting'):

                                if item.sorting == 1:
                                    yeka_businessblog = YekaBusinessBlog(
                                        finisDate=item.finisDate,
                                        startDate=item.startDate,
                                        completion_date=item.completion_date,
                                        sorting=item.sorting,
                                        businessTime=item.businessTime,
                                        status=item.status,
                                        time_type=item.time_type,
                                        indefinite=item.indefinite,
                                        businessblog=item.businessblog

                                    )
                                    parent_yeka_business_blog = yeka_businessblog
                                    yeka_businessblog.save()
                                    for param in item.parameter.all():
                                        new_param = YekaBusinessBlogParemetre(value=param.value, file=param.file,
                                                                              title=param.title,
                                                                              parametre=param.parametre)
                                        new_param.save()
                                        yeka_businessblog.parameter.add(new_param)
                                        yeka_businessblog.save()

                                else:
                                    yeka_businessblog = YekaBusinessBlog(

                                        parent=parent_yeka_business_blog,
                                        finisDate=item.finisDate,
                                        startDate=item.startDate,
                                        completion_date=item.completion_date,
                                        sorting=item.sorting,
                                        businessTime=item.businessTime,
                                        status=item.status,
                                        time_type=item.time_type,
                                        indefinite=item.indefinite,
                                        businessblog=item.businessblog
                                    )
                                    yeka_businessblog.save()
                                    for param in item.parameter.all():
                                        new_param = YekaBusinessBlogParemetre(value=param.value, file=param.file,
                                                                              title=param.title,
                                                                              parametre=param.parametre)
                                        new_param.save()
                                        yeka_businessblog.parameter.add(new_param)
                                        yeka_businessblog.save()

                                    parent_yeka_business_blog = yeka_businessblog
                                yeka_business.businessblogs.add(yeka_businessblog)
                                yeka_business.save()
                            competition.business = yeka_business
                            competition.save()
                            if competition.business.businessblogs.filter(businessblog__name='Yarışmanın Yapılması'):

                                if YekaHoldingCompetition.objects.filter(business=yeka.business):
                                    holding_competition = YekaHoldingCompetition(
                                        yekabusinessblog=competition.business.businessblogs.get(
                                            businessblog__name='Yarışmanın Yapılması'),
                                        business=competition.business,
                                        max_price=YekaHoldingCompetition.objects.get(business=yeka.business).max_price,
                                        unit=YekaHoldingCompetition.objects.get(business=yeka.business).unit

                                    )
                                    holding_competition.save()
                                if YekaContract.objects.filter(business=competition.business):
                                    contract = YekaContract.objects.get(business=competition.business)
                                else:
                                    contract = YekaContract(
                                        yekabusinessblog=competition.business.businessblogs.get(
                                            businessblog__name='YEKA Kullanım Hakkı Sözleşmesinin İmzalanması'),
                                        business=competition.business
                                    )
                                    contract.save()
                                if holding_competition.unit.name == 'TL Kuruş/kWh':
                                    contract.unit = ConnectionUnit.objects.get(name='TL Kuruş/kWh')
                                    contract.save()
                                elif holding_competition.unit.name == 'USD Cent/kWh':
                                    contract.unit = ConnectionUnit.objects.get(name='USD Cent/kWh')
                                    contract.save()

                            # Bagımlılıkları yeka yarışmasına taşıdık
                            for fcom in competition.business.businessblogs.filter(isDeleted=False).order_by('sorting'):
                                if yeka.business.businessblogs.filter(businessblog=fcom.businessblog, isDeleted=False):
                                    yeka_dependence_parent = \
                                        yeka.business.businessblogs.filter(businessblog=fcom.businessblog,
                                                                           isDeleted=False)[
                                            0].dependence_parent
                                    if yeka_dependence_parent:
                                        if competition.business.businessblogs.filter(
                                                businessblog=yeka_dependence_parent.businessblog, isDeleted=False):
                                            fcom.dependence_parent = competition.business.businessblogs.filter(
                                                businessblog=yeka_dependence_parent.businessblog, isDeleted=False)[0]
                                            fcom.save()

                                            x = fcom.dependence_parent
                                            x.child_block = fcom  # bir sonraki iş bloğu oluşturuldu
                                            x.save()

                    log = " Yeka Yarışması  eklendi"
                    log = general_methods.logwrite(request, request.user, log)
                    url = redirect('ekabis:view_yeka_competition_detail', yeka.uuid).url
                    html = '<a style="" href="' + url + '"> ID: ' + str(
                        competition.pk) + ' - ' + competition.name + '</a> YEKA yarışması eklendi.'
                    notification(request, html, competition.uuid, 'yeka_competition')
                    messages.success(request, 'Yeka Yarışması Kayıt Edilmiştir.')
                    return redirect('ekabis:view_yeka_competition_detail', competition.uuid)

                else:
                    error_message_region = get_error_messages(competition_form)

                    return render(request, 'YekaCompetition/add_competition.html',
                                  {'competition_form': competition_form, 'region': region,
                                   'error_messages': error_message_region, 'urls': urls, 'current_url': current_url,
                                   'url_name': url_name})

            return render(request, 'YekaCompetition/add_competition.html',
                          {'competition_form': competition_form, 'error_messages': '',
                           'region': region, 'urls': urls, 'current_url': current_url, 'url_name': url_name})

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, e)
        return redirect('ekabis:view_yeka')


@login_required
def delete_competition(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:

        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']
                competition_filter = {
                    'uuid': uuid
                }
                obj = YekaCompetition.objects.get(uuid=uuid)
                parent_filter = {
                    'parent': obj
                }

                if YekaCompetition.objects.filter(parent=obj):

                    return JsonResponse({'status': 'Fail', 'msg': ' Bağlı alt YEKA olduğu için silinemez.'})

                else:
                    log = str(obj.name) + "Yeka yarışması silindi."
                    log = general_methods.logwrite(request, request.user, log)
                    obj.isDeleted = True
                    obj.save()
                    if ProposalSubYeka.objects.filter(sub_yeka=obj):
                        sub_yeka = ProposalSubYeka.objects.get(sub_yeka=obj)
                        sub_yeka.delete()
                    url = redirect('ekabis:view_yeka').url
                    html = '<a style="" href="' + url + '"> ID: ' + str(
                        obj.pk) + ' - ' + obj.name + '</a> YEKA yarışması silindi.'
                    notification(request, html, obj.uuid, 'yeka_competition')
                    return JsonResponse({'status': 'Success', 'messages': 'save successfully'})




            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except obj.DoesNotExist:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def update_competition(request, region, competition):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        user = request.user
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        region_filter = {
            'uuid': region,
            'isDeleted': False,
        }
        region = ConnectionRegionGetService(request, region_filter)
        competition_filter = {
            'uuid': competition,
            'isDeleted': False,
        }
        competition = YekaCompetitionGetService(request, competition_filter)
        filter = {
            'user': user
        }
        make_change = False

        employee = Employee.objects.filter(person__user=user)
        if employee:
            employee = Employee.objects.filter(person__user=user)
            yeka_persons = YekaPerson.objects.filter(employee__in=employee).filter(
                yeka__connection_region__yekacompetition=competition)
        else:
            yeka_persons = None

        active = ActiveGroupGetService(request, filter)

        name = general_methods.yekaname(competition.business)

        if active.group.name == 'Admin':
            make_change = True
        elif yeka_persons:
            make_change = True
        if make_change:
            competition_form = YekaCompetitionForm(request.POST or None, instance=competition)
            with transaction.atomic():
                if request.method == 'POST':
                    if competition_form.is_valid():
                        competition = competition_form.save(request, commit=False)

                        total = int(
                            region.yekacompetition.all().exclude(id=competition.id).distinct().aggregate(
                                Sum('capacity'))['capacity__sum'] or 0)
                        total += competition.capacity

                        if total > region.capacity:
                            messages.warning(request, 'Yeka Yarışmalarının toplam Kapasitesi Bölgeden Büyük Olamaz')
                            return render(request, 'YekaCompetition/change_competition.html',
                                          {'competition_form': competition_form, 'region': region, 'urls': urls,
                                           'current_url': current_url, 'url_name': url_name,
                                           'competition': competition,
                                           })
                        competition.save()
                        url = redirect('ekabis:view_yeka_competition_detail', competition.uuid).url
                        html = '<a style="" href="' + url + '"> ID : ' + str(
                            competition.pk) + ' - ' + competition.name + ' </a>  YEKA yarışması güncellendi.'
                        notification(request, html, competition.uuid, 'yeka_competition')
                        for item in region.cities.all():
                            competition.city.add(item)
                            competition.save()
                        region.yekacompetition.add(competition)
                        region.save()

                        messages.success(request, 'Yeka Yarışması Kayıt Edilmiştir.')
                        if competition.parent:
                            return redirect('ekabis:view_yeka_competition_detail', competition.parent.uuid)
                        else:
                            return redirect('ekabis:view_yeka_competition_detail', competition.uuid)

                    else:
                        error_message_region = get_error_messages(competition_form)

                        return render(request, 'YekaCompetition/change_competition.html',
                                      {'competition_form': competition_form, 'region': region,
                                       'error_messages': error_message_region, 'urls': urls,
                                       'current_url': current_url, 'name': name,
                                       'url_name': url_name, 'competition': competition, })
                url = redirect('ekabis:view_yeka_competition_detail', competition.uuid).url
                html = '<a style="" href="' + url + '"> ID: ' + str(
                    competition.pk) + ' - ' + competition.name + '</a> YEKA yarışması güncellendi.'
                notification(request, html, competition.uuid, 'yeka_competition')
                return render(request, 'YekaCompetition/change_competition.html',
                              {'competition_form': competition_form, 'error_messages': '', 'urls': urls,
                               'current_url': current_url, 'url_name': url_name, 'competition': competition,
                               'region': region, 'name': name})
        else:
            messages.warning(request, 'İşlem yapma yetkiniz yoktur.')
            return HttpResponseRedirect(urls[0]['last'])

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, e)
        return redirect('ekabis:view_yeka')


@login_required()
def view_competition_yekabusinessBlog(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        competition_filter = {
            'uuid': uuid
        }
        competition = YekaCompetitionGetService(request, competition_filter)

        url = general_methods.competition_control(request, competition)
        if url and url != 'view_competitionbusinessblog':
            return redirect('ekabis:' + url, competition.uuid)
        yekabusinessbloks = None

        extratime_filter = {
            'business': competition.business
        }
        ekstratimes = ExtraTimeService(request, extratime_filter)

        if competition.business:
            yekabusiness = competition.business
            yekabusinessbloks = yekabusiness.businessblogs.filter(isDeleted=False).order_by('sorting')
        else:
            yekabusiness = None
            yekabusinessbloks = None

        return render(request, 'YekaCompetition/timeline.html',
                      {'yekabusinessbloks': yekabusinessbloks,
                       'competition': competition,
                       'ekstratimes': None, 'urls': urls, 'current_url': current_url, 'url_name': url_name
                       })

    except Exception as e:

        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required
def add_yekacompetitionbusiness(request, uuid):
    business = BusinessBlog.objects.filter(isDeleted=False)
    competition = YekaCompetition.objects.get(uuid=uuid)

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        if request.method == 'POST':
            with transaction.atomic():
                yekabusiness = YekaBusiness()
                yekabusiness.save()
                competition.business = yekabusiness
                competition.save()
                if request.POST.get('businessblog'):
                    blogs = request.POST.get('businessblog').split("-")
                    parent = YekaBusinessBlog.objects.none()
                    blog = None
                    for i in range(len(blogs)):
                        if i == 0:
                            blog = YekaBusinessBlog(businessblog=BusinessBlog.objects.get(pk=blogs[i]),
                                                    sorting=i + 1)
                            blog.save()
                            parent = blog

                        else:
                            blog = YekaBusinessBlog(businessblog=BusinessBlog.objects.get(pk=blogs[i]),

                                                    parent=parent,
                                                    dependence_parent=parent,

                                                    sorting=i + 1
                                                    )
                            blog.save()
                            parent.child_block = blog
                            parent.save()
                            parent = blog
                        yekabusiness.businessblogs.add(blog)
                        yekabusiness.save()
                        log = str(competition.name) + ' adlı yarışmaya - ' + str(
                            blog.businessblog.name) + " adlı iş bloğu atandı."
                        log = general_methods.logwrite(request, request.user, log)
                        url = redirect('ekabis:view_yeka_competition_detail', competition.uuid).url
                        html = '<a style="" href="' + url + '"> ID : ' + str(competition.pk) + ' - ' + str(
                            competition.name) + '</a> adlı yarışmaya - ' + str(
                            blog.businessblog.name) + " adlı iş bloğu atandı."
                        notification(request, html, competition.uuid, 'yeka_competition')

                    return redirect('ekabis:view_yeka_competition_detail', competition.uuid)

        return render(request, 'YekaCompetition/competition_businessblog_Add.html', {'business': business,

                                                                                     'error_messages': '', 'urls': urls,
                                                                                     'current_url': current_url,
                                                                                     'url_name': url_name
                                                                                     })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required
def change_yekacompetitionbusiness(request, uuid, competition):
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        business_filter = {
            'uuid': uuid
        }
        yekabusiness = YekaBusinessGetService(request, business_filter)
        business_form = YekaBusinessForm(request.POST or None, instance=yekabusiness)

        business = yekabusiness.businessblogs.filter(isDeleted=False).order_by('sorting')
        tk = []
        for item in business:
            tk.append(item.businessblog.pk)
        unbusiness = BusinessBlog.objects.exclude(id__in=tk).filter(isDeleted=False)
        if request.method == 'POST':
            with transaction.atomic():
                if request.POST.get('businessblog'):
                    blogs = request.POST.get('businessblog').split("-")
                    parent = None
                    blog = None
                    # olmayanları sil
                    if business:
                        removeBusiness = business.exclude(businessblog__id__in=blogs)
                        for i in removeBusiness:
                            i.isDeleted = True
                            i.save()

                    # olmayanı ekle sıralması degileni kaydet
                    for i in range(len(blogs)):

                        # is blogu varsa
                        if yekabusiness.businessblogs.filter(businessblog_id=blogs[i]):
                            if i == 0:
                                blog = yekabusiness.businessblogs.filter(businessblog_id=blogs[i])[0]
                                if blog.isDeleted:
                                    blog.isDeleted = False
                                blog.parent = None
                                blog.dependence_parent = None
                                blog.sorting = i + 1
                                blog.save()
                                parent = blog

                            else:

                                blog = yekabusiness.businessblogs.filter(businessblog_id=blogs[i])[0]
                                if blog.isDeleted:
                                    blog.isDeleted = False
                                blog.parent = parent
                                blog.dependence_parent = parent
                                blog.sorting = i + 1
                                blog.save()
                                parent.child_block = blog
                                parent.save()
                                parent = blog
                        # is blogu yoksa
                        else:
                            if i == 0:
                                blog = YekaBusinessBlog(businessblog=BusinessBlog.objects.get(pk=blogs[i]),
                                                        sorting=i + 1)
                                blog.save()
                                parent = blog


                            else:
                                blog = YekaBusinessBlog(businessblog=BusinessBlog.objects.get(pk=blogs[i]),
                                                        parent=parent, dependence_parent=parent,
                                                        sorting=i + 1
                                                        )
                                blog.save()
                                parent.child_block = blog
                                parent.save()
                                parent = blog
                            yekabusiness.businessblogs.add(blog)
                            yekabusiness.save()
                    yeka_competition = YekaCompetition.objects.get(uuid=competition)
                    url = redirect('ekabis:view_yeka_competition_detail', competition).url
                    html = '<a style="" href="' + url + '"> ID : ' + str(
                        yeka_competition.pk) + ' - ' + str(
                        yeka_competition.name) + '</a> adlı yarışmanın iş planı guncellendi.'
                    notification(request, html, competition, 'yeka_competition')

                else:
                    removeBusiness = yekabusiness.businessblogs.all()
                    for i in removeBusiness:
                        i.isDeleted = True
                        i.save()

                return redirect('ekabis:view_yeka_competition_detail', competition)
        return render(request, 'YekaCompetition/competition_businessblog_change.html', {'business_form': business_form,
                                                                                        'error_messages': '',
                                                                                        'unbusiness': unbusiness,
                                                                                        'business': business,
                                                                                        'urls': urls,
                                                                                        'current_url': current_url,
                                                                                        'url_name': url_name
                                                                                        })

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required()
def change_yekacompetitionbusinessBlog(request, competition, yekabusiness, business):  # yarisma iş bloğu düzenleme
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        competition_filter = {
            'uuid': competition
        }

        competition = YekaCompetitionGetService(request, competition_filter)

        yeka_yekabusiness_filter_ = {
            'uuid': yekabusiness
        }

        yekabussiness = YekaBusinessBlogGetService(request, yeka_yekabusiness_filter_)
        yeka_business_filter_ = {
            'uuid': business
        }
        form_contract = None
        purchase_guarantee_form = None
        holding_competition_form = None
        annual_spend_form = None
        employment_form = None
        budget_form = None

        business = BusinessBlogGetService(request, yeka_business_filter_)
        yekaBusinessBlogo_form = CompetitionBusinessBlockForm(business.pk, yekabussiness, request.POST or None,
                                                              request.FILES or None,
                                                              instance=yekabussiness)

        # if yekaBusinessBlogo_form['dependence_parent'].initial !=None:
        #     yekaBusinessBlogo_form.fields['startDate'].widget.attrs['readonly'] = True
        contract = None
        companies = None
        holding_competition = None
        if business.name == 'YEKA Kullanım Hakkı Sözleşmesinin İmzalanması':

            if Competition.objects.filter(yekabusinessblog__businessblog__name='Yarışmanın Yapılması'):
                companies = Competition.objects.get(
                    yekabusinessblog__businessblog__name='Yarışmanın Yapılması').company.all()

            if YekaContract.objects.filter(business=competition.business):
                contract = YekaContract.objects.get(business=competition.business)
            else:
                contract = YekaContract(
                    yekabusinessblog=yekabussiness,
                    business=competition.business
                )
                contract.save()
            form_contract = YekaContractForm(request.POST or None, request.FILES or None, instance=contract)
            form_contract.fields['unit'].initial = contract.unit
            form_contract.fields['unit'].widget.attrs = {'class': 'form-control', 'disabled': 'true'}
            if contract.unit:
                if contract.unit.name == 'USD Cent/kWh':
                    form_contract.fields['eskalasyonMaxPrice'].widget.attrs = {'class': 'form-control',
                                                                               'readonly': 'readonly',
                                                                               'placeholder': 'BİRİM USD Cent/kWh SEÇİLMİŞTİR'}
                else:
                    form_contract.fields['eskalasyonMaxPrice'].initial = contract.eskalasyonMaxPrice
            else:
                form_contract.fields['eskalasyonMaxPrice'].initial = contract.eskalasyonMaxPrice
        elif business.name == 'Alım Garantisi':
            purchase_guarantee = None

            if YekaPurchaseGuarantee.objects.filter(business=competition.business):
                purchase_guarantee = YekaPurchaseGuarantee.objects.get(business=competition.business)
            else:
                purchase_guarantee = YekaPurchaseGuarantee(
                    yekabusinessblog=yekabussiness,
                    business=competition.business
                )
                purchase_guarantee.save()
            purchase_guarantee_form = PurchaseGuaranteeForm(request.POST or None, request.FILES or None,
                                                            instance=purchase_guarantee)
        elif business.name == 'Yarışmanın Yapılması':

            if YekaHoldingCompetition.objects.filter(business=competition.business):
                holding_competition = YekaHoldingCompetition.objects.get(business=competition.business)
            else:
                holding_competition = YekaHoldingCompetition(
                    yekabusinessblog=yekabussiness,
                    business=competition.business
                )
                holding_competition.save()
            holding_competition_form = YekaHoldingCompetitionForm(request.POST or None, request.FILES or None,
                                                                  instance=holding_competition)
        name = general_methods.yekaname(competition.business)

        yekaBusinessBlogo_form.fields['dependence_parent'].queryset = competition.business.businessblogs.exclude(
            uuid=yekabussiness.uuid).filter(isDeleted=False)

        yekaBusinessBlogo_form.fields['child_block'].queryset = competition.business.businessblogs.exclude(
            uuid=yekabussiness.uuid).filter(isDeleted=False)

        if request.POST:
            # form_contract = YekaContractForm(request.POST or None, request.FILES or None, instance=contract)

            yekaBusinessBlogo_form = CompetitionBusinessBlockForm(business.pk, yekabussiness, request.POST or None,
                                                                  request.FILES or None,
                                                                  instance=yekabussiness)
            if form_contract:
                if form_contract.is_valid():
                    contract_form = form_contract.save(request, commit=False)
                    contract.eskalasyonMaxPrice = form_contract.cleaned_data['eskalasyonMaxPrice']
                    contract.price = form_contract.cleaned_data['price']
                    contract.company = form_contract.cleaned_data['company']
                    if YekaHoldingCompetition.objects.filter(business=competition.business):
                        comp = YekaHoldingCompetition.objects.get(business=competition.business)
                        if comp.unit:
                            contract.unit = YekaHoldingCompetition.objects.get(business=competition.business).unit
                            if contract.unit.name == 'USD Cent/kWh':
                                contract.eskalasyonMaxPrice = None
                    contract.contract = form_contract.cleaned_data['contract']

                    contract.save()
                    competition.business.company = contract_form.company
                    competition.business.save()
                    competition.save()
                    if yekabussiness.completion_date:
                        contract.contract_date = yekabussiness.completion_date
                    elif yekabussiness.startDate:
                        contract.contract_date = yekabussiness.startDate
                    else:
                        contract.contract_date = None
                    contract.save()
                    # if request.POST['company']:
                    #     company=request.POST['company']
                    #     contract.company=Company.objects.get(uuid=company)
                    #     contract.save()

            if purchase_guarantee_form:
                if purchase_guarantee_form.is_valid():
                    if purchase_guarantee_form.cleaned_data['type'] == 'Süre':
                        purchase_guarantee_form.cleaned_data['total_quantity'] = competition.capacity
                    elif purchase_guarantee_form.cleaned_data['type'] == 'Miktar':
                        purchase_guarantee_form.cleaned_data['time'] = None
                    purchase_guarantee = purchase_guarantee_form.save(request, commit=False)
                    purchase_guarantee.save()
                    if purchase_guarantee_form.cleaned_data['time']:
                        time = purchase_guarantee_form.cleaned_data['time'] * 365. / 12
                        purchase_guarantee.time = int(time)
                        purchase_guarantee.type = purchase_guarantee_form.cleaned_data['type']
                        purchase_guarantee.save()
            if holding_competition_form:
                if holding_competition_form.is_valid():
                    holding_comp = holding_competition_form.save(request, commit=False)
                    holding_comp.save()
                    contract = YekaContract.objects.get(business=competition.business)
                    if holding_competition_form.cleaned_data['unit'].name == 'TL Kuruş/kWh':
                        contract.unit = ConnectionUnit.objects.get(name='TL Kuruş/kWh')
                        contract.save()
                    elif holding_competition_form.cleaned_data['unit'].name == 'USD Cent/kWh':
                        contract.unit = ConnectionUnit.objects.get(name='USD Cent/kWh')
                        contract.save()
            if yekaBusinessBlogo_form.is_valid():

                if yekaBusinessBlogo_form['child_block'].data == yekaBusinessBlogo_form['dependence_parent'].data:
                    messages.warning(request, 'Bir önceki iş bloğu ile bir sonraki iş bloğu aynı olamaz.')
                    return render(request, 'Yeka/YekabussinesBlogUpdate.html',
                                  {
                                      'yekaBusinessBlogo_form': yekaBusinessBlogo_form,
                                      'competition': competition, 'urls': urls,
                                      'current_url': current_url, 'contract_form': form_contract,
                                      'purchase_guarantee_form': purchase_guarantee_form,
                                      'url_name': url_name, 'companies': companies,
                                      'name': name, 'employment_form': employment_form, 'budget_form': budget_form,
                                      'annual_spend_form': annual_spend_form
                                  })
                # dosya boyutu
                for item in yekabussiness.parameter.filter(isDeleted=False):
                    if item.parametre.type == 'file':
                        if item.file:
                            if yekaBusinessBlogo_form.files:
                                file_size = 0
                                if Settings.objects.filter(key='file_size'):
                                    file_size = float(Settings.objects.get(key='file_size').value)
                                if file_size >= yekaBusinessBlogo_form.files[
                                    item.parametre.title].size:
                                    if item.file:
                                        yekaBusinessBlogo_form.fields[
                                            item.parametre.title].initial = item.file
                                        yekaBusinessBlogo_form.fields[item.parametre.title].widget.attrs = {
                                            'class': 'form-control'}
                                    else:
                                        yekaBusinessBlogo_form.fields[
                                            item.parametre.title].initial = item.file
                                else:
                                    messages.warning(request,
                                                     ' ' + item.parametre.title + ' Dosya Boyutu Büyük.(Maksimum yüklenmesi gereken dosya boyutu: ' + str(
                                                         file_size) + ' MB')
                                    return render(request, 'Yeka/YekabussinesBlogUpdate.html',
                                                  {
                                                      'yekaBusinessBlogo_form': yekaBusinessBlogo_form,
                                                      'competition': competition, 'urls': urls,
                                                      'current_url': current_url, 'contract_form': form_contract,
                                                      'purchase_guarantee_form': purchase_guarantee_form,
                                                      'url_name': url_name, 'companies': companies,
                                                      'name': name, 'employment_form': employment_form,
                                                      'budget_form': budget_form,
                                                      'annual_spend_form': annual_spend_form,
                                                      'holding_competition_form': holding_competition_form
                                                  })

                yekaBusinessBlogo_form.save(yekabussiness.pk, business.pk)

                childblock = yekabussiness.child_block
                if childblock:
                    childblock.parent = yekabussiness
                    childblock.dependence_parent = yekabussiness
                    childblock.save()
                if not yekabussiness.indefinite and yekabussiness.startDate:
                    dependence_blocks = YekaBusinessBlog.objects.filter(dependence_parent=yekabussiness)
                    for dependence_block in dependence_blocks:
                        add_time_next(yekabussiness.pk, dependence_block.pk, competition)
                if yekaBusinessBlogo_form.cleaned_data['status']=='1':
                    region = ConnectionRegion.objects.get(yekacompetition=competition)
                    yeka_name = Yeka.objects.get(connection_region=region).definition
                    if CalendarYeka.objects.filter(calendarName__name=yeka_name+'-'+competition.name+'-'+business.name):
                        calendar_yeka = CalendarYeka.objects.get(calendarName__name=yeka_name+'-'+competition.name+'-'+business.name)
                        calendar_yeka.delete()

                messages.success(request, 'Başarıyla Kayıt Edilmiştir.')
                url = redirect('ekabis:view_yeka_competition_detail', competition.uuid).url
                html = '<a style="" href="' + url + '"> ID : ' + str(business.pk) + ' - ' + str(
                    business.name) + '</a> adlı iş bloğu güncellendi.'
                notification(request, html, competition.uuid, 'yeka_competition')
                if competition.parent:
                    return redirect('ekabis:view_sub_yeka_competition_detail', competition.uuid)
                else:
                    return redirect('ekabis:view_yeka_competition_detail', competition.uuid)
        else:

            for item in yekabussiness.parameter.filter(isDeleted=False):
                if item.parametre.type == 'file':
                    if item.file:
                        yekaBusinessBlogo_form.fields[item.parametre.title].initial = item.file
                        yekaBusinessBlogo_form.fields[item.parametre.title].widget.attrs = {'class': 'form-control'}
                    else:
                        yekaBusinessBlogo_form.fields[item.parametre.title].initial = item.file
                else:
                    yekaBusinessBlogo_form.fields[item.parametre.title].initial = item.value

        return render(request, 'Yeka/YekabussinesBlogUpdate.html',
                      {
                          'yekaBusinessBlogo_form': yekaBusinessBlogo_form,
                          'competition': competition, 'urls': urls,
                          'current_url': current_url, 'contract_form': form_contract,
                          'purchase_guarantee_form': purchase_guarantee_form,
                          'url_name': url_name, 'companies': companies, 'contract': contract,
                          'name': name, 'holding_competition_form': holding_competition_form,
                          'employment_form': employment_form, 'budget_form': budget_form,
                          'annual_spend_form': annual_spend_form
                      })
    except Exception as e:

        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
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
        return redirect('ekabis:view_yeka_competition_detail', yeka.uuid)
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


def yeka_person_list(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    yekacompetition_filter = {
        'uuid': uuid,
    }
    competition = YekaCompetitionGetService(request, yekacompetition_filter)
    yekacompetition_person_filter = {
        'competition': competition,
        'isDeleted': False,
        'is_active': True
    }
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    yeka_person = YekaCompetitionPersonService(request, yekacompetition_person_filter).order_by('-creationDate')
    name = general_methods.yekaname(competition.business)
    array = []
    for person in yeka_person:
        array.append(person.employee.uuid)

    # ekstra servis yazılacak
    persons = Employee.objects.filter(isDeleted=False).exclude(uuid__in=array).order_by('-creationDate')
    if request.POST:
        with transaction.atomic():
            if request.POST.get('yeka') == 'add':
                persons = request.POST.getlist('employee')
                if persons:
                    for person_id in persons:
                        person_filter = {
                            'pk': person_id
                        }
                        person = EmployeeGetService(request, person_filter)
                        person_yeka = YekaCompetitionPerson(competition=competition, employee=person, is_active=True)
                        person_yeka.save()

                        personHistory = YekaCompetitionPersonHistory(competition=competition, person=person,
                                                                     is_active=True)
                        personHistory.save()

                        log = str(competition.name) + ' adlı yekaya - ' + str(
                            person.person.user.get_full_name()) + " adlı personel atandı."
                        log = general_methods.logwrite(request, request.user, log)
                        url = redirect('ekabis:view_yeka_competition_detail', competition.uuid).url
                        html = '<a style="" href="' + url + '"> ' + str(
                            competition.pk) + ' - ' + str(
                            competition.name) + '</a> adlı yarışmaya - ' + str(
                            person.person.user.get_full_name()) + " adlı personel atandı."
                        notification(request, html, competition.uuid, 'yeka_competition')
            else:
                persons = request.POST.getlist('sub_employee')
                if persons:
                    for person_id in persons:
                        person_filter = {
                            'pk': person_id
                        }
                        person = EmployeeGetService(request, person_filter)
                        yeka_person = YekaCompetitionPerson.objects.get(
                            Q(isDeleted=False) & Q(competition__uuid=uuid) & Q(employee__uuid=person.uuid))

                        yeka_person.isDeleted = True
                        yeka_person.is_active = False
                        yeka_person.save()

                        personHistory = YekaCompetitionPersonHistory(competition=yeka_person.competition, person=person,
                                                                     is_active=False)
                        personHistory.save()

                        log = str(yeka_person.competition.name) + ' adlı yekadan -' + str(
                            person.person.user.get_full_name()) + " personeli çıkarıldı."
                        log = general_methods.logwrite(request, request.user, log)
                        url = redirect('ekabis:view_yeka_competition_detail', competition.uuid).url
                        html = '<a style="" href="' + url + '"> ' + str(
                            competition.pk) + ' - ' + str(
                            competition.name) + '</a> adlı yarışmaya - ' + str(
                            person.person.user.get_full_name()) + " adlı personel çıkarıldı."
                        notification(request, html, competition.uuid, 'yeka_competition')

        if competition.parent:
            return redirect('ekabis:view_yeka_competition_detail', competition.parent.uuid)
        else:
            return redirect('ekabis:view_yeka_competition_detail', competition.uuid)

    return render(request, 'Yeka/yekaPersonList.html',
                  {'persons': persons, 'yeka_persons': yeka_person, 'yeka_uuid': uuid, 'urls': urls,
                   'current_url': current_url, 'url_name': url_name, 'competition': competition, 'name': name})


@login_required
def return_sub_competition(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)

        competition_filter = {
            'uuid': uuid,
            'isDeleted': False,
        }
        parent_competition = YekaCompetitionGetService(request, competition_filter)
        competitions = YekaCompetition.objects.filter(parent=parent_competition, isDeleted=False)
        region = ConnectionRegion.objects.get(yekacompetition=parent_competition)
        return render(request, 'YekaCompetition/view_sub_competition.html',
                      {'parent_competition': parent_competition, 'competitions': competitions, 'region': region,
                       'urls': urls, 'current_url': current_url, 'url_name': url_name})
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required
def add_sumcompetition(request, uuid, proposal_uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    competition_form = YekaCompetitionForm()

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)

        competition_filter = {
            'uuid': uuid,
            'isDeleted': False,
        }
        parent_competition = YekaCompetitionGetService(request, competition_filter)
        proposal = None
        holding_competition = None
        if Proposal.objects.filter(uuid=proposal_uuid):
            proposal = Proposal.objects.get(uuid=proposal_uuid)

        competition_form.fields['capacity'].initial = proposal.capacity
        competition_form.fields['name'].initial = proposal.name
        name = general_methods.yekaname(parent_competition.business)

        with transaction.atomic():

            if request.method == 'POST':

                competition_form = YekaCompetitionForm(request.POST)

                if competition_form.is_valid():

                    competition = competition_form.save(request, commit=False)
                    if ProposalSubYeka.objects.filter(proposal=proposal):
                        name = general_methods.yekaname(parent_competition.business)
                        yeka_proposal = YekaProposal.objects.get(proposal=proposal)
                        messages.warning(request, 'Aday YEKA ya ait nihai yeka kayıt edilmiştir.')
                        return redirect('ekabis:proposal_add_sub_yeka', yeka_proposal.business.uuid,
                                        yeka_proposal.yekabusinessblog.uuid)

                    # # baglı oldugu yarışmanın kapsitesinden fazla olamaz
                    # total = int(
                    #     YekaCompetition.objects.filter(parent=parent_competition, isDeleted=False).distinct().aggregate(
                    #         Sum('capacity'))[
                    #         'capacity__sum'] or 0)
                    # total += proposal.capacity

                    # if total > parent_competition.capacity:
                    #     name = general_methods.yekaname(parent_competition.business)
                    #     messages.warning(request, 'Nihai YEKA yarışmalarının kapasite toplamı yarışmadan Büyük Olamaz')
                    #     return render(request, 'YekaCompetition/add_sub_competition.html',
                    #                   {'competition_form': competition_form, 'parent_competition': parent_competition,
                    #                    'error_messages': '', 'urls': urls, 'current_url': current_url,
                    #                    'url_name': url_name,'name':name
                    #                    })

                    competition.parent = parent_competition
                    competition.save()
                    competition.capacity = proposal.capacity
                    competition.save()

                    proposal_sub_yeka = ProposalSubYeka(proposal=proposal, sub_yeka=competition)
                    proposal_sub_yeka.save()
                    proposal.status = True
                    proposal.save()

                    if parent_competition.business:
                        yeka_business = YekaBusiness(name=parent_competition.business.name)
                        yeka_business.save()
                        if parent_competition.business.businessblogs.filter(isDeleted=False):
                            parent_yeka_business_blog = YekaBusinessBlog.objects.none()
                            for item in parent_competition.business.businessblogs.filter(isDeleted=False).order_by(
                                    'sorting'):

                                if item.sorting == 1:
                                    yeka_businessblog = YekaBusinessBlog(
                                        finisDate=item.finisDate,
                                        startDate=item.startDate,
                                        completion_date=item.completion_date,
                                        sorting=item.sorting,
                                        businessTime=item.businessTime,
                                        status=item.status,
                                        businessblog=item.businessblog

                                    )
                                    yeka_businessblog.save()
                                    for param in item.parameter.all():
                                        new_param = YekaBusinessBlogParemetre(value=param.value, file=param.file,
                                                                              title=param.title,
                                                                              parametre=param.parametre)
                                        new_param.save()
                                        yeka_businessblog.parameter.add(new_param)
                                        yeka_businessblog.save()

                                    parent_yeka_business_blog = yeka_businessblog

                                else:
                                    yeka_businessblog = YekaBusinessBlog(parent=parent_yeka_business_blog,
                                                                         finisDate=item.finisDate,
                                                                         businessblog=item.businessblog,
                                                                         startDate=item.startDate,
                                                                         completion_date=item.completion_date,
                                                                         sorting=item.sorting,
                                                                         businessTime=item.businessTime,
                                                                         status=item.status,
                                                                         )
                                    yeka_businessblog.save()
                                    for param in item.parameter.filter(isDeleted=False):
                                        new_param = YekaBusinessBlogParemetre(value=param.value, file=param.file,
                                                                              title=param.title,
                                                                              parametre=param.parametre)
                                        new_param.save()
                                        yeka_businessblog.parameter.add(new_param)
                                        yeka_businessblog.save()
                                    parent_yeka_business_blog = yeka_businessblog

                                if item.companies.filter(isDeleted=False):
                                    for company in item.companies.filter(isDeleted=False):
                                        yeka_businessblog.companies.add(company)
                                        yeka_businessblog.save()

                                yeka_business.save()
                                yeka_business.businessblogs.add(yeka_businessblog)
                                yeka_business.save()

                            competition.business = yeka_business
                            competition.save()
                            if parent_competition.business.businessblogs.filter(
                                    businessblog__name='Yarışmanın Yapılması'):

                                if YekaHoldingCompetition.objects.filter(business=parent_competition.business):
                                    holding_competition = YekaHoldingCompetition(
                                        yekabusinessblog=competition.business.businessblogs.get(
                                            businessblog__name='Yarışmanın Yapılması'),
                                        business=competition.business,
                                        max_price=YekaHoldingCompetition.objects.get(
                                            business=parent_competition.business).max_price,
                                        unit=YekaHoldingCompetition.objects.get(
                                            business=parent_competition.business).unit

                                    )
                                    holding_competition.save()
                                    if YekaContract.objects.filter(business=competition.business):
                                        contract = YekaContract.objects.get(business=competition.business)
                                    else:
                                        contract = YekaContract(
                                            yekabusinessblog=competition.business.businessblogs.get(
                                                businessblog__name='YEKA Kullanım Hakkı Sözleşmesinin İmzalanması'),
                                            business=competition.business
                                        )
                                        contract.save()
                                    if holding_competition.unit.name == 'TL Kuruş/kWh':
                                        contract.unit = ConnectionUnit.objects.get(name='TL Kuruş/kWh')
                                        contract.save()
                                    elif holding_competition.unit.name == 'USD Cent/kWh':
                                        contract.unit = ConnectionUnit.objects.get(name='USD Cent/kWh')
                                        contract.save()

                            # Bagıntılıkları yeka yarışmasına taşıdık
                            for fcom in competition.business.businessblogs.filter(isDeleted=False).order_by('sorting'):
                                if parent_competition.business.businessblogs.filter(businessblog=fcom.businessblog,
                                                                                    isDeleted=False):
                                    yeka_dependence_parent = \
                                        parent_competition.business.businessblogs.filter(businessblog=fcom.businessblog,
                                                                                         isDeleted=False)[
                                            0].dependence_parent
                                    if yeka_dependence_parent:
                                        if competition.business.businessblogs.filter(
                                                businessblog=yeka_dependence_parent.businessblog, isDeleted=False):
                                            fcom.dependence_parent = competition.business.businessblogs.filter(
                                                businessblog=yeka_dependence_parent.businessblog, isDeleted=False)[0]
                                            fcom.save()
                                            x = fcom.dependence_parent
                                            x.child_block = fcom  # bir sonraki iş bloğu oluşturuldu
                                            x.save()
                    yeka_persons = YekaCompetitionPerson.objects.filter(competition=parent_competition)
                    if yeka_persons:
                        for person in yeka_persons:
                            sub_yeka_person = YekaCompetitionPerson(competition=competition, employee=person.employee,
                                                                    is_active=person.is_active,
                                                                    task_date=person.task_date)
                            sub_yeka_person.save()
                    url = redirect('ekabis:view_sub_yeka_competition_detail', competition.uuid).url
                    html = '<a style="" href="' + url + '"> ' + str(
                        competition.pk) + ' - ' + str(
                        competition.name) + '</a> adlı alt yeka eklendi.'
                    notification(request, html, competition.uuid, 'yeka_competition')
                    messages.success(request, 'Yeka Yarışması Kayıt Edilmiştir.')
                    return redirect('ekabis:view_sub_yeka_competition_detail', competition.uuid)

                else:
                    error_message_region = get_error_messages(competition_form)

                    return render(request, 'YekaCompetition/add_sub_competition.html',
                                  {'competition_form': competition_form, 'parent_competition': parent_competition,
                                   'error_messages': error_message_region, 'urls': urls, 'current_url': current_url,
                                   'url_name': url_name, 'name': name, 'proposal': proposal})

            competitions = YekaCompetition.objects.filter(parent=parent_competition)
            return render(request, 'YekaCompetition/add_sub_competition.html',
                          {'competition_form': competition_form, 'competitions': competitions, 'error_messages': '',
                           'parent_competition': parent_competition, 'urls': urls, 'current_url': current_url,
                           'url_name': url_name, 'name': name, 'proposal': proposal})

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required
def change_sumcompetition(request, uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:

        competition_filter = {
            'uuid': uuid,
            'isDeleted': False,
        }
        competition = YekaCompetitionGetService(request, competition_filter)
        competition_form = YekaCompetitionForm(request.POST or None, instance=competition)
        with transaction.atomic():
            if request.method == 'POST':
                if competition_form.is_valid():
                    competition = competition_form.save(request, commit=False)

                    total = int(
                        YekaCompetition.objects.exclude(uuid=competition.uuid).filter(parent=competition.parent,
                                                                                      isDeleted=False).distinct().aggregate(
                            Sum('capacity'))[
                            'capacity__sum'] or 0)
                    total += competition.capacity

                    if total > competition.parent.capacity:
                        messages.warning(request, 'Yeka Yarışmalarının toplam Kapasitesi Bölgeden Büyük Olamaz')
                        return render(request, 'YekaCompetition/change_sumcompetition.html',
                                      {'competition_form': competition_form, 'competition': competition,
                                       })
                    competition.save()

                    url = redirect('ekabis:view_sub_yeka_competition_detail', competition.uuid).url
                    html = '<a style="" href="' + url + '"> ' + str(
                        competition.pk) + ' - ' + str(
                        competition.name) + '</a> adlı alt yeka guncellendi.'
                    notification(request, html, competition.uuid, 'yeka_competition')
                    messages.success(request, 'Alt Yeka  Güncellenmiştir.')
                    return redirect('ekabis:view_sub_yeka_competition_detail', competition.uuid)

                else:
                    error_message_region = get_error_messages(competition_form)

                    return render(request, 'YekaCompetition/change_sumcompetition.html',
                                  {'competition_form': competition_form, 'compeititon': competition,
                                   'error_messages': error_message_region})

            return render(request, 'YekaCompetition/change_sumcompetition.html',
                          {'competition_form': competition_form, 'error_messages': '',
                           'competition': competition})

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required()
def view_yeka_competition_detail(request, uuid):
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
        yeka = YekaCompetitionGetService(request, yeka_filter)
        user = request.user
        employee = None

        if YekaCompetitionPerson.objects.filter(employee__person__user=user, competition=yeka, isDeleted=False):
            employee = YekaCompetitionPerson.objects.get(employee__person__user=user, competition=yeka, isDeleted=False)
        competition_persons = YekaCompetitionPerson.objects.filter(competition=yeka)

        eskalasyon = YekaCompetitionEskalasyon.objects.filter(competition=yeka)
        name = general_methods.yekaname(yeka.business)
        competitions = YekaCompetition.objects.filter(parent=yeka, isDeleted=False)
        if YekaProgressReport.objects.filter(competition=yeka):
            report_progress = YekaProgressReport.objects.get(competition=yeka)
        else:
            report_progress=None
        yekabusinessbloks_sub = None
        proposal_array = []
        proposal_sub_yeka = ProposalSubYeka.objects.filter(sub_yeka__parent=yeka).filter(isDeleted=False).order_by(
            'proposal__order')
        for proposal in proposal_sub_yeka:
            sub_prelicence_date = '---'
            sub_prelicence_time = '---'
            sub_prelicence_finish_date = '--'
            sub_licence_date = '---'
            sub_licence_time = '---'
            sub_licence_finish_date = '---'
            sub_build_date = '---'
            sub_serh_date = '---'
            sub_prelicence_file=None
            sub_licence_file=None

            if proposal.sub_yeka.business:
                yekabusiness_sub = proposal.sub_yeka.business
                yekabusinessbloks_sub = yekabusiness_sub.businessblogs.filter(isDeleted=False).order_by('sorting')

            for block in yekabusinessbloks_sub:

                if block.businessblog.name == 'Ön Lisans Dönemi':

                    if block.startDate:
                        sub_prelicence_finish_date = block.startDate.date().strftime("%d/%m/%Y")
                    if block.parameter:
                        if block.parameter.filter(parametre__title='Ön Lisans Belgesi'):
                            sub_prelicence_file = block.parameter.get(parametre__title='Ön Lisans Belgesi').file
                        if block.parameter.filter(parametre__title='Ön Lisans Süresi (Yıl/Ay/Gün)'):
                            value = block.parameter.get(parametre__title='Ön Lisans Süresi (Yıl/Ay/Gün)').value
                            if value:
                                values = value.split('/')
                                if values.__len__() == 1:
                                    sub_prelicence_time = values[0] + ' Yıl '
                                elif values.__len__() == 2:
                                    sub_prelicence_time = values[0] + ' Yıl ' + values[1] + ' Ay '
                                elif values.__len__() == 3:
                                    sub_prelicence_time = values[0] + ' Yıl ' + values[1] + ' Ay ' + values[2] + ' Gün'
                        if block.parameter.filter(parametre__title='Ön Lisans Tarihi'):
                            sub_prelicence_date = block.parameter.get(parametre__title='Ön Lisans Tarihi').value
                if block.businessblog.name == 'Lisans Alma Tarihi':
                    if block.startDate:
                        sub_licence_finish_date = block.startDate.date().strftime("%d/%m/%Y")
                    if block.parameter:
                        if block.parameter.filter(parametre__title='Lisans Belgesi'):
                            sub_licence_file = block.parameter.get(parametre__title='Lisans Belgesi').file
                        if block.parameter.filter(parametre__title='Lisans Tarihi'):
                            sub_licence_date = block.parameter.get(parametre__title='Lisans Tarihi').value
                        if block.parameter.filter(parametre__title='Lisans Süresi (Yıl/Ay/Gün)'):
                            value = block.parameter.get(parametre__title='Lisans Süresi (Yıl/Ay/Gün)').value
                            if value:
                                values = value.split('/')
                                if values.__len__() == 1:
                                    sub_licence_time = values[0] + ' Yıl '
                                elif values.__len__() == 2:
                                    sub_licence_time = values[0] + ' Yıl ' + values[1] + ' Ay '
                                elif values.__len__() == 3:
                                    sub_licence_time = values[0] + ' Yıl ' + values[1] + ' Ay ' + values[2] + ' Gün'

                if block.businessblog.name == 'Tesis İnşaatının Tamamlanması':
                    if block.startDate:
                        sub_build_date = block.startDate.date().strftime("%d/%m/%Y")
                if block.businessblog.name == 'YEKA İlan Edilmesi':
                    if block.startDate:
                        sub_serh_date = block.startDate.date() + relativedelta(years=3)
            proposal_info_dict = {}
            proposal_info_dict['proposal'] = proposal.sub_yeka
            proposal_info_dict['build_date'] = sub_build_date
            proposal_info_dict['licence_date'] = sub_licence_date
            proposal_info_dict['licence_finish_date'] = sub_licence_finish_date
            proposal_info_dict['licence_time'] = sub_licence_time
            proposal_info_dict['prelicence_date'] = sub_prelicence_date
            proposal_info_dict['prelicence_finish_date'] = sub_prelicence_finish_date
            proposal_info_dict['prelicence_time'] = sub_prelicence_time
            proposal_info_dict['serh_date'] = sub_serh_date
            proposal_info_dict['licence_file'] = sub_licence_file
            proposal_info_dict['prelicence_file'] = sub_prelicence_file


            proposal_array.append(proposal_info_dict)
        if yeka.parent:
            region = ConnectionRegion.objects.get(yekacompetition=yeka.parent)
            comp_yeka = Yeka.objects.get(connection_region=region)


        else:
            region = ConnectionRegion.objects.get(yekacompetition=yeka)
            comp_yeka = Yeka.objects.get(connection_region=region)
        filter = {
            'connection_region': region
        }
        definiton_yeka = YekaService(request, filter).first()

        yekabusinessbloks = None
        if yeka.business:
            yekabusiness = yeka.business
            yekabusinessbloks = yekabusiness.businessblogs.filter(isDeleted=False).order_by('sorting')

        employe_filter = {
            'competition': yeka
        }
        blocks = []
        dependency = []
        indemnity_bond_file = None
        indemnity_quantity = None
        guarantee = YekaGuarantee.objects.filter(business=yeka.business)
        guarantees = None
        if guarantee:
            guarantees = YekaGuarantee.objects.get(business=yeka.business).guarantee.filter(isDeleted=False).last()

        prelicence_date = '---'
        prelicence_time = '---'
        prelicence_finish_date = '--'
        licence_date = '---'
        licence_time = '---'
        licence_finish_date = '---'
        contract_price = '---'
        eskalasyon_price = '---'
        build_date = '---'
        serh_date = '---'
        total = 0
        eskalasyon_date = '---'
        unit = '---'
        for block in yekabusinessbloks:
            if block.businessblog.name == 'Ön Lisans Dönemi':
                if block.businessTime:
                    prelicence_time = block.businessTime
                if block.startDate:
                    prelicence_finish_date = block.startDate.date().strftime("%d/%m/%Y")
                if block.parameter:
                    if block.parameter.filter(parametre__title='Ön Lisans Tarihi'):
                        prelicence_date = block.parameter.get(parametre__title='Ön Lisans Tarihi').value
            if block.businessblog.name == 'Lisans Alma Tarihi':
                if block.startDate:
                    licence_finish_date = block.startDate.date().strftime("%d/%m/%Y")
                if block.businessTime:
                    licence_time = block.businessTime
                if block.parameter:
                    if block.parameter.filter(parametre__title='Lisans Tarihi'):
                        licence_date = block.parameter.get(parametre__title='Lisans Tarihi').value

            if block.businessblog.name == 'Tesis İnşaatının Tamamlanması':
                if block.startDate:
                    build_date = block.startDate.date().strftime("%d/%m/%Y")
            if block.businessblog.name == 'YEKA İlan Edilmesi':
                if block.startDate:
                    serh_date = block.startDate.date() + relativedelta(years=3)
            if block.businessblog.name == 'YEKA Kullanım Hakkı Sözleşmesinin İmzalanması':
                if YekaContract.objects.filter(business=yeka.business):
                    contract = YekaContract.objects.get(business=yeka.business)
                    if contract.unit:
                        contract_price = str(contract.price) + ' ' + contract.unit.name
                        unit = contract.unit.name
                        if contract.unit.name == 'TL Kuruş/kWh':
                            if YekaCompetitionEskalasyon.objects.filter(competition=yeka):
                                eskalasyon = YekaCompetitionEskalasyon.objects.filter(competition=yeka).last()
                                eskalasyon_price = str(eskalasyon.result) + ' ' + 'TL'
                                eskalasyon_date = eskalasyon.creationDate.date().strftime("%d/%m/%Y")
            if block.businessblog.name == 'Kabuller':
                if YekaAccept.objects.filter(business=yeka.business):
                    yeka_accept = YekaAccept.objects.get(business=yeka.business)
                    accepts = yeka_accept.accept.filter(isDeleted=False)
                    if accepts:
                        for accept in accepts:
                            total += float(accept.currentPower)
                    total = round(float("{:.5f}".format(total)), 5)

            bloc_dict = {}
            dict = {}
            bloc_dict['yekabusinessblog'] = block
            bloc_dict['businessblog'] = block.businessblog.uuid
            bloc_dict['yeka'] = yeka.uuid

            html = ''
            for param in block.parameter.filter(isDeleted=False):
                if param.parametre.type == 'file':
                    html += '<div class="form-group"> <label>' + param.parametre.title + ' : </label> <a href="' + MEDIA_URL + param.file.name + '" target="_blank">' + param.file.name + '</div>'
                else:
                    html += '<div class="form-group"> <label>' + param.parametre.title + ' : </label>' + str(
                        param.value) + '</div>'
            bloc_dict['html'] = html
            blocks.append(bloc_dict)
        yeka_info_dict = {}
        yeka_info_dict['serh_date'] = serh_date
        yeka_info_dict['unit'] = unit
        yeka_info_dict['accept_total'] = total
        yeka_info_dict['eskalasyon_price'] = eskalasyon_price
        yeka_info_dict['eskalasyon_date'] = eskalasyon_date

        yeka_info_dict['contract_price'] = contract_price
        yeka_info_dict['build_date'] = build_date
        yeka_info_dict['licence_date'] = licence_date
        yeka_info_dict['licence_finish_date'] = licence_finish_date
        yeka_info_dict['licence_time'] = licence_time
        yeka_info_dict['prelicence_date'] = prelicence_date
        yeka_info_dict['prelicence_finish_date'] = prelicence_finish_date
        yeka_info_dict['prelicence_time'] = prelicence_time
        employees = YekaCompetitionPersonService(request, employe_filter)
        array_proposal = []
        yekaproposal = None
        positive = 0
        negative = 0
        not_result = 0
        if YekaProposal.objects.filter(business=yeka.business):
            yekaproposal = YekaProposal.objects.get(business=yeka.business)
            pro_list = []
            proposals = yekaproposal.proposal.filter(isDeleted=False).order_by('name')

            for key, proposal in enumerate(proposals):
                if key == 0:
                    if not proposal.order:
                        proposal.order = 1
                        proposal.save()
                else:
                    if not proposal.order:
                        last = proposals.filter(order__isnull=False).order_by('order').last().order
                        proposal.order = int(last) + 1
                        proposal.save()
            array_proposal = []
            proposals = yekaproposal.proposal.filter(isDeleted=False).order_by('order')

            for proposal in proposals:

                proposal_dict = {}
                proposal_dict['status'] = '##ffffff'
                olumsuz = proposal.institution.filter(status='Olumsuz', isDeleted=False)
                sonuclanmadi = proposal.institution.filter(status='Sonuçlanmadı', isDeleted=False)
                olumlu = proposal.institution.filter(status='Olumlu', isDeleted=False)

                if olumsuz:
                    proposal_dict['status'] = '#ff3a3a'
                    proposal_dict['proposal'] = proposal
                elif sonuclanmadi:
                    proposal_dict['status'] = '#ffff6e'
                    proposal_dict['proposal'] = proposal
                elif olumlu:
                    proposal_dict['status'] = '#8cff8c'
                    proposal_dict['proposal'] = proposal
                else:
                    proposal_dict['status'] = '#ffff6e'
                    proposal_dict['proposal'] = proposal
                array_proposal.append(proposal_dict)

        return render(request, 'Yeka/yeka_competition_detail.html',
                      {'urls': urls, 'current_url': current_url, 'proposal_sub_yeka': proposal_sub_yeka,
                       'url_name': url_name, 'name': name, 'blocks': blocks, 'definition': definiton_yeka,
                       'yeka': yeka, 'yekabusinessbloks': yekabusinessbloks, 'array_proposal': array_proposal,
                       'yeka_eskalasyon': eskalasyon, 'employee': employee, 'competition_persons': competition_persons,
                       'employees': employees, 'competitions': competitions, 'region': region,
                       'yekaproposal': yekaproposal, 'report_progress': report_progress,
                       'indemnity': guarantees, 'comp_yeka': comp_yeka,
                       'yeka_info': yeka_info_dict, 'proposal_array': proposal_array
                       })

    except Exception as e:

        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required()
def view_sub_yeka_competition_detail(request, uuid):
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
        yeka = YekaCompetitionGetService(request, yeka_filter)
        user = request.user
        employee = None

        if YekaCompetitionPerson.objects.filter(employee__person__user=user, competition=yeka, isDeleted=False):
            employee = YekaCompetitionPerson.objects.get(employee__person__user=user, competition=yeka, isDeleted=False)
        proposal_sub_yeka = None
        yeka_proposal = None
        if ProposalSubYeka.objects.filter(sub_yeka=yeka, isDeleted=False):
            proposal_sub_yeka = ProposalSubYeka.objects.filter(sub_yeka=yeka, isDeleted=False).first()
            yeka_proposal = YekaProposal.objects.filter(proposal=proposal_sub_yeka.proposal).first()
        name = general_methods.yekaname(yeka.business)

        yekabusinessbloks = None
        if yeka.business:
            yekabusiness = yeka.business
            yekabusinessbloks = yekabusiness.businessblogs.filter(isDeleted=False).order_by('sorting')

        if yeka.parent:
            region = ConnectionRegion.objects.get(yekacompetition=yeka.parent)
            comp_yeka = Yeka.objects.get(connection_region=region)


        else:
            region = ConnectionRegion.objects.get(yekacompetition=yeka)
            comp_yeka = Yeka.objects.get(connection_region=region)
        employe_filter = {
            'competition': yeka
        }
        blocks = []
        prelicence_date = '---'
        prelicence_time = '---'
        prelicence_finish_date = '--'
        licence_date = '---'
        licence_time = '---'
        licence_finish_date = '---'
        build_date = '---'
        serh_date = '---'
        licence_file=None
        prelicence_file=None
        total = 0
        for block in yekabusinessbloks:
            block_dict = {}
            block_dict['yekabusinessblog'] = block
            block_dict['businessblog'] = block.businessblog.uuid
            block_dict['yeka'] = yeka.uuid

            blocks.append(block_dict)
            if block.businessblog.name == 'Ön Lisans Dönemi':
                if block.startDate:
                    prelicence_finish_date = block.startDate.date().strftime("%d/%m/%Y")
                if block.parameter:
                    if block.parameter.filter(parametre__title='Ön Lisans Belgesi'):
                        prelicence_file = block.parameter.get(parametre__title='Ön Lisans Belgesi').file
                    if block.parameter.filter(parametre__title='Ön Lisans Tarihi'):
                        prelicence_date = block.parameter.get(parametre__title='Ön Lisans Tarihi').value
                    if block.parameter.filter(parametre__title='Ön Lisans Süresi (Yıl/Ay/Gün)'):
                        value = block.parameter.get(parametre__title='Ön Lisans Süresi (Yıl/Ay/Gün)').value
                        if value:
                            values = value.split('/')
                            if values.__len__() == 1:
                                prelicence_time = values[0] + ' Yıl '
                            elif values.__len__() == 2:
                                prelicence_time = values[0] + ' Yıl ' + values[1] + ' Ay '
                            elif values.__len__() == 3:
                                prelicence_time = values[0] + ' Yıl ' + values[1] + ' Ay ' + values[2] + ' Gün'

            if block.businessblog.name == 'Lisans Alma Tarihi':
                if block.startDate:
                    licence_finish_date = block.startDate.date().strftime("%d/%m/%Y")
                if block.parameter:
                    if block.parameter.filter(parametre__title='Lisans Belgesi'):
                        licence_file = block.parameter.get(parametre__title='Lisans Belgesi').file
                    if block.parameter.filter(parametre__title='Lisans Tarihi'):
                        licence_date = block.parameter.get(parametre__title='Lisans Tarihi').value
                    if block.parameter.filter(parametre__title='Lisans Süresi (Yıl/Ay/Gün)'):
                        value = block.parameter.get(parametre__title='Lisans Süresi (Yıl/Ay/Gün)').value
                        if value:
                            values = value.split('/')
                            if values.__len__() == 1:
                                licence_time = values[0] + ' Yıl '
                            elif values.__len__() == 2:
                                licence_time = values[0] + ' Yıl ' + values[1] + ' Ay '
                            elif values.__len__() == 3:
                                licence_time = values[0] + ' Yıl ' + values[1] + ' Ay ' + values[2] + ' Gün'

            if block.businessblog.name == 'Tesis İnşaatının Tamamlanması':
                if block.startDate:
                    build_date = block.startDate.date().strftime("%d/%m/%Y")
            if block.businessblog.name == 'YEKA İlan Edilmesi':
                if block.startDate:
                    serh_date = block.startDate.date() + relativedelta(years=3)
            if block.businessblog.name == 'YEKA Kullanım Hakkı Sözleşmesinin İmzalanması':
                if YekaContract.objects.filter(business=yeka.business):
                    contract = YekaContract.objects.get(business=yeka.business)
                    if contract.unit:
                        contract_price = str(contract.price) + ' ' + contract.unit.name
                        if contract.unit.name == 'TL Kuruş/kWh':
                            if YekaCompetitionEskalasyon.objects.filter(competition=yeka):
                                eskalasyon_price = str(YekaCompetitionEskalasyon.objects.filter(
                                    competition=yeka).last().result) + ' ' + 'TL'
            if block.businessblog.name == 'Kabuller':
                if YekaAccept.objects.filter(business=yeka.business):
                    yeka_accept = YekaAccept.objects.get(business=yeka.business)
                    accepts = yeka_accept.accept.filter(isDeleted=False)
                    if accepts:
                        for accept in accepts:
                            total += float(accept.currentPower)
                    total = round(float("{:.5f}".format(total)), 5)
        yeka_info_dict = {}
        yeka_info_dict['serh_date'] = serh_date
        yeka_info_dict['prelicence_file']=prelicence_file
        yeka_info_dict['licence_file']=licence_file
        yeka_info_dict['accept_total'] = total
        yeka_info_dict['build_date'] = build_date
        yeka_info_dict['licence_date'] = licence_date
        yeka_info_dict['licence_finish_date'] = licence_finish_date
        yeka_info_dict['licence_time'] = licence_time
        yeka_info_dict['prelicence_date'] = prelicence_date
        yeka_info_dict['prelicence_finish_date'] = prelicence_finish_date
        yeka_info_dict['prelicence_time'] = prelicence_time
        employees = YekaCompetitionPersonService(request, employe_filter)

        return render(request, 'YekaCompetition/sub_yeka_detail.html',
                      {'urls': urls, 'current_url': current_url, 'proposal_sub_yeka': proposal_sub_yeka,
                       'url_name': url_name, 'name': name, 'blocks': blocks, 'yeka_proposal': yeka_proposal,
                       'yeka': yeka, 'yekabusinessbloks': yekabusinessbloks, 'employe': employee,'competition':yeka.parent,
                       'employees': employees, 'yeka_info': yeka_info_dict,'comp_yeka': comp_yeka,'region':region

                       })

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required
def view_person_competition(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    yeka_form = YekaForm()

    try:
        user = request.user
        person_filter = {
            'user': user,
        }

        employee = EmployeeGetService(request, person_filter)
        competition_filter = {
            'employee': employee,
        }
        competitions = YekaCompetitionService(request, competition_filter)
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        with transaction.atomic():
            return render(request, 'YekaCompetition/view_competition.html',
                          {'competitions': competitions, 'yeka_form': yeka_form, 'error_messages': '',
                           'urls': urls, 'current_url': current_url, 'url_name': url_name})

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')
