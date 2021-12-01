import copy
import datetime
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
    YekaBusinessBlogParemetre, BusinessBlogParametreType, YekaCompetitionEskalasyon, YekaAccept
from ekabis.models.YekaContract import YekaContract
from ekabis.services.general_methods import control_access
from ekabis.services.services import last_urls, YekaService, ConnectionRegionService, YekaCompetitionService, \
    CompanyService

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
                       'businessblogs': businessblogs, 'license': license, 'selectblog': selectblog

                       })

    except Exception as e:

        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')


# reporting the information of YEKA in the system with a general table -ORACLE-
def general_reporting_orcl(request):
    try:
        with connection.cursor() as cursor:
            urls = last_urls(request)
            current_url = resolve(request.path_info)
            url_name = Permission.objects.get(codename=current_url.url_name)
            sql = " SELECT  yeka_business.ID AS blok_id,yeka_business_block.ID AS yeka_business_block_id,"
            sql += " firma.TAXNUMBER AS vergi_no , firma.TAXOFFICE AS vergi_dairesi ,sozlesme.contract_tarih as sozlesme_tarih, baglanti_bol.NAME AS baglanti_bolgesi, yeka.DEFINITION AS yeka ,yarisma.ID AS yarisma_id ,firma.NAME AS firma , "
            sql += " firma.MAIL AS firma_mail  , yarisma.NAME AS yarisma , sozlesme.PRICE AS sozlesme_fiyat "
            sql += " ,business_block.NAME AS is_blogu ,yeka_business_block.STATUS AS is_blok_durumu, yeka_business_block.STARTDATE AS baslangic_tarihi ,city.name as sehir ,district.name as ilce,neighborhood.name as mah,"
            sql += " yeka_eskalasyon.RESULT as guncel_fiyat,location.PARCEL AS ada_parsel,"
            sql += " yeka_business_block.FINISDATE AS bitis_tarihi "
            sql += " FROM EKABIS_YEKACOMPETITION yarisma "
            sql += " LEFT JOIN EKABIS_CONNECTIONREGION_YE1C75 x ON x.YEKACOMPETITION_ID = yarisma.ID "
            sql += " LEFT JOIN EKABIS_CONNECTIONREGION baglanti_bol ON baglanti_bol.ID=x.CONNECTIONREGION_ID "
            sql += " LEFT JOIN EKABIS_YEKA_CONNECTION_REGION y ON y.CONNECTIONREGION_ID=baglanti_bol.ID "
            sql += " LEFT JOIN EKABIS_YEKA yeka ON yeka.ID=y.YEKA_ID"
            sql += " LEFT JOIN EKABIS_YEKACOMPANY  yeka_company ON yarisma.ID=yeka_company.COMPETITION_ID "
            sql += " LEFT JOIN EKABIS_COMPANY firma ON firma.ID=yeka_company.COMPANY_ID"
            sql += " LEFT JOIN EKABIS_YEKACONTRACT sozlesme ON sozlesme.BUSINESS_ID=yarisma.BUSINESS_ID "
            sql += " LEFT JOIN EKABIS_YEKABUSINESS yeka_business ON yeka_business.ID=yarisma.BUSINESS_ID "
            sql += " LEFT JOIN EKABIS_YEKABUSINESS_BUSINE12FF ybb ON ybb.YEKABUSINESS_ID=yeka_business.ID "
            sql += " LEFT JOIN EKABIS_YEKABUSINESSBLOG yeka_business_block ON yeka_business_block.ID=ybb.YEKABUSINESSBLOG_ID "
            sql += " LEFT JOIN EKABIS_BUSINESSBLOG business_block ON business_block.ID=yeka_business_block.BUSINESSBLOG_ID "
            sql += " LEFT JOIN EKABIS_BUSINESSBLOG_PARAMETRE business_parametre ON business_parametre.BUSINESSBLOG_ID=business_block.ID "
            sql += " LEFT JOIN EKABIS_BUSINESSBLOGPARAMET80EE parametre_type ON parametre_type.ID=business_parametre.BUSINESSBLOGPARAMETRETYPE_ID "
            sql += " LEFT JOIN EKABIS_YEKABUSINESSBLOGPAR118F yeka_blok_parametre ON yeka_blok_parametre.PARAMETRE_ID=parametre_type.ID "
            sql += " LEFT JOIN EKABIS_YEKACOMPETITIONESKA02C8 yeka_eskalasyon ON yeka_eskalasyon.competition_id=yarisma.ID "
            sql += " LEFT JOIN EKABIS_YEKACOMPETITIONESKAC10D e ON e.YEKA_COMPETITION_ESKALASYON_ID=yeka_eskalasyon.ID "
            sql += " LEFT JOIN EKABIS_ESKALASYON eskalasyon ON eskalasyon.ID=e.ESKALASYON_INFO_ID "
            sql += " LEFT JOIN EKABIS_YEKACOMPETITIONESKA02C8 yeka_eskalasyon ON yeka_eskalasyon.competition_id=yarisma.ID "
            sql += " LEFT JOIN EKABIS_YEKACOMPETITIONESKAC10D e ON e.YEKA_COMPETITION_ESKALASYON_ID=yeka_eskalasyon.ID "
            sql += " LEFT JOIN EKABIS_YEKAPROPOSAL yeka_proposal ON yeka_proposal.BUSINESS_ID=yeka_business.ID "
            sql += " LEFT JOIN EKABIS_YEKAPROPOSAL_PROPOSAL yekaproposal_proposal ON yekaproposal_proposal.YEKAPROPOSAL_ID=yeka_proposal.ID "
            sql += " LEFT JOIN EKABIS_PROPOSAL_LOCATION proposal_location ON proposal_location.PROPOSAL_ID=yekaproposal_proposal.PROPOSAL_ID "
            sql += " LEFT JOIN EKABIS_LOCATION location ON location.ID=proposal_location.LOCATION_ID "
            sql += " LEFT JOIN EKABIS_CITY city ON city.ID=location.city "
            sql += " LEFT JOIN EKABIS_DISTRICT district ON district.ID=location.DISTRICT_ID "
            sql += " LEFT JOIN EKABIS_NEIGHBORHOOD neighborhood  ON neighborhood.ID=location.NEIGHBORHOOD_ID "
            sql += " LEFT JOIN  EKABIS_YEKAACCEPT yeka_accept ON yeka_accept.BUSINESS_ID=yeka_business.ID "
            sql += " LEFT JOIN EKABIS_YEKAACCEPT_ACCEPT yeka_yekaaccept ON yeka_yekaaccept.YEKAACCEPT_ID=yeka_accept.ID "
            sql += " LEFT JOIN EKABIS_ACCEPT accept ON accept.ID=yeka_yekaaccept.ACCEPT_ID "
            sql += " WHERE yeka_business_block.STATUS= 3  and yeka.isDeleted=FALSE"

            sql2 = " SELECT SUM(accept.CURRENTPOWER) AS total_elektriksel_guc , SUM(accept.INSTALLEDPOWER) AS total_mekanik_guc ,yarisma.ID AS yarisma_id "
            sql2 += " FROM EKABIS_YEKACOMPETITION yarisma "
            sql2 += " LEFT JOIN EKABIS_YEKABUSINESS yeka_business ON yeka_business.ID=yarisma.BUSINESS_ID "
            sql2 += " LEFT JOIN EKABIS_YEKABUSINESS_BUSINE12FF ybb ON ybb.YEKABUSINESS_ID=yeka_business.ID "
            sql2 += " LEFT JOIN EKABIS_YEKABUSINESSBLOG yeka_business_block ON yeka_business_block.ID=ybb.YEKABUSINESSBLOG_ID "
            sql2 += " LEFT JOIN EKABIS_BUSINESSBLOG business_block ON business_block.ID=yeka_business_block.BUSINESSBLOG_ID "
            sql2 += " LEFT JOIN EKABIS_BUSINESSBLOG_PARAMETRE business_parametre ON business_parametre.BUSINESSBLOG_ID=business_block.ID "
            sql2 += " LEFT JOIN EKABIS_BUSINESSBLOGPARAMET80EE  parametre_type ON parametre_type.ID=business_parametre.BUSINESSBLOGPARAMETRETYPE_ID "
            sql2 += " LEFT JOIN EKABIS_YEKABUSINESSBLOGPAR118F yeka_blok_parametre ON yeka_blok_parametre.PARAMETRE_ID=parametre_type.ID "
            sql2 += " LEFT JOIN  EKABIS_YEKAACCEPT yeka_accept ON yeka_accept.BUSINESS_ID=yeka_business.ID "
            sql2 += " LEFT JOIN EKABIS_YEKAACCEPT_ACCEPT yeka_yekaaccept ON yeka_yekaaccept.YEKAACCEPT_ID=yeka_accept.ID "
            sql2 += " LEFT JOIN EKABIS_ACCEPT accept ON accept.ID=yeka_yekaaccept.ACCEPT_ID "
            sql2 += " WHERE business_block.name='Kabuller'  "

            params = ["3","False"]
            params2 = ["Kabuller"]

            competition_id = None

            if request.method == 'POST':
                if not request.POST['select_yeka'] == 'not_matter':
                    sql += ' and yeka.ID= %s '
                    yeka_id = request.POST['select_yeka']
                    params.append(yeka_id)
                if not request.POST['select_region'] == 'not_matter':
                    region_id = request.POST['select_region']
                    sql += ' and baglanti_bol.ID= %s '
                    params.append(region_id)
                if not request.POST['select_competition'] == 'not_matter':
                    competition_id = request.POST['select_competition']
                    sql += ' and yarisma.ID= %s '
                    sql2 += ' and yarisma.ID= %s '
                    params.append(competition_id)
                    params2.append(competition_id)
                if not request.POST['select_company'] == 'not_matter':
                    company_id = request.POST['select_company']
                    sql += ' and firma.ID = %s '
                    params.append(company_id)

                sql2 += ' group by yarisma.ID '

            else:
                sql2 += ' group by yarisma.ID '
            join_select = 'B.yarisma_id,blok_id,yeka_business_block_id ,yeka_business_block_id,vergi_no,is_blogu,vergi_dairesi,baglanti_bolgesi,yeka,A.yarisma_id,A.firma,A.firma_mail,yarisma,A.sozlesme_fiyat,A.is_blok_durumu,A.bitis_tarihi,A.baslangic_tarihi, A.guncel_fiyat,A.ada_parsel,A.sehir,A.ilce,A.mah,A.sozlesme_tarih'
            select_sql = 'B.yarisma_id ,A.blok_id, A.yeka_business_block_id, A.yeka_business_block_id ,A.vergi_no ,A.vergi_dairesi, A.is_blogu ,A.baglanti_bolgesi,A.yeka,A.yarisma_id ,A.sozlesme_tarih,A.firma,A.firma_mail,A.yarisma,A.sozlesme_fiyat,A.is_blok_durumu,A.bitis_tarihi,A.baslangic_tarihi,A.guncel_fiyat,A.ada_parsel,A.sehir,A.ilce,A.mah'
            sql_join = 'SELECT ' + select_sql + ' FROM ( ' + sql + ' ) A  LEFT JOIN  (' + sql2 + ') B ON A.yarisma_id=B.yarisma_id group by  ' + join_select + ' '
            print(sql_join)
            yeka = YekaService(request, None)
            regions = ConnectionRegionService(request, None)
            competitions = YekaCompetitionService(request, None)
            companies = CompanyService(request, None)

            cursor.execute(sql_join)
            results = dictfetchall(cursor)
            keys = results

            result_array = table_column_name(keys)
            parameters = BusinessBlogParametreType.objects.filter(isDeleted=False)

            end_result = []
            for i, result in enumerate(results):
                parameter_dict = dict()
                if YekaCompetition.objects.filter(pk=result['yarisma_id']):
                    competititon = YekaCompetition.objects.get(pk=result['yarisma_id'])
                    for parameter in parameters:
                        parameter_dict[parameter.title] = None
                    # We delete the column names that do not want to appear in the table.
                    result.pop('blok_id')
                    result.pop('yarisma_id')
                    result.pop('yeka_business_block_id')
                    result.pop('is_blok_durumu')
                    parameter_dict['result'] = result
                    for blog in competititon.business.businessblogs.all():
                        for blog_parameter in blog.parameter.all():
                            print(blog.businessblog.name + ' - ' + blog_parameter.parametre.title)
                            if blog_parameter.parametre.type == 'file':
                                path = MEDIA_URL + blog_parameter.file.name
                                parameter_dict[blog_parameter.parametre.title] = mark_safe(
                                    '<a download="' + blog_parameter.file.name + '" href="' + path + '">' + blog_parameter.file.name + '</a>')
                            else:
                                parameter_dict[blog_parameter.parametre.title] = blog_parameter.value
                    end_result.append(parameter_dict)

                results = result_array['results']
            return render(request, 'Yeka/general_report.html',
                          {'block_results': end_result,
                           'keys': result_array['key_array'], 'yekas': yeka, 'regions': regions, 'companies': companies,
                           'competitions': competitions, 'urls': urls, 'current_url': current_url,
                           'url_name': url_name.name})
    except Exception as e:

        traceback.print_exc()
        messages.warning(request, e)
        return redirect('ekabis:view_yeka')


# reporting the information of YEKA in the system with a general table -MYSQL-
def general_reporting(request):
    try:
        with connection.cursor() as cursor:
            urls = last_urls(request)
            current_url = resolve(request.path_info)
            url_name = Permission.objects.get(codename=current_url.url_name)
            f = open("sql-1.txt", "r")
            sql = f.read()
            f.close()

            f = open("sql-2.txt", "r")
            sql2 = f.read()
            f.close()

            params = ["3","False"]
            params2 = ["Kabuller"]
            competition_id = None

            if request.method == 'POST':
                if not request.POST['select_yeka'] == 'not_matter':
                    sql += ' and yeka.ID= %s '
                    yeka_id = request.POST['select_yeka']
                    params.append(yeka_id)
                if not request.POST['select_region'] == 'not_matter':
                    region_id = request.POST['select_region']
                    sql += ' and baglanti_bol.ID= %s '
                    params.append(region_id)
                if not request.POST['select_competition'] == 'not_matter':
                    competition_id = request.POST['select_competition']
                    sql += ' and yarisma.ID= %s '
                    sql2 += ' and yarisma.ID= %s '
                    params.append(competition_id)
                    params2.append(competition_id)
                if not request.POST['select_company'] == 'not_matter':
                    company_id = request.POST['select_company']
                    sql += ' and firma.ID = %s '
                    params.append(company_id)

                sql2 += ' group by yarisma.ID '

            else:
                sql2 += ' group by yarisma.ID '
            join_select = 'B.yarisma_id,blok_id,yeka_business_block_id ,yeka_business_block_id,vergi_no,is_blogu,vergi_dairesi,baglanti_bolgesi,yeka,A.yarisma_id,A.firma,A.firma_mail,yarisma,A.sozlesme_fiyat,A.is_blok_durumu,A.bitis_tarihi,A.baslangic_tarihi, A.guncel_fiyat,A.ada_parsel,A.sehir,A.ilce,A.mah,A.sozlesme_tarih'
            select_sql = 'B.yarisma_id ,A.blok_id, A.yeka_business_block_id, A.yeka_business_block_id ,A.vergi_no ,A.vergi_dairesi, A.is_blogu ,A.baglanti_bolgesi,A.yeka,A.yarisma_id ,A.sozlesme_tarih,A.firma,A.firma_mail,A.yarisma,A.sozlesme_fiyat,A.is_blok_durumu,A.bitis_tarihi,A.baslangic_tarihi,A.guncel_fiyat,A.ada_parsel,A.sehir,A.ilce,A.mah'
            sql_join = 'SELECT ' + select_sql + ' FROM ( ' + sql + ' ) A  LEFT JOIN  (' + sql2 + ') B ON A.yarisma_id=B.yarisma_id group by  ' + join_select + ' '
            print(sql_join)
            yeka = YekaService(request, None)
            regions = ConnectionRegionService(request, None)
            competitions = YekaCompetitionService(request, None)
            companies = CompanyService(request, None)

            cursor.execute(sql_join, params + params2)
            results = dictfetchall(cursor)
            keys = results

            result_array = table_column_name(keys)
            parameters = BusinessBlogParametreType.objects.filter(isDeleted=False)

            end_result = []
            for i, result in enumerate(results):
                parameter_dict = dict()
                if YekaCompetition.objects.filter(pk=result['yarisma_id']):
                    competititon = YekaCompetition.objects.get(pk=result['yarisma_id'])
                    for parameter in parameters:
                        parameter_dict[parameter.title] = None
                    # We delete the column names that do not want to appear in the table.
                    result.pop('blok_id')
                    result.pop('yarisma_id')
                    result.pop('yeka_business_block_id')
                    result.pop('is_blok_durumu')
                    parameter_dict['result'] = result
                    for blog in competititon.business.businessblogs.all():
                        for blog_parameter in blog.parameter.all():
                            print(blog.businessblog.name + ' - ' + blog_parameter.parametre.title)
                            if blog_parameter.parametre.type == 'file':
                                path = MEDIA_URL + blog_parameter.file.name
                                parameter_dict[blog_parameter.parametre.title] = mark_safe(
                                    '<a download="' + blog_parameter.file.name + '" href="' + path + '">' + blog_parameter.file.name + '</a>')
                            else:
                                parameter_dict[blog_parameter.parametre.title] = blog_parameter.value
                    end_result.append(parameter_dict)

                results = result_array['results']
            return render(request, 'Yeka/general_report.html',
                          {'block_results': end_result,
                           'keys': result_array['key_array'], 'yekas': yeka, 'regions': regions, 'companies': companies,
                           'competitions': competitions, 'urls': urls, 'current_url': current_url,
                           'url_name': url_name.name})
    except Exception as e:

        traceback.print_exc()
        messages.warning(request, e)
        return redirect('ekabis:view_yeka')


# will return all matching records in ** dictionary list** format with key, value
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


# making column naming of general reporting
def table_column_name(results):
    try:
        key_array = []
        column_name = []
        result_dict = dict()
        new_result = copy.deepcopy(results)
        dinamik_params = []
        dinamik_values = []

        for i, result in enumerate(new_result):
            params = []
            for key, value in result.items():

                x = dict()
                x['value'] = value
                if key == 'baglanti_bolgesi':
                    if key not in column_name:
                        key_array.append('Bağlanti Bölgesi')
                    x['key'] = 'Bağlanti Bölgesi'
                    params.append(value)

                elif key == 'yeka':
                    if key not in column_name:
                        key_array.append('YEKA')
                    x['key'] = 'YEKA'
                    params.append(value)

                elif key == 'firma':
                    if key not in column_name:
                        key_array.append('Firma')
                    x['key'] = 'Firma'
                    params.append(value)

                elif key == 'vergi_no':
                    if key not in column_name:
                        key_array.append('Vergi Numarası')
                    x['key'] = 'Vergi Numarası'
                    params.append(value)

                elif key == 'vergi_dairesi':
                    if key not in column_name:
                        key_array.append('Vergi Dairesi')
                    x['key'] = 'Vergi Dairesi'
                    params.append(value)

                elif key == 'firma_mail':
                    if key not in column_name:
                        key_array.append('E-mail')
                    x['key'] = 'E-mail'
                    params.append(value)

                elif key == 'yarisma':
                    if key not in column_name:
                        key_array.append('Yarışma')
                    x['key'] = 'Yarışma'
                    params.append(value)

                elif key == 'sozlesme_fiyat':
                    if key not in column_name:
                        key_array.append('Sözleşme Fiyatı')
                    x['key'] = 'Sözleşme Fiyatı'
                    params.append(value)

                elif key == 'sozlesme_tarih':
                    if key not in column_name:
                        key_array.append('Sözleşme Tarihi')
                    x['key'] = 'Sözleşme Tarihi'
                    params.append(value)

                elif key == 'is_blogu':
                    if key not in column_name:
                        key_array.append('Durumu')
                    x['key'] = 'Durumu'
                    params.append(value)

                elif key == 'guncel_fiyat':
                    if key not in column_name:
                        key_array.append('Güncel Fiyat')
                    x['key'] = 'Güncel Fiyat'
                    params.append(value)

                elif key == 'ada_parsel':
                    if key not in column_name:
                        key_array.append('Ada-Parsel')
                    x['key'] = 'Ada-Parsel'
                    params.append(value)

                elif key == 'sehir':
                    if key not in column_name:
                        key_array.append('İl')
                    x['key'] = 'İl'
                    params.append(value)
                elif key == 'ilce':
                    if key not in column_name:
                        key_array.append('İlçe')
                    x['key'] = 'İlçe'
                    params.append(value)
                elif key == 'mah':
                    if key not in column_name:
                        key_array.append('Mahalle')
                    x['key'] = 'Mahalle'
                    params.append(value)

                elif key == 'baslangic_tarihi':
                    if key not in column_name:
                        key_array.append('Başlangıç Tarihi')
                    x['key'] = 'Başlangıç Tarihi'
                    if value:
                        params.append(value.strftime("%d-%m-%Y "))
                        result['baslangic_tarihi'] = value.strftime("%d-%m-%Y ")
                    else:
                        params.append(value)
                        result['baslangic_tarihi'] = value



                elif key == 'bitis_tarihi':
                    if key not in column_name:
                        key_array.append('Bitiş Tarihi')
                    x['key'] = 'Bitiş Tarihi'
                    if value:
                        params.append(value.strftime("%d-%m-%Y "))
                        result['bitis_tarihi'] = value.strftime("%d-%m-%Y ")
                    else:
                        params.append(value)
                        result['bitis_tarihi'] = value


                elif key == 'total_elektriksel_guc':
                    if key not in column_name:
                        key_array.append('Toplam Elektriksel Güç(MWe)')
                    x['key'] = 'Toplam Elektriksel Güç(MWe)'
                    params.append(value)

                elif key == 'total_mekanik_guc':
                    if key not in column_name:
                        key_array.append('Toplam Mekanik Güç(MWm)')
                    x['key'] = 'Toplam Mekanik Güç(MWm)'
                    params.append(value)

                else:
                    result[key] = 'yok'
                column_name.append(key)

        result_dict['results'] = new_result
        result_dict['key_array'] = key_array
        return result_dict

    except Exception as e:

        traceback.print_exc()
        return redirect('ekabis:view_yeka')
