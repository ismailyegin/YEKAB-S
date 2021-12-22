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

        yekas = YekaService(request, None)

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
                if not yeka.isDeleted:
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
            if ConnectionRegion.objects.filter(yekacompetition=competition):
                region = ConnectionRegion.objects.get(yekacompetition=competition)
                yeka = Yeka.objects.get(connection_region=region)
                if not yeka.isDeleted:
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
                if Yeka.objects.filter(business=business, isDeleted=False):
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

                elif YekaCompetition.objects.filter(business=business, isDeleted=False):
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
            if Yeka.objects.filter(business=business, isDeleted=False):
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

            elif YekaCompetition.objects.filter(business=business, isDeleted=False):
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

            blogs = YekaBusinessBlog.objects.filter(businessblog__id=request.POST.get('business_type'))
            selectblog = []
            for item in blogs:
                business = YekaBusiness.objects.filter(businessblogs=item)[0]

                if Yeka.objects.filter(business=business, isDeleted=False):
                    yeka = Yeka.objects.get(business=business)
                    if not yeka.isDeleted:
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

                elif YekaCompetition.objects.filter(business=business, isDeleted=False):

                    try:
                        competition = YekaCompetition.objects.get(business=business)
                        region = ConnectionRegion.objects.get(yekacompetition=competition)
                        yeka = Yeka.objects.get(connection_region=region)

                        beka = {
                            'yeka_name': yeka.name,
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
                       'yekas': yekas

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

        proposal_array = []
        with transaction.atomic():
            if request.method == 'POST':
                yeka_uuid = request.POST['yeka_uuid']
                yeka = Yeka.objects.get(uuid=yeka_uuid)
                name = general_methods.yekaname(yeka.business)
                connection_regions = yeka.connection_region.filter(isDeleted=False)
                for region in connection_regions:

                    competitions = region.yekacompetition.filter(isDeleted=False, parent=None)
                    for competition in competitions:

                        proposal_dict = dict()
                        first_accept_date='---'
                        if YekaBusiness.objects.filter(uuid=competition.business.uuid):
                            comp_business = YekaBusiness.objects.get(uuid=competition.business.uuid)
                            competititon_business_block = comp_business.businessblogs.get(
                                businessblog__name='YEKA İlan Edilmesi')
                            build_time='---'
                            build_business_block = comp_business.businessblogs.filter(
                                businessblog__name='İnşaat Süresi')
                            if build_business_block:
                                build_business_block =comp_business.businessblogs.get(
                                businessblog__name='İnşaat Süresi')
                                build_time = build_business_block.businessTime
                            proposal_dict['build_time'] = build_time

                            if YekaAccept.objects.filter(business=competition.business):
                                yeka_accept=YekaAccept.objects.get(business=competition.business)
                                if yeka_accept.accept.all():
                                    first_accept_date=yeka_accept.accept.first().date.strftime("%d-%m-%Y")
                            proposal_dict['accept_date'] = first_accept_date
                            value='---'
                            prelicence_date='---'
                            licence_value='---'
                            licence_date='---'
                            licence_time='---'
                            prelicence_time='---'
                            prelicence_business_block = comp_business.businessblogs.filter(
                                businessblog__name='Ön Lisans Dönemi')
                            if prelicence_business_block:
                                prelicence_business_block = comp_business.businessblogs.get(
                                    businessblog__name='Ön Lisans Dönemi')
                                prelicence_time=prelicence_business_block.businessTime
                            else:
                                prelicence_business_block=None
                            licence_business_block = comp_business.businessblogs.filter(
                                businessblog__name='Lisans Dönemi')
                            if licence_business_block:
                                licence_business_block = comp_business.businessblogs.get(
                                    businessblog__name='Lisans Dönemi')
                                licence_time=licence_business_block.businessTime
                            else:
                                licence_business_block=None
                            proposal_dict['prelicence_time'] = prelicence_time
                            proposal_dict['licence_time'] = licence_time

                            if  prelicence_business_block.parameter:
                                if prelicence_business_block.parameter.filter(parametre__title='Ön Lisans Numarası'):
                                    value=prelicence_business_block.parameter.get(parametre__title='Ön Lisans Numarası').value
                                if prelicence_business_block.parameter.filter(parametre__title='Ön Lisans Tarihi'):
                                    prelicence_date=prelicence_business_block.parameter.get(parametre__title='Ön Lisans Tarihi').value
                            if licence_business_block.parameter:
                                if licence_business_block.parameter.filter(parametre__title='Lisans Numarası'):
                                    licence_value = licence_business_block.parameter.get(
                                        parametre__title='Lisans Numarası').value
                                if licence_business_block.parameter.filter(parametre__title='Lisans Tarihi'):
                                    licence_date = licence_business_block.parameter.get(
                                        parametre__title='Lisans Tarihi').value

                            proposal_dict['prelicence_business_value'] = value
                            proposal_dict['prelicence_business_date'] = prelicence_date
                            proposal_dict['licence_business_value'] = licence_value
                            proposal_dict['licence_business_date'] = licence_date


                            prelicence_app_business_block = comp_business.businessblogs.get(
                                businessblog__name='Ön Lisans Başvurusu')

                            if prelicence_app_business_block.completion_date:
                                proposal_dict[
                                    'prelicence_app_business_date'] = prelicence_app_business_block.completion_date
                            elif prelicence_app_business_block.startDate:
                                proposal_dict['prelicence_app_business_date'] = prelicence_app_business_block.startDate
                            else:
                                proposal_dict['prelicence_app_business_date'] = '---'

                            if competititon_business_block.completion_date:
                                proposal_dict['competition_business_date'] = competititon_business_block.completion_date
                            elif competititon_business_block.startDate:
                                proposal_dict['competition_business_date'] = competititon_business_block.startDate
                            else:
                                proposal_dict['competition_business_date'] = '---'

                        proposal_dict['contact_price'] = 0
                        if YekaContract.objects.filter(business=competition.business):
                            contract = YekaContract.objects.get(business=competition.business)
                            if contract.price:
                                proposal_dict['contact_price'] = contract.price
                        proposal_dict['company'] = competition.business.company
                        proposal_dict['competition'] = competition
                        proposal_dict['yeka'] = yeka

                        guarantee = None
                        if YekaGuarantee.objects.filter(business=competition.business):
                            yeka_guarantee = YekaGuarantee.objects.get(business=competition.business)
                            guarantee = yeka_guarantee.guarantee.filter(isDeleted=False).last()
                        proposal_dict['guarantee'] = guarantee
                        comp_proposals = []
                        comp_proposal = dict()
                        if YekaProposal.objects.filter(business=competition.business, isDeleted=False):
                            yeka_proposal = YekaProposal.objects.get(business=competition.business, isDeleted=False)
                            proposals = yeka_proposal.proposal.filter(isDeleted=False)
                            comp_proposals = []
                            if proposals:
                                for proposal in proposals:
                                    comp_proposal = dict()
                                    negative = proposal.institution.filter(status='Olumsuz').count()
                                    not_negative = proposal.institution.filter(status='Olumlu').count()
                                    if negative:
                                        comp_proposal['status_color'] = '#ff3a3a'
                                        comp_proposal['status'] = 'Olumsuz'
                                        comp_proposal['proposal'] = proposal
                                    elif not_negative:
                                        comp_proposal['status_color'] = '#8cff8c'
                                        comp_proposal['status'] = 'Olumlu'
                                        comp_proposal['proposal'] = proposal
                                    else:
                                        comp_proposal['status_color'] = '#ffff6e'
                                        comp_proposal['status'] = 'Sonuçlanmadı'
                                        comp_proposal['proposal'] = proposal
                                    comp_proposals.append(comp_proposal)
                            else:
                                comp_proposal['status_color'] = '#ffff'
                                comp_proposal['status'] = '---'
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
                      {'urls': urls, 'current_url': current_url, 'proposal_array': proposal_array, 'name': name})
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, e)
        return redirect('ekabis:view_yeka')
