import traceback

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect

from ekabis.Forms.BusinessBlogForm import BusinessBlogForm
from ekabis.Forms.BusinessBlogParametreForm import BusinessBlogParametreForm
from ekabis.models.BusinessBlog import BusinessBlog
from ekabis.models.BusinessBlogParametreType import BusinessBlogParametreType
from ekabis.services import general_methods
from ekabis.services.general_methods import get_error_messages

from ekabis.models.YekaBussiness import YekaBusiness
from ekabis.Forms.YekaBusinessForm import YekaBusinessForm
from ekabis.models.YekaBusinessBlog import YekaBusinessBlog


@login_required
def add_yekabusiness(request,):
    business = BusinessBlog.objects.filter(isDeleted=False)
    form=YekaBusinessForm()

    try:
        if request.method == 'POST':
            with transaction.atomic():
                form = YekaBusinessForm(request.POST)
                if form.is_valid():
                    yekabusiness=form.save(commit=False)
                    yekabusiness.save()
                    if request.POST.get('businessblog'):
                         blogs= request.POST.get('businessblog').split("-")
                         parent=YekaBusinessBlog.objects.none()
                         blog=None
                         for i in range(len(blogs)):
                             if i==0:
                                 blog = YekaBusinessBlog(businessblog=BusinessBlog.objects.get(pk=blogs[i]))
                                 blog.save()
                                 parent = blog

                             else:

                                 blog = YekaBusinessBlog(businessblog=BusinessBlog.objects.get(pk=blogs[i-1]),
                                                         parent=parent
                                                         )
                                 blog.save()
                                 parent = blog
                             yekabusiness.businessblogs.add(blog)
                             yekabusiness.save()




        return render(request, 'Yeka/yekabusinessAdd.html', {'business': business,
                                                             'yekabusiness_form':form})
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_businessBlog')


@login_required
def delete_businessBlogParametre(request):
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
                log = str(obj.pk) + " iş blogu parametresi silindi"
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
def delete_businessBlog(request):
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
def add_businessBlogParametre(request, uuid):
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
    parametre = business.parametre.filter(isDeleted=False)
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
                                                                            'parametre': parametre
                                                                            })
        return render(request, 'Yeka/businessBlogUpdate.html', {'business_form': business_form,
                                                                'error_messages': '',
                                                                'business': business,
                                                                'parametre': parametre
                                                                })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_businessBlog')


@login_required
def change_businessBlogParametre(request, uuid, uuidparametre):
    parametre = BusinessBlogParametreType.objects.get(uuid=uuidparametre)
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
                    return redirect('ekabis:change_businessBlog', business.uuid)
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




def view_yekabusiness(request):
    yeka_business = YekaBusiness.objects.all()
    try:
        # if request.method == 'POST':
        #     pass
        #     # with transaction.atomic():
        #
        #         # if business_form.is_valid():
        #         #     businessparametre = business_form.save(commit=False)
        #         #     businessparametre.save()
        #         #     messages.success(request, 'Parametre  güncellenmiştir.')
        #         #     log = str(businessparametre.title) + "'Paremetre  güncellenmiştir."
        #         #     log = general_methods.logwrite(request, request.user, log)
        #         #     business = BusinessBlog.objects.get(uuid=uuid)
        #         #     return redirect('ekabis:change_businessBlog', business.uuid)
        #         # else:
        #         #     error_messages = get_error_messages(business_form)
        #         #     return render(request, 'Yeka/parametreUpdate.html', {'business_form': business_form,
        #         #                                                          'error_messages': error_messages,
        #         #                                                          })
        return render(request, 'Yeka/YekabusinessList.html', {'yeka_business': yeka_business,
                                                             'error_messages': '',
                                                             })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_businessBlog')

