from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

from sbs.Forms.UserForm import UserForm
from sbs.Forms.UserSearchForm import UserSearchForm
from accounts.models import Forgot
from sbs.models import SportClubUser, Person, Communication
from sbs.services import general_methods

from unicode_tr import unicode_tr


@login_required
def return_users(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    users = User.objects.none()
    user_form = UserSearchForm()
    if request.method == 'POST':
        user_form = UserSearchForm(request.POST)
        if user_form.is_valid():

            firstName = unicode_tr(request.POST.get('first_name')).upper()
            lastName = unicode_tr(request.POST.get('last_name')).upper()
            email = user_form.cleaned_data.get('email')
            active = request.POST.get('is_active')
            if not (firstName or lastName or email or active):
                users = User.objects.all()
            else:
                query = Q()
                if lastName:
                    query &= Q(last_name__icontains=lastName)
                if firstName:
                    query &= Q(first_name__icontains=firstName)
                if email:
                    query &= Q(email__icontains=email)
                if active == 'True':
                    query &= Q(is_active=True)
                if active == 'False':
                    query &= Q(is_active=False)
                users = User.objects.filter(query)
    return render(request, 'kullanici/kullanicilar.html', {'users': users, 'user_form': user_form})


@login_required
def update_user(request, pk):
    user = User.objects.get(pk=pk)
    user_form = UserForm(request.POST or None, instance=user)


    if request.method == 'POST':

        if user_form.is_valid():

            user.username = user_form.cleaned_data['email']

            user.first_name = unicode_tr(user_form.cleaned_data['first_name']).upper()
            user.last_name = unicode_tr(user_form.cleaned_data['last_name']).upper()
            user.email = user_form.cleaned_data['email']

            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Kullanıcı Başarıyla Güncellendi')
            return redirect('sbs:kullanicilar')
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'kullanici/kullanici-duzenle.html',
                  {'user_form': user_form})


@login_required
def active_user(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():

        obj = User.objects.get(pk=pk)
        if obj.is_active:
            obj.is_active = False
            obj.save()
        else:
            obj.is_active = True
            obj.save()

        log = str(obj.get_full_name()) + " ->" + str(obj.is_active) + "Durumu degiştirildi "
        log = general_methods.logwrite(request, request.user, log)
        return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})



@login_required
def send_information(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():

        user = User.objects.get(pk=pk)

        if not user.is_active:
            return JsonResponse({'status': 'Fail', 'msg': 'Kullanıcıyı aktifleştirin.'})
        fdk = Forgot(user=user, status=False)
        fdk.save()


        html_content = ''
        subject, from_email, to = 'Taekwondo Bilgi Sistemi Kullanıcı Bilgileri', 'taekwondo@kobiltek.com', user.email
        html_content = '<h2>TÜRKİYE TAEKWONDO FEDERASYONU BİLGİ SİSTEMİ</h2>'
        html_content = html_content + '<p><strong>Kullanıcı Adınız :' + str(fdk.user.username) + '</strong></p>'
        html_content = html_content + '<p> <strong>Site adresi:</strong> <a href="http://172.16.5.25/TaekwondoArsiv/newpassword?query=' + str(
            fdk.uuid) + '">http://172.16.5.25/sbs/profil-guncelle/?query=' + str(fdk.uuid) + '</p></a>'
        msg = EmailMultiAlternatives(subject, '', from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        log = str(user.get_full_name()) + " sifre gonderildi"
        log = general_methods.logwrite(request, request.user, log)

        return JsonResponse({'status': 'Success', 'msg': 'Şifre başarıyla gönderildi'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
