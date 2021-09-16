import traceback
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import resolve
from ekabis.Forms.PermissionForm import PermissionForm
from ekabis.models import Permission
from ekabis.services import general_methods
from ekabis.services.general_methods import get_error_messages
from ekabis.services.services import last_urls


import inspect
from ekabis.Views import  AdminViews,CompanyView, EmployeeViews, GroupView, ConnectionRegionViews, YekaViews, BusinessBlogViews,YekaCompetitionViews, VacationDayViews,FactoryViews, \
    YekaBussinessBlogStaticView



@login_required
def view_permission(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)

        permissions=Permission.objects.all()
        return render(request, 'Permission/view_permission.html', {'permissions':permissions,'urls': urls, 'current_url': current_url, 'url_name': url_name})
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')

@login_required
def change_permission(request,uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:

        permission=Permission.objects.get(uuid=uuid)
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        permission_form=PermissionForm(request.POST or None,instance=permission)
        # Bu alan sistem çalışmasından sonra silinecegi icin kod düzenlemsinde cast edilmesinde önem verilmedi
        urls = []
        from ekabis.urls import urlpatterns
        for urlpattern in urlpatterns:
            if urlpattern.name==permission.codename:
                view_url=urlpattern.lookup_str
        url=view_url.split('.')

        code=change_permission
        if url[0]=='ekabis':
            if url[2]=='AdminViews':
                result = getattr(AdminViews,url[3])
                code = inspect.getsource(result)
            elif url[2]=='CompanyView':
                result = getattr(CompanyView,url[3])
                code = inspect.getsource(result)
            elif url[2]=='EmployeeViews':
                result = getattr(EmployeeViews,url[3])
                code = inspect.getsource(result)
            elif url[2]=='YekaViews':
                result = getattr(YekaViews,url[3])
                code = inspect.getsource(result)
            elif url[2]=='BusinessBlogViews':
                result = getattr(BusinessBlogViews,url[3])
                code = inspect.getsource(result)
            elif url[2]=='YekaBussinessBlogStaticView':
                result = getattr(YekaBussinessBlogStaticView,url[3])
                code = inspect.getsource(result)
            elif url[2]=='YekaCompetitionViews':
                result = getattr(YekaCompetitionViews,url[3])
                code = inspect.getsource(result)
            elif url[2] == 'ConnectionRegionViews':
                result = getattr(ConnectionRegionViews, url[3])
                code = inspect.getsource(result)
            elif url[2]=='GroupView':
                result = getattr(GroupView,url[3])
                code = inspect.getsource(result)
            elif url[2] == 'VacationDayViews':
                result = getattr(VacationDayViews, url[3])
                code = inspect.getsource(result)
            elif url[2] == 'FactoryViews':
                result = getattr(FactoryViews, url[3])
                code = inspect.getsource(result)

        with transaction.atomic():
            if request.method == 'POST':
                if permission_form.is_valid():
                    perm=permission_form.save(request,commit=False)
                    perm.save()
                    messages.success(request, 'İzin Güncellenmiştir.')
                    return redirect('ekabis:view_permission')
                else:
                    error_messages = get_error_messages(permission_form)
                    return render(request, 'Permission/change_permission.html',
                                  {
                                   'urls': urls,
                                   'current_url': current_url,
                                   'url_name': url_name,
                                   'error_messages': error_messages,
                                   'permission_form':permission_form,
                                      'code':code
                                   })
            return render(request, 'Permission/change_permission.html',
                          { 'urls': urls,
                           'current_url': current_url, 'url_name': url_name,
                           'permission_form':permission_form,
                            'code': code
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')