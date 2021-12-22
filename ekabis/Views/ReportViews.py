import copy
import datetime
import os
import traceback

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db import transaction, connection
from django.db.models import Q, Sum, Count
from django.http import JsonResponse, Http404, HttpResponse, FileResponse
from django.shortcuts import redirect, render
from django.templatetags.static import static
from django.urls import resolve
from django.utils.safestring import mark_safe

from ekabis.models import City, YekaBusinessBlog, YekaCompetition, BusinessBlog, Yeka, YekaBusiness, ConnectionRegion, \
    YekaBusinessBlogParemetre, BusinessBlogParametreType, YekaCompetitionEskalasyon, YekaAccept, YekaGuarantee
from ekabis.models.YekaContract import YekaContract
from ekabis.models.YekaProposal import YekaProposal
from ekabis.services import general_methods
from ekabis.services.general_methods import control_access
from ekabis.services.services import last_urls, YekaService, ConnectionRegionService, YekaCompetitionService, \
    CompanyService, YekaGetService

from ekabis.models.Permission import Permission
from oxiterp.settings.base import MEDIA_URL


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

        city = City.objects.all()
        selectblog = None
        businessblogs = BusinessBlog.objects.all()

        yekas=YekaService(request,None)

        # ön lisans sürecindekiler
        blogs = YekaBusinessBlog.objects.filter(businessblog__name='Ön Lisans Dönemi', status='3')
        prelicense = []
        installedPower_array = []
        currentPower_array = []
        yeka_capacity_array = []
        company_array = []
        yeka_acccepts = YekaAccept.objects.filter(isDeleted=False)

        yeka_array = []
        competitions = YekaCompetition.objects.filter(isDeleted=False)
        # yeka bazında yapılan yarışmalar
        for competition in competitions:
            yeka_dict = dict()
            if ConnectionRegion.objects.filter(yekacompetition=competition):
                region = ConnectionRegion.objects.get(yekacompetition=competition)
                yeka = Yeka.objects.get(connection_region=region)
                yeka_dict['competition'] = competition
                yeka_dict['yeka'] = yeka
                yeka_dict['region'] = region
                yeka_array.append(yeka_dict)

        # kabulde ulaşılan güce göre yarışmalar
        for yeka_accept in yeka_acccepts:
            accept_dict = dict()
            currentPower_dict = dict()
            yeka_capacity_dict = dict()
            company_dict = dict()
            competition = YekaCompetition.objects.get(business=yeka_accept.business)
            accept_dict['label'] = competition.name
            total = yeka_accept.accept.filter(isDeleted=False).aggregate(Sum('installedPower'))
            currentPower = yeka_accept.accept.filter(isDeleted=False).aggregate(Sum('currentPower'))
            if total['installedPower__sum'] is None:
                total['installedPower__sum'] = 0
            if currentPower['currentPower__sum'] is None:
                currentPower['currentPower__sum'] = 0
            accept_dict['power'] = total['installedPower__sum']
            currentPower_dict['power'] = currentPower['currentPower__sum']
            currentPower_dict['label'] = competition.name
            total_capacity = int(total['installedPower__sum']) + int(currentPower['currentPower__sum'])
            installedPower_array.append(accept_dict)
            accept_company = competition.company
            company_dict['electrical_power'] = currentPower['currentPower__sum']
            contract = YekaContract.objects.filter(business=competition.business)
            if contract:
                if contract[0].company:
                    company_dict['contract'] = YekaContract.objects.get(business=competition.business)
                else:
                    company_dict['contract'] = None
            else:
                company_dict['contract'] = None
            company_dict['mechanical_power'] = total['installedPower__sum']
            company_dict['competition'] = competition
            company_dict['company'] = accept_company
            if YekaCompetitionEskalasyon.objects.filter(competition=competition):
                company_dict['price'] = YekaCompetitionEskalasyon.objects.get(competition=competition)
            else:
                company_dict['price'] = None
            company_array.append(company_dict)

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
                prelicense.append(beka)

            elif YekaCompetition.objects.filter(business=business):
                yeka = YekaCompetition.objects.get(business=business)
                beka = {
                    'name': yeka.name,
                    'startdate': item.startDate,
                    'finishdate': item.finisDate,
                    'blogname': item.businessblog.name,
                    'capacity': yeka.capacity,
                    'type': "",
                    'firma': yeka.business.company,
                    'yeka': False,
                    'uuid': yeka.uuid
                }
                prelicense.append(beka)
        # lisans sürecindekiler
        blogs = YekaBusinessBlog.objects.filter(businessblog__name='Lisans Dönemi', status='3')
        license = []
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
                license.append(beka)

            elif YekaCompetition.objects.filter(business=business):
                yeka = YekaCompetition.objects.get(business=business)
                beka = {
                    'name': yeka.name,
                    'startdate': item.startDate,
                    'finishdate': item.finisDate,
                    'blogname': item.businessblog.name,
                    'capacicty': yeka.capacity,
                    'type': "",
                    'firma': yeka.business.company,
                    'yeka': False,
                    'uuid': yeka.uuid
                }
                license.append(beka)

        if 'business' in request.POST:
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
                      {'urls': urls, 'current_url': current_url, 'accept_array': company_array,
                       'url_name': url_name, 'city': city, 'prelicense': prelicense, 'yeka_list': yeka_array,
                       'businessblogs': businessblogs, 'license': license, 'selectblog': selectblog,
                       'yekas':yekas

                       })

    except Exception as e:

        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


def proposal_yeka_report(request):
    perm = control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:

        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)

        proposal_array=[]
        with transaction.atomic():
            if request.method == 'POST':
                yeka_uuid=request.POST['yeka_uuid']
                yeka = Yeka.objects.get(uuid=yeka_uuid)
                name=general_methods.yekaname(yeka.business)
                connection_regions=yeka.connection_region.filter(isDeleted=False)
                for region in connection_regions:

                    competitions=region.yekacompetition.filter(isDeleted=False,parent=None)
                    for competition in competitions:
                        proposal_dict = dict()
                        proposal_dict['company'] = competition.business.company
                        proposal_dict['competition']=competition
                        guarantee=None
                        if YekaGuarantee.objects.filter(business=competition.business):
                            yeka_guarantee=YekaGuarantee.objects.get(business=competition.business)
                            guarantee=yeka_guarantee.guarantee.filter(isDeleted=False).last()
                        proposal_dict['guarantee']=guarantee
                        comp_proposals = []
                        comp_proposal = dict()
                        if YekaProposal.objects.filter(business=competition.business,isDeleted=False):
                            yeka_proposal=YekaProposal.objects.get(business=competition.business,isDeleted=False)
                            proposals=yeka_proposal.proposal.filter(isDeleted=False)
                            comp_proposals=[]
                            if proposals:
                                for proposal in proposals:
                                    comp_proposal=dict()
                                    negative = proposal.institution.filter(status='Olumsuz').count()
                                    not_negative = proposal.institution.filter(status='Olumlu').count()
                                    if negative:
                                        comp_proposal['status_color'] = '#ff3a3a'
                                        comp_proposal['status'] = 'Olumsuz'
                                        comp_proposal['proposal']=proposal
                                    elif not_negative:
                                        comp_proposal['status_color'] = '#8cff8c'
                                        comp_proposal['status'] = 'Olumlu'
                                        comp_proposal['proposal']=proposal
                                    else:
                                        comp_proposal['status_color'] = '#ffff6e'
                                        comp_proposal['status'] = 'Sonuçlanmadı'
                                        comp_proposal['proposal']=proposal
                                    comp_proposals.append(comp_proposal)
                            else:
                                comp_proposal['status_color'] = '#ffff'
                                comp_proposal['status'] = 'Yok'
                                comp_proposal['proposal'] = None
                                comp_proposals.append(comp_proposal)
                            proposal_dict['proposals'] = comp_proposals
                            proposal_dict['proposals'] = comp_proposals

                        else:
                            comp_proposal['status_color'] = '#ffff'
                            comp_proposal['status'] = 'Yok'
                            comp_proposal['proposal'] = None
                            comp_proposals.append(comp_proposal)
                            proposal_dict['proposals'] = comp_proposals
                        proposal_array.append(proposal_dict)

        return render(request, 'Report/proposal_yeka_report.html',
                      {'urls': urls, 'current_url': current_url,'proposal_array':proposal_array,'name':name})
    except Exception as e:
        traceback.print_exc()
        messages.warning(request,e)
        return redirect('ekabis:view_yeka')
