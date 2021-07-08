from django.contrib import auth, messages
from django.contrib.auth import logout
from django.contrib.auth.models import Group, User
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.shortcuts import render, redirect
from accounts.models import Forgot
from ekabis.services import general_methods
# from accounts.forms import LoginForm

from ekabis.urls import urlpatterns
from ekabis.models.Permission import Permission
from ekabis.models.PermissionGroup import PermissionGroup

from ekabis.services.services import UserService

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

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            # correct username and password login the user
            auth.login(request, user)

            active = general_methods.controlGroup(request)
            log = general_methods.logwrite(request, request.user, " Giris yapti")
            # eger user.groups birden fazla ise klup üyesine gönder yoksa devam et

            # sms entegrasyonu yapılacak servis 2 tane yazılacak control //Berktug
            if active == 'Personel':
                return redirect('ekabis:view_personel')
            elif active == 'Yonetim':
                return redirect('ekabis:view_federasyon')

            elif active == 'Admin':
                return redirect('ekabis:view_admin')
            else:
                return redirect('accounts:view_logout')

        else:

            messages.warning(request, 'Mail Adresi Ve Şifre Uyumsuzluğu')
            return render(request, 'registration/login.html')

    return render(request, 'registration/login.html')

def forgot(request):
    if request.method == 'POST':
        mail = request.POST.get('username')
        userfilter={
            'username' : mail
        }
        if UserService(request,userfilter):
            user = UserService(request,userfilter)[0]
            user.is_active = True
            user.save()

            fdk = Forgot(user=user, status=False)
            fdk.save()

            html_content = ''
            subject, from_email, to = 'THF Bilgi Sistemi Kullanıcı Bilgileri', 'fatih@kobiltek.com', mail
            html_content = '<h2>YEKABİS</h2>'
            html_content = html_content + '<p><strong>Kullanıcı Adınız :' + str(fdk.user.username) + '</strong></p>'
            html_content = html_content + '<p> <strong>Site adresi:</strong> <a href="http://127.0.0.1:8000/newpassword?query=' + str(
                fdk.uuid) + '">http://127.0.0.1:8000/sbs/profil-guncelle/?query=' + str(fdk.uuid) + '</p></a>'
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
        perm = Permission(codename=entry.name, codeurl=entry.pattern.regex.pattern,name=entry.name)
        if not (Permission.objects.filter(codename=entry.name)):
            perm.save()

    # bütün yetkiler verildi
    groups=Group.objects.all()
    for group in groups:
        for item in Permission.objects.all():
            if not (PermissionGroup.objects.filter(group=group, permissions=item)):
                perm = PermissionGroup(group=group, permissions=item)
                perm.save()
    return redirect('accounts:login')
