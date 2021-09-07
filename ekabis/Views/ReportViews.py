import datetime
import traceback

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, Http404, HttpResponse, FileResponse
from django.shortcuts import redirect, render
from django.urls import resolve

from ekabis.models import City
from ekabis.services.general_methods import control_access
from ekabis.services.services import last_urls


from ekabis.models.Permission import Permission

@login_required()
def view_report(request):
    perm = control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:

        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)

        city=City.objects.all()



        return render(request, 'Report/reportList.html',
                      {'urls': urls, 'current_url': current_url,
                       'url_name': url_name,'city':city

                       })

    except Exception as e:

        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')