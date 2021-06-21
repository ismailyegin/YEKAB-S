from datetime import datetime

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
# from rest_framework_simplejwt import views as jwt_views
from django.http import JsonResponse
from django.shortcuts import render, redirect


from ekabis.services import general_methods
from ekabis.models.ActiveGroup import ActiveGroup


from ekabis.models.Logs import Logs


@login_required
def return_directory_dashboard(request):
    perm = general_methods.control_access(request)
    # x = general_methods.import_csv()

    if not perm:
        logout(request)
        return redirect('accounts:login')



    return render(request, 'anasayfa/federasyon.html',
                  {


                  })



@login_required
def return_personel_dashboard(request):
    active = general_methods.controlGroup(request)
    perm = general_methods.control_access_personel(request)


    if not perm:
        logout(request)
        return redirect('accounts:login')

    login_user = request.user
    user = User.objects.get(pk=login_user.pk)

    return render(request, 'anasayfa/personel.html',
                  {})


@login_required
def return_admin_dashboard(request):
    perm = general_methods.control_access(request)
    # x = general_methods.import_csv()

    if not perm:
        logout(request)
        return redirect('accounts:login')

    # son eklenen 8 sporcuyu ekledik


    return render(request, 'anasayfa/admin.html',
                  {


                  })

@login_required
def activeGroup(request, pk):
    userActive = ActiveGroup.objects.get(user=request.user)
    group = Group.objects.get(pk=pk)
    userActive.group = group
    userActive.save()
    if group.name == "Admin":
        return redirect('ekabis:admin')

    elif group.name == 'Yonetim':
        return redirect('ekabis:federasyon')
    elif group.name == 'Personel':
        return redirect('ekabis:personel')
    else:
        return {}
