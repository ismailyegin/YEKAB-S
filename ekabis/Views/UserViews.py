import traceback

from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from ekabis.Forms.UserForm import UserForm
from ekabis.Forms.UserSearchForm import UserSearchForm
from accounts.models import Forgot
from ekabis.services import general_methods
from ekabis.services.services import UserService


@login_required
def return_users(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    users = User.objects.none()
    user_form = UserSearchForm()
    try:
        with transaction.atomic():
            if request.method == 'POST':

                user_form = UserSearchForm(request.POST)
                if user_form.is_valid():
                    firstName = user_form.cleaned_data.get('first_name')
                    lastName = user_form.cleaned_data.get('last_name')
                    email = user_form.cleaned_data.get('email')
                    active = request.POST.get('is_active')
                    print(active)
                    if not (firstName or lastName or email or active):
                        users = UserService(request, None)
                    else:
                        query = Q()
                        if lastName:
                            query &= Q(last_name__icontains=lastName)
                        if firstName:
                            query &= Q(first_name__icontains=firstName)
                        if email:
                            query &= Q(email__icontains=email)
                        if active == 'True':
                            print(active)
                            query &= Q(is_active=True)
                        if active == 'False':
                            query &= Q(is_active=False)
                        users = UserService(request, query)

            return render(request, 'kullanici/kullanicilar.html', {'users': users, 'user_form': user_form})
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')


@login_required
def update_user(request, pk):
    userfilter = {
        'pk': pk
    }
    user = UserService(request, userfilter).first()
    user_form = UserForm(request.POST or None, instance=user)
    try:
        with transaction.atomic():
            if request.method == 'POST':

                if user_form.is_valid():
                    user.username = user_form.cleaned_data['email']
                    user.first_name = user_form.cleaned_data['first_name']
                    user.last_name = user_form.cleaned_data['last_name']
                    user.email = user_form.cleaned_data['email']
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, 'Kullanıcı Başarıyla Güncellendi')
                    return redirect('ekabis:view_user')
                else:
                    messages.warning(request, 'Alanları Kontrol Ediniz')

        return render(request, 'kullanici/kullanici-duzenle.html',
                      {'user_form': user_form})

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')


@login_required
def active_user(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():

                userfilter = {
                    'pk': pk
                }

                obj = UserService(request, userfilter).first()
                if obj.is_active:
                    obj.is_active = False
                    obj.save()
                else:
                    obj.is_active = True
                    obj.save()
                print(obj.is_active)
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})


            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')


@login_required
def send_information(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():

                userfilter = {
                    'pk': pk
                }

                user = UserService(request, userfilter)

                if not user.is_active:
                    return JsonResponse({'status': 'Fail', 'msg': 'Kullanıcıyı aktifleştirin.'})
                fdk = Forgot(user=user, status=False)
                fdk.save()
                html_content = ''
                subject, from_email, to = 'Etut Proje Bilgi Sistemi Kullanıcı Bilgileri', 'etutproje@kobiltek.com', user.email
                html_content = '<h2>ADALET BAKANLIGI PROJE TAKİP  SİSTEMİ</h2>'
                html_content = html_content + '<p><strong>Kullanıcı Adınız :' + str(fdk.user.username) + '</strong></p>'
                # html_content = html_content + '<p> <strong>Site adresi:</strong> <a href="http://127.0.0.1:8000/newpassword?query=' + str(
                #     fdk.uuid) + '">http://127.0.0.1:8000/sbs/profil-guncelle/?query=' + str(fdk.uuid) + '</p></a>'
                html_content = html_content + '<p> <strong>Yeni şifre oluşturma linki:</strong> <a href="https://www.kobiltek.com:81/etutproje/sbs/newpassword?query=' + str(
                    fdk.uuid) + '">https://www.kobiltek.com:81/etutproje/sbs/profil-guncelle/?query=' + str(
                    fdk.uuid) + '</p></a>'
                msg = EmailMultiAlternatives(subject, '', from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                log = general_methods.logwrite(request, " Yeni giris maili gönderildi" + str(user))
                return JsonResponse({'status': 'Success', 'msg': 'Şifre başarıyla gönderildi'})

            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
