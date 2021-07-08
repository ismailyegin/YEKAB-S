import traceback

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction

from django.http import JsonResponse
from django.shortcuts import render, redirect
from ekabis.services import general_methods
from ekabis.services.general_methods import get_error_messages

# form
from ekabis.Forms.BusinessBlogForm import BusinessBlogForm
from ekabis.Forms.BusinessBlogParametreForm import BusinessBlogParametreForm

# model
from ekabis.models.BusinessBlog import BusinessBlog
from ekabis.models.BusinessBlogParametreType import BusinessBlogParametreType

from ekabis.models.YekaBusinessBlog import YekaBusinessBlog
from ekabis.models.YekaBussiness import YekaBusiness


@login_required
def view_businessBlog(request):
    business_blog = BusinessBlog.objects.filter(isDeleted=False)
    return render(request, 'Yeka/businessBlogList.html', {'business_blog': business_blog})


@login_required
def add_businessBlog(request):
    business_form = BusinessBlogForm()
    try:
        if request.method == 'POST':
            with transaction.atomic():
                business_form = BusinessBlogForm(request.POST)

                if business_form.is_valid():
                    business = business_form.save(commit=False)
                    business.save()
                    messages.success(request, 'is  Blogu  Eklenmiştir.')
                    log = str(business.name) + "'is  Blogu  Eklenmiştir."
                    log = general_methods.logwrite(request, request.user, log)
                    return redirect('ekabis:view_businessBlog')
                else:
                    error_messages = get_error_messages(business_form)
                    return render(request, 'Yeka/businessBlogAdd.html', {'business_form': business_form,
                                                                         'error_messages': error_messages,
                                                                         })

        return render(request, 'Yeka/businessBlogAdd.html', {'business_form': business_form,
                                                             'error_messages': '',
                                                             })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_businessBlog')


@login_required
def change_businessBlog(request, uuid):
    business = BusinessBlog.objects.get(uuid=uuid)
    business_form = BusinessBlogForm(request.POST or None, instance=business)
    parametre=business.parametre.filter(isDeleted=False)
    try:
        if request.method == 'POST':
            with transaction.atomic():
                if business_form.is_valid():
                    business = business_form.save(commit=False)
                    business.save()
                    messages.success(request, 'iş  Blogu  güncellenmiştir.')
                    log = str(business.name) + "'is  Blogu  güncellenmiştir."
                    log = general_methods.logwrite(request, request.user, log)
                    return redirect('ekabis:view_businessBlog')
                else:
                    error_messages = get_error_messages(business_form)
                    return render(request, 'Yeka/businessBlogUpdate.html', {'business_form': business_form,
                                                                            'error_messages': error_messages,
                                                                            'business': business,
                                                                            'parametre':parametre
                                                                            })

        return render(request, 'Yeka/businessBlogUpdate.html', {'business_form': business_form,
                                                                'error_messages': '',
                                                                'business': business,
                                                                 'parametre':parametre
                                                                })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_businessBlog')


@login_required
def delete_businessBlog(request):
=======
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render

from ekabis.Forms.YekaForm import YekaForm
from ekabis.models.Yeka import Yeka
from ekabis.models.Company import Company
from ekabis.services import general_methods
from ekabis.services.general_methods import get_error_messages
from ekabis.services.services import YekaService


@login_required
def return_yeka(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    yeka_form = YekaForm()
    parent_yekalar = Yeka.objects.filter(Q(isDeleted=False) & Q(yekaParent=None))
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

                    for employee in yeka_form.cleaned_data['employee']:
                        yeka.employee.add(employee)
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
                    return render(request, 'Yeka/view_yeka.html',
                                  {'yeka_form': yeka_form, 'error_messages': error_message_unit,
                                   'parent_yekalar': parent_yekalar, 'companies': companies,
                                   })

            return render(request, 'Yeka/view_yeka.html',
                          {'yeka_form': yeka_form, 'error_messages': '',
                           'parent_yekalar': parent_yekalar, 'companies': companies,
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


                obj = BusinessBlog.objects.get(uuid=uuid)
                #
                log = str(obj.pk) + " iş blogu  silindi"
                log = general_methods.logwrite(request, request.user, log)
                obj.isDeleted = True
                obj.save()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except Exception as e:

        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')

        return redirect('ekabis:view_businessBlog')


@login_required
def add_businessBlogParametre(request,uuid):

    business_form = BusinessBlogParametreForm()
    try:

        if request.method == 'POST':
            with transaction.atomic():
                business_form = BusinessBlogParametreForm(request.POST)

                if business_form.is_valid():

                    businessparametre = business_form.save(commit=False)
                    businessparametre.save()

                    business = BusinessBlog.objects.get(uuid=uuid)
                    business.parametre.add(businessparametre)
                    business.save()

                    messages.success(request, 'Parametre Başarıyla  Eklenmiştir.')
                    log = str(business.name) + "parametre  Eklenmiştir."
                    log = general_methods.logwrite(request, request.user, log)
                    return redirect('ekabis:change_businessBlog', business.uuid)
                else:
                    error_messages = get_error_messages(business_form)
                    return render(request, 'Yeka/parametreAdd.html', {'business_form': business_form,
                                                                         'error_messages': error_messages,
                                                                         })

        return render(request, 'Yeka/parametreAdd.html', {'business_form': business_form,
                                                             'error_messages': '',
                                                             })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_businessBlog')


@login_required
def change_businessBlogParametre(request, uuid,uuidparametre):
    parametre=BusinessBlogParametreType.objects.get(uuid=uuidparametre)
    business_form = BusinessBlogParametreForm(request.POST or None, instance=parametre)
    try:
        if request.method == 'POST':
            with transaction.atomic():
                if business_form.is_valid():
                    businessparametre = business_form.save(commit=False)
                    businessparametre.save()
                    messages.success(request, 'Parametre  güncellenmiştir.')
                    log = str(businessparametre.title) + "'Paremetre  güncellenmiştir."
                    log = general_methods.logwrite(request, request.user, log)
                    business = BusinessBlog.objects.get(uuid=uuid)
                    return redirect('ekabis:change_businessBlog',business.uuid)
                else:
                    error_messages = get_error_messages(business_form)
                    return render(request, 'Yeka/parametreUpdate.html', {'business_form': business_form,
                                                                            'error_messages': error_messages,
                                                                            })
        return render(request, 'Yeka/parametreUpdate.html', {'business_form': business_form,
                                                                'error_messages': '',
                                                                })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_businessBlog')


@login_required
def delete_businessBlogParametre(request):

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
    alt_yekalar = Yeka.objects.filter(isDeleted=False, yekaParent__uuid=uuid)
    try:
        with transaction.atomic():
            if request.method == 'POST':

                if yeka_form.is_valid():

                    form_capacity = int(yeka_form.cleaned_data['capacity'])

                    total_capacity = 0

                    if alt_yekalar:
                        for yeka in alt_yekalar:
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
                                  {'yeka_form': yeka_form, 'error_messages': error_message_unit,
                                   })

            return render(request, 'Yeka/change_yeka.html',
                          {'yeka_form': yeka_form, 'error_messages': '',
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


@login_required
def alt_yeka_ekle(request, uuid):

    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']

                obj = BusinessBlogParametreType.objects.get(uuid=uuid)
                #
                log = str(obj.pk) + " Parametre silindi"
                log = general_methods.logwrite(request, request.user, log)
                obj.isDeleted = True
                obj.save()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except Exception as e:

        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_businessBlog')




@login_required
def add_yekabusiness(request):
    business=BusinessBlog.objects.filter(isDeleted=False)
    try:
        if request.method == 'POST':
            with transaction.atomic():
                pass

        return render(request, 'Yeka/yekabusinessAdd.html', {'business': business, })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_businessBlog')

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
                    return redirect('ekabis:view_yeka')

                else:
                    error_message_unit = get_error_messages(yeka_form)
                    return render(request, 'Yeka/add_sub_yeka.html',
                                  {'yeka_form': yeka_form, 'error_messages': error_message_unit,
                                   'alt_yekalar': alt_yekalar
                                   })

            return render(request, 'Yeka/add_sub_yeka.html',
                          {'yeka_form': yeka_form, 'error_messages': '', 'alt_yekalar': alt_yekalar
                           })

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')

