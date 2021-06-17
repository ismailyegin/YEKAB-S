from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

from sbs.Forms.CommunicationForm import CommunicationForm
from sbs.Forms.DisabledCommunicationForm import DisabledCommunicationForm
from sbs.Forms.DisabledPersonForm import DisabledPersonForm
from sbs.Forms.DisabledSportClubUserForm import DisabledSportClubUserForm
from sbs.Forms.DisabledUserForm import DisabledUserForm
from sbs.Forms.PersonForm import PersonForm
from sbs.Forms.SportClubUserForm import SportClubUserForm
from sbs.Forms.UserForm import UserForm
from sbs.Forms.UserSearchForm import UserSearchForm
from sbs.services import general_methods

from sbs.models import ActiveGroup, Coach, Judge, DirectoryMember, SportClubUser, Athlete, ClubRole, Person, \
    Communication, DirectoryMemberRole, DirectoryCommission


@login_required
def updateProfile(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    user = request.user
    user_form = DisabledUserForm(request.POST or None, instance=user)
    password_form = SetPasswordForm(request.user, request.POST)
    if request.method == 'POST':
        if password_form.is_valid():
            user.set_password(password_form.cleaned_data['new_password1'])
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Şifre Başarıyla Güncellenmiştir.')
            aktif = general_methods.controlGroup(request)
            if aktif == "Admin":
                log = str(user.get_full_name()) + " admin sifre guncellendi"
                log = general_methods.logwrite(request, request.user, log)
                return redirect('sbs:admin-profil-guncelle')
            elif aktif == "Arsiv":
                log = str(user.get_full_name()) + " arsiv yönetici sifre guncellendi"
                log = general_methods.logwrite(request, request.user, log)
                return redirect('sbs:evrak-anasayfa')
        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'admin/admin-profil-guncelle.html',
                  {'user_form': user_form, 'password_form': password_form})


@login_required
def activeGroup(request, pk):
    group = Group.objects.get(name=request.GET.get('group'))
    pk = request.GET.get('pk')
    communication = Communication.objects.get(pk=request.GET.get('communication'))
    person = Person.objects.get(pk=request.GET.get('person'))
    user = User.objects.get(pk=request.GET.get('user'))

    if group.name == "Antrenor":
        coach = Coach(person=person,
                      communication=communication,
                      user=user)
        coach.save()
        user.groups.add(group)
        user.save()
        return redirect('sbs:update-coach', pk=coach.pk)
    elif group.name == "Hakem":
        judge = Judge(person=person,
                      communication=communication, user=user)
        judge.save()
        user.groups.add(group)
        user.save()
        return redirect('sbs:hakem-duzenle', pk=judge.pk)
    elif group.name == "Admin":
        user.groups.add(group)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        return redirect('sbs:admin')
    elif group.name == "KlupUye":
        clupuser = SportClubUser(person=person,
                                 communication=communication, user=user, role=ClubRole.objects.all()[0])
        clupuser.save()
        user.groups.add(group)
        user.save()
        return redirect('sbs:kulup-uyesi-guncelle', pk=clupuser.pk)
    elif group.name == "Sporcu":
        athlete = Athlete(person=person,
                          communication=communication,
                          user=user)
        athlete.save()
        user.groups.add(group)
        user.save()
        return redirect('sbs:update-athletes', pk=athlete.pk)
    elif group.name == "Yonetim":
        member = DirectoryMember(person=person, communication=communication, user=user,
                                 role=DirectoryMemberRole.objects.all()[0],
                                 commission=DirectoryCommission.objects.all()[0])
        member.save()
        user.groups.add(group)
        user.save()
        return redirect('sbs:kurul-uyesi-duzenle', pk=member.pk)
    return {}
