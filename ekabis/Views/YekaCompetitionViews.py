import traceback

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.urls import resolve

from ekabis.Forms.ConnectionRegionForm import ConnectionRegionForm
from ekabis.Forms.YekaBusinessBlogForm import YekaBusinessBlogForm
from ekabis.Forms.YekaBusinessForm import YekaBusinessForm
from ekabis.Forms.YekaCompetitionForm import YekaCompetitionForm
from ekabis.Forms.YekaContractForm import YekaContractForm
from ekabis.Forms.YekaForm import YekaForm
from ekabis.Views.VacationDayViews import is_vacation_day
from ekabis.models.YekaBusinessBlog import YekaBusinessBlog
from ekabis.models import YekaCompetition, YekaBusiness, BusinessBlog, Employee, YekaPerson, \
    YekaPersonHistory, Permission, ConnectionRegion
from ekabis.models.YekaCompetitionPerson import YekaCompetitionPerson
from ekabis.models.YekaCompetitionPersonHistory import YekaCompetitionPersonHistory
from ekabis.models.YekaContract import YekaContract
from ekabis.services import general_methods
from ekabis.services.general_methods import get_error_messages
from ekabis.services.services import YekaGetService, ConnectionRegionGetService, YekaCompetitionGetService, \
    YekaBusinessGetService, YekaBusinessBlogGetService, BusinessBlogGetService, YekaCompetitionPersonService, \
    EmployeeGetService, last_urls, ExtraTimeService, YekaCompetitionService, YekaService
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
                        YekaCompetition.objects.filter(connectionregion=region, isDeleted=False).distinct().aggregate(
                            Sum('capacity'))[
                            'capacity__sum'] or 0)
                    total += competition.capacity

                    if total > region.capacity:
                        messages.warning(request, 'Yeka Yarışmalarının toplam Kapasitesi Bölgeden Büyük Olamaz')
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

                    log = " Yeka Yarışması  eklendi"
                    log = general_methods.logwrite(request, request.user, log)
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
        competition_form = YekaCompetitionForm(request.POST or None, instance=competition)
        with transaction.atomic():
            if request.method == 'POST':
                if competition_form.is_valid():
                    competition = competition_form.save(request, commit=False)

                    total = int(
                        YekaCompetition.objects.filter(connectionregion=region).distinct().aggregate(Sum('capacity'))[
                            'capacity__sum'] or 0)
                    total += competition.capacity

                    if total > region.capacity:
                        messages.warning(request, 'Yeka Yarışmalarının toplam Kapasitesi Bölgeden Büyük Olamaz')
                        return render(request, 'YekaCompetition/change_competition.html',
                                      {'competition_form': competition_form, 'region': region, 'urls': urls,
                                       'current_url': current_url, 'url_name': url_name, 'competition': competition,
                                       })
                    competition.save()
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
                                   'error_messages': error_message_region, 'urls': urls, 'current_url': current_url,
                                   'url_name': url_name, 'competition': competition, })

            competitions = region.yekacompetition.filter(isDeleted=False)
            return render(request, 'YekaCompetition/change_competition.html',
                          {'competition_form': competition_form, 'error_messages': '', 'urls': urls,
                           'current_url': current_url, 'url_name': url_name, 'competition': competition,
                           'region': region})

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
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
                                                    parent=parent,dependence_parent=parent,
                                                    sorting=i + 1
                                                    )
                            blog.save()
                            blog.dependence_parent = parent
                            parent = blog
                        yekabusiness.businessblogs.add(blog)
                        yekabusiness.save()
                        log = str(competition.name) + ' adlı yarışmaya - ' + str(
                            blog.businessblog.name) + " adlı iş bloğu atandı."
                        log = general_methods.logwrite(request, request.user, log)

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
                                parent = blog
                            yekabusiness.businessblogs.add(blog)
                            yekabusiness.save()


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
def change_yekacompetitionbusinessBlog(request, competition, yekabusiness, business):
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

        business = BusinessBlogGetService(request, yeka_business_filter_)
        if business.name=='YEKA Kullanım Hakkı Sözleşmesinin İmzalanması':
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
            form_contract.fields['unit'].required=True

        name = general_methods.yekaname(competition.business)

        yekaBusinessBlogo_form = YekaBusinessBlogForm(business.pk, yekabussiness, instance=yekabussiness)
        yekaBusinessBlogo_form.fields['dependence_parent'].queryset = competition.business.businessblogs.exclude(
            uuid=yekabussiness.uuid).filter(isDeleted=False)

        for item in yekabussiness.paremetre.all():
            if item.parametre.type == 'file':
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
            if yekaBusinessBlogo_form.is_valid():
                finish_date = ''
                start_date = ''



                time = (yekaBusinessBlogo_form.cleaned_data['businessTime']) - 1
                if not yekaBusinessBlogo_form.cleaned_data['indefinite']:
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
                yekaBusinessBlogo_form.save(yekabussiness.pk, business.pk)

                messages.success(request, 'Basarıyla Kayıt Edilmiştir.')
                return redirect('ekabis:view_yeka_competition_detail', competition.uuid)
        return render(request, 'Yeka/YekabussinesBlogUpdate.html',
                      {
                          'yekaBusinessBlogo_form': yekaBusinessBlogo_form,
                          'competition': competition, 'urls': urls,
                          'current_url': current_url,'contract_form':form_contract,
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
def add_sumcompetition(request, uuid):
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

        with transaction.atomic():

            if request.method == 'POST':

                competition_form = YekaCompetitionForm(request.POST)

                if competition_form.is_valid():

                    competition = competition_form.save(request, commit=False)

                    # baglı oldugu yarışmanın kapsitesinden fazla olamaz
                    total = int(
                        YekaCompetition.objects.filter(parent=parent_competition).distinct().aggregate(Sum('capacity'))[
                            'capacity__sum'] or 0)
                    total += competition.capacity

                    if total > parent_competition.capacity:
                        messages.warning(request, 'Yeka Yarışmalarının toplam Kapasitesi Bölgeden Büyük Olamaz')
                        return render(request, 'YekaCompetition/add_sub_competition.html',
                                      {'competition_form': competition_form, 'parent_competition': parent_competition,
                                       'error_messages': '', 'urls': urls, 'current_url': current_url,
                                       'url_name': url_name
                                       })
                    competition.parent = parent_competition
                    competition.save()

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
                                if item.companys.all():
                                    for company in item.companys.all():
                                        yeka_businessblog.companys.add(company)
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
        name = general_methods.yekaname(yeka.business)
        competitions = YekaCompetition.objects.filter(parent=yeka, isDeleted=False)
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

        for blok in yekabusinessbloks:
            bloc_dict = {}
            dict = {}
            bloc_dict['yekabusinessblog'] = blok
            bloc_dict['businessblog'] = blok.businessblog.uuid
            bloc_dict['yeka'] = yeka.uuid

            html = ''
            for param in blok.paremetre.all():
                if param.parametre.type == 'file':
                    html += '<div class="form-group"> <label>' + param.parametre.title + ' :</label> <a href="' + MEDIA_URL + param.file.name + '" target="_blank">' + param.file.name + '</div>'
                else:
                    html += '<div class="form-group"> <label>' + param.parametre.title + ' :</label>' + str(
                        param.value) + '</div>'
            bloc_dict['html'] = html
            blocks.append(bloc_dict)

        employees = YekaCompetitionPersonService(request, employe_filter)

        return render(request, 'Yeka/yeka_competition_detail.html',
                      {'urls': urls, 'current_url': current_url,
                       'url_name': url_name, 'name': name, 'bloks': blocks, 'definition': definiton_yeka,
                       'yeka': yeka, 'yekabusinessbloks': yekabusinessbloks,
                       'employees': employees, 'competitions': competitions, 'region': region

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
                      {'urls': urls, 'current_url': current_url,
                       'url_name': url_name, 'name': name, 'bloks': blocks,
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
