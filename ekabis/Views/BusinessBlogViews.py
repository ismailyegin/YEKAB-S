import traceback

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import resolve

from ekabis.Forms.BusinessBlogForm import BusinessBlogForm
from ekabis.Forms.BusinessBlogParametreForm import BusinessBlogParametreForm
from ekabis.Forms.YekaBusinessForm import YekaBusinessForm
from ekabis.models import Permission
from ekabis.models.BusinessBlog import BusinessBlog
from ekabis.models.BusinessBlogParametreType import BusinessBlogParametreType
from ekabis.models.YekaBusinessBlog import YekaBusinessBlog
from ekabis.models.Yeka import Yeka
from ekabis.models.YekaBussiness import YekaBusiness
from ekabis.services import general_methods
from ekabis.services.general_methods import get_error_messages
from ekabis.services.services import YekaBusinessGetService, last_urls


@login_required
def add_yekabusiness(request, uuid):
    business = BusinessBlog.objects.filter(isDeleted=False)
    yeka = Yeka.objects.get(uuid=uuid)
    form = YekaBusinessForm()
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        if request.method == 'POST':
            with transaction.atomic():
                form = YekaBusinessForm(request.POST)
                if form.is_valid():
                    yekabusiness = form.save(request, commit=False)
                    yekabusiness.save()
                    yeka.business = yekabusiness
                    yeka.save()
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
                                parent = blog
                            yekabusiness.businessblogs.add(blog)
                            yekabusiness.save()
                            log = str(blog.businessblog.name) + " İş bloğu " + yeka.definition + " eklendi. "
                            log = general_methods.logwrite(request, request.user, log)

                        return redirect('ekabis:view_yeka_detail', uuid)
                else:
                    error_messages = get_error_messages(form)
                    return render(request, 'Yeka/yekabusinessAdd.html', {'business_form': form,
                                                                         'error_messages': error_messages, 'urls': urls,
                                                                         'current_url': current_url,
                                                                         'url_name': url_name, 'yeka': yeka,
                                                                         })

        return render(request, 'Yeka/yekabusinessAdd.html', {'business': business,
                                                             'yekabusiness_form': form,
                                                             'error_messages': '', 'urls': urls,
                                                             'current_url': current_url, 'url_name': url_name,
                                                             'yeka': yeka,
                                                             })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yekabusiness')


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
                log = str(obj.pk) + " İş bloğu parametresi silindi"
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

                if not general_methods.fixed_block_control(request, obj.name):
                    log = str(obj.pk) + " İş bloğu  silindi"
                    log = general_methods.logwrite(request, request.user, log)
                    obj.isDeleted = True
                    obj.save()
                    return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
                else:
                    return JsonResponse({'status': 'Fail', 'msg': 'Sabit  Blok Oldugu için Silinemez'})



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
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        if request.method == 'POST':
            with transaction.atomic():
                business_form = BusinessBlogParametreForm(request.POST)

                if business_form.is_valid():

                    businessparametre = business_form.save(request, commit=False)
                    businessparametre.save()

                    business = BusinessBlog.objects.get(uuid=uuid)
                    business.parametre.add(businessparametre)
                    business.save()

                    messages.success(request, 'Parametre Başarıyla  Eklenmiştir.')
                    return redirect('ekabis:change_businessBlog', business.uuid)
                else:
                    error_messages = get_error_messages(business_form)
                    return render(request, 'Yeka/parametreAdd.html', {'business_form': business_form,
                                                                      'error_messages': error_messages, 'urls': urls,
                                                                      'current_url': current_url, 'url_name': url_name
                                                                      })

        return render(request, 'Yeka/parametreAdd.html', {'business_form': business_form,
                                                          'error_messages': '', 'urls': urls,
                                                          'current_url': current_url, 'url_name': url_name
                                                          })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_businessBlog')


@login_required
def view_businessBlog(request):
    business_blog = BusinessBlog.objects.filter(isDeleted=False)
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)
    return render(request, 'Yeka/businessBlogList.html',
                  {'business_blog': business_blog, 'urls': urls, 'current_url': current_url, 'url_name': url_name})


@login_required
def add_businessBlog(request):
    business_form = BusinessBlogForm()
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        if request.method == 'POST':
            with transaction.atomic():
                business_form = BusinessBlogForm(request.POST)

                if business_form.is_valid():
                    business = business_form.save(request, commit=False)
                    business.save()
                    messages.success(request, 'İş  Blogu  Eklenmiştir.')
                    return redirect('ekabis:view_businessBlog')
                else:
                    error_messages = get_error_messages(business_form)
                    return render(request, 'Yeka/businessBlogAdd.html', {'business_form': business_form,
                                                                         'error_messages': error_messages, 'urls': urls,
                                                                         'current_url': current_url,
                                                                         'url_name': url_name
                                                                         })

        return render(request, 'Yeka/businessBlogAdd.html', {'business_form': business_form,
                                                             'error_messages': '', 'urls': urls,
                                                             'current_url': current_url, 'url_name': url_name
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
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        if request.method == 'POST':
            with transaction.atomic():
                if business_form.is_valid():
                    if not general_methods.fixed_block_control(request, BusinessBlog.objects.get(uuid=uuid).name):
                        business = business_form.save(request, commit=False)
                        business.save()
                        messages.success(request, 'İş  bloğu  güncellenmiştir.')
                        return redirect('ekabis:view_businessBlog')
                    else:
                        business = business_form.save(request, commit=False)
                        if BusinessBlog.objects.get(uuid=uuid).name != business_form.data['name']:
                            messages.warning(request, 'İş  bloğu  sabit olduğu için tanımı güncellenemez.')
                            business.name = BusinessBlog.objects.get(uuid=uuid).name
                            business.save()
                        else:
                            business.save()
                            messages.success(request, 'İş  bloğu  güncellenmiştir.')
                            return redirect('ekabis:view_businessBlog')



                else:
                    error_messages = get_error_messages(business_form)
                    return render(request, 'Yeka/businessBlogUpdate.html', {'business_form': business_form,
                                                                            'error_messages': error_messages,
                                                                            'business': business,
                                                                            'parametre': parametre, 'urls': urls,
                                                                            'current_url': current_url,
                                                                            'url_name': url_name
                                                                            })
        return render(request, 'Yeka/businessBlogUpdate.html', {'business_form': business_form,
                                                                'error_messages': '',
                                                                'business': business,
                                                                'parametre': parametre, 'urls': urls,
                                                                'current_url': current_url, 'url_name': url_name
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
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        if request.method == 'POST':
            with transaction.atomic():
                if business_form.is_valid():
                    businessparametre = business_form.save(request, commit=False)
                    businessparametre.save()
                    messages.success(request, 'Parametre  güncellenmiştir.')

                    business = BusinessBlog.objects.get(uuid=uuid)
                    return redirect('ekabis:change_businessBlog', business.uuid)
                else:
                    error_messages = get_error_messages(business_form)
                    return render(request, 'Yeka/parametreUpdate.html', {'business_form': business_form,
                                                                         'error_messages': error_messages, 'urls': urls,
                                                                         'current_url': current_url,
                                                                         'url_name': url_name
                                                                         })
        return render(request, 'Yeka/parametreUpdate.html', {'business_form': business_form,
                                                             'error_messages': '', 'urls': urls,
                                                             'current_url': current_url, 'url_name': url_name
                                                             })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_businessBlog')


@login_required
def change_yekabusiness(request, uuid, yeka):
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
                        removeBusiness =business.exclude(businessblog__id__in=blogs)
                        for i in removeBusiness:
                            i.isDeleted = True
                            i.save()

                    # olmayanı ekle sıralması degileni kaydet
                    for i in range(len(blogs)):

                        # is blogu varsa
                        if yekabusiness.businessblogs.filter(businessblog_id=blogs[i]):
                            if i == 0:
                                blog = yekabusiness.businessblogs.filter(businessblog_id=blogs[i])[0]
                                if  blog.isDeleted:
                                    blog.isDeleted=False
                                blog.parent = None
                                blog.sorting = i + 1
                                blog.save()
                                parent = blog

                            else:

                                blog = yekabusiness.businessblogs.filter(businessblog_id=blogs[i])[0]
                                if  blog.isDeleted:
                                    blog.isDeleted=False
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
                return redirect('ekabis:view_yeka_detail', yeka)

        return render(request, 'Yeka/YekabusinessUpdate.html', {'business_form': business_form,
                                                                'error_messages': '',
                                                                'unbusiness': unbusiness,
                                                                'business': business, 'urls': urls,
                                                                'current_url': current_url, 'url_name': url_name
                                                                })

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yekabusiness')


@login_required
def delete_yekabusiness(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']

                obj = YekaBusiness.objects.get(uuid=uuid)
                #
                log = str(obj.pk) + " yeka  iş bloğu  silindi"
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
