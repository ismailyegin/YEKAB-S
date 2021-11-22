import calendar
import json
import traceback

from bs4 import BeautifulSoup
from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth import logout
from django.db import transaction
from django.shortcuts import redirect

from ekabis.models import YekaCompetition, YekaCompetitionEskalasyon, YekaBusiness, YekaCompetitionEskalasyon_eskalasyon
from ekabis.models.Settings import Settings
from ekabis.models.Eskalasyon import Eskalasyon

import requests

from ekabis.models.YekaContract import YekaContract
from ekabis.services import general_methods
from ekabis.services.NotificationServices import notification
from ekabis.services.services import YekaCompetitionService


def EskalasyonCalculation(request, uuid):
    try:
        with transaction.atomic():

            current_energy_price = ''
            competition = YekaCompetition.objects.get(uuid=uuid)

            if YekaCompetitionEskalasyon.objects.filter(competition=competition):
                current_energy_price = YekaCompetitionEskalasyon.objects.filter(competition=competition).order_by(
                    '-creationDate').first().result
            else:
                if YekaContract.objects.filter(business=competition.business):
                    if YekaContract.objects.get(business=competition.business).price:
                        current_energy_price = YekaContract.objects.get(business=competition.business).price
                    else:
                        return {}
                else:
                    return {}

            if YekaBusiness.objects.get(pk=competition.business.pk).businessblogs.filter(
                    businessblog__name="YEKA Kullanım Hakkı Sözleşmesinin İmzalanması"):
                yeka_business = YekaBusiness.objects.get(pk=competition.business.pk).businessblogs.get(
                    businessblog__name="YEKA Kullanım Hakkı Sözleşmesinin İmzalanması")
                if YekaContract.objects.get(business=competition.business).unit == '1':
                    if yeka_business.parameter.filter(parametre__title='Tavan Fiyatı (USD)'):
                        peak_value = yeka_business.parameter.get(
                            parametre__title='Tavan Fiyatı (USD)').value  # Sözleşme iş bloğunda girilen eskalasyon pik değeri (USD)
                        startDate = 'startDate=' + str(datetime.today().date().strftime('%d-%m-%Y')) + '&'
                        endDate = 'endDate=' + str(datetime.today().date().strftime('%d-%m-%Y'))
                        date = startDate + endDate
                        url = 'https://evds2.tcmb.gov.tr/service/evds/series=TP.DK.USD.S.YTL&' + date + '&type=json&key=cakxFSu6Oh&aggregationTypes=max&formulas=0&frequency=1'
                        payload = {}
                        headers = {
                            'Cookie': 'TS01ab7d04=015d31d69177a668a8501cee5acf4e7218ddba7c5142b3bd18702be96d61d829a97551ffd1193c8ce196ebe26d8d3a618ea6f63f1c'
                        }
                        response = requests.request("GET", url, headers=headers, data=payload)
                        x = json.loads(response.text)  # Pik değerini hesaplamak için günlük dolar ortalaması
                        peak_value = float(peak_value.replace(',', '.')) * float(
                            x['items'][0]['TP_DK_USD_S_YTL'])  # eskalasyon pik değeri( TL )
                        if competition.is_calculation:  # pik değerine ulaşmış yarışmaların hesaplaması yapılmaz
                            yeka_competition_eskalasyon = YekaCompetitionEskalasyon(competition=competition,
                                                                                    pre_result=current_energy_price)
                            yeka_competition_eskalasyon.save()

                            month_name = calendar.month_name[(datetime.today().month)]
                            current_date = datetime.today().date()

                            # 3 aylık dönemin ilk ayından önceki 2. aya ait UFE-TUFE
                            date_second = (current_date - relativedelta(months=2)).strftime("%d-%m-%Y")
                            date_second = str(date_second).split('-', 1)[1]
                            ufe_tufe_second = month_value_tufe_ufe(date_second, '2')
                            eskalasyon_ufe = Eskalasyon.objects.get(uuid=ufe_tufe_second['eskalasyon_ufe'])
                            eskalasyon_tufe = Eskalasyon.objects.get(uuid=ufe_tufe_second['eskalasyon_tufe'])
                            YekaCompetitionEskalasyon_eskalasyon(
                                yeka_competition_eskalasyon=yeka_competition_eskalasyon,
                                eskalasyon_info=eskalasyon_tufe).save()
                            YekaCompetitionEskalasyon_eskalasyon(
                                yeka_competition_eskalasyon=yeka_competition_eskalasyon,
                                eskalasyon_info=eskalasyon_ufe).save()

                            # 3 aylık dönemin ilk ayından önceki 5. aya ait UFE-TUFE
                            date_fifth = (current_date - relativedelta(months=5)).strftime("%d-%m-%Y")
                            date_fifth = str(date_fifth).split('-', 1)[1]
                            ufe_tufe_fifth = month_value_tufe_ufe(date_fifth, '5')
                            eskalasyon_ufe = Eskalasyon.objects.get(uuid=ufe_tufe_fifth['eskalasyon_ufe'])
                            eskalasyon_tufe = Eskalasyon.objects.get(uuid=ufe_tufe_fifth['eskalasyon_tufe'])
                            YekaCompetitionEskalasyon_eskalasyon(
                                yeka_competition_eskalasyon=yeka_competition_eskalasyon,
                                eskalasyon_info=eskalasyon_tufe).save()
                            YekaCompetitionEskalasyon_eskalasyon(
                                yeka_competition_eskalasyon=yeka_competition_eskalasyon,
                                eskalasyon_info=eskalasyon_ufe).save()

                            # 3 aylık dönemin ilk ayından önceki 2. 3. 4. ayların USD ortalaması
                            endDate = (current_date - relativedelta(months=2)).strftime("%d-%m-%Y")
                            startDate = (current_date - relativedelta(months=5)).strftime("%d-%m-%Y")
                            second_usd_avg = usd_euro_exchange_rate(startDate, endDate, '2-3-4', 'TP.DK.USD.S.YTL')
                            eskalasyon = Eskalasyon.objects.get(uuid=second_usd_avg['eskalasyon_uuid'])
                            YekaCompetitionEskalasyon_eskalasyon(
                                yeka_competition_eskalasyon=yeka_competition_eskalasyon,
                                eskalasyon_info=eskalasyon).save()

                            # 3 aylık dönemin ilk ayından önceki 2. 3. 4. ayların EURO ortalaması
                            second_euro_avg = usd_euro_exchange_rate(startDate, endDate, '2-3-4', 'TP.DK.EUR.S.YTL')
                            eskalasyon = Eskalasyon.objects.get(uuid=second_euro_avg['eskalasyon_uuid'])
                            YekaCompetitionEskalasyon_eskalasyon(
                                yeka_competition_eskalasyon=yeka_competition_eskalasyon,
                                eskalasyon_info=eskalasyon).save()

                            # 3 aylık dönemin ilk ayından önceki 5. 6. 7. ayların EURO ortalaması
                            endDate = (current_date - relativedelta(months=5)).strftime("%d-%m-%Y")
                            startDate = (current_date - relativedelta(months=7)).strftime("%d-%m-%Y")
                            fifth_euro_avg = usd_euro_exchange_rate(startDate, endDate, '5-6-7', 'TP.DK.EUR.S.YTL')
                            eskalasyon = Eskalasyon.objects.get(uuid=fifth_euro_avg['eskalasyon_uuid'])
                            YekaCompetitionEskalasyon_eskalasyon(
                                yeka_competition_eskalasyon=yeka_competition_eskalasyon,
                                eskalasyon_info=eskalasyon).save()

                            # 3 aylık dönemin ilk ayından önceki 5. 6. 7. ayların USD ortalaması
                            fifth_usd_avg = usd_euro_exchange_rate(startDate, endDate, '5-6-7', 'TP.DK.USD.S.YTL')
                            eskalasyon = Eskalasyon.objects.get(uuid=fifth_usd_avg['eskalasyon_uuid'])
                            YekaCompetitionEskalasyon_eskalasyon(
                                yeka_competition_eskalasyon=yeka_competition_eskalasyon,
                                eskalasyon_info=eskalasyon).save()

                            # SONUÇ
                            ufe_result = 0.26 * float(ufe_tufe_second['ufe']) / float(ufe_tufe_fifth['ufe'])
                            tufe_result = 0.26 * float(ufe_tufe_second['tufe']) / float(ufe_tufe_fifth['tufe'])
                            usd_result = 0.24 * float(second_usd_avg['result']) / float(fifth_usd_avg['result'])
                            euro_result = 0.24 * float(second_euro_avg['result']) / float(fifth_euro_avg['result'])
                            result = float(current_energy_price) * (ufe_result + tufe_result + usd_result + euro_result)

                            if result >= peak_value:
                                result = peak_value
                                competition.is_calculation = False
                                competition.save()

                            yeka_competition_eskalasyon.result = result
                            yeka_competition_eskalasyon.save()
                            url = redirect('ekabis:view_yeka_competition_detail', competition.uuid).url
                            html = '<a style="color:black;" href="' + url + '"> ID : ' + str(
                                competition.pk) + ' - ' + str(
                                competition.name) + '</a> adlı yarışmanın eskalasyon hesabı yapıldı.'
                            notification(request, html, competition.uuid, 'yeka_competition')
                            return result

    except Exception as e:
        traceback.print_exc()


def month_value_tufe_ufe(date, month):
    try:
        url = "https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/Istatistikler/Enflasyon+Verileri/Uretici+Fiyatlari"
        payload = {}
        headers = {
            'Cookie': 'TS01ab7d04=015d31d69177a668a8501cee5acf4e7218ddba7c5142b3bd18702be96d61d829a97551ffd1193c8ce196ebe26d8d3a618ea6f63f1c'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        html = response.content
        soup = BeautifulSoup(html, "html.parser")
        tr = soup.find_all("tr")
        for td in tr:
            if not td.find_all("strong"):
                t = td.text.split('\n')
                if len(t) == 7 and t:
                    if t[1] == date:
                        desc = 'Geçerli Olacak 3 aylık dönemin ilk ayından önceki ' + month + '. aya ait UFE değeri'
                        eskalasyon = Eskalasyon(startDate=date, endDate=date,
                                                result=t[3],
                                                result_description=desc)
                        eskalasyon.save()
                        desc2 = 'Geçerli Olacak 3 aylık dönemin ilk ayından önceki ' + month + '. aya ait TUFE değeri'

                        eskalasyon2 = Eskalasyon(startDate=date, endDate=date,
                                                 result=t[5],
                                                 result_description=desc2)
                        eskalasyon2.save()
                        result = {
                            'date': t[1],
                            'ufe': t[3],
                            'tufe': t[5],
                            'eskalasyon_tufe': eskalasyon2.uuid,
                            'eskalasyon_ufe': eskalasyon.uuid
                        }
                        return result
    except Exception as e:
        traceback.print_exc()


def usd_euro_exchange_rate(startDate, endDate, month,
                           seri):  # 3 aylık dönemin belirtilen aylarının belirtilen seri  ortalaması
    try:
        key = Settings.objects.get(key='eskalasyon_api_key').value

        url = "https://evds2.tcmb.gov.tr/service/evds/"

        series = 'series=' + seri + '&'
        startDate = 'startDate=' + startDate + '&'
        endDate = 'endDate=' + endDate + '&'
        type = 'type=json&'
        key = 'key=' + key + '&'
        aggregationTypes = 'aggregationTypes=avg&'
        formulas = 'formulas=0&'
        frequency = 'frequency=5'

        url = url + series + startDate + endDate + type + key + aggregationTypes + formulas + frequency
        payload = {}
        headers = {
            'Cookie': 'SessionCookie=!Z78N3h3fWdr0f//qkygjtJLA5IKF7ZYBWbEt0TFirbUJcrbqBVPTlbzzj2q3s7dVx5GrxoxKZR0RwN4=; TS013c5758=015d31d6911ebe7c3a90785cc18d5719e8da6b2fd3f98252aeb94d76c86b5006761812066936d3857e3296b6ba1ffe608fa0ffb852c6149ea3eae64b4e661a7ce7ba034f33'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        x = json.loads(response.text)

        total = 0.0
        if seri == 'TP.DK.USD.S.YTL':
            seri = 'TP_DK_USD_S_YTL'
            seri_name = 'USD'

        else:
            seri = 'TP_DK_EUR_S_YTL'
            seri_name = 'EURO'

        for item in x['items']:
            print(item)
            total = total + float(item[seri])

        result = str(round(total / 3, 2))
        desc = 'Geçerli olacak 3 aylık dönemin ilk ayından önceki ' + month + '. ayların ' + seri_name + ' ortalaması'
        eskalasyon = Eskalasyon(series=seri, startDate=startDate, endDate=endDate, key=key,
                                aggregationTypes='avg', formulas='0', frequency='5', result=result,
                                result_description=desc)
        eskalasyon.save()

        result_dict = {
            'result': result,
            'eskalasyon_uuid': eskalasyon.uuid
        }

        return result_dict
    except Exception as e:
        traceback.print_exc()


def yeka_competition_eskalasyon(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)

    try:

        filter = {
            'is_calculation': True,
        }
        yeka_competitions = YekaCompetitionService(request, filter)
        for competition in yeka_competitions:
            EskalasyonCalculation(request, competition.uuid)
        return redirect('ekabis:yeka_report')
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
