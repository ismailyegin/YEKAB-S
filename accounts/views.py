import datetime
from django.contrib import auth, messages
from django.contrib.auth import logout
from django.contrib.auth.models import Group, User
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from accounts.models import Forgot
from ekabis.models import ActiveGroup, Person, HelpMenu
from ekabis.models.Settings import Settings
from ekabis.services import general_methods
from ekabis.urls import urlpatterns
from ekabis.models.Permission import Permission
from ekabis.models.PermissionGroup import PermissionGroup
from ekabis.services.services import UserService, UserGetService, EmployeeGetService, CompanyUserGetService, \
    ActiveGroupGetService


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
        login_user=None
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username):
            login_user = User.objects.get(username=username)
        filter = {
            'user': login_user
        }
        active_user = None
        user = auth.authenticate(username=username, password=password)

        if user:  # Şifrenin doğru girilmesi
            if user.is_superuser :
                auth.login(request, user)
                return redirect('ekabis:view_admin')
            person = Person.objects.get(user=login_user)

            if datetime.datetime.now() - person.failed_time < datetime.timedelta(
                        minutes=int(Settings.objects.get(key='failed_time').value)):
                    messages.warning(request, 'Çok Fazla Hatalı Girişten Dolayı ' + str(
                        datetime.datetime.now() - person.failed_time) + ' dk beklemelisiniz.')

                    return render(request, 'registration/login.html')
            else:
                    person.failed_login = 0
                    person.save()
            active = ActiveGroupGetService(request, filter)
            if not active:
                active = ActiveGroup(user=login_user, group=login_user.groups.all()[0])
                active.save()
            if active.group.name == 'Firma':
                auth.login(request, user)
                return redirect('ekabis:view_federasyon')
            elif active.group.name == 'Admin' or person.user.is_superuser:
                auth.login(request, user)
                return redirect('ekabis:view_admin')
            else:
                auth.login(request, user)
                return redirect('ekabis:view_personel')

        else: #Şifrenin yanlış girilme durumu
            if login_user:
                person = Person.objects.get(user=login_user)
                if person.failed_login == int(Settings.objects.get(key='failed_login').value):
                    wait_time = int(Settings.objects.get(key='failed_time').value)
                    if datetime.datetime.now() - person.failed_time > datetime.timedelta(
                            minutes=wait_time):
                        person.failed_login = 1
                        person.save()

                    else:
                        messages.warning(request, 'Çok Fazla Hatalı Girişten Dolayı Hesabınız ' + str(
                            wait_time) + ' dk Kilitlenmiştir.')
                        return render(request, 'registration/login.html')

                else:
                    person.failed_login =person.failed_login + 1
                    person.save()
                    if person.failed_login == int(Settings.objects.get(key='failed_login').value):
                        person.failed_time = datetime.datetime.now()
                        person.save()


        messages.warning(request, 'Mail Adresi Ve Şifre Uyumsuzluğu')

    return render(request, 'registration/login.html')




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
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    for entry in urlpatterns:
        perm = Permission(codename=entry.name, codeurl=entry.pattern.regex.pattern, name=entry.name)
        if not (Permission.objects.filter(codename=entry.name)):
            perm.save()

    # bütün yetkiler verildi
    groups = Group.objects.all()
    for group in groups:
        for item in Permission.objects.all():
            if not (PermissionGroup.objects.filter(group=group, permissions=item)):
                if group.name == 'Admin':
                    perm = PermissionGroup(group=group,
                                           permissions=item,
                                           is_active=True)
                else:
                    perm = PermissionGroup(group=group,
                                           permissions=item,
                                           is_active=False)

                perm.save()
    #Bütün url ler için yardım metni oluşturuldu.
    for item in Permission.objects.all():
            if not HelpMenu.objects.filter(url=item):
                help = HelpMenu(
                    text=" ",
                    url=item
                )
                help.save()
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
