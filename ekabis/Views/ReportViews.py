import copy
import datetime
import traceback

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db import transaction, connection
from django.db.models import Q
from django.http import JsonResponse, Http404, HttpResponse, FileResponse
from django.shortcuts import redirect, render
from django.urls import resolve

from ekabis.models import City, YekaBusinessBlog, YekaCompetition, BusinessBlog, Yeka, YekaBusiness, ConnectionRegion, \
    YekaBusinessBlogParemetre, BusinessBlogParametreType
from ekabis.services.general_methods import control_access
from ekabis.services.services import last_urls, YekaService, ConnectionRegionService, YekaCompetitionService, \
    CompanyService

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

        city = City.objects.all()
        selectblog = None
        businessblogs = BusinessBlog.objects.all()

        # ön lisans sürecindekiler
        blogs = YekaBusinessBlog.objects.filter(businessblog__name='Ön Lisans Süreci')
        prelicense = []
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
                    'capacicty': yeka.capacity,
                    'type': "",
                    'firma': yeka.business.company,
                    'yeka': False,
                    'uuid': yeka.uuid
                }
                prelicense.append(beka)
        # lisans sürecindekiler
        blogs = YekaBusinessBlog.objects.filter(businessblog__name='Lisans')
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
                      {'urls': urls, 'current_url': current_url,
                       'url_name': url_name, 'city': city, 'prelicense': prelicense,
                       'businessblogs': businessblogs, 'license': license, 'selectblog': selectblog

                       })

    except Exception as e:

        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')

# reporting the information of YEKA in the system with a general table
def general_reporting(request):
    try:
        with connection.cursor() as cursor:
            urls = last_urls(request)
            current_url = resolve(request.path_info)
            url_name = Permission.objects.get(codename=current_url.url_name)
            sql = "  SELECT  yeka_business.id as blok_id,yeka_business_block.id as yeka_business_block_id, baglanti_bol.name as baglanti_bolgesi, yeka.definition as yeka ,yarisma.id as yarisma_id , "
            sql += "  firma.name as firma , firma.taxnumber as vergi_no , firma.taxOffice as vergi_dairesi , "
            sql += "  firma.mail as firma_mail  , yarisma.name as yarisma , sozlesme.price as sozlesme_fiyat , "
            sql += "  sozlesme.date as sozlesme_tarih , business_block.name as is_blogu ,yeka_business_block.status as is_blok_durumu , "
            sql += "  eskalasyon.result as guncel_fiyat , location.parcel as ada_parsel , yeka_business_block.startDate as baslangic_tarihi , "
            sql += " yeka_business_block.finisDate as bitis_tarihi "
            sql += " FROM ekabis_yekacompetition yarisma "
            sql += " LEFT JOIN ekabis_connectionregion_yekacompetition x ON x.yekacompetition_id=yarisma.id "  # yarisma.id
            sql += " LEFT JOIN ekabis_connectionregion baglanti_bol ON baglanti_bol.id=x.connectionregion_id "
            sql += " LEFT JOIN ekabis_yeka_connection_region y ON y.yeka_id=x.connectionregion_id "
            sql += " LEFT JOIN ekabis_yeka yeka ON yeka.id=y.yeka_id "  # y.yeka_id
            sql += " LEFT JOIN ekabis_yekacompany  yeka_company ON yeka_company.competition_id=yarisma.id "  # yarisma.id
            sql += " LEFT JOIN ekabis_company firma ON firma.id=yeka_company.company_id "
            sql += " LEFT JOIN ekabis_yekacontract sozlesme ON sozlesme.business_id=yarisma.business_id "
            sql += " LEFT JOIN ekabis_yekabusiness yeka_business ON yeka_business.id=yarisma.business_id "
            sql += " LEFT JOIN ekabis_yekabusiness_businessblogs ybb ON ybb.yekabusiness_id=yeka_business.id "
            sql += "  LEFT JOIN ekabis_yekabusinessblog yeka_business_block ON yeka_business_block.id=ybb.yekabusinessblog_id "
            sql += "  LEFT JOIN ekabis_businessblog business_block ON business_block.id=yeka_business_block.businessblog_id "
            sql += "  left JOIN ekabis_businessblog_parametre business_parametre ON business_parametre.businessblog_id=business_block.id "
            sql += "  left JOIN ekabis_businessblogparametretype parametre_type ON parametre_type.id=business_parametre.businessblogparametretype_id "
            sql += "  left JOIN ekabis_yekabusinessblogparemetre yeka_blok_parametre ON yeka_blok_parametre.parametre_id=parametre_type.id "
            sql += "  LEFT JOIN ekabis_yekaconnectionregion y_con ON y_con.yeka_id=yeka.id "  # yeka.id
            sql += "  LEFT JOIN ekabis_yekacompetitioneskalasyon yeka_eskalasyon ON yeka_eskalasyon.competition_id=yarisma.id "
            sql += "  LEFT JOIN ekabis_yekacompetitioneskalasyon_eskalasyon e ON e.yeka_competition_eskalasyon_id=yeka_eskalasyon.id "
            sql += "  LEFT JOIN ekabis_eskalasyon eskalasyon ON eskalasyon.id=e.eskalasyon_info_id "
            sql += "  LEFT JOIN ekabis_yekaproposal yeka_proposal ON yeka_proposal.business_id=yeka_business.id "
            sql += "  LEFT JOIN ekabis_yekaproposal_proposal yekaproposal_proposal ON yekaproposal_proposal.yekaproposal_id=yeka_proposal.id "
            sql += "  LEFT JOIN ekabis_proposal_location proposal_location ON proposal_location.proposal_id=yekaproposal_proposal.proposal_id "
            sql += "  LEFT JOIN ekabis_location location ON location.id=proposal_location.location_id "
            sql += "  LEFT JOIN  ekabis_yekaaccept yeka_accept ON yeka_accept.business_id=yeka_business.id "
            sql += "  LEFT JOIN ekabis_yekaaccept_accept yeka_yekaaccept ON yeka_yekaaccept.yekaaccept_id=yeka_accept.id "
            sql += "  LEFT JOIN ekabis_accept accept ON accept.id=yeka_yekaaccept.accept_id "
            sql += "  where  yeka.id is  not null and yeka_business_block.status= %s "

            # f = open("sql-2.txt", "r")
            #sql2 = f.read()
            # f.close()

            sql2 = " SELECT SUM(accept.currentPower) as total_elektriksel_guc , SUM(accept.installedPower) as total_mekanik_guc , yarisma.id as yarisma_id "
            sql2 += " FROM ekabis_yekacompetition yarisma "
            sql2 += " left JOIN ekabis_yekabusiness yeka_business ON yeka_business.id=yarisma.business_id "
            sql2 += " left JOIN ekabis_yekabusiness_businessblogsybb ON ybb.yekabusiness_id=yeka_business.id "
            sql2 += " left JOIN ekabis_yekabusinessblog yeka_business_block ON yeka_business_block.id=ybb.yekabusinessblog_id "
            sql2 += " left JOIN ekabis_businessblog business_block ON business_block.id=yeka_business_block.businessblog_id "
            sql2 += " left JOIN ekabis_businessblog_parametre business_parametre ON business_parametre.businessblog_id=business_block.id "
            sql2 += " left JOIN ekabis_businessblogparametretype  parametre_type ON parametre_type.id=business_parametre.businessblogparametretype_id "
            sql2 += " left JOIN ekabis_yekabusinessblogparemetre yeka_blok_parametre ON yeka_blok_parametre.parametre_id=parametre_type.id "
            sql2 += " LEFT JOIN  ekabis_yekaaccept yeka_accept ON yeka_accept.business_id=yeka_business.id "
            sql2 += " LEFT JOIN ekabis_yekaaccept_accept yeka_yekaaccept ON yeka_yekaaccept.yekaaccept_id=yeka_accept.id "
            sql2 += " LEFT JOIN ekabis_accept accept ON accept.id=yeka_yekaaccept.accept_id "
            sql2 += " where business_block.name= %s "

            params = ['3']
            params2 = ['Kabuller']
            competition_id = None

            if request.method == 'POST':
                if not request.POST['select_yeka'] == 'not_matter':
                    sql += " and yeka.id= %s "
                    yeka_id = request.POST['select_yeka']
                    params.append(yeka_id)
                if not request.POST['select_region'] == 'not_matter':
                    region_id = request.POST['select_region']
                    sql += " and baglanti_bol.id= %s "
                    params.append(region_id)
                if not request.POST['select_competition'] == 'not_matter':
                    competition_id = request.POST['select_competition']
                    sql += " and yarisma.id= %s "
                    sql2 += " and yarisma.id= %s "
                    params.append(competition_id)
                    params2.append(competition_id)
                if not request.POST['select_company'] == 'not_matter':
                    company_id = request.POST['select_company']
                    sql += " and firma.id= %s "
                    params.append(company_id)
                sql += " group by yeka_business_block.id"
                sql2 += " group by yeka_business_block.id"

            else:
                sql += " group by yeka_business_block.id "
                sql2 += " group by yeka_business_block.id "

            sql_join = "SELECT * FROM ( " + sql + " ) A  LEFT JOIN  (" + sql2 + ") B ON A.yarisma_id=B.yarisma_id group by  B.yarisma_id "
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
                            parameter_dict[blog_parameter.parametre.title] = blog_parameter.value
                    end_result.append(parameter_dict)

                results = result_array['results']
            return render(request, 'Yeka/general_report.html',
                          {'block_results': end_result,
                           'keys': result_array['key_array'], 'yekas': yeka, 'regions': regions, 'companies': companies,
                           'competitions': competitions,'urls': urls, 'current_url': current_url,
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
