import datetime
import json

from captcha.helpers import captcha_image_url, captcha_audio_url
from captcha.models import CaptchaStore
from django.contrib import auth, messages
from django.contrib.auth import logout
from django.contrib.auth.models import Group, User
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import timezone

from accounts.forms import LoginForm, CaptchaForm
from accounts.models import Forgot
from ekabis.models import Employee, CompanyUser
from ekabis.models.Settings import Settings
from ekabis.services import general_methods
# from accounts.forms import LoginForm

from ekabis.urls import urlpatterns
from ekabis.models.Permission import Permission
from ekabis.models.PermissionGroup import PermissionGroup

from ekabis.services.services import UserService, UserGetService, EmployeeGetService, PersonGetService, \
    CompanyUserGetService, ActiveGroupService, ActiveGroupGetService
from oxiterp import settings


def index(request):
    return render(request, 'accounts/index.html')


def pagelogout(request):
    log = general_methods.logwrite(request, request.user, "  Cikis yapti ")
    logout(request)

    return redirect('accounts:login')


def login(request):
    if request.user.is_authenticated is True:
        # aktif rol şeklinde degişmeli
        return redirect('ekabis:view_admin')
    form = CaptchaForm()

    if request.method == 'POST':
        form = CaptchaForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            login_user = User.objects.get(username=username)
            filter = {
                'user': login_user
            }
            active = ActiveGroupGetService(request, filter)
            active_user = None
            user = auth.authenticate(username=username, password=password)

            if active:
                if active.group.name == 'Firma':
                    active_user = CompanyUserGetService(request, filter)
                elif active.group.name == 'Admin':
                    if user is not None:
                        user.is_active = True
                        user.save()
                        auth.login(request, user)
                        log = general_methods.logwrite(request, request.user, " Giris yapti")
                        return redirect('ekabis:view_admin')
                    messages.warning(request, 'Mail Adresi Ve Şifre Uyumsuzluğu')
                    return render(request, 'registration/login.html')
                else:
                    active_user = EmployeeGetService(request, filter)

                if user is not None and datetime.datetime.now() - active_user.person.failed_time >= datetime.timedelta(
                        minutes=5):
                    login_user.is_active = True
                    login_user.save()
                    active_user.person.failed_login = 0
                    active_user.person.save()
                    # correct username and password login the user
                    auth.login(request, user)
                    active = general_methods.controlGroup(request)
                    log = general_methods.logwrite(request, request.user, " Giris yapti")
                    # eger user.groups birden fazla ise klup üyesine gönder yoksa devam et

                    # sms entegrasyonu yapılacak servis 2 tane yazılacak control //Berktug
                    if active == 'Personel':
                        return redirect('ekabis:view_personel')
                    if active == 'Firma':
                        return redirect('ekabis:view_federasyon')
                    else:
                        return redirect('accounts:view_logout')

                else:
                    if active_user.person.failed_login == int(Settings.objects.get(key='failed_login').value):
                        wait_time = int(Settings.objects.get(key='failed_time').value)
                        if datetime.datetime.now() - active_user.person.failed_time > datetime.timedelta(
                                minutes=wait_time):
                            login_user.is_active = True
                            login_user.save()
                            active_user.person.failed_login = 1
                            active_user.person.save()

                        else:
                            messages.warning(request, 'Çok Fazla Hatalı Girişten Dolayı Hesabınız ' + str(
                                wait_time) + ' dk Kilitlenmiştir.')
                            return render(request, 'registration/login.html')

                    else:
                        active_user.person.failed_login = active_user.person.failed_login + 1
                        active_user.person.save()
                        if active_user.person.failed_login == int(Settings.objects.get(key='failed_login').value):
                            active_user.person.failed_time = datetime.datetime.now()
                            active_user.person.save()
                            login_user.is_active = False
                            login_user.save()
                messages.warning(request, 'Mail Adresi Ve Şifre Uyumsuzluğu')
                return render(request, 'registration/login.html',{'form': form})

    return render(request, 'registration/login.html', {'form': form})


def forgot(request):
    if request.method == 'POST':
        mail = request.POST.get('username')
        userfilter = {
            'username': mail
        }
        if UserService(request, userfilter):
            user = UserGetService(request, userfilter)
            user.is_active = True
            user.save()

            fdk = Forgot(user=user, status=False)
            fdk.save()

            html_content = ''
            subject, from_email, to = 'Yekabis Kullanıcı Bilgileri', 'fatih@kobiltek.com', mail
            html_content = '<h2>YEKABİS</h2>'
            html_content = html_content + '<p><strong>Kullanıcı Adınız :' + str(fdk.user.username) + '</strong></p>'
            html_content = html_content + '<p> <strong>Site adresi:</strong> <a href="http://127.0.0.1:8000/newpassword?query=' + str(
                fdk.uuid) + '">/sbs/profil-guncelle/?query=' + str(fdk.uuid) + '</p></a>'
            # html_content = html_content + '<p> <strong>Site adresi:</strong> <a href="http://sbs.badminton.gov.tr/newpassword?query=' + str(
            #     fdk.uuid) + '">http://sbs.badminton.gov.tr/sbs/profil-guncelle/?query=' + str(fdk.uuid) + '</p></a>'

            msg = EmailMultiAlternatives(subject, '', from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            log = str(user.get_full_name()) + "yeni şifre emaili gönderildi"
            log = general_methods.logwrite(request, fdk.user, log)

            messages.success(request, "Giriş bilgileriniz mail adresinize gönderildi. ")
            return redirect("accounts:login")
        else:
            messages.warning(request, "Geçerli bir mail adresi giriniz.")
            return redirect("accounts:view_forgot")

    return render(request, 'registration/forgot-password.html')


def show_urls(request):
    for entry in urlpatterns:
        perm = Permission(codename=entry.name, codeurl=entry.pattern.regex.pattern, name=entry.name)
        if not (Permission.objects.filter(codename=entry.name)):
            perm.save()

    # bütün yetkiler verildi
    groups = Group.objects.all()
    for group in groups:
        for item in Permission.objects.all():
            if not (PermissionGroup.objects.filter(group=group, permissions=item)):
                perm = PermissionGroup(group=group,
                                       permissions=item,
                                       is_active=True)
                perm.save()
    return redirect('accounts:login')





def handler404(request, *args, **argv):
    return redirect('accounts:handler404template')

def handler500(request, *args, **argv):
    return redirect('accounts:handler500template')

def handle400Template(request):
    return render(request, '404.html')

def handle500Template(request):
    return render(request, '500.html')


def handler404(request, *args, **argv):
    return redirect('accounts:404')


def handler500(request, *args, **argv):
    return redirect('accounts:500')


def handle400Template(request):
    return render(request, 'Ayar/404.html')


def handle500Template(request):
    return render(request, 'Ayar/500.html')
