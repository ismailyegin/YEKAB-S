import traceback

from django import forms
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db.models import Q
from django.urls import resolve

from ekabis.Forms.ConnectionRegionForm import ConnectionRegionForm
from ekabis.Forms.PurchaseGuaranteeForm import PurchaseGuaranteeForm
from ekabis.Forms.YekaBusinessBlogForm import YekaBusinessBlogForm
from ekabis.Forms.YekaBusinessForm import YekaBusinessForm
from ekabis.Forms.YekaCompetitionForm import YekaCompetitionForm
from ekabis.Forms.YekaContractForm import YekaContractForm
from ekabis.Forms.YekaForm import YekaForm
from ekabis.Views.VacationDayViews import is_vacation_day
from ekabis.models.Proposal import Proposal
from ekabis.models.YekaBusinessBlog import YekaBusinessBlog
from ekabis.models import YekaCompetition, YekaBusiness, BusinessBlog, Employee, YekaPerson, \
    YekaPersonHistory, Permission, ConnectionRegion, YekaPurchaseGuarantee, ProposalSubYeka, YekaCompetitionEskalasyon
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
        if Yeka.objects.filter(connection_region=region):
            yeka = Yeka.objects.filter(connection_region=region)[0]
            competition_form = YekaCompetitionForm()  # initial={'date': yeka.date} yeka resmi gazete tarihi  miras
        with transaction.atomic():
            if request.method == 'POST':

                competition_form = YekaCompetitionForm(request.POST)

                if competition_form.is_valid():

                    competition = competition_form.save(request, commit=False)

                    total = int(
                        region.yekacompetition.all().exclude(id=competition.id).distinct().aggregate(Sum('capacity'))[
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
                                        sorting=item.sorting,
                                        businessTime=item.businessTime,
                                        status=item.status,
                                        businessblog=item.businessblog

                                    )
                                    parent_yeka_business_blog = yeka_businessblog
                                    yeka_businessblog.save()

                                else:
                                    yeka_businessblog = YekaBusinessBlog(

                                        parent=parent_yeka_business_blog,
                                        finisDate=item.finisDate,
                                        startDate=item.startDate,
                                        businessblog=item.businessblog,
                                        sorting=item.sorting,
                                        businessTime=item.businessTime,
                                        status=item.status,
                                    )
                                    yeka_businessblog.save()
                                    parent_yeka_business_blog = yeka_businessblog
                                yeka_business.businessblogs.add(yeka_businessblog)
                                yeka_business.save()
                            competition.business = yeka_business
                            competition.save()

                            # Bagıntılıkları yeka yarışmasına taşıdık
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
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
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
                obj = YekaCompetitionGetService(request, competition_filter)
                parent_filter = {
                    'parent': obj
                }

                if YekaCompetitionService(request, parent_filter):

                    return JsonResponse({'status': 'Fail', 'msg': ' Bağlı alt YEKA olduğu için silinemez.'})

                else:
                    log = str(obj.name) + "Yeka yarışması silindi."
                    log = general_methods.logwrite(request, request.user, log)
                    obj.isDeleted = True
                    obj.save()
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
                                blog.sorting = i + 1
                                blog.save()

                                parent = blog

                            else:

                                blog = yekabusiness.businessblogs.filter(businessblog_id=blogs[i])[0]
                                if blog.isDeleted:
                                    blog.isDeleted = False
                                blog.parent = parent
                                blog.sorting = i + 1
                                blog.save()
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
                                                        parent=parent,
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
def change_yekacompetitionbusinessBlog(request, competition, yekabusiness, business):  # yeka iş bloğu düzenleme
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

        business = BusinessBlogGetService(request, yeka_business_filter_)
        yekaBusinessBlogo_form = YekaBusinessBlogForm(business.pk, yekabussiness, instance=yekabussiness)

        # if yekaBusinessBlogo_form['dependence_parent'].initial !=None:
        #     yekaBusinessBlogo_form.fields['startDate'].widget.attrs['readonly'] = True


        if business.name == 'YEKA Kullanım Hakkı Sözleşmesinin İmzalanması':
            contract = None
            if YekaContract.objects.filter(business=competition.business):
                contract = YekaContract.objects.get(business=competition.business)
            else:
                contract = YekaContract(
                    yekabusinessblog=yekabussiness,
                    business=competition.business
                )
                contract.save()
            form_contract = YekaContractForm(request.POST or None, request.FILES or None, instance=contract)
            form_contract.fields['unit'].required = True
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

        name = general_methods.yekaname(competition.business)

        yekaBusinessBlogo_form.fields['dependence_parent'].queryset = competition.business.businessblogs.exclude(
            uuid=yekabussiness.uuid).filter(isDeleted=False)

        yekaBusinessBlogo_form.fields['child_block'].queryset = competition.business.businessblogs.exclude(
            uuid=yekabussiness.uuid).filter(isDeleted=False)

        for item in yekabussiness.parameter.all():
            if item.parametre.type == 'file':
                yekaBusinessBlogo_form.fields[item.parametre.title].required = False
                yekaBusinessBlogo_form.fields[item.parametre.title].initial = item.file
                yekaBusinessBlogo_form.fields[
                    item.parametre.title].hidden_widget.template_name = "django/forms/widgets/clearable_file_input.html"
            else:
                yekaBusinessBlogo_form.fields[item.parametre.title].initial = item.value

        if request.POST:
            yekaBusinessBlogo_form = YekaBusinessBlogForm(business.pk, yekabussiness, request.POST or None,
                                                          request.FILES or None,
                                                          instance=yekabussiness)
            if form_contract:
                if form_contract.is_valid():
                    contract = form_contract.save(request, commit=False)
                    contract.save()
                    competition.business.company = contract.company
                    competition.save()
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

            if yekaBusinessBlogo_form.is_valid():
                finish_date = ''
                start_date = ''
                time = 0
                if not yekaBusinessBlogo_form.cleaned_data['indefinite']:
                    time = (yekaBusinessBlogo_form.cleaned_data['businessTime']) - 1
                    time_type = yekaBusinessBlogo_form.cleaned_data['time_type']
                    startDate = yekaBusinessBlogo_form.cleaned_data['startDate']
                    if time_type == 'is_gunu':
                        time = yekaBusinessBlogo_form.cleaned_data['businessTime']
                        add_time = time
                        start_date = startDate.date()
                        count = 0
                        while add_time > 1:
                            start_date = start_date + datetime.timedelta(days=1)
                            count = count + 1
                            is_vacation = is_vacation_day(start_date)
                            if not is_vacation:
                                add_time = add_time - 1
                    else:

                        start_date = startDate.date() + datetime.timedelta(days=time)
                    yekabussiness.startDate = startDate
                    yekabussiness.finisDate = start_date
                    yekabussiness.save()
                else:
                    yekabussiness.businessTime = 0
                    yekabussiness.finisDate = yekaBusinessBlogo_form.cleaned_data['startDate']
                    yekabussiness.save()
                yekaBusinessBlogo_form.save(yekabussiness.pk, business.pk, commit=False)
                if yekaBusinessBlogo_form['child_block'].data == yekaBusinessBlogo_form['dependence_parent'].data:
                    messages.warning(request, 'Bir önceki iş bloğu ile bir sonraki iş bloğu aynı olamaz.')
                    return render(request, 'Yeka/YekabussinesBlogUpdate.html',
                                  {
                                      'yekaBusinessBlogo_form': yekaBusinessBlogo_form,
                                      'competition': competition, 'urls': urls,
                                      'current_url': current_url, 'contract_form': form_contract,
                                      'purchase_guarantee_form': purchase_guarantee_form,
                                      'url_name': url_name,
                                      'name': name
                                  })
                else:
                    yekaBusinessBlogo_form.save(yekabussiness.pk, business.pk)

                if yekabussiness.completion_date:

                    dependence_block = YekaBusinessBlog.objects.get(dependence_parent=yekabussiness)
                    x = YekaBusiness.objects.get(businessblogs=dependence_block)
                    list = x.businessblogs.filter(sorting__gte=dependence_block.sorting)
                    i = 0
                    while dependence_block:

                            start_date = yekabussiness.completion_date.date()
                            for block in list:
                                if yekabussiness.time_type == 'is_gunu':
                                    time = yekabussiness.businessTime
                                    add_time = time

                                    count = 0
                                    while add_time > 1:
                                        start_date = start_date + datetime.timedelta(days=1)
                                        count = count + 1
                                        is_vacation = is_vacation_day(start_date)
                                        if not is_vacation:
                                            add_time = add_time - 1
                                else:
                                    start_date = start_date + datetime.timedelta(days=time)
                                block.startDate = start_date
                                block.save()
                                dependence_block = YekaBusinessBlog.objects.filter(dependence_parent=block)
                                i = i + 1
                                start_date = block.finisDate
                else:
                    dependence_block = YekaBusinessBlog.objects.filter(dependence_parent=yekabussiness)

                    if dependence_block:
                        dependence_block = YekaBusinessBlog.objects.get(dependence_parent=yekabussiness)
                        start_date = yekabussiness.startDate.date()
                        if yekabussiness.businessTime:
                            time = yekabussiness.businessTime
                        else:
                            return redirect('ekabis:view_yeka_competition_detail', competition.uuid)

                        if yekabussiness.time_type == 'is_gunu':
                            add_time = time

                            count = 0
                            while add_time > 1:
                                start_date = start_date + datetime.timedelta(days=1)
                                count = count + 1
                                is_vacation = is_vacation_day(start_date)
                                if not is_vacation:
                                    add_time = add_time - 1
                        else:
                            start_date = start_date + datetime.timedelta(days=time)
                        dependence_block.startDate = start_date
                        dependence_block.save()

                        dependence_block = YekaBusinessBlog.objects.get(dependence_parent=dependence_block)
                        x = YekaBusiness.objects.get(businessblogs=dependence_block)
                        list = x.businessblogs.filter(sorting__gte=dependence_block.sorting)
                        i = 0

                        while dependence_block:

                            start_date = dependence_block.startDate
                            for block in list:
                                if block.businessTime:
                                    time = block.businessTime

                                else:
                                    dependence_block = None
                                    break

                                if block.time_type == 'is_gunu':
                                    add_time = time

                                    count = 0
                                    while add_time > 1:
                                        start_date = start_date + datetime.timedelta(days=1)
                                        count = count + 1
                                        is_vacation = is_vacation_day(start_date)
                                        if not is_vacation:
                                            add_time = add_time - 1
                                else:
                                    start_date = start_date + datetime.timedelta(days=time)
                                block.startDate = start_date
                                block.save()
                                dependence_block = YekaBusinessBlog.objects.filter(dependence_parent=block)
                                start_date = block.startDate
                messages.success(request, 'Basarıyla Kayıt Edilmiştir.')
                url = redirect('ekabis:view_yeka_competition_detail', competition.uuid).url
                html = '<a style="" href="' + url + '"> ID : ' + str(business.pk) + ' - ' + str(
                    business.name) + '</a> adlı iş bloğu guncellendi.'
                notification(request, html, competition.uuid, 'yeka_competition')
                return redirect('ekabis:view_yeka_competition_detail', competition.uuid)
        return render(request, 'Yeka/YekabussinesBlogUpdate.html',
                      {
                          'yekaBusinessBlogo_form': yekaBusinessBlogo_form,
                          'competition': competition, 'urls': urls,
                          'current_url': current_url, 'contract_form': form_contract,
                          'purchase_guarantee_form': purchase_guarantee_form,
                          'url_name': url_name,
                          'name': name
                      })
    except Exception as e:

        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


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
        if Proposal.objects.filter(uuid=proposal_uuid):
            proposal = Proposal.objects.get(uuid=proposal_uuid)

        with transaction.atomic():

            if request.method == 'POST':

                competition_form = YekaCompetitionForm(request.POST)

                if competition_form.is_valid():

                    competition = competition_form.save(request, commit=False)

                    # baglı oldugu yarışmanın kapsitesinden fazla olamaz
                    total = int(
                        YekaCompetition.objects.filter(parent=parent_competition, isDeleted=False).distinct().aggregate(
                            Sum('capacity'))[
                            'capacity__sum'] or 0)
                    total += proposal.capacity

                    if total > parent_competition.capacity:
                        messages.warning(request, 'Yeka Yarışmalarının toplam Kapasitesi Bölgeden Büyük Olamaz')
                        return render(request, 'YekaCompetition/add_sub_competition.html',
                                      {'competition_form': competition_form, 'parent_competition': parent_competition,
                                       'error_messages': '', 'urls': urls, 'current_url': current_url,
                                       'url_name': url_name
                                       })
                    else:
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
                                        sorting=item.sorting,
                                        businessTime=item.businessTime,
                                        status=item.status,
                                        businessblog=item.businessblog

                                    )
                                    parent_yeka_business_blog = yeka_businessblog
                                    yeka_businessblog.save()

                                else:
                                    yeka_businessblog = YekaBusinessBlog(parent=parent_yeka_business_blog,
                                                                         finisDate=item.finisDate,
                                                                         businessblog=item.businessblog,
                                                                         startDate=item.startDate,
                                                                         sorting=item.sorting,
                                                                         businessTime=item.businessTime,
                                                                         status=item.status,
                                                                         )
                                    yeka_businessblog.save()
                                    parent_yeka_business_blog = yeka_businessblog
                                if item.companies.all():
                                    for company in item.companies.all():
                                        yeka_businessblog.companies.add(company)
                                        yeka_businessblog.save()

                                yeka_business.save()
                                yeka_business.businessblogs.add(yeka_businessblog)
                                yeka_business.save()
                            competition.business = yeka_business
                            competition.save()

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
                                   'url_name': url_name})

            competitions = YekaCompetition.objects.filter(parent=parent_competition)
            return render(request, 'YekaCompetition/add_sub_competition.html',
                          {'competition_form': competition_form, 'competitions': competitions, 'error_messages': '',
                           'parent_competition': parent_competition, 'urls': urls, 'current_url': current_url,
                           'url_name': url_name})

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
        eskalasyon=YekaCompetitionEskalasyon.objects.filter(competition=yeka)
        name = general_methods.yekaname(yeka.business)
        competitions = YekaCompetition.objects.filter(parent=yeka, isDeleted=False)
        proposal_sub_yeka = ProposalSubYeka.objects.filter(sub_yeka__parent=yeka, isDeleted=False)
        if yeka.parent:
            region = ConnectionRegion.objects.get(yekacompetition=yeka.parent)

        else:
            region = ConnectionRegion.objects.get(yekacompetition=yeka)
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

        for block in yekabusinessbloks:
            bloc_dict = {}
            dict = {}
            bloc_dict['yekabusinessblog'] = block
            bloc_dict['businessblog'] = block.businessblog.uuid
            bloc_dict['yeka'] = yeka.uuid

            html = ''
            for param in block.parameter.all():
                if param.parametre.type == 'file':
                    html += '<div class="form-group"> <label>' + param.parametre.title + ' : </label> <a href="' + MEDIA_URL + param.file.name + '" target="_blank">' + param.file.name + '</div>'
                else:
                    html += '<div class="form-group"> <label>' + param.parametre.title + ' : </label>' + str(
                        param.value) + '</div>'
            bloc_dict['html'] = html
            blocks.append(bloc_dict)

        employees = YekaCompetitionPersonService(request, employe_filter)
        array_proposal=[]
        yekaproposal=None
        if YekaProposal.objects.filter(business=yeka.business):
            yekaproposal = YekaProposal.objects.get(business=yeka.business)

            proposals=yekaproposal.proposal.all()
            array_proposal=[]
            for proposal in proposals:
                proposal_dict = {}
                proposal_dict['status'] = '##ffffff'
                olumsuz=proposal.institution.filter(status='Olumsuz')
                sonuclanmadi = proposal.institution.filter(status='Sonuclanmadi')
                if olumsuz:
                    proposal_dict['status']='#ff3a3a'
                    proposal_dict['proposal']=proposal
                elif sonuclanmadi:
                    proposal_dict['status'] = '#ffff6e'
                    proposal_dict['proposal'] = proposal
                else:
                    proposal_dict['status'] = '#8cff8c'
                    proposal_dict['proposal'] = proposal
                array_proposal.append(proposal_dict)

        return render(request, 'Yeka/yeka_competition_detail.html',
                      {'urls': urls, 'current_url': current_url, 'proposal_sub_yeka': proposal_sub_yeka,
                       'url_name': url_name, 'name': name, 'blocks': blocks, 'definition': definiton_yeka,
                       'yeka': yeka, 'yekabusinessbloks': yekabusinessbloks,'array_proposal':array_proposal,
                       'yeka_eskalasyon':eskalasyon,
                       'employees': employees, 'competitions': competitions, 'region': region,'yekaproposal':yekaproposal

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

        employe_filter = {
            'competition': yeka
        }
        blocks = []

        for blok in yekabusinessbloks:
            bloc_dict = {}
            bloc_dict['yekabusinessblog'] = blok
            bloc_dict['businessblog'] = blok.businessblog.uuid
            bloc_dict['yeka'] = yeka.uuid

            blocks.append(bloc_dict)

        employees = YekaCompetitionPersonService(request, employe_filter)

        return render(request, 'YekaCompetition/sub_yeka_detail.html',
                      {'urls': urls, 'current_url': current_url, 'proposal_sub_yeka': proposal_sub_yeka,
                       'url_name': url_name, 'name': name, 'blocks': blocks, 'yeka_proposal': yeka_proposal,
                       'yeka': yeka, 'yekabusinessbloks': yekabusinessbloks,
                       'employees': employees,

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
