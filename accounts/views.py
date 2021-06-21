from django.contrib import auth, messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import Group, Permission, User
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.shortcuts import render, redirect
# from zeep import Client

from accounts.models import Forgot
from ekabis import urls

from ekabis.models.Communication import Communication

from ekabis.models.Person import Person

from ekabis.services import general_methods



def index(request):
    return render(request, 'accounts/index.html')


def login(request):
    if request.user.is_authenticated is True:
        # aktif rol şeklinde degişmeli
        return redirect('ekabis:admin')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            # correct username and password login the user
            auth.login(request, user)

            # print(general_methods.get_client_ip(request))

            active = general_methods.controlGroup(request)
            log = general_methods.logwrite(request, request.user, " Giris yapti")
            # eger user.groups birden fazla ise klup üyesine gönder yoksa devam et

            if active == 'Personel':
                return redirect('ekabis:personel')

            elif active == 'Yonetim':
                return redirect('ekabis:federasyon')

            elif active == 'Admin':
                return redirect('ekabis:admin')

            else:
                return redirect('accounts:logout')

        else:

            messages.warning(request, 'Mail Adresi Ve Şifre Uyumsuzluğu')
            return render(request, 'registration/login.html')

    return render(request, 'registration/login.html')


# def forgot(request):
#     if request.method == 'POST':
#         mail = request.POST.get('username')
#         obj = User.objects.filter(username=mail)
#         if obj.count() != 0:
#             obj = obj[0]
#             password = User.objects.make_random_password()
#             obj.set_password(password)
#             # form.cleaned_data['password'] = make_password(form.cleaned_data['password'])
#
#             user = obj.save()
#             html_content = ''
#
#             subject, from_email, to = 'TWF Bilgi Sistemi Kullanıcı Bilgileri', 'no-reply@twf.gov.tr', obj.email
#             html_content = '<h2>Aşağıda ki bilgileri kullanarak sisteme giriş yapabilirsiniz.</h2>'
#             html_content = html_content+'<p> <strong>Site adresi:</strong> <a href="http://sbs.twf.gov.tr:81"></a>sbs.twf.gov.tr:81</p>'
#             html_content = html_content + '<p><strong>Kullanıcı Adı:</strong>' + obj.username + '</p>'
#             html_content = html_content + '<p><strong>Şifre:</strong>' + password + '</p>'
#             msg = EmailMultiAlternatives(subject, '', from_email, [to])
#             msg.attach_alternative(html_content, "text/html")
#             msg.send()
#
#             messages.success(request, "Giriş bilgileriniz mail adresinize gönderildi. ")
#             return redirect("accounts:login")
#         else:
#             messages.warning(request, "Geçerli bir mail adresi giriniz.")
#             return redirect("accounts:forgot")
#
#     return render(request, 'registration/forgot-password.html')



def pagelogout(request):
    log = "  Cikis yapti "
    log = general_methods.logwrite(request, request.user, log)
    logout(request)

    return redirect('accounts:login')


def mail(request):
    return redirect('accounts:login')


def groups(request):
    group = Group.objects.all()

    return render(request, 'permission/groups.html', {'groups': group})



@login_required
def permission(request, pk):
    general_methods.show_urls(urls.urlpatterns, 0)
    group = Group.objects.get(pk=pk)
    menu = ""
    ownMenu = ""

    groups = group.permissions.all()
    per = []
    menu2 = []

    for gr in groups:
        per.append(gr.codename)

    ownMenu = group.permissions.all()

    menu = Permission.objects.all()

    for men in menu:
        if men.codename in per:
            print("echo")
        else:
            menu2.append(men)

    return render(request, 'permission/izin-ayar.html',
                  {'menu': menu2, 'ownmenu': ownMenu, 'group': group})


@login_required
def permission_post(request):
    if request.POST:
        try:
            permissions = request.POST.getlist('values[]')
            group = Group.objects.get(pk=request.POST.get('group'))

            group.permissions.clear()
            group.save()
            if len(permissions) == 0:
                return JsonResponse({'status': 'Success', 'messages': 'Sınıf listesi boş'})
            else:
                for id in permissions:
                    perm = Permission.objects.get(pk=id)
                    group.permissions.add(perm)

            group.save()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Permission.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


def updateUrlProfile(request):
    if request.method == 'GET':
        try:
            data = request.GET.get('query')
            gelen = Forgot.objects.get(uuid=data)
            user = gelen.user
            password_form = SetPasswordForm(user)
            if gelen.status == False:
                gelen.status = True
                gelen.save()
                return render(request, 'registration/newPassword.html',
                              {'password_form': password_form})

            else:
                return redirect('accounts:login')
        except:
            return redirect('accounts:login')

    if request.method == 'POST':
        try:
            gelen = Forgot.objects.get(uuid=request.GET.get('query'))
            password_form = SetPasswordForm(gelen.user, request.POST)
            user = gelen.user
            if password_form.is_valid():
                user.set_password(password_form.cleaned_data['new_password1'])
                user.save()
                # zaman kontrolüde yapilacak
                gelen.status = True
                messages.success(request, 'Şifre Başarıyla Güncellenmiştir.')

                return redirect('accounts:login')


            else:

                messages.warning(request, 'Alanları Kontrol Ediniz')
                return render(request, 'registration/newPassword.html',
                              {'password_form': password_form})
        except:
            return redirect('accounts:login')

    return render(request, 'accounts/index.html')


def forgot(request):
    if request.method == 'POST':
        mail = request.POST.get('username')
        obj = User.objects.filter(username=mail)
        if obj.count() != 0:
            user = User.objects.get(username=mail)
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
            return redirect("accounts:forgot")

    return render(request, 'registration/forgot-password.html')

