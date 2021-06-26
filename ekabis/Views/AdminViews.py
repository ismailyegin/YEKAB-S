from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.shortcuts import render, redirect
from ekabis.Forms.DisabledUserForm import DisabledUserForm
from ekabis.services import general_methods
from ekabis.models import ActiveGroup, DirectoryMember, Person,Communication, DirectoryMemberRole, DirectoryCommission,Employee,CategoryItem


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
            log = str(user.get_full_name()) + " admin sifre guncellendi"
            log = general_methods.logwrite(request, request.user, log)
            return redirect('ekabis:admin-profil-guncelle')

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

    if group.name == "Admin":
        user.groups.add(group)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        return redirect('ekabis:admin')
    elif group.name == "Personel":
        clupuser = Employee(person=person,
                                 communication=communication, user=user,workDefinition=CategoryItem.objects.all()[0])
        clupuser.save()
        user.groups.add(group)
        user.save()
        return redirect('ekabis:kulup-uyesi-guncelle', pk=clupuser.pk)

    elif group.name == "Yonetim":
        member = DirectoryMember(person=person, communication=communication, user=user,
                                 role=DirectoryMemberRole.objects.all()[0],
                                 commission=DirectoryCommission.objects.all()[0])
        member.save()
        user.groups.add(group)
        user.save()
        return redirect('ekabis:admin:kurul-uyesi-duzenle', pk=member.pk)
    return {}
