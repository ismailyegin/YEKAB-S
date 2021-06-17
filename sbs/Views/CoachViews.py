import datetime
import email
from _socket import gaierror
from typing import re
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

from sbs.Forms import VisaForm
from sbs.Forms.CategoryItemForm import CategoryItemForm
from sbs.Forms.CommunicationForm import CommunicationForm
from sbs.Forms.DisabledCommunicationForm import DisabledCommunicationForm
from sbs.Forms.DisabledPersonForm import DisabledPersonForm
from sbs.Forms.DisabledUserForm import DisabledUserForm
from sbs.Forms.GradeForm import GradeForm
from sbs.Forms.UserForm import UserForm
from sbs.Forms.VisaForm import VisaForm
from sbs.Forms.PersonForm import PersonForm
from sbs.Forms.CoachSearchForm import CoachSearchForm
from sbs.Forms.SearchClupForm import SearchClupForm
from sbs.Forms.IbanCoachForm import IbanCoachForm

from sbs.Forms.ReferenceCoachForm import RefereeCoachForm

from sbs.Forms.UserSearchForm import UserSearchForm
from sbs.Forms.CompetitionForm import CompetitionForm
from sbs.Forms.VisaSeminarForm import VisaSeminarForm
from sbs.models import Coach, Athlete, Person, Communication, SportClubUser, Level, SportsClub

from sbs.models.ReferenceCoach import ReferenceCoach
from sbs.models.CategoryItem import CategoryItem
from sbs.models.VisaSeminar import VisaSeminar
from sbs.models.EnumFields import EnumFields
from sbs.services import general_methods
from datetime import date, datetime
from django.utils import timezone

from accounts.models import Forgot

# from zeep import Client
from sbs.models.PreRegistration import PreRegistration
from sbs.models.ReferenceReferee import ReferenceReferee
from sbs.models.ReferenceCoach import ReferenceCoach

from sbs.models.Penal import Penal
from sbs.models.Document import Document
from sbs.Forms.PenalForm import PenalForm
from sbs.Forms.DocumentForm import DocumentForm

from sbs.models.Competition import Competition
from sbs.models.Material import Material
from sbs.models.CompetitionCoach import CompetitionCoach

from sbs.Forms.MaterialForm import MaterialForm

from sbs.models.Logs import Logs

from unicode_tr import unicode_tr

from sbs.Forms.VisaSeminarSearchForm import VisaSeminarSearchForm
from sbs.models.CoachApplication import CoachApplication

# visaseminer ekle
@login_required
def visaSeminar_ekle(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    visaSeminar = VisaSeminarForm()
    if request.method == 'POST':
        visaSeminar = VisaSeminarForm(request.POST)
        if visaSeminar.is_valid():

            visa = visaSeminar.save()
            type = request.POST.get('typeSeminar')
            if type == 'claim':
                visa.forWhichClazz = 'COACH_CLAIM'
            else:
                visa.forWhichClazz = 'COACH'
            visa.save()
            messages.success(request, 'Vize Semineri Başari  Kaydedilmiştir.')

            return redirect('sbs:visa-seminar')
        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'antrenor/visaSeminar-ekle.html',
                  {'competition_form': visaSeminar})


# # visaseminar liste
# @login_required
# def return_visaSeminar(request):
#     perm = general_methods.control_access_klup(request)
#
#     if not perm:
#         logout(request)
#         return redirect('accounts:login')
#
#     search_form = VisaSeminarSearchForm(request.POST or None)
#     Seminar = VisaSeminar.objects.none()
#
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         location = request.POST.get('location')
#         startDate = request.POST.get('startDate')
#         finishDate = request.POST.get('finishDate')
#
#         if search_form.is_valid():
#             finishDate = search_form.cleaned_data['finishDate']
#             startDate = search_form.cleaned_data['startDate']
#             if not (name or location or startDate or finishDate):
#                 Seminar = VisaSeminar.objects.filter(forWhichClazz='COACH')
#                 test = VisaSeminar.objects.filter()
#
#             else:
#                 query = Q()
#                 if name:
#                     query &= Q(name__icontains=name)
#                 if location:
#                     query &= Q(location__icontains=location)
#                 if finishDate:
#                     query &= Q(finishDate=finishDate)
#                 if startDate:
#                     query &= Q(startDate=startDate)
#                 Seminar = VisaSeminar.objects.filter(query).filter(forWhichClazz='COACH').distinct()
#
#     return render(request, 'antrenor/VisaSeminar.html', {'competitions': Seminar, 'search_form': search_form})


@login_required
def return_visaSeminar(request):
    perm = general_methods.control_access_klup(request)
    aktif = general_methods.controlGroup(request)


    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user
    seminar = VisaSeminar.objects.none()
    if aktif == "Antrenor":
        seminar = VisaSeminar.objects.exclude(coachApplication__coach__user=user).filter(forWhichClazz='COACH')
        seminar |= VisaSeminar.objects.filter(forWhichClazz='COACH').filter(coachApplication__coach__user=user).exclude(coachApplication__status=VisaSeminar.WAITED).exclude(coachApplication__status=VisaSeminar.APPROVED)
        seminar |= VisaSeminar.objects.exclude(coachApplication__coach__user=user).filter(forWhichClazz='COACH_CLAIM')
        seminar = seminar.distinct()

    elif aktif == "Admin":
        seminar = VisaSeminar.objects.filter(forWhichClazz='COACH')
        seminar |= VisaSeminar.objects.filter(forWhichClazz='COACH_CLAIM')

    if request.method == 'POST':
        if user.groups.filter(name='Antrenor').exists():
            vizeSeminer = VisaSeminar.objects.get(pk=request.POST.get('pk'))
            coach = Coach.objects.get(user=request.user)
            try:
                if request.FILES['file']:
                    document = request.FILES['file']
                    data = CoachApplication()
                    data.dekont = document
                    data.coach = coach
                    data.save()
                    vizeSeminer.coachApplication.add(data)
                    vizeSeminer.save()

                    messages.success(request, 'Vize Seminerine Başvuru  gerçekleşmiştir.')
                    return redirect('sbs:visa-seminar-basvuru')


            except:
                messages.warning(request, 'Lütfen yeniden deneyiniz')

    return render(request, 'antrenor/VisaSeminarAplication.html', {'competitions': seminar})




@login_required
def visaSeminar_duzenle(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    seminar = VisaSeminar.objects.get(pk=pk)
    coach = seminar.coach.all()
    competition_form = VisaSeminarForm(request.POST or None, instance=seminar)
    if request.method == 'POST':
        if competition_form.is_valid():
            competition_form.save()
            type = request.POST.get('typeSeminar')
            if type == 'claim':
                seminar.forWhichClazz = 'COACH_CLAIM'
            else:
                seminar.forWhichClazz = 'COACH'
            seminar.save()
            messages.success(request, 'Vize Seminer Başarıyla Güncellenmiştir.')

            return redirect('sbs:seminar-duzenle', seminar.pk)
        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')


    return render(request, 'antrenor/VizeSeminar-Duzenle.html',
                  {'competition_form': competition_form, 'competition': seminar, 'athletes': coach})


@login_required
def visaSeminar_sil(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = VisaSeminar.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Competition.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def return_add_coach(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    user_form = UserForm()
    person_form = PersonForm()
    communication_form = CommunicationForm()
    iban_form = IbanCoachForm()
    grade_form = GradeForm()

    if request.method == 'POST':

        user_form = UserForm(request.POST)
        person_form = PersonForm(request.POST, request.FILES)
        communication_form = CommunicationForm(request.POST)
        iban_form = IbanCoachForm(request.POST)
        grade_form = GradeForm(request.POST)




        mail = request.POST.get('email')

        if User.objects.filter(email=mail) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
                email=mail) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
            email=mail) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(
            email=mail):
            messages.warning(request, 'Mail adresi başka bir kullanici tarafından kullanilmaktadir.')
            return render(request, 'antrenor/antrenor-ekle.html',
                          {'user_form': user_form, 'person_form': person_form,
                           'communication_form': communication_form, 'iban_form': iban_form, 'grade_form': grade_form})

        tc = request.POST.get('tc')
        if Person.objects.filter(tc=tc) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
                tc=tc) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
            tc=tc) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(tc=tc):
            messages.warning(request, 'Tc kimlik numarasi sisteme kayıtlıdır. ')
            return render(request, 'antrenor/antrenor-ekle.html',
                          {'user_form': user_form, 'person_form': person_form,
                           'communication_form': communication_form, 'iban_form': iban_form, 'grade_form': grade_form})

        name = request.POST.get('first_name')
        surname = request.POST.get('last_name')
        year = request.POST.get('birthDate')
        year = year.split('/')

        # client = Client('https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL')
        # if not (client.service.TCKimlikNoDogrula(tc, name, surname, year[2])):
        #     messages.warning(request, 'Tc kimlik numarasi ile isim  soyisim dogum yılı  bilgileri uyuşmamaktadır. ')
        #     return render(request, 'antrenor/antrenor-ekle.html',
        #                   {'user_form': user_form, 'person_form': person_form,
        #                    'communication_form': communication_form, 'iban_form': iban_form, 'grade_form': grade_form})

        if user_form.is_valid() and person_form.is_valid() and communication_form.is_valid() and iban_form.is_valid() and grade_form.is_valid():
            user = User()
            user.username = user_form.cleaned_data['email']
            user.first_name = unicode_tr(user_form.cleaned_data['first_name']).upper()
            user.last_name = unicode_tr(user_form.cleaned_data['last_name']).upper()


            user.email = user_form.cleaned_data['email']
            group = Group.objects.get(name='Antrenor')
            password = User.objects.make_random_password()
            user.set_password(password)
            user.is_active = True
            user.save()
            user.groups.add(group)

            user.save()

            log = str(user.get_full_name()) + " Antrenoru ekledi"
            log = general_methods.logwrite(request, request.user, log)

            person = person_form.save(commit=False)
            communication = communication_form.save(commit=False)
            person.save()
            communication.save()

            coach = Coach(user=user, person=person, communication=communication)
            coach.iban = iban_form.cleaned_data['iban']
            coach.save()
            grade = grade_form.save(commit=False)
            grade.save()
            coach.grades.add(grade)
            coach.save()
            # antroner kaydından sonra mail gönderilmeyecek

            # subject, from_email, to = 'Halter - Antrenör Bilgi Sistemi Kullanıcı Giriş Bilgileri', 'no-reply@twf.gov.tr', user.email
            # text_content = 'Aşağıda ki bilgileri kullanarak sisteme giriş yapabilirsiniz.'
            # html_content = '<p> <strong>Site adresi: </strong> <a href="http://sbs.twf.gov.tr:81/"></a>sbs.twf.gov.tr:81</p>'
            # html_content = html_content + '<p><strong>Kullanıcı Adı:  </strong>' + user.username + '</p>'
            # html_content = html_content + '<p><strong>Şifre: </strong>' + password + '</p>'
            # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()

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

            messages.success(request, 'Antrenör Başarıyla Kayıt Edilmiştir.')

            return redirect('sbs:update-coach', coach.pk)

        else:

            for x in user_form.errors.as_data():
                messages.warning(request, user_form.errors[x][0])

    return render(request, 'antrenor/antrenor-ekle.html',
                  {'user_form': user_form, 'person_form': person_form,
                   'communication_form': communication_form, 'iban_form': iban_form, 'grade_form': grade_form})


@login_required
def return_coachs(request):
    perm = general_methods.control_access(request)
    active = general_methods.controlGroup(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    coachs = Coach.objects.none()
    user_form = CoachSearchForm()
    searchClupForm = SearchClupForm()

    if request.method == 'POST':
        user_form = CoachSearchForm(request.POST)
        searchClupForm = SearchClupForm(request.POST)
        branch = request.POST.get('branch')
        grade = request.POST.get('definition')
        visa = request.POST.get('visa')
        firstName = unicode_tr(request.POST.get('first_name')).upper()
        lastName = unicode_tr(request.POST.get('last_name')).upper()
        email = request.POST.get('email')

        if not (firstName or lastName or email or branch or grade or visa):
            if active == 'KlupUye':
                sc_user = SportClubUser.objects.get(user=user)
                clubsPk = []
                clubs = SportsClub.objects.filter(clubUser=sc_user)
                for club in clubs:
                    clubsPk.append(club.pk)
                coachs = Coach.objects.filter(sportsclub__in=clubsPk).distinct()
            elif active == 'Yonetim' or active == 'Admin':
                coachs = Coach.objects.all()
        else:
            query = Q()
            if lastName:
                query &= Q(user__last_name__icontains=lastName)
            if firstName:
                query &= Q(user__first_name__icontains=firstName)
            if email:
                query &= Q(user__email__icontains=email)
            if branch:
                query &= Q(grades__branch=branch, grades__status='Onaylandı')
            if grade:
                query &= Q(grades__definition__name=grade, grades__status='Onaylandı')
            if visa == 'VISA':
                query &= Q(visa__startDate__year=timezone.now().year, visa__status='Onaylandı')

            if active == 'KlupUye':
                sc_user = SportClubUser.objects.get(user=user)
                clubsPk = []
                clubs = SportsClub.objects.filter(clubUser=sc_user)
                for club in clubs:
                    clubsPk.append(club.pk)
                coachs = Coach.objects.filter(query).filter(sportsclub__in=clubsPk).distinct()
            elif active == 'Yonetim' or active == 'Admin':
                coachs = Coach.objects.filter(query)
            if visa == 'NONE':
                coachs = coachs.exclude(visa__startDate__year=timezone.now().year, visa__status='Onaylandı')
    return render(request, 'antrenor/antrenorler.html',
                  {'coachs': coachs, 'user_form': user_form, 'branch': searchClupForm})


@login_required
def return_grade(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    category_item_form = CategoryItemForm()

    if request.method == 'POST':

        category_item_form = CategoryItemForm(request.POST)
        name = request.POST.get('name')
        if name is not None:
            categoryItem = CategoryItem(name=name)
            categoryItem.forWhichClazz = "COACH_GRADE"
            categoryItem.isFirst = False
            categoryItem.save()
            return redirect('sbs:kademe')


        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')
    categoryitem = CategoryItem.objects.filter(forWhichClazz="COACH_GRADE")
    return render(request, 'antrenor/kademe.html',
                  {'category_item_form': category_item_form, 'categoryitem': categoryitem})


@login_required
def antrenor_kademe_ekle(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    coach = Coach.objects.get(pk=pk)
    grade_form = GradeForm()
    category_item_form = CategoryItemForm()
    if request.method == 'POST':
        grade_form = GradeForm(request.POST, request.FILES)
        category_item_form = CategoryItemForm(request.POST, request.FILES)

        if grade_form.is_valid() and grade_form.cleaned_data['dekont'] is not None and request.POST.get(
                'branch') is not None:
            grade = Level(definition=grade_form.cleaned_data['definition'],
                          startDate=grade_form.cleaned_data['startDate'],
                          dekont=grade_form.cleaned_data['dekont'],
                          branch=grade_form.cleaned_data['branch'])
            grade.levelType = EnumFields.LEVELTYPE.GRADE
            grade.status = Level.WAITED
            grade.save()
            coach.grades.add(grade)
            coach.save()

            log = str(coach.user.get_full_name()) + " Kademe eklendi"
            log = general_methods.logwrite(request, request.user, log)

            messages.success(request, 'Kademe Başarıyla Eklenmiştir.')
            return redirect('sbs:update-coach', pk=pk)

        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    grade_form.fields['definition'].queryset = CategoryItem.objects.filter(forWhichClazz='COACH_GRADE')
    return render(request, 'antrenor/antrenor-kademe-ekle.html',
                  {'grade_form': grade_form})


@login_required
def categoryItemDelete(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = CategoryItem.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except CategoryItem.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def categoryItemUpdate(request, pk):
    perm = general_methods.control_access(request)


    if not perm:
        logout(request)
        return redirect('accounts:login')
    categoryItem = CategoryItem.objects.get(id=pk)
    category_item_form = CategoryItemForm(request.POST or None, instance=categoryItem)
    if request.method == 'POST':
        if request.POST.get('name') is not None:
            categoryItem.name = request.POST.get('name')
            categoryItem.save()
            messages.success(request, 'Başarıyla Güncellendi')
            return redirect('sbs:kademe')
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'antrenor/kademeDuzenle.html',
                  {'category_item_form': category_item_form})


@login_required
def deleteCoach(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = Coach.objects.get(pk=pk)
            log = str(obj.user.get_full_name()) + " Antrenor sildi"
            log = general_methods.logwrite(request, request.user, log)

            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Coach.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def referenceCoachStatus(request, pk):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        referenceCoach = ReferenceCoach.objects.get(pk=pk)

        if referenceCoach.status != ReferenceCoach.APPROVED:
            user = User()
            user.username = referenceCoach.email
            user.first_name = unicode_tr(referenceCoach.first_name).upper()
            user.last_name = unicode_tr(referenceCoach.last_name).upper()
            user.email = referenceCoach.email
            group = Group.objects.get(name='Antrenor')

            user.save()
            user.groups.add(group)
            user.is_active = True
            user.save()

            person = Person()
            person.tc = referenceCoach.tc
            person.motherName = referenceCoach.motherName
            person.fatherName = referenceCoach.fatherName
            person.profileImage = referenceCoach.profileImage
            person.birthDate = referenceCoach.birthDate
            person.bloodType = referenceCoach.bloodType
            if referenceCoach.gender == 'Erkek':
                person.gender = Person.MALE
            else:
                person.gender = Person.FEMALE
            person.save()
            communication = Communication()
            communication.postalCode = referenceCoach.postalCode
            communication.phoneNumber = referenceCoach.phoneNumber
            communication.phoneNumber2 = referenceCoach.phoneNumber2
            communication.address = referenceCoach.address
            communication.city = referenceCoach.city
            communication.country = referenceCoach.country
            communication.save()

            coach = Coach(user=user, person=person, communication=communication)
            coach.iban = referenceCoach.iban
            coach.save()

            grade = Level(definition=referenceCoach.kademe_definition,
                          startDate=referenceCoach.kademe_startDate,
                          dekont=referenceCoach.kademe_belge,
                          branch=EnumFields.BADMİNTON.value)
            grade.levelType = EnumFields.LEVELTYPE.GRADE
            grade.status = Level.APPROVED
            grade.isActive = True
            grade.save()
            coach.grades.add(grade)
            coach.save()

            messages.success(request, 'Antrenör Başarıyla Eklenmiştir')
            referenceCoach.status = ReferenceCoach.APPROVED
            referenceCoach.save()

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

        else:
            messages.success(request, 'Antrenör daha önce onylanmıştır.')

    except:
        messages.warning(request, 'Tekrar deneyiniz.')
    return redirect('sbs:basvuru-coach')


@login_required
def referenappcoverCoach(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            referenceCoach = ReferenceCoach.objects.get(pk=pk)

            if referenceCoach.status != ReferenceCoach.APPROVED:
                user = User()
                user.username = referenceCoach.email
                user.first_name = unicode_tr(referenceCoach.first_name).upper()
                user.last_name = unicode_tr(referenceCoach.last_name).upper()
                user.email = referenceCoach.email
                user.is_active = True
                group = Group.objects.get(name='Antrenor')

                user.save()

                user.groups.add(group)

                user.save()

                person = Person()
                person.tc = referenceCoach.tc
                person.motherName = referenceCoach.motherName
                person.fatherName = referenceCoach.fatherName
                person.profileImage = referenceCoach.profileImage
                person.birthDate = referenceCoach.birthDate
                person.birthplace = referenceCoach.birthplace
                person.bloodType = referenceCoach.bloodType
                if referenceCoach.gender == 'Erkek':
                    person.gender = Person.MALE
                else:
                    person.gender = Person.FEMALE
                person.save()
                communication = Communication()
                communication.postalCode = referenceCoach.postalCode
                communication.phoneNumber = referenceCoach.phoneNumber
                communication.phoneNumber2 = referenceCoach.phoneNumber2
                communication.address = referenceCoach.address
                communication.city = referenceCoach.city
                communication.country = referenceCoach.country
                communication.save()

                coach = Coach(user=user, person=person, communication=communication)
                coach.iban = referenceCoach.iban
                coach.save()

                grade = Level(definition=referenceCoach.kademe_definition,
                              startDate=referenceCoach.kademe_startDate,
                              dekont=referenceCoach.kademe_belge,
                              branch=EnumFields.BADMİNTON.value)
                grade.levelType = EnumFields.LEVELTYPE.GRADE
                grade.status = Level.APPROVED
                grade.isActive = True
                grade.save()
                coach.grades.add(grade)
                coach.save()

                messages.success(request, 'Antrenör Başarıyla Eklenmiştir')
                referenceCoach.status = ReferenceCoach.APPROVED
                referenceCoach.save()

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

                log = str(user.get_full_name()) + " Antrenor basvurusu onaylandi"
                log = general_methods.logwrite(request, request.user, log)

                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

            else:
                messages.success(request, 'Antrenör daha önce onylanmıştır.')
                return JsonResponse({'status': 'Fail', 'msg': 'Antrenör daha önce onylanmıştır.'})

        except:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def referencedeniedCoach(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = ReferenceCoach.objects.get(pk=pk)
            obj.status = ReferenceCoach.DENIED
            obj.save()

            log = str(obj.first_name) + " " + str(obj.last_name) + " Antrenor   basvurusu reddedildi"
            log = general_methods.logwrite(request, request.user, log)

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Coach.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def coachreferenceUpdate(request, pk):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    coach = ReferenceCoach.objects.get(pk=pk)
    coach_form = RefereeCoachForm(request.POST or None, request.FILES or None, instance=coach,
                                  initial={'kademe_definition': coach.kademe_definition})
    if request.method == 'POST':

        mail = request.POST.get('email')
        if mail != coach.email:

            if User.objects.filter(email=mail) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
                    email=mail) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
                email=mail) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(
                email=mail):
                messages.warning(request, 'Mail adresi başka bir kullanici tarafından kullanilmaktadir.')
                return render(request, 'antrenor/AntronerBasvuruUpdate.html',
                              {'preRegistrationform': coach_form})

        tc = request.POST.get('tc')
        if tc != coach.tc:
            if Person.objects.filter(tc=tc) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
                    tc=tc) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
                tc=tc) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(tc=tc):
                messages.warning(request, 'Tc kimlik numarasi sisteme kayıtlıdır. ')
                return render(request, 'antrenor/AntronerBasvuruUpdate.html',
                              {'preRegistrationform': coach_form})

        name = request.POST.get('first_name')
        surname = request.POST.get('last_name')
        year = request.POST.get('birthDate')
        year = year.split('/')

        # client = Client('https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL')
        # if not (client.service.TCKimlikNoDogrula(tc, name, surname, year[2])):
        #     messages.warning(request, 'Tc kimlik numarasi ile isim  soyisim dogum yılı  bilgileri uyuşmamaktadır. ')
        #     return render(request, 'antrenor/AntronerBasvuruUpdate.html',
        #                   {'preRegistrationform': coach_form})

        if coach_form.is_valid():
            coach_form.save()

            messages.success(request, 'Antrenör Başvurusu Güncellendi')
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'antrenor/AntronerBasvuruUpdate.html',
                  {'preRegistrationform': coach_form})


@login_required
def coachUpdate(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    coach = Coach.objects.get(pk=pk)

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
    user_form = UserForm(request.POST or None, instance=user)
    person_form = PersonForm(request.POST or None, request.FILES or None, instance=person)
    iban_form = IbanCoachForm(request.POST or None, instance=coach)

    logs = Logs.objects.filter(user=user)

    communication = Communication.objects.get(pk=coach.communication.pk)
    if person.material:
        metarial = Material.objects.get(pk=coach.person.material.pk)
    else:
        metarial = Material()
        metarial.save()
        person.material = metarial
        person.save()

    communication_form = CommunicationForm(request.POST or None, instance=communication)
    metarial_form = MaterialForm(request.POST or None, instance=metarial)

    #
    # coa = []
    # for item in CompetitionCoach.objects.filter(coach=coach):
    #     coa.append(item)

    competitions = Competition.objects.none()





    if request.method == 'POST':
        user = User.objects.get(pk=coach.user.pk)
        user_form = UserForm(request.POST or None, instance=user)
        person_form = PersonForm(request.POST, request.FILES, instance=person)
        communication_form = CommunicationForm(request.POST or None, instance=communication)
        iban_form = IbanCoachForm(request.POST or None, instance=coach)

        mail = request.POST.get('email')
        if mail != coach.user.email:

            if User.objects.filter(email=mail) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
                    email=mail) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
                email=mail) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(
                email=mail):
                messages.warning(request, 'Mail adresi başka bir kullanici tarafından kullanilmaktadir.')
                return render(request, 'antrenor/antrenorDuzenle.html',
                              {'user_form': user_form, 'communication_form': communication_form,
                               'person_form': person_form, 'grades_form': grade_form, 'coach': coach,
                               'personCoach': person, 'visa_form': visa_form, 'iban_form': iban_form, 'groups': groups,
                               'metarial_form': metarial_form, 'competitions': competitions, 'logs': logs
                               })

        tc = request.POST.get('tc')
        if tc != coach.person.tc:
            if Person.objects.filter(tc=tc) or ReferenceCoach.objects.exclude(status=ReferenceCoach.DENIED).filter(
                    tc=tc) or ReferenceReferee.objects.exclude(status=ReferenceReferee.DENIED).filter(
                tc=tc) or PreRegistration.objects.exclude(status=PreRegistration.DENIED).filter(tc=tc):
                messages.warning(request, 'Tc kimlik numarasi sisteme kayıtlıdır. ')
                return render(request, 'antrenor/antrenorDuzenle.html',
                              {'user_form': user_form, 'communication_form': communication_form,
                               'person_form': person_form, 'grades_form': grade_form, 'coach': coach,
                               'personCoach': person, 'visa_form': visa_form, 'iban_form': iban_form, 'groups': groups,
                               'metarial_form': metarial_form, 'competitions': competitions, 'logs': logs
                               })

        name = request.POST.get('first_name')
        surname = request.POST.get('last_name')
        year = request.POST.get('birthDate')
        year = year.split('/')

        # client = Client('https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL')
        # if not (client.service.TCKimlikNoDogrula(tc, name, surname, year[2])):
        #     messages.warning(request, 'Tc kimlik numarasi ile isim  soyisim dogum yılı  bilgileri uyuşmamaktadır. ')
        #     return render(request, 'antrenor/antrenorDuzenle.html',
        #                   {'user_form': user_form, 'communication_form': communication_form,
        #                    'person_form': person_form, 'grades_form': grade_form, 'coach': coach,
        #                    'personCoach': person, 'visa_form': visa_form, 'iban_form': iban_form, 'groups': groups,
        #                    'metarial_form': metarial_form, 'competitions': competitions, 'logs': logs
        #                    })

        if user_form.is_valid() and person_form.is_valid() and communication_form.is_valid() and iban_form.is_valid() and metarial_form.is_valid():

            user.username = user_form.cleaned_data['email']
            user.first_name = unicode_tr(user_form.cleaned_data['first_name']).upper()
            user.last_name = unicode_tr(user_form.cleaned_data['last_name']).upper()

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


            messages.success(request, 'Antrenör Başarıyla Güncellendi')
            # return redirect('sbs:antrenorler')
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'antrenor/antrenorDuzenle.html',
                  {'user_form': user_form, 'communication_form': communication_form,
                   'person_form': person_form, 'grades_form': grade_form, 'coach': coach,
                   'personCoach': person, 'visa_form': visa_form, 'iban_form': iban_form, 'groups': groups,
                   'metarial_form': metarial_form, 'competitions': competitions, 'logs': logs
                   })
@login_required
def updateCoachProfile(request):
    perm = general_methods.control_access_klup(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    user = request.user
    directory_user = Coach.objects.get(user=user)
    person = Person.objects.get(pk=directory_user.person.pk)
    communication = Communication.objects.get(pk=directory_user.communication.pk)
    user_form = DisabledUserForm(request.POST or None, instance=user)
    person_form = DisabledPersonForm(request.POST or None, instance=person)
    communication_form = DisabledCommunicationForm(request.POST or None, instance=communication)
    password_form = SetPasswordForm(request.user, request.POST)

    if request.method == 'POST':

        data = request.POST.copy()
        person_form = DisabledPersonForm(data)

        if len(request.FILES) > 0:
            person.profileImage = request.FILES['profileImage']
            person.save()
            messages.success(request, 'Profil Fotoğrafı Başarıyla Güncellenmiştir.')

            log = str(user) + " Profil resmini degiştirdi."
            log = general_methods.logwrite(request, request.user, log)

        if password_form.is_valid():
            log = str(user) + "Şifresini degiştirdi."
            log = general_methods.logwrite(request, request.user, log)

            user.set_password(password_form.cleaned_data['new_password2'])
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Şifre Başarıyla Güncellenmiştir.')

            return redirect('sbs:antrenor')




        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'antrenor/antrenor-profil-guncelle.html',
                  {'user_form': user_form, 'communication_form': communication_form,
                   'person_form': person_form, 'password_form': password_form})

@login_required
def kademe_delete(request, grade_pk, coach_pk):
    perm = general_methods.control_access(request)


    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:

            obj = Level.objects.get(pk=grade_pk)
            coach = Coach.objects.get(pk=coach_pk)
            coach.grades.remove(obj)

            log = str(coach.user.get_full_name()) + " Kademe silindi "
            log = general_methods.logwrite(request, request.user, log)

            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Level.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})
    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def vize_delete(request, grade_pk, coach_pk):
    perm = general_methods.control_access(request)


    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:

            obj = Level.objects.get(pk=grade_pk)
            coach = Coach.objects.get(pk=coach_pk)
            coach.visa.remove(obj)

            coach = Coach.objects.get(pk=coach_pk)

            log = str(coach.user.get_full_name()) + " vize silindi"
            log = general_methods.logwrite(request, request.user, log)


            obj.delete()

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Level.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})
    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})



@login_required
def kademe_onay(request, grade_pk, coach_pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    grade = Level.objects.get(pk=grade_pk)
    coach = Coach.objects.get(pk=coach_pk)
    try:
        for item in coach.grades.all():
            if item.branch == grade.branch:
                item.isActive = False
                item.save()
        grade.status = Level.APPROVED
        grade.isActive = True
        grade.save()

        log = str(coach.user.get_full_name()) + " Kademe onaylandi"
        log = general_methods.logwrite(request, request.user, log)

        messages.success(request, 'Kademe   Onaylanmıştır')
    except:
        messages.warning(request, 'Lütfen yeniden deneyiniz.')
    return redirect('sbs:update-coach', pk=coach_pk)
@login_required
def visa_onay(request, grade_pk, coach_pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    visa = Level.objects.get(pk=grade_pk)
    visa.status = Level.APPROVED
    visa.save()

    coach = Coach.objects.get(pk=coach_pk)

    log = str(coach.user.get_full_name()) + " vize onaylandi"
    log = general_methods.logwrite(request, request.user, log)

    messages.success(request, 'Vize onaylanmıştır')
    return redirect('sbs:update-coach', pk=coach_pk)

@login_required
def kademe_reddet(request, grade_pk, coach_pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    grade = Level.objects.get(pk=grade_pk)
    grade.status = Level.DENIED
    grade.save()

    coach = Coach.objects.get(pk=coach_pk)

    log = str(coach.user.get_full_name()) + " Kademe reddedildi"
    log = general_methods.logwrite(request, request.user, log)

    messages.success(request, 'Kademe Reddedilmistir.')
    return redirect('sbs:update-coach', pk=coach_pk)


@login_required
def vize_reddet(request, grade_pk, coach_pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    visa = Level.objects.get(pk=grade_pk)
    visa.status = Level.DENIED
    visa.save()

    coach = Coach.objects.get(pk=coach_pk)

    log = str(coach.user.get_full_name()) + " vize reddedildi"
    log = general_methods.logwrite(request, request.user, log)

    messages.warning(request, 'Vize Reddedilmistir.')
    return redirect('sbs:update-coach', pk=coach_pk)



@login_required
def kademe_update(request, grade_pk, coach_pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    grade = Level.objects.get(pk=grade_pk)
    coach = Coach.objects.get(pk=coach_pk)
    categoryItem = Level.objects.get(pk=grade_pk)
    grade_form = GradeForm(request.POST or None, request.FILES or None, instance=grade,
                           initial={'definition': grade.definition})
    if request.method == 'POST':
        if grade_form.is_valid():
            grade_form.save()

            log = str(coach.user.get_full_name()) + " Kademe güncellendi"
            log = general_methods.logwrite(request, request.user, log)

            messages.success(request, 'Kademe Başarılı bir şekilde güncellenmiştir.')
            return redirect('sbs:update-coach', pk=coach_pk)

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'antrenor/kademe-update.html',
                  {'grade_form': grade_form})


@login_required
def kademe_list(request):
    perm = general_methods.control_access(request)
    active = general_methods.controlGroup(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    user_form = CoachSearchForm()
    searchClupForm = SearchClupForm()
    coachs = Coach.objects.none()
    user_form = CoachSearchForm()
    searchClupForm = SearchClupForm()

    if request.method == 'POST':
        user_form = CoachSearchForm(request.POST)
        searchClupForm = SearchClupForm(request.POST)
        branch = request.POST.get('branch')
        grade = request.POST.get('definition')
        visa = request.POST.get('visa')

        firstName = unicode_tr(request.POST.get('first_name')).upper()
        lastName = unicode_tr(request.POST.get('last_name')).upper()
        email = request.POST.get('email')

        if not (firstName or lastName or email or branch or grade or visa):
            if active == 'KlupUye':
                sc_user = SportClubUser.objects.get(user=user)
                clubsPk = []
                clubs = SportsClub.objects.filter(clubUser=sc_user)
                for club in clubs:
                    clubsPk.append(club.pk)
                coachs = Coach.objects.filter(sportsclub__in=clubsPk).distinct()
            elif active == 'Yonetim' or active == 'Admin':
                coachs = Coach.objects.all()
        else:
            query = Q()
            if lastName:
                query &= Q(user__last_name__icontains=lastName)
            if firstName:
                query &= Q(user__first_name__icontains=firstName)
            if email:
                query &= Q(user__email__icontains=email)
            if branch:
                query &= Q(grades__branch=branch, grades__status='Onaylandı')
            if grade:
                query &= Q(grades__definition__name=grade, grades__status='Onaylandı')
            if visa == 'VISA':
                query &= Q(visa__startDate__year=timezone.now().year, visa__status='Onaylandı')

            if active == 'KlupUye':
                sc_user = SportClubUser.objects.get(user=user)
                clubsPk = []
                clubs = SportsClub.objects.filter(clubUser=sc_user)
                for club in clubs:
                    clubsPk.append(club.pk)
                coachs = Coach.objects.filter(query).filter(sportsclub__in=clubsPk).distinct()
            elif active == 'Yonetim' or active == 'Admin':
                coachs = Coach.objects.filter(query)
            if visa == 'NONE':
                coachs = coachs.exclude(visa__startDate__year=timezone.now().year, visa__status='Onaylandı')

    # coa = []
    # for item in CategoryItem.objects.filter(forWhichClazz='COACH_GRADE'):
    #     coa.append(item.pk)
    # grade = Level.objects.filter(definition_id__in=coa, levelType=EnumFields.LEVELTYPE.GRADE).distinct()
    return render(request, 'antrenor/Kademe-Listesi.html',
                  {'coachs': coachs, 'user_form': user_form, 'branch': searchClupForm})




@login_required
def vize_list(request):
    perm = general_methods.control_access(request)
    active = general_methods.controlGroup(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    coachs = Coach.objects.none()
    user_form = CoachSearchForm()
    searchClupForm = SearchClupForm()

    if request.method == 'POST':
        user_form = CoachSearchForm(request.POST)
        searchClupForm = SearchClupForm(request.POST)
        branch = request.POST.get('branch')
        grade = request.POST.get('definition')
        visa = request.POST.get('visa')

        firstName = unicode_tr(request.POST.get('first_name')).upper()
        lastName = unicode_tr(request.POST.get('last_name')).upper()
        email = request.POST.get('email')

        if not (firstName or lastName or email or branch or grade or visa):
            if active == 'KlupUye':
                sc_user = SportClubUser.objects.get(user=user)
                clubsPk = []
                clubs = SportsClub.objects.filter(clubUser=sc_user)
                for club in clubs:
                    clubsPk.append(club.pk)
                coachs = Coach.objects.filter(sportsclub__in=clubsPk).distinct()
            elif active == 'Yonetim' or active == 'Admin':
                coachs = Coach.objects.all()
        else:
            query = Q()
            if lastName:
                query &= Q(user__last_name__icontains=lastName)
            if firstName:
                query &= Q(user__first_name__icontains=firstName)
            if email:
                query &= Q(user__email__icontains=email)
            if branch:
                query &= Q(grades__branch=branch, grades__status='Onaylandı')
            if grade:
                query &= Q(grades__definition__name=grade, grades__status='Onaylandı')
            if visa == 'VISA':
                query &= Q(visa__startDate__year=timezone.now().year, visa__status='Onaylandı')

            if active == 'KlupUye':
                sc_user = SportClubUser.objects.get(user=user)
                clubsPk = []
                clubs = SportsClub.objects.filter(clubUser=sc_user)
                for club in clubs:
                    clubsPk.append(club.pk)
                coachs = Coach.objects.filter(query).filter(sportsclub__in=clubsPk).distinct()
            elif active == 'Yonetim' or active == 'Admin':
                coachs = Coach.objects.filter(query)
            if visa == 'NONE':
                coachs = coachs.exclude(visa__startDate__year=timezone.now().year, visa__status='Onaylandı')
    return render(request, 'antrenor/Vize-Listesi.html',
                  {'coachs': coachs, 'user_form': user_form, 'branch': searchClupForm})



@login_required
def kademe_onayla(request, grade_pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    grade = Level.objects.get(pk=grade_pk)
    coach = grade.CoachGrades.first()
    try:
        for item in coach.grades.all():
            if item.branch == grade.branch:
                item.isActive = False
                item.save()
        grade.status = Level.APPROVED
        grade.isActive = True
        grade.save()
        messages.success(request, 'Kademe   Onaylanmıştır')
    except:
        messages.warning(request, 'Lütfen yeniden deneyiniz.')

    return redirect('sbs:kademe-listesi')

@login_required
def kademe_reddet_liste(request, grade_pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    grade = Level.objects.get(pk=grade_pk)
    grade.status = Level.DENIED
    grade.save()
    messages.success(request, 'Kademe   Onaylanmıştır')
    return redirect('sbs:kademe-listesi')

@login_required
def vize_onayla_liste(request, grade_pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    visa = Level.objects.get(pk=grade_pk)
    visa.status = Level.APPROVED
    visa.save()
    messages.success(request, 'Vize Onaylanmıştır')
    return redirect('sbs:vize-listesi')
@login_required
def vize_reddet_liste(request, grade_pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    visa = Level.objects.get(pk=grade_pk)
    visa.status = Level.DENIED
    visa.save()
    messages.success(request, 'Vize reddedilmistir.')
    return redirect('sbs:vize-listesi')


@login_required
def kademe_reddet_hepsi(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    coa = []
    for item in CategoryItem.objects.filter(forWhichClazz='COACH_GRADE'):
        coa.append(item.pk)
    Belt = Level.objects.filter(definition_id__in=coa, levelType=EnumFields.LEVELTYPE.GRADE, status="Beklemede")
    for belt in Belt:
        belt.status = CoachLevel.DENIED
        belt.save()
    messages.success(request, 'Beklemede olan kademeler   Onaylanmıştır')
    return redirect('sbs:kademe-listesi')


@login_required
def kademe_onay_hepsi(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    coa = []
    for item in CategoryItem.objects.filter(forWhichClazz='COACH_GRADE'):
        coa.append(item.pk)
    Belt = Level.objects.filter(definition_id__in=coa, levelType=EnumFields.LEVELTYPE.GRADE, status="Beklemede")

    for grade in Belt:
        coach = grade.CoachGrades.first()
        try:
            for item in coach.grades.all():
                if item.branch == grade.branch:
                    item.isActive = False
                    item.save()
            grade.status = Level.APPROVED
            grade.isActive = True
            grade.save()
            messages.success(request, 'Beklemede olan Kademeler Onaylanmıştır')
        except:
            messages.warning(request, 'Lütfen yeniden deneyiniz.')

    return redirect('sbs:kademe-listesi')


@login_required
def kademe_bekle_hepsi(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    Belt = CoachLevel.objects.filter(levelType=EnumFields.LEVELTYPE.GRADE)
    for belt in Belt:
        belt.status = CoachLevel.WAITED
        belt.save()
    messages.success(request, 'Kademe   Onaylanmıştır')
    return redirect('sbs:kademe-listesi')


@login_required
def antrenor_vısa_ekle(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    coach = Coach.objects.get(pk=pk)
    visa_form = VisaForm()
    category_item_form = CategoryItemForm()

    if request.method == 'POST':
        visa_form = VisaForm(request.POST, request.FILES)
        category_item_form = CategoryItemForm(request.POST, request.FILES)

        try:
            visa = Level(dekont=request.POST.get('dekont'), branch=request.POST.get('branch'))
            visa.startDate = date(int(request.POST.get('startDate')), 1, 1)
            visa.definition = CategoryItem.objects.get(forWhichClazz='VISA')
            visa.levelType = EnumFields.LEVELTYPE.VISA
            visa.status = Level.APPROVED

            for item in coach.visa.all():
                if item.branch == visa.branch:
                    item.isActive = False
                    item.save()
            visa.isActive = True
            visa.save()
            coach.visa.add(visa)
            coach.save()

            coach = Coach.objects.get(pk=coach_pk)

            log = str(coach.user.get_full_name()) + " vize eklendi"
            log = general_methods.logwrite(request, request.user, log)

            messages.success(request, 'Vize Başarıyla Eklenmiştir.')
            return redirect('sbs:update-coach', pk=pk)
        except:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'antrenor/Vize-ekle.html',
                  {'grade_form': visa_form, 'category_item_form': category_item_form})

@login_required
def vize_update(request, grade_pk, coach_pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    grade = Level.objects.get(pk=grade_pk)
    coach = Coach.objects.get(pk=coach_pk)
    grade_form = VisaForm(request.POST or None, request.FILES or None, instance=grade)

    if request.method == 'POST':
        if grade_form.is_valid():
            grade.save()
            messages.success(request, 'Vize Başarılı bir şekilde güncellenmiştir.')

            coach = Coach.objects.get(pk=coach_pk)

            log = str(coach.user.get_full_name()) + " vize güncellendi"
            log = general_methods.logwrite(request, request.user, log)

            return redirect('sbs:update-coach', pk=coach_pk)
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')
    return render(request, 'antrenor/Vize-update.html',
                  {'grade_form': grade_form})


@login_required
def choose_coach(request, pk):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    visa = VisaSeminar.objects.get(pk=pk)
    coa = []
    for item in visa.coach.all():
        coa.append(item.user.pk)

    athletes = Coach.objects.exclude(visaseminar__coach__user_id__in=coa)
    if request.method == 'POST':
        athletes1 = request.POST.getlist('selected_options')
        if athletes1:
            for x in athletes1:
                if not visa.coach.all().filter(beltexam__coachs__user_id=x):
                    visa.coach.add(x)
                    visa.save()
        return redirect('sbs:seminar-duzenle', pk=pk)
    return render(request, 'antrenor/visaSeminarCoach.html', {'athletes': athletes})


@login_required
def visaSeminar_Delete_Coach(request, pk, competition):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            visa = VisaSeminar.objects.get(pk=competition)
            visa.coach.remove(Coach.objects.get(pk=pk))
            visa.save()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def visaSeminar_onayla(request, pk):
    seminar = VisaSeminar.objects.get(pk=pk)
    if seminar.status == VisaSeminar.WAITED:

        for item in seminar.coach.all():

            visa = Level(dekont='Federasyon', branch=seminar.branch)
            visa.startDate = date(timezone.now().year, 1, 1)
            visa.definition = CategoryItem.objects.get(forWhichClazz='VISA')
            visa.levelType = EnumFields.LEVELTYPE.VISA
            visa.status = Level.APPROVED
            visa.isActive = True
            visa.save()
            for coach in item.visa.all():
                if coach.branch == visa.branch:
                    coach.isActive = False
                    coach.save()
            item.visa.add(visa)
            item.save()
        seminar.status = VisaSeminar.APPROVED
        seminar.save()
    else:
        messages.warning(request, 'Seminer Daha Önce Onaylanmistir.')

    return redirect('sbs:seminar-duzenle', pk=pk)

    return render(request, 'antrenor/VisaSeminar.html')
    # {'grade_form': grade_form})


@login_required
def coach_penal_add(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    athlete = Coach.objects.get(pk=pk)
    user = request.user

    penal_form = PenalForm()

    if request.method == 'POST':
        penal_form = PenalForm(request.POST, request.FILES or None)
        if penal_form.is_valid():
            ceza = penal_form.save()
            athlete.person.penal.add(ceza)
            athlete.save()
            messages.success(request, 'Belge Başarıyla Eklenmiştir.')

            log = str(athlete.user.get_full_name()) + " Ceza eklendi"
            log = general_methods.logwrite(request, request.user, log)
            return redirect('sbs:update-coach', pk=pk)



        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'antrenor/antrenor-ceza-ekle.html',
                  {'ceza': penal_form})


@login_required
def coach_penal_delete(request, athlete_pk, document_pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:

            athlete = Coach.objects.get(pk=athlete_pk)
            document = Penal.objects.get(pk=document_pk)
            athlete.person.penal.remove(document)
            athlete.save()
            document.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except CategoryItem.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def antrenor_belge_ekle(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    athlete = Coach.objects.get(pk=pk)
    user = request.user

    document_form = DocumentForm()

    if request.method == 'POST':
        document_form = DocumentForm(request.POST, request.FILES or None)
        if document_form.is_valid():
            document = document_form.save()
            athlete.person.document.add(document)
            athlete.save()
            messages.success(request, 'Belge Başarıyla Eklenmiştir.')

            log = str(athlete.user.get_full_name()) + " Belge eklendi"
            log = general_methods.logwrite(request, request.user, log)

            return redirect('sbs:update-coach', pk=pk)

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'antrenor/Antrenor-belge-ekle.html',
                  {'belge': document_form})


@login_required
def coach_document_delete(request, athlete_pk, document_pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:

            athlete = Coach.objects.get(pk=athlete_pk)
            document = Document.objects.get(pk=document_pk)
            athlete.person.document.remove(document)
            athlete.save()
            document.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except CategoryItem.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def visaSeminar_Onayla_Coach_application(request, pk, competition):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():

        try:
            coachApplication = CoachApplication.objects.get(pk=pk)
            seminer = VisaSeminar.objects.get(pk=competition)
            seminer.coach.add(coachApplication.coach)
            seminer.save()
            coachApplication.status = CoachApplication.APPROVED
            coachApplication.save()

            html_content = ''
            subject, from_email, to = 'Badminton Bilgi Sistemi', 'no-reply@badminton.gov.tr', coachApplication.coach.user.email
            html_content = '<h2>TÜRKİYE BADMİNTON FEDERASYONU BİLGİ SİSTEMİ</h2>'
            html_content = '<p><strong>' + str(seminer.name) + '</strong> Başvurunuz onaylanmıştır.</p>'

            msg = EmailMultiAlternatives(subject, '', from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            log = str(seminer.name) + "    seminer basvusu onaylanmıştır    " + str(
                coachApplication.coach.user.get_full_name())
            log = general_methods.logwrite(request, request.user, log)

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def visaSeminar_Delete_Coach_application(request, pk, competition):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        coachApplication = CoachApplication.objects.get(pk=pk)
        coachApplication.status = CoachApplication.DENIED
        coachApplication.save()

        seminer = VisaSeminar.objects.get(pk=competition)

        html_content = ''
        subject, from_email, to = 'Sbs Bilgi Sistemi', 'no-reply@badminton.gov.tr', coachApplication.coach.user.email
        html_content = '<h2>TÜRKİYE BADMİNTON FEDERASYONU BİLGİ SİSTEMİ</h2>'
        html_content = '<p><strong>' + str(seminer.name) + '</strong> Başvurunuz reddilmiştir.</p>'

        msg = EmailMultiAlternatives(subject, '', from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        log = str(seminer.name) + "    Seminer basvusu reddedilmiştir.    " + str(
            coachApplication.coach.user.get_full_name())
        log = general_methods.logwrite(request, request.user, log)

        # try:
        #     print()
        #
        #     return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        # except:
        #     return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def return_visaSeminar_Basvuru(request):
    perm = general_methods.control_access_klup(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user
    basvurularim = CoachApplication.objects.none()
    if request.user.groups.filter(name='Antrenor').exists():
        seminar = VisaSeminar.objects.filter(coachApplication__coach__user=user).filter(
            forWhichClazz='COACH').distinct()
        basvurularim = CoachApplication.objects.filter(coach__user=user)

    else:
        seminar = VisaSeminar.objects.filter(forWhichClazz='COACH')

    return render(request, 'antrenor/VizeSeminerBasvuru.html', {'seminer': seminar,
                                                                'basvuru': basvurularim,
                                                                'user': user})
