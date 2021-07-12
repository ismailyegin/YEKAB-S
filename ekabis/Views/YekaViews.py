import traceback

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from ekabis.Forms.YekaForm import YekaForm
from ekabis.models import YekaPerson, Employee
from ekabis.models.YekaPersonHistory import YekaPersonHistory
from ekabis.models.Yeka import Yeka
from ekabis.models.Company import Company
from ekabis.services import general_methods
from ekabis.services.general_methods import get_error_messages
from ekabis.services.services import YekaService

from ekabis.models.YekaBusinessBlog import YekaBusinessBlog
from ekabis.Forms.YekaBusinessBlogForm import YekaBusinessBlogForm
from ekabis.models.BusinessBlog import BusinessBlog

@login_required
def add_yeka(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    yeka_form = YekaForm()
    companies = Company.objects.filter(isDeleted=False)
    try:
        with transaction.atomic():
            if request.method == 'POST':
                yeka_form = YekaForm(request.POST)
                if yeka_form.is_valid():
                    yeka = Yeka(definition=yeka_form.cleaned_data['definition'], date=yeka_form.cleaned_data['date'],
                                unit=yeka_form.cleaned_data['unit'], capacity=yeka_form.cleaned_data['capacity']
                                )
                    yeka.save()
                    for company in yeka_form.cleaned_data['company']:
                        yeka.company.add(company)
                    yeka.save()

                    log = " Yeka eklendi"
                    log = general_methods.logwrite(request, request.user, log)
                    messages.success(request, 'Yeka Başarıyla Kayıt Edilmiştir.')
                    return redirect('ekabis:view_yeka')

                else:
                    error_message_unit = get_error_messages(yeka_form)
                    yekafilter = {
                        'isDeleted': False,
                        'yekaParent': None
                    }
                    parent_yekalar = YekaService(request, yekafilter)
                    return render(request, 'Yeka/yekaAdd.html',
                                  {'yeka_form': yeka_form, 'error_messages': error_message_unit,
                                    'companies': companies,
                                   })

            return render(request, 'Yeka/yekaAdd.html',
                          {'yeka_form': yeka_form, 'error_messages': '',
                            'companies': companies,
                           })

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required
def view_yeka(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')


    try:
        parent_yekalar=Yeka.objects.filter(isDeleted=False , yekaParent=None)
        with transaction.atomic():
            if request.method == 'POST':
                pass
            return render(request, 'Yeka/view_yeka.html',
                          {
                              'parent_yekalar':parent_yekalar
                           })

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
                parent = Yeka.objects.filter(Q(isDeleted=False) & Q(yekaParent__uuid=obj.uuid))
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

    yeka = Yeka.objects.get(uuid=uuid)
    yeka_form = YekaForm(request.POST or None, instance=yeka)
    sub_yeka = Yeka.objects.filter(isDeleted=False, yekaParent__uuid=uuid)


    try:
        with transaction.atomic():
            if request.method == 'POST':

                if yeka_form.is_valid():

                    form_capacity = int(yeka_form.cleaned_data['capacity'])

                    total_capacity = 0

                    if sub_yeka:
                        for yeka in sub_yeka:
                            total_capacity = total_capacity + yeka.capacity

                    if form_capacity >= total_capacity:
                        yeka.definition = yeka_form.cleaned_data['definition']
                        yeka.date = yeka_form.cleaned_data['date']
                        yeka.unit = yeka_form.cleaned_data['unit']
                        yeka.capacity = int(yeka_form.cleaned_data['capacity'])
                        yeka.save()

                        yeka.company.clear()
                        for company in yeka_form.cleaned_data['company']:
                            yeka.company.add(company)

                        yeka.employee.clear()
                        for employee in yeka_form.cleaned_data['employee']:
                            yeka.employee.add(employee)

                    else:
                        messages.warning(request, 'Yeka Kapasitesi Alt Yekaların Toplam Kapasitesinden Küçük Olamaz.')
                        return redirect('ekabis:change_yeka', uuid)

                    messages.success(request, 'Yeka Başarıyla Güncellendi')
                    return redirect('ekabis:view_yeka')
                else:
                    error_message_unit = get_error_messages(yeka_form)
                    return render(request, 'Yeka/change_yeka.html',
                                  {'yeka_form': yeka_form,
                                   'error_messages': error_message_unit,
                                   'yeka':yeka,
                                   'sub_yeka':sub_yeka
                                   })

            return render(request, 'Yeka/change_yeka.html',
                          {'yeka_form': yeka_form,
                           'error_messages': '',
                           'yeka': yeka,
                           'sub_yeka': sub_yeka,
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required
def alt_yeka_ekle(request, uuid):
    yeka_form = YekaForm()
    yeka = Yeka.objects.get(uuid=uuid)
    alt_yekalar = Yeka.objects.filter(yekaParent=yeka, isDeleted=False)
    try:
        with transaction.atomic():
            if request.method == 'POST':

                yeka_form = YekaForm(request.POST)

                if yeka_form.is_valid():

                    form_capacity = int(yeka_form.cleaned_data['capacity'])
                    total_capacity = 0


                    # filtre ile sum alınabilir for gerek yok
                    if alt_yekalar:

                        for yeka in alt_yekalar:
                            total_capacity = total_capacity + yeka.capacity

                    if yeka.capacity >= total_capacity + form_capacity:
                        new_yeka = Yeka(definition=yeka_form.cleaned_data['definition'],
                                        date=yeka_form.cleaned_data['date'],
                                        unit=yeka_form.cleaned_data['unit'], capacity=form_capacity
                                        )
                        new_yeka.save()
                        new_yeka.yekaParent = yeka
                        new_yeka.save()

                    else:
                        messages.warning(request, 'Alt Yekaların Toplam Kapasitesi Yeka Kapasitesinden Büyük Olamaz.')
                        return redirect('ekabis:add_sub_yeka', uuid)

                    log = "Alt Yeka eklendi"
                    log = general_methods.logwrite(request, request.user, log)
                    messages.success(request, 'Yeka Başarıyla Kayıt Edilmiştir.')
                    return redirect('ekabis:change_yeka',yeka.uuid)

                else:
                    error_message_unit = get_error_messages(yeka_form)
                    return render(request, 'Yeka/add_sub_yeka.html',
                                  {'yeka_form': yeka_form, 'error_messages': error_message_unit,
                                   'alt_yekalar': alt_yekalar
                                   })

            return render(request, 'Yeka/add_sub_yeka.html',
                          {'yeka_form': yeka_form,
                           'error_messages': '',
                           'alt_yekalar': alt_yekalar,
                           })

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required()
def view_yekabusinessBlog(request,uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        yeka=Yeka.objects.get(uuid=uuid)
        yekabusinessbloks=None
        if yeka.business:
            yekabusiness = yeka.business
            yekabusinessbloks = yekabusiness.businessblogs.filter(isDeleted=False).order_by('sorting')
        return render(request, 'Yeka/timeline.html',
                      {'yekabusinessbloks':yekabusinessbloks,
                       'yeka':yeka,
                       })

    except Exception as e:

        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')
@login_required()
def change_yekabusinessBlog(request,yeka,yekabusiness,business):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        yeka=Yeka.objects.get(uuid=yeka)
        yekabussiness=YekaBusinessBlog.objects.get(pk=yekabusiness)
        business = BusinessBlog.objects.get(pk=business)
        yekaBusinessBlogo_form=YekaBusinessBlogForm(business.pk,request.POST or None, instance=yekabussiness)
        for item in yekabussiness.paremetre.all():
            yekaBusinessBlogo_form.fields[item.parametre.title].initial = item.value
        if request.POST:
            if yekaBusinessBlogo_form.is_valid():
                yekaBusinessBlogo_form.save(yekabussiness.pk,business.pk)
                return redirect('ekabis:view_yekabusinessBlog' ,yeka.uuid)
        return render(request, 'Yeka/YekabussinesBlogUpdate.html',
                      {
                       'yekaBusinessBlogo_form':yekaBusinessBlogo_form,
                       'yeka':yeka
                       })
    except Exception as e:

        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


def yekaPerson_List(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    yeka = Yeka.objects.get(uuid=uuid)

    yeka_person = YekaPerson.objects.filter(Q(yeka=yeka) & Q(isDeleted=False))

    persons = Employee.objects.filter(Q(isDeleted=False) & Q(is_yekaPersonel=False))

    return render(request, 'Yeka/yekaPersonList.html',
                  {'persons': persons, 'yeka_persons': yeka_person, 'yeka_uuid': uuid})


def yekaPerson_assignment(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                person_uuid = request.POST['person_uuid']
                yeka_uuid = request.POST['yeka_uuid']

                yeka = Yeka.objects.get(uuid=yeka_uuid)
                person = Employee.objects.get(uuid=person_uuid)

                person_yeka = YekaPerson(yeka=yeka,
                                         employee=Employee.objects.get(uuid=person_uuid))
                person_yeka.save()

                person.is_yekaPersonel = True
                person.save()

                personHistory = YekaPersonHistory(yeka=yeka, employee=person, is_active=True)
                personHistory.save()

                log = str(yeka.definition) + '-' + str(person.user.get_full_name()) + " personeli atandı."
                log = general_methods.logwrite(request, request.user, log)

                return JsonResponse({'status': 'Success', 'msg': 'save successfully'})

            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


def yekaPerson_remove(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']
                person = Employee.objects.get(uuid=uuid)

                yeka_person = YekaPerson.objects.get(Q(uuid=request.POST['yeka_uuid']) & Q(employee__uuid=uuid))

                yeka_person.isDeleted = True
                yeka_person.save()

                person.is_yekaPersonel = False
                person.save()

                personHistory = YekaPersonHistory(yeka=yeka_person.yeka, employee=person)
                personHistory.save()

                log = str(yeka_person.yeka.definition) + '-' + str(
                    person.user.get_full_name()) + " personeli çıkarıldı."
                log = general_methods.logwrite(request, request.user, log)

                return JsonResponse({'status': 'Success', 'msg': 'save successfully'})

            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})
