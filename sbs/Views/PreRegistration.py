from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
# from zeep import Client

from accounts.models import Forgot
from sbs.Forms.PreRegidtrationForm import PreRegistrationForm
from sbs.models import SportsClub, SportClubUser, Communication, Person
from sbs.models.CategoryItem import CategoryItem
from sbs.models.Coach import Coach
from sbs.models.Level import Level
from sbs.models.PreRegistration import PreRegistration
from sbs.models.ReferenceCoach import ReferenceCoach
from sbs.models.ReferenceReferee import ReferenceReferee
from sbs.services import general_methods
from sbs.models.EnumFields import EnumFields

from unicode_tr import unicode_tr


def update_preRegistration(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    veri = PreRegistration.objects.get(pk=pk)

    try:
        if CategoryItem.objects.get(name=veri.kademe_definition):
            kategori = CategoryItem.objects.get(name=veri.kademe_definition)
            form = PreRegistrationForm(request.POST or None, request.FILES or None, instance=veri,
                                       initial={'kademe_definition': kategori.name})
        else:
            form = PreRegistrationForm(request.POST or None, request.FILES or None, instance=veri)
    except:
        form = PreRegistrationForm(request.POST or None, request.FILES or None, instance=veri)
    if request.method == 'POST':
        mail = request.POST.get('email')
        if mail != veri.email:
            if User.objects.filter(email=mail) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
                    email=mail) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
                email=mail) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(
                email=mail):
                messages.warning(request, 'Mail adresi başka bir kullanici tarafından kullanilmaktadir.')
                return render(request, 'kulup/kulup-basvuru-duzenle.html',
                              {'preRegistrationform': form, })

        tc = request.POST.get('tc')
        if tc != veri.tc:

            if Person.objects.filter(tc=tc) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
                    tc=tc) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
                tc=tc) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(tc=tc):
                messages.warning(request, 'Tc kimlik numarasi sistemde kayıtlıdır. ')
                return render(request, 'kulup/kulup-basvuru-duzenle.html',
                              {'preRegistrationform': form, })

        name = request.POST.get('first_name')
        surname = request.POST.get('last_name')
        year = request.POST.get('birthDate')
        year = year.split('/')

        # client = Client('https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL')
        #
        # if not (client.service.TCKimlikNoDogrula(tc, name, surname, year[2])):
        #     messages.warning(request, 'Tc kimlik numarasi ile isim,soyisim,dogum yılı  bilgileri uyuşmamaktadır. ')
        #     return render(request, 'kulup/kulup-basvuru-duzenle.html',
        #                   {'preRegistrationform': form, })
        form = PreRegistrationForm(request.POST, request.FILES or None, instance=veri)

        if form.is_valid():
            form.save()
            # print(request.POST.get('kademe_definition'))

            messages.success(request, 'Basarili bir şekilde kaydedildi ')
            return redirect('sbs:basvuru-listesi')
        else:
            messages.warning(request, 'Alanlari kontrol ediniz')
    return render(request, 'kulup/kulup-basvuru-duzenle.html',
                  {'preRegistrationform': form, })


@login_required
def rejected_preRegistration(request, pk):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    messages.success(request, 'Klup basvurusu reddedildi ')
    veri = PreRegistration.objects.get(pk=pk)
    veri.status = PreRegistration.DENIED
    veri.save()
    prepegidtration = PreRegistration.objects.all()
    log = str(veri.name) + " Klup basvurusu reddedildi"
    log = general_methods.logwrite(request, request.user, log)
    return render(request, 'kulup/kulupBasvuru.html',
                  {'prepegidtration': prepegidtration})

@login_required
def approve_preRegistration(request, pk):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    basvuru = PreRegistration.objects.get(pk=pk)
    if basvuru.status != PreRegistration.APPROVED:
        mail = basvuru.email
        if not (User.objects.filter(email=mail) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
                email=mail) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(email=mail)):

            user = User()
            user.username = basvuru.email
            user.first_name = unicode_tr(basvuru.first_name).upper()
            user.last_name = unicode_tr(basvuru.last_name).upper()
            user.email = basvuru.email
            user.is_active = True
            user.is_staff = basvuru.is_staff
            group = Group.objects.get(name='KlupUye')
            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()
            user.groups.add(group)
            user.save()

            # person kaydet
            person = Person()
            person.tc = basvuru.tc
            person.birthplace = basvuru.birthplace
            person.motherName = basvuru.motherName
            person.fatherName = basvuru.fatherName
            person.profileImage = basvuru.profileImage
            person.birthDate = basvuru.birthDate
            person.bloodType = basvuru.bloodType
            if basvuru.gender == 'Erkek':
                person.gender = Person.MALE
            else:
                person.gender = Person.FEMALE
            person.save()

            # Communication kaydet
            com = Communication()
            com.postalCode = basvuru.postalCode
            com.phoneNumber = basvuru.phoneNumber
            com.phoneNumber2 = basvuru.phoneNumber2
            com.address = basvuru.address
            com.city = basvuru.city
            com.country = basvuru.country
            com.save()

            Sportclup = SportClubUser()
            Sportclup.user = user
            Sportclup.person = person
            Sportclup.communication = com
            Sportclup.role = basvuru.role
            Sportclup.save()

            comclup = Communication()
            comclup.postalCode = basvuru.clubpostalCode
            comclup.phoneNumber = basvuru.clubphoneNumber
            comclup.phoneNumber2 = basvuru.clubphoneNumber2
            comclup.address = basvuru.clubaddress
            comclup.city = basvuru.clubcity
            comclup.country = basvuru.clubcountry
            comclup.save()

            # SportClup
            clup = SportsClub()
            clup.name = basvuru.name
            clup.shortName = basvuru.shortName
            clup.foundingDate = basvuru.foundingDate
            clup.clubMail = basvuru.clubMail
            clup.logo = basvuru.logo
            clup.isFormal = basvuru.isFormal
            clup.petition = basvuru.petition
            clup.communication = comclup
            clup.save()
            clup.clubUser.add(Sportclup)
            clup.save()
            # burada kadik
            if basvuru.isCoach:

                coach = Coach()
                coach.user = user
                coach.person = person
                coach.communication = com
                coach.iban = basvuru.iban
                coach.save()
                group = Group.objects.get(name='Antrenor')
                user.groups.add(group)
                user.save()
                grade = Level(
                    startDate=basvuru.kademe_startDate,
                    dekont=basvuru.kademe_belge,
                    branch=EnumFields.HALTER.value)
                try:
                    grade.definition = CategoryItem.objects.get(name=basvuru.kademe_definition)
                except:
                    grade.definition = CategoryItem.objects.get(name='1.Kademe')

                grade.levelType = EnumFields.LEVELTYPE.GRADE
                grade.status = Level.APPROVED
                grade.isActive = True
                grade.save()
                coach.grades.add(grade)
                coach.save()

                clup.coachs.add(coach)
                clup.save()

            basvuru.status = PreRegistration.APPROVED
            basvuru.save()

            fdk = Forgot(user=user, status=False)
            fdk.save()

            html_content = ''
            subject, from_email, to = 'Bilgi Sistemi Kullanıcı Bilgileri', 'no-reply@badminton.gov.tr', user.email
            html_content = '<h2>TÜRKİYE BADMİNTON FEDERASYONU BİLGİ SİSTEMİ</h2>'
            html_content = html_content + '<p><strong>Kullanıcı Adınız :' + str(fdk.user.username) + '</strong></p>'
            html_content = html_content + '<p> <strong>Site adresi:</strong> <a href="http://sbs.badminton.gov.tr/newpassword?query=' + str(
                fdk.uuid) + '">http://sbs.badminton.gov.tr/sbs/profil-guncelle/?query=' + str(fdk.uuid) + '</p></a>'
            msg = EmailMultiAlternatives(subject, '', from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            messages.success(request, 'Başari ile kaydedildi')

            log = str(clup) + " Klup basvurusu onaylandi"
            log = general_methods.logwrite(request, request.user, log)

            # try:
            #     # user kaydet
            #     print()
            # except:
            #     messages.warning(request, 'Lütfen sistem yöneticisi ile görüşünüz ')
            #     log = str(basvuru.name) + " Klup basvurusu hata oldu"
            #     log = general_methods.logwrite(request, request.user, log)

        else:
            messages.warning(request, 'Mail adresi sistem de kayıtlıdır.')
    else:
        messages.warning(request, 'Bu basvuru sisteme kaydedilmistir.')

    prepegidtration = PreRegistration.objects.all()
    return render(request, 'kulup/kulupBasvuru.html',
                  {'prepegidtration': prepegidtration})




@login_required
def return_preRegistration(request):
    perm = general_methods.control_access(request)


    if not perm:
        logout(request)
        return redirect('accounts:login')

    prepegidtration = PreRegistration.objects.all().order_by('status')
    return render(request, 'kulup/kulupBasvuru.html',
                  {'prepegidtration': prepegidtration})
