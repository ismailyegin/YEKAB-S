import traceback
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
from django.contrib.admin.models import LogEntry
from django.contrib.auth import logout
from django.contrib.auth.models import User, Group
from django.contrib.messages import get_messages
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from django.urls import resolve, reverse
from django.utils.safestring import mark_safe
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from accounts.models import Forgot
from ekabis.models import Yeka, YekaPerson, HelpMenu, YekaCompetition, BusinessBlog, NotificationUser, YekaBusiness, \
    CalendarName, Calendar, YekaBusinessBlog, ConnectionRegion, CalendarYeka
from ekabis.models.ActiveGroup import ActiveGroup
from ekabis.models.Logs import Logs
from ekabis.models.Menu import Menu
from ekabis.models.PermissionGroup import PermissionGroup
from ekabis.models.Settings import Settings
from ekabis.models.YekaCompetitionPerson import YekaCompetitionPerson
from ekabis.services.services import ActiveGroupService, MenuService, EmployeeService, DirectoryMemberService, \
    UserService, PermissionGroupService, ActiveGroupGetService, EmployeeGetService, DirectoryMemberGetService, \
    YekaPersonService, YekaCompanyService, UserGetService, YekaCompetitionPersonService, CompanyUserGetService
from django.contrib import messages, auth

from ekabis.models.Permission import Permission
from ekabis.models.BlockEnumField import BlockEnumFields

import xml.etree.ElementTree as ET
from urllib.request import urlopen
import ssl


# from bs4 import BeautifulSoup
# import requests
from oxiterp.settings.base import EMAIL_HOST_USER


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def logwrite(request, user, log):
    try:
        logs = Logs(user=user, subject=log, ip=get_client_ip(request))
        logs.save()

        # Txt dosyaya kay??t
        # f = open("log.txt", "a")
        # log = get_client_ip(request) + "    [" + datetime.today().strftime('%d-%m-%Y %H:%M') + "] " + str(
        #     user) + " " + log + " \n "
        # f.write(log)
        # f.close()

    except Exception as e:
        f = open("log.txt", "a")
        log = "[" + datetime.today().strftime('%d-%m-%Y %H:%M') + "]  lag kaydetme hata   \n "
        f.write(log)
        f.close()

    return log


def getMenu(request):
    menus = MenuService(request, None)
    active = controlGroup(request)
    activefilter = {
        'group__name': active,
        'is_active': True

    }
    permGrup = PermissionGroupService(request, activefilter)
    menu = []
    activ_urls = None
    url = request.resolver_match.url_name
    if Permission.objects.filter(codename=request.resolver_match.url_name):
        login_url = Permission.objects.get(codename=request.resolver_match.url_name)
        if login_url:
            if login_url.parent:
                url = login_url.parent.codename
    for item in menus:
        if item.is_parent == False:
            if item.url:
                for tk in permGrup:
                    if tk.permissions.codename == item.url.split(":")[1]:
                        if url == item.url.split(":")[1]:
                            activ_urls = item
                        menu.append(item.pk)
                        menu.append(item.parent.pk)

                        pass

    menus = Menu.objects.filter(id__in=menu).distinct()
    return {'menus': menus, 'activ_url': activ_urls}


def control_access(request):
    is_exist = False
    groupfilter = {
        'user': request.user
    }
    if ActiveGroupService(request, groupfilter):
        aktifgroup = ActiveGroupGetService(request, groupfilter).group
        for perm in PermissionGroup.objects.filter(group=aktifgroup, is_active=True):
            if request.resolver_match.url_name == perm.permissions.codename:
                print('Okay')
                is_exist = True
    else:
        if request.user.groups.all():
            aktifgroup = ActiveGroup(
                user=request.user,
                group=request.user.groups.all()[0]
            )
            aktifgroup.save()
        else:
            logout(request)
            return is_exist

    if request.user.groups.filter(name="Admin"):
        is_exist = True
    return is_exist


def aktif(request):
    userfilter = {
        'pk': request.user.pk
    }
    if UserService(request, userfilter):
        activfilter = {
            'user': request.user
        }

        aktifgroup = None

        if not (ActiveGroupService(request, activfilter)):
            if request.user.groups.all():
                aktifgroup = ActiveGroup(user=request.user, group=request.user.groups.all()[0])
                aktifgroup.save()
                aktif = aktifgroup.group.name
            else:
                logout(request)
                return redirect('accounts:login')

        else:
            activfilter = {
                'user': request.user
            }
            aktifgroup = ActiveGroupGetService(request, activfilter)
            # aktifgroup = ActiveGroupService(request, activfilter)[0]
            aktif = aktifgroup.group.name
        perm = []

        groupfilter = {
            'group__id': aktifgroup.group.pk,
            'is_active': True
        }
        permission = PermissionGroupService(request, groupfilter)
        for item in permission:
            perm.append(item.permissions.codename)

        group = request.user.groups.all()
        return {'aktif': aktif,
                'group': group,
                'perm': perm,
                }
    else:
        return {}


def controlGroup(request):
    userfilter = {
        'pk': request.user.pk
    }
    if UserService(request, userfilter):
        activfilter = {
            'user': request.user
        }
        if not (ActiveGroupService(request, activfilter)):
            if request.user.groups.all():
                aktive = ActiveGroup(user=request.user, group=request.user.groups.all().last())
                aktive.save()
                active = request.user.groups.all().last().name
            else:
                logout(request)
                return redirect('accounts:login')

        else:
            activfilter = {
                'user': request.user
            }
            active = ActiveGroupGetService(request, activfilter)
            active = active.group.name
        return active

    else:
        return {}


def getProfileImage(request):
    if (request.user.id):
        userfilter = {
            'person__user': request.user
        }

        if request.user.groups.filter(name='Admin').exists():
            person = dict()
            person['profileImage'] = "profile/logo.png"
        elif request.user.groups.filter(name='Personel').exists():
            employee = EmployeeGetService(request, userfilter)
            person = employee.person.user
        elif request.user.groups.filter(name='Firma').exists():
            employee = CompanyUserGetService(request, userfilter)
            person = employee.person.user
        else:
            person = None
        return {'person': person}
    return {}


def get_notification(request):
    notifications = None
    date = None
    notification_count = 0
    if request.user.id:
        user = request.user
        notifications = NotificationUser.objects.filter(is_read=False, user=user).order_by('-creationDate')[:10]
        notification_count = NotificationUser.objects.filter(is_read=False, user=user).order_by('-creationDate').count()
        date = datetime.now().date()
    return {'notifications': notifications, 'date': date, 'notification_count': notification_count}


def get_error_messages(form):
    if form:
        error_messages = []
        for key in form.errors:
            for field in form.fields:
                if key == field:
                    entry = {'key': field, 'value': form.errors[key][0]}
                    error_messages.append(entry)
        return error_messages
    return {}


def get_help_text(request):
    current_url_name = resolve(request.path_info).url_name
    help_text = ''
    help_url = ''
    texts = HelpMenu.objects.filter(isDeleted=False)
    for text in texts:
        if text.url.codename == current_url_name:
            help_text = text.text
            help_url = text.uuid
            break
    return {'text': help_text
        , 'help_url': help_url}


def do_something_with_the_message(message):
    pass


def yeka_control(request, yeka):
    storage = get_messages(request)
    for message in storage:
        if message.level_tag == 'warning':
            return None
    message = []
    yekafilter = {
        'yeka': yeka
    }
    url = None
    # ??al??sma s??ras??na g??re  s??ralad??k ona g??re if d??ng??lerinin sonucunda deger alacak

    if not (yeka.business):
        messages.add_message(request, messages.WARNING, '???? Bloklar?? Bilgileri Eksik.')
        url = "view_yekabusinessBlog"

    # if not (YekaCompanyService(request,yekafilter)):
    #     messages.add_message(request, messages.WARNING, 'Firma Bilgileri Eksik.')
    #     url="view_yeka_company"

    # if not (YekaPersonService(request, yekafilter)):
    #     messages.add_message(request, messages.WARNING, 'Personel Bilgileri Eksik.')
    #     url = "view_yeka_personel"
    if url:
        return url
    else:
        return None


def competition_control(request, competiton):
    storage = get_messages(request)
    for message in storage:
        if message.level_tag == 'warning':
            return None
    message = []

    url = None
    # ??al??sma s??ras??na g??re  s??ralad??k ona g??re if d??ng??lerinin sonucunda deger alacak

    if not (competiton.business):
        messages.add_message(request, messages.WARNING, '???? Bloklar?? Bilgileri Eksik.')
        url = "view_competitionbusinessblog"

    # if not (YekaCompanyService(request,yekafilter)):
    #     messages.add_message(request, messages.WARNING, 'Firma Bilgileri Eksik.')
    #     url="view_yeka_company"

    # if not (YekaCompetitionPersonService(request, {'competition': competiton})):
    #     messages.add_message(request, messages.WARNING, 'Personel Bilgileri Eksik.')
    #     url = "view_yekacompetition_personel"
    if url:
        return url
    else:
        return None


def sendmail(request, pk):
    try:
        userfilter = {
            'pk': pk
        }
        user = UserGetService(request, userfilter)
        fdk = Forgot(user=user, status=False)
        fdk.save()

        subject, from_email, to = 'Yekabis Kullan??c?? Bilgileri', 'fatih@kobiltek.com', user.email
        html_content = '<h2>YEKAB??S</h2>'
        html_content = html_content + '<p><strong>Kullan??c?? Ad??n??z :' + str(fdk.user.username) + '</strong></p>'
        html_content = html_content + '<p> <strong>Aktivasyon adresi:</strong> <a href="http://127.0.0.1:8000/newpassword?query=' + str(
            fdk.uuid) + '">/sbs/profil-guncelle/?query=' + str(fdk.uuid) + '</p></a>'

        msg = EmailMultiAlternatives(subject, '', from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        log = str(user.get_full_name()) + "yeni ??ifre emaili g??nderildi"
        log = logwrite(request, fdk.user, log)

        return True
    except Exception as e:
        traceback.print_exc()


# g??nderilen parametrenin sabit mi oldugu kontrol edilecek kontrol icin i?? blogu g??nderilmeli onun i??inde bak??lmal?? -
def fixed_block_parameeter_control(request, block_name, parameter_name):
    try:
        is_active = False
        if BlockEnumFields.fixed_blocks.value:
            for item in BlockEnumFields.fixed_blocks.value:
                if item['tr_name'] == block_name:
                    if item['fixed_parameter']:
                        for k in item['fixed_parameter']:
                            print(k['name'])
                            if k['name'] == parameter_name:
                                is_active = True
        return is_active
    except Exception as e:
        traceback.print_exc()


# bu deger sabit bir blok mu kontrol yap??ld??
def fixed_block_control(request, name):
    try:
        is_active = False
        if BlockEnumFields.fixed_blocks.value:
            for item in BlockEnumFields.fixed_blocks.value:
                if item['tr_name'] == name:
                    is_active = True
        return is_active
    except Exception as e:
        traceback.print_exc()


def log(request):
    try:
        log = Logs()
        log.user = request.user
        log.ip = get_client_ip(request)
        url = Permission.objects.get(codename=request.resolver_match.url_name).name
        log.subject = url
        return log
    except Exception as e:
        traceback.print_exc()


def log_model(request, pre, next):
    try:
        log = Logs()
        log.user = request.user
        log.ip = get_client_ip(request)
        url = Permission.objects.get(codename=request.resolver_match.url_name).name
        log.subject = url
        log.previousData = pre
        log.nextData = next
        log.save()
        return log
    except Exception as e:
        traceback.print_exc()


def yekaname(yekabusiness):
    name = None
    path = ''
    html = ''
    if Yeka.objects.filter(business=yekabusiness):
        yeka = Yeka.objects.get(business=yekabusiness)
        path = redirect('ekabis:view_yeka_detail', yeka.uuid).url
        html = '<a href="' + path + '">' + yeka.definition + '</a>'
    elif YekaCompetition.objects.filter(business=yekabusiness):
        yeka = YekaCompetition.objects.get(business=yekabusiness)
        if yeka.parent:
            path = redirect('ekabis:view_sub_yeka_competition_detail', yeka.uuid).url
            html = '<a href="' + path + '">' + yeka.name + '</a>'
        else:
            path = redirect('ekabis:view_yeka_competition_detail', yeka.uuid).url
            html = '<a href="' + path + '">' + yeka.name + '</a>'
    return mark_safe(html)


def kur():
    # kur bilgilerinin al??nd??g?? alan
    url = "https://www.tcmb.gov.tr/kurlar/today.xml"
    gcontext = ssl.SSLContext()  # Only for gangstars
    info = urlopen(context=gcontext, url=url)
    tree = ET.parse(info)
    root = tree.getroot()
    son = {}
    data = []
    i = 0
    for kurlars in root.findall('Currency'):
        Kod = kurlars.get('Kod')
        Unit = kurlars.find('Unit').text  # <Unit>1</Unit>
        isim = kurlars.find('Isim').text  # <Isim>ABD DOLARI</Isim>
        CurrencyName = kurlars.find('CurrencyName').text  # <CurrencyName>US DOLLAR</CurrencyName>
        ForexBuying = kurlars.find('ForexBuying').text  # <ForexBuying>2.9587</ForexBuying>
        ForexSelling = kurlars.find('ForexSelling').text  # <ForexSelling>2.964</ForexSelling>
        BanknoteBuying = kurlars.find('BanknoteBuying').text  # <BanknoteBuying>2.9566</BanknoteBuying>
        BanknoteSelling = kurlars.find('BanknoteSelling').text  # <BanknoteSelling>2.9684</BanknoteSelling>
        CrossRateUSD = kurlars.find('CrossRateUSD').text  # <CrossRateUSD>1</CrossRateUSD>
        son = {
            "Kod": Kod,
            "isim": isim,
            "CurrencyName": CurrencyName,
            "Unit": Unit,
            "ForexBuying": ForexBuying,
            "ForexSelling": ForexSelling,
            "BanknoteBuying": BanknoteBuying,
            "BanknoteSelling": BanknoteSelling,
            "CrossRateUSD": CrossRateUSD
        }
        data.append(son)
    return data


# def ufe():
#     # ??fe t??fe bilgilerinin al??nd??g?? alan
#     data = []
#
#     url = "https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/Istatistikler/Enflasyon+Verileri/Uretici+Fiyatlari"
#     response = requests.get(url)
#     html_icerigi = response.content
#     soup = BeautifulSoup(html_icerigi, "html.parser")
#     tr = soup.find_all("tr")
#     data = []
#     for td in tr:
#         if td.find_all("strong"):
#             print(td.text)
#             test = td.text.split('\n')
#         else:
#             print(td.text)
#             t = td.text.split('\n')
#             if len(t) == 7 and t:
#                 beka = {
#                     'date': t[1],
#                     'yiufe': t[2],
#                     'ufe': t[3],
#                     'yitufe': t[4],
#                     'tufe': t[5],
#                 }
#                 data.append(beka)
#     return data


def add_block(request):
    try:
        if BlockEnumFields.fixed_blocks.value:
            for item in BlockEnumFields.fixed_blocks.value:
                if not BusinessBlog.objects.filter(name=item['tr_name']):
                    block = BusinessBlog()
                    block.name = item['tr_name']
                    block.start_notification = 2
                    block.finish_notification = 2
                    block.save()
        return redirect('ekabis:view_admin')
    except Exception as e:
        traceback.print_exc()
        return redirect('ekabis:view_admin')


def initial_data(request):
    try:
        settings = Settings.objects.all()
        if not settings:
            setting = Settings(key='maintenance', value=False)
            setting.save()
            setting = Settings(key='mail_companyuser', value=False)
            setting.save()
            setting = Settings(key='mail_person', value=False)
            setting.save()
            setting = Settings(key='mail_company_user', value=False)
            setting.save()
            setting = Settings(key='failed_login', value=2, label='Ba??ar??s??z Giri?? Say??s??')
            setting.save()
            setting = Settings(key='failed_time', value=2, label='Ba??ar??s??z Giri?? Bekleme S??resi')
            setting.save()
            setting = Settings(key='logout_time', value=60, label='Oturum A????k Kalma S??resi')
            setting.save()
            return redirect('ekabis:initial_data_success_page')
        else:
            return redirect('ekabis:initial_data_error_page')
    except Exception as e:
        traceback.print_exc()
        return redirect('ekabis:initial_data_error_page')


def yekaMenus(request):
    yekas = Yeka.objects.filter(isDeleted=False).order_by('-date')
    comp_array = []

    for yeka in yekas:
        yeka_dict = dict()
        competitions = []
        regions = yeka.connection_region.filter(isDeleted=False).order_by('name')
        for region in regions:
            for comp in region.yekacompetition.filter(isDeleted=False):
                competitions.append(comp)
        yeka_dict['yeka'] = yeka
        yeka_dict['regions'] = regions
        comp_array.append(yeka_dict)

    return {'yeka_competition_array': comp_array}


def yekaBusinessPlanReminder(request):
    date_now = datetime.now()
    yekas = YekaCompetition.objects.filter(isDeleted=False)

    for yeka in yekas:
        if yeka.business:
            business_block_actives = yeka.business.businessblogs.filter(status='3')
            if business_block_actives.count() == 1:
                business_block_active = yeka.business.businessblogs.get(status='3')
                block_date = business_block_active.startDate
                end_date = YekaBusinessBlog.objects.filter(pk=business_block_active.parent.pk)
                if end_date:
                    end_date = YekaBusinessBlog.objects.get(parent__id=business_block_active.pk)
                else:
                    end_date = business_block_active
                if ConnectionRegion.objects.filter(yekacompetition=yeka):
                    region = ConnectionRegion.objects.get(yekacompetition=yeka)
                    yeka_name = Yeka.objects.get(connection_region=region).definition
                    if not CalendarYeka.objects.filter(
                            calendarName__name=yeka_name + '-' + yeka.name + '-' + business_block_active.businessblog.name,
                            competition=yeka):
                        if business_block_active.startDate - timedelta(
                                days=business_block_active.businessblog.start_notification) <= date_now and date_now <= business_block_active.startDate + timedelta(
                            days=business_block_active.businessblog.finish_notification):
                            if yeka.parent:
                                comp_name = yeka_name + ' - ' + yeka.parent.name + ' - ' + yeka.name + ' - ' + business_block_active.businessblog.name
                            else:
                                comp_name = yeka_name + '-' + yeka.name + '-' + business_block_active.businessblog.name
                            new_calender = CalendarName(name=comp_name, color='#fff453')
                            new_calender.save()
                            calender = CalendarYeka(calendarName=new_calender, competition=yeka,
                                                    startDate=block_date, finishDate=end_date.startDate)
                            calender.save()

                            html_content = ''
                            subject, from_email, to = 'YEKAB??S ???? Plan??', 'byurdakul@kobiltek.com', EMAIL_HOST_USER
                            html_content += '<strong>Bu bir hat??rlatma mailidir.</strong>'
                            html_content += '<h4>'+comp_name+'</h4>'
                            html_content += '<p>???? blo??unun i?? yap??lma tarihine kalan g??n say??s?? : <strong>'+str((business_block_active.startDate-date_now).days)+'</strong> !! </p>'


                            msg = EmailMultiAlternatives(subject, '', from_email, [to])
                            msg.attach_alternative(html_content, "text/html")
                            msg.send()
                    else:
                        calender_yeka = CalendarYeka.objects.get(
                            calendarName__name=yeka_name + '-' + yeka.name + '-' + business_block_active.businessblog.name,
                            competition=yeka)
                        if not (calender_yeka.startDate - timedelta(
                                days=business_block_active.businessblog.start_notification) <= date_now and date_now <= calender_yeka.startDate + timedelta(
                            days=business_block_active.businessblog.finish_notification)):
                            calender_yeka.delete()

    return {'calender_nots': CalendarYeka.objects.filter(is_active=True)}
