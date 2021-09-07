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

from ekabis.models import City, YekaBusinessBlog, YekaCompetition, BusinessBlog, Yeka, YekaBusiness, ConnectionRegion
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
        selectblog=None
        businessblogs=BusinessBlog.objects.all()

        # ön lisans sürecindekiler
        blogs=YekaBusinessBlog.objects.filter(businessblog__name='Ön Lisans Süreci')
        prelicense=[]
        for item in blogs:
            business=YekaBusiness.objects.filter(businessblogs=item)[0]
            if Yeka.objects.filter(business=business):
                yeka=Yeka.objects.get(business=business)
                beka = {
                    'name': yeka.definition,
                    'startdate': item.startDate,
                    'finishdate': item.finisDate,
                    'blogname': item.businessblog.name,
                    'capacity': yeka.capacity,
                    'type': yeka.type,
                    'firma': yeka.business.company,
                    'yeka':True,
                    'uuid':yeka.uuid,
                }
                prelicense.append(beka)

            elif YekaCompetition.objects.filter(business=business):
                yeka=YekaCompetition.objects.get(business=business)
                beka = {
                    'name': yeka.name,
                    'startdate': item.startDate,
                    'finishdate': item.finisDate,
                    'blogname': item.businessblog.name,
                    'capacicty': yeka.capacity,
                    'type': "",
                    'firma':yeka.business.company,
                    'yeka':False,
                    'uuid':yeka.uuid
                }
                prelicense.append(beka)
        # lisans sürecindekiler
        blogs=YekaBusinessBlog.objects.filter(businessblog__name='Lisans')
        license=[]
        for item in blogs:
            business=YekaBusiness.objects.filter(businessblogs=item)[0]
            if Yeka.objects.filter(business=business):
                yeka=Yeka.objects.get(business=business)
                beka = {
                    'name': yeka.definition,
                    'startdate': item.startDate,
                    'finishdate': item.finisDate,
                    'blogname': item.businessblog.name,
                    'capacity': yeka.capacity,
                    'type': yeka.type,
                    'firma': yeka.business.company,
                    'yeka':True,
                    'uuid':yeka.uuid,
                }
                license.append(beka)

            elif YekaCompetition.objects.filter(business=item.business):
                yeka=YekaCompetition.objects.get(business=item.business)
                beka = {
                    'name': yeka.name,
                    'startdate': item.startDate,
                    'finishdate': item.finisDate,
                    'blogname': item.businessblog.name,
                    'capacicty': yeka.capacity,
                    'type': "",
                    'firma':yeka.business.company,
                    'yeka':False,
                    'uuid':yeka.uuid
                }
                license.append(beka)

        if 'business'  in request.POST:
            # lisans sürecindekiler
            blogs = YekaBusinessBlog.objects.filter(businessblog__id=request.POST.get('business_type'))
            selectblog = []
            for item in blogs:
                business = YekaBusiness.objects.filter(businessblogs=item)[0]
                if Yeka.objects.filter(business=business):
                    yeka = Yeka.objects.get(business=business)
                    beka = {
                        'name': yeka.definition,
                        'startdate': item.startDate,
                        'finishdate': item.finisDate,
                        'blogname': item.businessblog.name,
                        'capacity': yeka.capacity,
                        'type': yeka.type,
                        'firma': yeka.business.company,
                        'yeka': True,
                        'uuid': yeka.uuid,
                    }
                    selectblog.append(beka)

                elif YekaCompetition.objects.filter(business=business):
                    try:
                        competition = YekaCompetition.objects.get(business=business)
                        region = ConnectionRegion.objects.get(yekacompetition=competition)
                        yeka = Yeka.objects.get(connection_region=region)
                        beka = {
                            'name': competition.name,
                            'startdate': item.startDate,
                            'finisdate': item.finisDate,
                            'blogname': item.businessblog.name,
                            'capacicty': yeka.capacity,
                            'type': None,
                            'firma': competition.business.company,
                            'yeka': False,
                            'uuid': yeka.uuid
                        }
                        selectblog.append(beka)
                    except:
                        pass

        return render(request, 'Report/reportList.html',
                      {'urls': urls, 'current_url': current_url,
                       'url_name': url_name,'city':city,'prelicense':prelicense,
                       'businessblogs':businessblogs,'license':license,'selectblog':selectblog

                       })

    except Exception as e:

        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')