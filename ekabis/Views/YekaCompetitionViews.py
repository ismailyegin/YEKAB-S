import traceback

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from ekabis.Forms.ConnectionRegionForm import ConnectionRegionForm
from ekabis.Forms.YekaBusinessBlogForm import YekaBusinessBlogForm
from ekabis.Forms.YekaBusinessForm import YekaBusinessForm
from ekabis.Forms.YekaCompetitionForm import YekaCompetitionForm
from ekabis.Forms.YekaForm import YekaForm
from ekabis.models import YekaCompetition, YekaBusiness, YekaBusinessBlog, BusinessBlog, Employee, YekaPerson, \
    YekaPersonHistory
from ekabis.models.YekaCompetitionPerson import YekaCompetitionPerson
from ekabis.models.YekaCompetitionPersonHistory import YekaCompetitionPersonHistory
from ekabis.services import general_methods
from ekabis.services.general_methods import get_error_messages
from ekabis.services.services import YekaGetService, ConnectionRegionGetService, YekaCompetitionGetService, \
    YekaBusinessGetService, YekaBusinessBlogGetService, BusinessBlogGetService, YekaCompetitionPersonService, \
    EmployeeGetService
import  datetime
from django.db.models import Sum
@login_required
def view_competition(request,uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    yeka_form = YekaForm()

    try:
        with transaction.atomic():
            return render(request, 'Competition/view_competition.html',
                          {'yeka_form': yeka_form, 'error_messages': '', })

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')




@login_required
def add_competition(request,region):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    competition_form = YekaCompetitionForm()

    try:

        region_filter={
            'uuid' :region,
            'isDeleted' : False,
        }
        region=ConnectionRegionGetService(request,region_filter)
        with transaction.atomic():

            if request.method == 'POST':

                competition_form = YekaCompetitionForm(request.POST)

                if competition_form.is_valid():

                    competition = competition_form.save(commit=False)

                    total = int(
                        YekaCompetition.objects.filter(connectionregion=region).distinct().aggregate(Sum('capacity'))[
                            'capacity__sum'] or 0)
                    total +=competition.capacity

                    if total>region.capacity:
                        messages.warning(request, 'Yeka Yarışmalarının toplam Kapasitesi Bölgeden Büyük Olamaz')
                        return render(request, 'Competition/add_competition.html',
                                      {'competition_form': competition_form, 'region': region,
                                       })



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
                            for item in yeka.business.businessblogs.all().order_by('sorting'):

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
                            competition.business=yeka_business
                            competition.save()
                    log = " Yeka Yarışması  eklendi"
                    log = general_methods.logwrite(request, request.user, log)
                    messages.success(request, 'Yeka Yarışması Kayıt Edilmiştir.')
                    return redirect('ekabis:add_competition' ,region.uuid)

                else:
                    error_message_region = get_error_messages(competition_form)

                    return render(request, 'Competition/add_competition.html',
                                  {'competition_form': competition_form, 'region':region, 'error_messages': error_message_region})

            competitions = region.yekacompetition.filter(isDeleted=False)
            return render(request, 'Competition/add_competition.html',
                          {'competition_form': competition_form, 'competitions': competitions, 'error_messages': '', 'region':region})

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
                regionfilter = {
                    'uuid': uuid
                }
                obj = ConnectionRegionGetService(request, regionfilter)
                # not: Silme işleminde kontrol yapılacak yarışma var mı şimdi yarışma alanını yazmadıgım için kontrol edemiyorum
                region_capacities = YekaCompetition.objects.filter(isDeleted=False)
                if region_capacities:
                    return JsonResponse(
                        {'status': 'Fail', 'msg': 'Bölge için tanımlanmış yarışmalar  var. Bölge silinemez'})
                else:
                    log = str(obj.name) + "Bölge silindi"
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
def update_competition(request, uuid,yeka):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        regionfilter = {
            'uuid': uuid,
            'isDeleted': False
        }
        yeka_filter={
            'uuid':yeka,
            'isDeleted': False

        }
        yeka=YekaGetService(request,yeka_filter)
        region = ConnectionRegionGetService(request, regionfilter)
        region_form = ConnectionRegionForm(request.POST or None, instance=region)
        with transaction.atomic():
            if request.method == 'POST':

                if region_form.is_valid():
                    region.name = region_form.cleaned_data['name']
                    region.value = region_form.cleaned_data['value']



                    region.save()

                    messages.success(request, 'Bölge Başarıyla Güncellendi')
                    return redirect('ekabis:add_region' ,yeka.uuid)
                else:
                    error_message_unit = get_error_messages(region_form)
                    return render(request, 'Competition/change_competition.html',
                                  {'region_form': region_form, 'error_messages': error_message_unit, 'units': ''})

            return render(request, 'Competition/change_competition.html',
                          {'region_form': region_form, 'error_messages': '', 'units': ''})
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')


@login_required()
def view_competition_yekabusinessBlog(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        competition_filter = {
            'uuid': uuid
        }
        competition = YekaCompetitionGetService(request, competition_filter)

        # url = general_methods.yeka_control(request, yeka)
        # if url and url != 'view_yekabusinessBlog':
        #     return redirect('ekabis:' + url, yeka.uuid)
        # yekabusinessbloks = None
        #
        # extratime_filter = {
        #     'yeka': yeka
        # }
        # ekstratimes = ExtraTimeService(request, extratime_filter)


        if competition.business:
            yekabusiness = competition.business
            yekabusinessbloks = yekabusiness.businessblogs.filter(isDeleted=False).order_by('sorting')
        else:
            yekabusiness = None
            yekabusinessbloks = None

        return render(request, 'Competition/timeline.html',
                      {'yekabusinessbloks': yekabusinessbloks,
                       'competition': competition,
                       'ekstratimes': None
                       })

    except Exception as e:

        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')

@login_required
def add_yekacompetitionbusiness(request,uuid):
    business = BusinessBlog.objects.filter(isDeleted=False)
    competition=YekaCompetition.objects.get(uuid=uuid)
    try:
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
                                                    sorting=i + 1
                                                    )
                            blog.save()
                            parent = blog
                        yekabusiness.businessblogs.add(blog)
                        yekabusiness.save()

                    return redirect('ekabis:view_competitionbusinessblog',competition.uuid)



        return render(request, 'Competition/competition_businessblog_Add.html', {'business': business,

                                                             'error_messages': '',
                                                             })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yekabusiness')


@login_required
def change_yekacompetitionbusiness(request, uuid,competition):



    try:
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

                if business_form.is_valid():
                    yekabu = business_form.save(commit=False)
                    yekabu.save()
                    if request.POST.get('businessblog'):

                        blogs = request.POST.get('businessblog').split("-")
                        parent = None
                        blog = None
                        # olmayanları sil
                        if business:
                            removeBusiness = business.exclude(isDeleted=False , id__in=blogs)
                            for i in removeBusiness:
                                i.isDeleted = True
                                i.save()


                        # olmayanı ekle sıralması degileni kaydet
                        for i in range(len(blogs)):


                            # is blogu varsa
                            if yekabusiness.businessblogs.filter(isDeleted=False, pk=blogs[i]):
                                if i == 0:
                                    blog = yekabusiness.businessblogs.get(isDeleted=False, pk=blogs[i])
                                    blog.parent = None
                                    blog.sorting=i+1
                                    blog.save()
                                    parent = blog

                                else:
                                    blog = yekabusiness.businessblogs.get(isDeleted=False, pk=blogs[i])
                                    blog.parent = parent
                                    blog.sorting=i+1
                                    blog.save()
                                    parent = blog
                            # is blogu yoksa
                            else:
                                if i == 0:
                                    blog = YekaBusinessBlog(businessblog=BusinessBlog.objects.get(pk=blogs[i]),
                                                            sorting=i+1)
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


                    return redirect('ekabis:view_competitionbusinessblog',competition)
                else:
                    error_messages = get_error_messages(business_form)

                    return render(request, 'Competition/competition_businessblog_change.html', {'business_form': business_form,
                                                                            'error_messages': error_messages,
                                                                            'unbusiness': unbusiness,
                                                                            'business': business
                                                                            })

        return render(request, 'Competition/competition_businessblog_change.html', {'business_form': business_form,
                                                                'error_messages': '',
                                                                'unbusiness': unbusiness,
                                                                'business': business
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
                return redirect('ekabis:view_competitionbusinessblog',competition.uuid)
        return render(request, 'Yeka/YekabussinesBlogUpdate.html',
                      {
                          'yekaBusinessBlogo_form': yekaBusinessBlogo_form,
                          'competition': competition
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
        'is_active':True
    }

    yeka_person = YekaCompetitionPersonService(request,yekacompetition_person_filter).order_by('-creationDate')
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
                        person_yeka = YekaCompetitionPerson(competition=competition, employee=person, is_active=True)
                        person_yeka.save()

                        personHistory = YekaCompetitionPersonHistory(competition=competition, person=person, is_active=True)
                        personHistory.save()

                        log = str(competition.name) + ' adlı yekaya - ' + str(
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
                        yeka_person = YekaCompetitionPerson.objects.get(
                            Q(isDeleted=False) & Q(competition__uuid=uuid) & Q(employee__uuid=person.uuid))

                        yeka_person.isDeleted = True
                        yeka_person.is_active = False
                        yeka_person.save()

                        personHistory = YekaCompetitionPersonHistory(competition=yeka_person.competition, person=person, is_active=False)
                        personHistory.save()

                        log = str(yeka_person.competition.name) + ' adlı yekadan -' + str(
                            person.user.get_full_name()) + " personeli çıkarıldı."
                        log = general_methods.logwrite(request, request.user, log)


        return redirect('ekabis:view_yekacompetition_personel', uuid)

    return render(request, 'Yeka/yekaPersonList.html',
                  {'persons': persons, 'yeka_persons': yeka_person, 'yeka_uuid': uuid})

