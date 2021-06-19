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
from sbs import urls
from sbs.Forms.ClubForm import ClubForm
from sbs.Forms.CommunicationForm import CommunicationForm
from sbs.Forms.IbanCoachForm import IbanCoachForm
from sbs.Forms.IbanFormJudge import IbanFormJudge
from sbs.Forms.MaterialForm import MaterialForm
from sbs.Forms.PersonForm import PersonForm
from sbs.Forms.PreRegidtrationForm import PreRegistrationForm
from sbs.Forms.ReferenceCoachForm import RefereeCoachForm
from sbs.Forms.ReferenceRefereeForm import RefereeForm
from sbs.Forms.SportClubUserForm import SportClubUserForm
from sbs.Forms.UserForm import UserForm
from sbs.models import SportsClub, \
    SportClubUser, CategoryItem, Coach
from sbs.models.Communication import Communication
from sbs.models.Competition import Competition
from sbs.models.Judge import Judge
from sbs.models.Material import Material
from sbs.models.Person import Person
from sbs.models.PreRegistration import PreRegistration
from sbs.models.ReferenceCoach import ReferenceCoach
from sbs.models.ReferenceReferee import ReferenceReferee
from sbs.services import general_methods



def index(request):
    return render(request, 'accounts/index.html')


def login(request):
    if request.user.is_authenticated is True:
        # aktif rol şeklinde degişmeli
        return redirect('sbs:admin')

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

            if active == 'KlupUye':
                return redirect('ekabis:kulup-uyesi')

            elif active == 'Antrenor':
                return redirect('ekabis:antrenor')

            elif active == 'Hakem':
                return redirect('ekabis:hakem')

            elif active == 'Sporcu':
                return redirect('ekabis:sporcu')

            elif active == 'Yonetim':
                return redirect('ekabis:federasyon')

            elif active == 'Admin':
                return redirect('ekabis:admin')
            elif active == 'Arsiv':
                return redirect('ekabis:evrak-anasayfa')
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


def pre_registration(request):
    PreRegistrationform = PreRegistrationForm()

    if request.method == 'POST':
        PreRegistrationform = PreRegistrationForm(request.POST or None, request.FILES or None)

        mail = request.POST.get('email')

        if User.objects.filter(email=mail) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
                email=mail) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
            email=mail) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(
            email=mail):
            messages.warning(request, 'Mail adresi başka bir kullanici tarafından kullanilmaktadir.')
            return render(request, 'registration/cluppre-registration.html',
                          {'preRegistrationform': PreRegistrationform})

        tc = request.POST.get('tc')
        if Person.objects.filter(tc=tc) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
                tc=tc) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
            tc=tc) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(tc=tc):
            messages.warning(request, 'Tc kimlik numarasi sistemde  kayıtlıdır. ')
            return render(request, 'registration/cluppre-registration.html',
                          {'preRegistrationform': PreRegistrationform})

        # name = request.POST.get('first_name')
        # surname = request.POST.get('last_name')
        # year = request.POST.get('birthDate')
        # year = year.split('/')
        # 
        # client = Client('https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL')
        # if not (client.service.TCKimlikNoDogrula(tc, name, surname, year[2])):
        #     messages.warning(request,
        #                      'Tc kimlik numarasi ile isim  soyisim dogum yılı  bilgileri uyuşmamaktadır. ')
        #     return render(request, 'registration/cluppre-registration.html',
        #                   {'preRegistrationform': PreRegistrationform})

        # -------------------------------------

        if PreRegistrationform.is_valid():
            PreRegistrationform.save()
            messages.success(request,
                             "Başarili bir şekilde kayıt başvurunuz alındı Yetkili onayından sonra girdiginiz mail adresinize gelen mail ile Spor Bilgi Sistemine  giris yapabilirsiniz.")
            return redirect('accounts:login')


        else:
            messages.warning(request, "Alanlari kontrol ediniz")

    return render(request, 'registration/cluppre-registration.html', {'preRegistrationform': PreRegistrationform})


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


def adminlte(request):

    return render(request, 'accounts/adminlte.html')



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
            subject, from_email, to = 'THF Bilgi Sistemi Kullanıcı Bilgileri', 'no-reply@badminton.gov.tr', mail
            html_content = '<h2>TÜRKİYE BADMİNTON FEDERASYONU BİLGİ SİSTEMİ</h2>'
            html_content = html_content + '<p><strong>Kullanıcı Adınız :' + str(fdk.user.username) + '</strong></p>'
            # html_content = html_content + '<p> <strong>Site adresi:</strong> <a href="http://127.0.0.1:8000/newpassword?query=' + str(
            #     fdk.uuid) + '">http://127.0.0.1:8000/sbs/profil-guncelle/?query=' + str(fdk.uuid) + '</p></a>'
            html_content = html_content + '<p> <strong>Site adresi:</strong> <a href="http://sbs.badminton.gov.tr/newpassword?query=' + str(
                fdk.uuid) + '">http://sbs.badminton.gov.tr/sbs/profil-guncelle/?query=' + str(fdk.uuid) + '</p></a>'

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


def newlogin(request, pk):
    clup = SportsClub.objects.get(pk=pk)
    # clüp
    club_form = ClubForm(instance=clup)
    communication_formclup = CommunicationForm(instance=clup.communication)
    # klüp üyesi
    user_form = UserForm()
    person_form = PersonForm()
    communication_form = CommunicationForm()
    sportClubUser_form = SportClubUserForm()

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        person_form = PersonForm(request.POST, request.FILES)
        communication_form = CommunicationForm(request.POST, request.FILES)
        sportClubUser_form = SportClubUserForm(request.POST)

        club_form = ClubForm(request.POST, request.FILES)
        communication_formclup = CommunicationForm(request.POST, request.FILES)

        if club_form.is_valid() and user_form.is_valid() and person_form.is_valid() and communication_form.is_valid() and sportClubUser_form.is_valid():

            tc = request.POST.get('tc')

            if Coach.objects.get(person__tc=tc):
                # print("Bu degerde elimde tc si olan bir antrenör var ")
                coach = Coach.objects.get(person__tc=tc)
                user = coach.user

                club_person = SportClubUser(user=coach.user, person=coach.person, communication=coach.communication,
                                            role=sportClubUser_form.cleaned_data['role'])
                club_person.save()

                group = Group.objects.get(name='KlupUye')
                coach.user.groups.add(group)
                coach.save()

                communication = communication_formclup.save(commit=False)
                communication.save()
                clup.communication = communication
                clup.coachs.add(coach)
                clup.save()
                messages.success(request, 'Antrenör şifreniz ile sisteme giriş yapabilirsiniz')
                log = general_methods.logwrite(request, user, "Antrenör klup üyesi olarak giris yaptı new login ")

            else:

                mail = request.POST.get('email')
                if User.objects.filter(email=mail) or ReferenceCoach.objects.filter(
                        email=mail) or ReferenceReferee.objects.filter(email=mail) or PreRegistration.objects.filter(
                    email=mail):
                    messages.warning(request, 'Mail adresi başka bir kullanici tarafından kullanilmaktadir.')
                    return render(request, 'registration/newlogin.html',
                                  {'user_form': user_form, 'person_form': person_form,
                                   'communication_form': communication_form,
                                   'sportClubUser_form': sportClubUser_form, 'club_form': club_form,
                                   'communication_formclup': communication_formclup})

                tc = request.POST.get('tc')
                if Person.objects.filter(tc=tc) or ReferenceCoach.objects.filter(
                        tc=tc) or ReferenceReferee.objects.filter(
                    tc=tc) or PreRegistration.objects.filter(tc=tc):
                    messages.warning(request, 'Tc kimlik numarasi sistemde kayıtlıdır. ')
                    return render(request, 'registration/newlogin.html',
                                  {'user_form': user_form, 'person_form': person_form,
                                   'communication_form': communication_form,
                                   'sportClubUser_form': sportClubUser_form, 'club_form': club_form,
                                   'communication_formclup': communication_formclup})

                name = request.POST.get('first_name')
                surname = request.POST.get('last_name')
                year = request.POST.get('birthDate')
                year = year.split('/')

                # client = Client('https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL')
                # if not (client.service.TCKimlikNoDogrula(tc, name, surname, year[2])):
                #     messages.warning(request,
                #                      'Tc kimlik numarasi ile isim  soyisim dogum yılı  bilgileri uyuşmamaktadır. ')
                #     return render(request, 'registration/newlogin.html',
                #                   {'user_form': user_form, 'person_form': person_form,
                #                    'communication_form': communication_form,
                #                    'sportClubUser_form': sportClubUser_form, 'club_form': club_form,
                #                    'communication_formclup': communication_formclup})

                clup.name = request.POST.get('name')
                clup.shortName = request.POST.get('shortName')
                clup.foundingDate = request.POST.get('foundingDate')
                clup.logo = request.POST.get('logo')
                clup.clubMail = request.POST.get('clubMail')
                clup.petition = request.POST.get('petition')
                clup.isFormal = request.POST.get('isFormal')
                user = User()
                user.username = user_form.cleaned_data['email']
                user.first_name = user_form.cleaned_data['first_name']
                user.last_name = user_form.cleaned_data['last_name']
                user.email = user_form.cleaned_data['email']
                group = Group.objects.get(name='KlupUye')
                user.save()
                user.groups.add(group)
                user.save()

                communication = communication_formclup.save(commit=False)
                communication.save()
                clup.communication = communication
                clup.save()

                person = person_form.save(commit=False)
                communication = communication_form.save(commit=False)
                person.save()
                communication.save()

                club_person = SportClubUser(
                    user=user, person=person, communication=communication,
                    role=sportClubUser_form.cleaned_data['role'],

                )

                club_person.save()
                fdk = Forgot(user=user, status=False)
                fdk.save()

                html_content = ''
                subject, from_email, to = 'TWF Bilgi Sistemi Kullanıcı Bilgileri', 'no-reply@badminton.gov.tr', user.email
                html_content = '<h2>TÜRKİYE BADMİNTON FEDERASYONU BİLGİ SİSTEMİ</h2>'
                html_content = html_content + '<p><strong>Kullanıcı Adınız :' + str(fdk.user.username) + '</strong></p>'
                # html_content = html_content + '<p> <strong>Site adresi:</strong> <a href="http://127.0.0.1:8000/newpassword?query=' + str(
                #     fdk.uuid) + '">http://127.0.0.1:8000/sbs/profil-guncelle/?query=' + str(fdk.uuid) + '</p></a>'
                html_content = html_content + '<p> <strong>Site adresi:</strong> <a href="http://sbs.badminton.gov.tr/newpassword?query=' + str(
                    fdk.uuid) + '">http://sbs.badminton.gov.tr/sbs/profil-guncelle/?query=' + str(fdk.uuid) + '</p></a>'

                msg = EmailMultiAlternatives(subject, '', from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                messages.success(request, 'Mail adresinize gelen link ile sistemde giriş yapabilirsiniz.')

            clup.clubUser.add(club_person)
            clup.dataAccessControl = False
            clup.isRegister = True

            clup.save()
            log = general_methods.logwrite(request, user, "Eski sifre ile giris yapildi")

            return redirect("accounts:login")

    return render(request, 'registration/newlogin.html',
                  {'user_form': user_form, 'person_form': person_form, 'communication_form': communication_form,
                   'sportClubUser_form': sportClubUser_form, 'club_form': club_form,
                   'communication_formclup': communication_formclup})


def referenceReferee(request):
    logout(request)
    referee = RefereeForm()

    if request.method == 'POST':
        referee = RefereeForm(request.POST, request.FILES)
        mail = request.POST.get('email')
        if User.objects.filter(email=mail) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
                email=mail) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
            email=mail) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(
            email=mail):
            messages.warning(request, 'Mail adresi başka bir kullanici tarafından kullanilmaktadir.')
            return render(request, 'registration/Referee.html', {'preRegistrationform': referee})

        tc = request.POST.get('tc')
        if Person.objects.filter(tc=tc) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
                tc=tc) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
            tc=tc) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(tc=tc):
            messages.warning(request, 'Tc kimlik numarasi sistemde kayıtlıdır. ')
            return render(request, 'registration/Referee.html',
                          {'preRegistrationform': referee})

        name = request.POST.get('first_name')
        surname = request.POST.get('last_name')
        year = request.POST.get('birthDate')
        year = year.split('/')

        # client = Client('https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL')
        # if not (client.service.TCKimlikNoDogrula(tc, name, surname, year[2])):
        #     messages.warning(request, 'Tc kimlik numarasi ile isim  soyisim dogum yılı  bilgileri uyuşmamaktadır. ')
        #     return render(request, 'registration/Referee.html',
        #                   {'preRegistrationform': referee})

        if referee.is_valid():
            if request.POST.get('kademe_definition'):
                hakem = referee.save(commit=False)
                hakem.kademe_definition = CategoryItem.objects.get(name=request.POST.get('kademe_definition'))
                hakem.save()

                messages.success(request,
                                 'Başvurunuz onaylandiktan sonra email adresinize şifre bilgileriniz gönderilecektir.')
                return redirect("accounts:login")
            else:
                messages.warning(request, 'Lütfen bilgilerinizi kontrol ediniz. Kademe bilgisi giriniz:')

        else:
            messages.warning(request, 'Lütfen bilgilerinizi kontrol ediniz. ')
    return render(request, 'registration/Referee.html',
                  {'preRegistrationform': referee})


def referenceCoach(request):
    logout(request)
    coach_form = RefereeCoachForm()
    if request.method == 'POST':
        coach_form = RefereeCoachForm(request.POST, request.FILES)
        mail = request.POST.get('email')

        if User.objects.filter(email=mail) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
                email=mail) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
            email=mail) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(
            email=mail):
            messages.warning(request, 'Mail adresi  sistemde  kayıtlıdır. ')
            return render(request, 'registration/Coach.html', {'preRegistrationform': coach_form})

        tc = request.POST.get('tc')
        if Person.objects.filter(tc=tc) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
                tc=tc) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
            tc=tc) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(tc=tc):
            messages.warning(request, 'Tc kimlik numarasi sistemde  kayıtlıdır. ')
            return render(request, 'registration/Coach.html', {'preRegistrationform': coach_form})

        name = request.POST.get('first_name')
        surname = request.POST.get('last_name')
        year = request.POST.get('birthDate')
        year = year.split('/')

        # client = Client('https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL')
        # if not (client.service.TCKimlikNoDogrula(tc, name, surname, year[2])):
        #     messages.warning(request, 'Tc kimlik numarasi ile isim  soyisim dogum yılı  bilgileri uyuşmamaktadır. ')
        #     return render(request, 'registration/Coach.html', {'preRegistrationform': coach_form})

        if coach_form.is_valid():

            veri = coach_form.save(commit=False)
            veri.kademe_definition = CategoryItem.objects.get(name=request.POST.get('kademe_definition'))

            veri.save()

            messages.success(request,
                             'Başvurunuz onaylandiktan sonra email adresinize şifre bilgileriniz gönderilecektir.')
            return redirect("accounts:login")

        else:
            messages.warning(request, 'Lütfen bilgilerinizi kontrol ediniz.')
    return render(request, 'registration/Coach.html',
                  {'preRegistrationform': coach_form})


def referenceAthlete(request):
    logout(request)
    athlete = RefereeAthleteForm()
    if request.method == 'POST':
        athlete = RefereeAthleteForm(request.POST, request.FILES)
        if User.objects.filter(email=mail) or ReferenceCoach.objects.filter(
                email=mail) or ReferenceReferee.objects.filter(email=mail) or PreRegistration.objects.filter(
            email=mail):
            messages.warning(request, 'Mail adresi başka bir kullanici tarafından kullanilmaktadir.')
            return render(request, 'registration/Athlete.html', {'preRegistrationform': athlete})
        if athlete.is_valid():
            athlete.save()
            messages.success(request,
                             'Başvurunuz onaylandiktan sonra email adresinize şifre bilgileriniz gönderilecektir.')
            return redirect("accounts:login")

        else:
            messages.warning(request, 'Lütfen bilgilerinizi kontrol ediniz.')

    return render(request, 'registration/Athlete.html',
                  {'preRegistrationform': athlete})


def lastlogin(request):
    # tc="51838348932"
    # name ="tayyar"
    # email = "tesdt "
    # surname = "karadağ"
    # date ='2/3/1986'
    if request.POST.get("tcno"):

        tc = request.POST.get("tcno")
        if Person.objects.filter(tc=tc):
            name = request.POST.get('isim')
            surname = request.POST.get('soyisim')
            date = request.POST.get('tarih')
            year = date.split('/')

            # client = Client('https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL')
            # if not (client.service.TCKimlikNoDogrula(tc, name, surname, year[2])):
            #     messages.warning(request,
            #                      'Tc kimlik numarasi ile isim  soyisim dogum yılı  bilgileri uyuşmamaktadır. ')
            #     return render(request, 'registration/lastlogin.html')
            # else:
            #     # if SportClubUser.objects.filter(person__tc=tc):
            #     #     print('klup yöneticisi')
            #     if Coach.objects.filter(person__tc=tc):
            #         return redirect('accounts:update-coach', tc, Coach.objects.filter(person__tc=tc)[0].pk)
            #
            #
            #     elif Judge.objects.filter(person__tc=tc):
            #         return redirect('accounts:update-judge', tc, Judge.objects.filter(person__tc=tc)[0].pk)
            #
            #
            #     else:
            #         return redirect('accounts:login')
        else:
            messages.warning(request, 'Sistem de kaydınız bulunmamaktadır.')

    return render(request, 'registration/lastlogin.html')


def updatecoach(request, tc, pk):
    coach = Coach.objects.filter(person__tc=tc)[0]
    if coach.pk == Coach.objects.filter(person__tc=tc)[0].pk:
        if not coach.user.groups.all():
            user = coach.user
            coach.user.groups.add(Group.objects.get(name="Antrenor"))
            coach.save()
        groups = Group.objects.all()
        grade_form = coach.grades.all()
        visa_form = coach.visa.all()
        user = User.objects.get(pk=coach.user.pk)
        person = Person.objects.get(pk=coach.person.pk)
        communication = Communication.objects.get(pk=coach.communication.pk)
        user_form = UserForm(request.POST or None, instance=coach.user)
        person_form = PersonForm(request.POST or None, request.FILES or None, instance=coach.person)
        iban_form = IbanCoachForm(request.POST or None, instance=coach)
        communication = Communication.objects.get(pk=coach.communication.pk)
        communication_form = CommunicationForm(request.POST or None, instance=coach.communication)
        if person.material:
            metarial = Material.objects.get(pk=coach.person.material.pk)
        else:
            metarial = Material()
            metarial.save()
            person.material = metarial
            person.save()
        metarial_form = MaterialForm(request.POST or None, instance=coach.person.material)

        if request.method == 'POST':
            mail = request.POST.get('email')
            if mail != coach.user.email:

                if User.objects.filter(email=mail) or ReferenceCoach.objects.exclude(
                        status=ReferenceCoach.DENIED).filter(
                    email=mail) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
                    email=mail) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(
                    email=mail):
                    messages.warning(request, 'Mail adresi başka bir kullanici tarafından kullanilmaktadir.')
                    return render(request, 'registration/CoachUpdate.html',
                                  {'user_form': user_form, 'communication_form': communication_form,
                                   'person_form': person_form, 'grades_form': grade_form, 'coach': coach.pk,
                                   'personCoach': person, 'visa_form': visa_form, 'iban_form': iban_form,
                                   'groups': groups,
                                   'metarial_form': metarial_form,})

            tc = request.POST.get('tc')
            if tc != coach.person.tc:
                if Person.objects.filter(tc=tc) or ReferenceCoach.objects.exclude(
                        status=ReferenceCoach.DENIED).filter(
                    tc=tc) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
                    tc=tc) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(tc=tc):
                    messages.warning(request, 'Tc kimlik numarasi sisteme kayıtlıdır. ')
                    return render(request, 'registration/CoachUpdate.html',
                                  {'user_form': user_form, 'communication_form': communication_form,
                                   'person_form': person_form, 'grades_form': grade_form, 'coach': coach.pk,
                                   'personCoach': person, 'visa_form': visa_form, 'iban_form': iban_form,
                                   'groups': groups,
                                   'metarial_form': metarial_form,
                                   })

            name = request.POST.get('first_name')
            surname = request.POST.get('last_name')
            year = request.POST.get('birthDate')
            year = year.split('/')

            # client = Client('https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL')
            # if not (client.service.TCKimlikNoDogrula(tc, name, surname, year[2])):
            #     messages.warning(request,
            #                      'Tc kimlik numarasi ile isim  soyisim dogum yılı  bilgileri uyuşmamaktadır. ')
            #     return render(request, 'registration/CoachUpdate.html',
            #                   {'user_form': user_form, 'communication_form': communication_form,
            #                    'person_form': person_form, 'grades_form': grade_form, 'coach': coach.pk,
            #                    'personCoach': person, 'visa_form': visa_form, 'iban_form': iban_form,
            #                    'groups': groups,
            #                    'metarial_form': metarial_form,
            #                    })
            if user_form.is_valid() and person_form.is_valid() and communication_form.is_valid() and iban_form.is_valid() and metarial_form.is_valid():
                user.username = user_form.cleaned_data['email']
                user.first_name = user_form.cleaned_data['first_name']
                user.last_name = user_form.cleaned_data['last_name']
                user.email = user_form.cleaned_data['email']
                user.save()

                user = user_form.save(commit=False)
                user.username = user_form.cleaned_data['email']
                user.save()

                iban_form.save()
                person_form.save()
                communication_form.save()

                log = str(user.get_full_name()) + " Antrenor güncelledi"
                log = general_methods.logwrite(request, request.user, log)

                fdk = Forgot(user=user, status=False)
                fdk.save()

                html_content = ''
                subject, from_email, to = 'Badminton Bilgi Sistemi Kullanıcı Bilgileri', 'no-reply@badminton.gov.tr', user.email
                html_content = '<h2>TÜRKİYE BADMİNTON FEDERASYONU BİLGİ SİSTEMİ</h2>'
                html_content = html_content + '<p><strong>Kullanıcı Adınız :' + str(
                    fdk.user.username) + '</strong></p>'
                # html_content = html_content + '<p> <strong>Site adresi:</strong> <a href="http://127.0.0.1:8000/newpassword?query=' + str(
                #     fdk.uuid) + '">http://127.0.0.1:8000/sbs/profil-guncelle/?query=' + str(fdk.uuid) + '</p></a>'
                html_content = html_content + '<p> <strong>Site adresi:</strong> <a href="http://sbs.badminton.gov.tr/newpassword?query=' + str(
                    fdk.uuid) + '">http://sbs.badminton.gov.tr/sbs/profil-guncelle/?query=' + str(
                    fdk.uuid) + '</p></a>'

                msg = EmailMultiAlternatives(subject, '', from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                user.is_active = True
                user.save()
                messages.success(request, 'Giris Bilgileriniz Mail Adresinize Gönderildi')
                return redirect('accounts:login')
            else:
                messages.warning(request, 'Alanlari Kontrol Ediniz')

        return render(request, 'registration/CoachUpdate.html',
                      {'user_form': user_form, 'communication_form': communication_form,
                       'person_form': person_form, 'grades_form': grade_form, 'coach': coach,
                       'personCoach': person, 'visa_form': visa_form, 'iban_form': iban_form,
                       'groups': groups,
                       })
    else:
        return redirect('accounts:last-login')

    return render(request, 'registration/CoachUpdate.html')


def updatejudge(request, tc, pk):
    judge = Judge.objects.filter(person__tc=tc)[0]
    if not (judge.user.groups.all()):
        user = judge.user
        judge.user.groups.add(Group.objects.get(name="Hakem"))
        judge.save()
    groups = Group.objects.all()

    user = User.objects.get(pk=judge.user.pk)
    person = Person.objects.get(pk=judge.person.pk)

    user_form = UserForm(request.POST or None, instance=user)
    person_form = PersonForm(request.POST or None, request.FILES or None, instance=person)

    communication = Communication.objects.get(pk=judge.communication.pk)
    if person.material:
        metarial = Material.objects.get(pk=judge.person.material.pk)
    else:
        metarial = Material()
        metarial.save()
        person.material = metarial
        person.save()

    communication_form = CommunicationForm(request.POST or None, instance=communication)

    metarial_form = MaterialForm(request.POST or None, instance=metarial)
    if Competition.objects.filter(judges=judge).distinct():
        competitions = Competition.objects.filter(judges=judge).distinct()
    else:
        competitions = Competition.objects.none()

    iban_form = IbanFormJudge(request.POST or None, instance=judge)

    grade_form = judge.grades.all()
    visa_form = judge.visa.all()

    if request.method == "POST":
        name = request.POST.get('first_name')
        surname = request.POST.get('last_name')
        year = request.POST.get('birthDate')
        year = year.split('/')
        mail = request.POST.get('email')
        if mail != judge.user.email:

            if User.objects.filter(email=mail) or ReferenceCoach.objects.exclude(
                    status=ReferenceCoach.DENIED).filter(
                email=mail) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
                email=mail) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(
                email=mail):
                messages.warning(request, 'Mail adresi başka bir kullanici tarafından kullanilmaktadir.')
                return render(request, 'hakem/hakemDuzenle.html',
                              {'user_form': user_form, 'communication_form': communication_form,
                               'person_form': person_form, 'judge': judge, 'grade_form': grade_form,
                               'visa_form': visa_form, 'iban_form': iban_form, 'groups': groups,
                               'metarial_form': metarial_form})

        tc = request.POST.get('tc')
        if tc != judge.person.tc:
            if Person.objects.filter(tc=tc) or ReferenceCoach.objects.exclude(
                    status=ReferenceCoach.DENIED).filter(
                tc=tc) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
                tc=tc) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(tc=tc):
                messages.warning(request, 'Tc kimlik numarasi sisteme kayıtlıdır. ')
                return render(request, 'hakem/hakemDuzenle.html',
                              {'user_form': user_form, 'communication_form': communication_form,
                               'person_form': person_form, 'judge': judge, 'grade_form': grade_form,
                               'visa_form': visa_form, 'iban_form': iban_form, 'groups': groups,
                               'metarial_form': metarial_form,
                               })

        # client = Client('https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL')
        # if not (client.service.TCKimlikNoDogrula(tc, name, surname, year[2])):
        #     messages.warning(request,
        #                      'Tc kimlik numarasi ile isim  soyisim dogum yılı  bilgileri uyuşmamaktadır. ')
        #     return render(request, 'registration/JudgeUpdate.html',
        #                   {'user_form': user_form, 'communication_form': communication_form,
        #                    'person_form': person_form, 'judge': judge, 'grade_form': grade_form,
        #                    'visa_form': visa_form, 'iban_form': iban_form, 'groups': groups,
        #                    'metarial_form': metarial_form,
        #                    })

        if user_form.is_valid() and person_form.is_valid() and communication_form.is_valid() and iban_form.is_valid() and metarial_form.is_valid():

            user.username = user_form.cleaned_data['email']
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.email = user_form.cleaned_data['email']
            user.save()

            log = str(user.get_full_name()) + " Hakemi güncelledi"
            log = general_methods.logwrite(request, request.user, log)

            iban_form.save()

            person_form.save()

            communication_form.save()
            metarial_form.save()
            fdk = Forgot(user=user, status=False)
            fdk.save()

            html_content = ''
            subject, from_email, to = 'Badminton Bilgi Sistemi Kullanıcı Bilgileri', 'no-reply@badminton.gov.tr', user.email
            html_content = '<h2>TÜRKİYE BADMİNTON FEDERASYONU BİLGİ SİSTEMİ</h2>'
            html_content = html_content + '<p><strong>Kullanıcı Adınız :' + str(
                fdk.user.username) + '</strong></p>'
            # html_content = html_content + '<p> <strong>Site adresi:</strong> <a href="http://127.0.0.1:8000/newpassword?query=' + str(
            #     fdk.uuid) + '">http://127.0.0.1:8000/sbs/profil-guncelle/?query=' + str(fdk.uuid) + '</p></a>'
            html_content = html_content + '<p> <strong>Site adresi:</strong> <a href="http://sbs.badminton.gov.tr/newpassword?query=' + str(
                fdk.uuid) + '">http://sbs.badminton.gov.tr/sbs/profil-guncelle/?query=' + str(
                fdk.uuid) + '</p></a>'

            msg = EmailMultiAlternatives(subject, '', from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            user.is_active = True
            user.save()
            messages.success(request, 'Giris Bilgileriniz mail adresinize Gönderildi')
            return redirect('accounts:login')
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'registration/JudgeUpdate.html',
                  {'user_form': user_form, 'communication_form': communication_form,
                   'person_form': person_form, 'judge': judge, 'grade_form': grade_form,
                   'visa_form': visa_form, 'iban_form': iban_form, 'groups': groups,
                   'metarial_form': metarial_form, 'competitions': competitions
                   })
    return render(request, 'registration/JudgeUpdate.html')




def getfiles(request):
    # Files (local path) to put in the .zip
    # FIXME: Change this (get paths from DB etc)
    filenames = ["/tmp/file1.txt", "/tmp/file2.txt"]

    # Folder name in ZIP archive which contains the above files
    # E.g [thearchive.zip]/somefiles/file2.txt
    # FIXME: Set this to something better
    zip_subdir = "somefiles"
    zip_filename = "%s.zip" % zip_subdir

    # Open StringIO to grab in-memory ZIP contents
    s = StringIO.StringIO()

    # The zip compressor
    zf = zipfile.ZipFile(s, "w")

    for fpath in filenames:
        # Calculate path for file in zip
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)

        # Add file, at correct path
        zf.write(fpath, zip_path)

    # Must close zip for all contents to be written
    zf.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = HttpResponse(s.getvalue(), mimetype = "application/x-zip-compressed")
    # ..and correct content-disposition
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

    return resp
