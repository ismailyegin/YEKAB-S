import traceback

from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User, Group
from django.db import transaction
from django.db.models import Q
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from unicode_tr import unicode_tr

from ekabis.Forms.CategoryItemForm import CategoryItemForm
from ekabis.Forms.CommunicationForm import CommunicationForm
from ekabis.Forms.DisabledCommunicationForm import DisabledCommunicationForm
from ekabis.Forms.DisabledPersonForm import DisabledPersonForm
from ekabis.Forms.DisabledUserForm import DisabledUserForm
from ekabis.Forms.EmployeeForm import EmployeeForm
from ekabis.Forms.PersonForm import PersonForm
from ekabis.Forms.UserForm import UserForm
from ekabis.Forms.UserSearchForm import UserSearchForm
from ekabis.models.Communication import Communication
from ekabis.models.Person import Person
from ekabis.models.CategoryItem import CategoryItem
from ekabis.models.Country import Country
from ekabis.models.Employee import Employee
from ekabis.services import general_methods
from ekabis.services.general_methods import get_error_messages
from ekabis.services.services import CategoryItemService, EmployeeService


@login_required
def add_employee(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    user_form = UserForm()
    person_form = PersonForm()
    communication = Communication()
    communication_form = CommunicationForm()
    employee_form = EmployeeForm()
    categorItemfilter = {
        'forWhichClazz': "EMPLOYEE_WORKDEFINITION"

    }
    employee_form.fields['workDefinition'].queryset = CategoryItemService(request, categorItemfilter)
    try:
        with transaction.atomic():
            if request.method == 'POST':
                user_form = UserForm(request.POST)
                person_form = PersonForm(request.POST, request.FILES)
                communication_form = CommunicationForm(request.POST, request.FILES)

                employe_form = EmployeeForm(request.POST)

                if user_form.is_valid() and person_form.is_valid() and communication_form.is_valid() and employe_form.is_valid():
                    user = User()
                    user.username = user_form.cleaned_data['email']
                    user.firstName = unicode_tr(user_form.cleaned_data['first_name']).upper()
                    user.lastName = unicode_tr(user_form.cleaned_data['last_name']).upper()
                    user.email = user_form.cleaned_data['email']
                    group = Group.objects.get(name=request.POST.get('group'))
                    password = User.objects.make_random_password()
                    user.set_password(password)
                    user.save()
                    user.groups.add(group)
                    user.save()

                    person = person_form.save(commit=False)
                    communication = communication_form.save(commit=False)
                    person.save()
                    communication.save()

                    personel = Employee(
                        user=user, person=person, communication=communication,
                        workDefinition=employe_form.cleaned_data['workDefinition'],

                    )

                    personel.save()

                    log = str(user.get_full_name()) + " personelini  kaydetti"
                    log = general_methods.logwrite(request, request.user, log)
                    messages.success(request, 'Personel Başarıyla Kayıt Edilmiştir.')

                    return redirect('ekabis:view_employee')

                else:

                    for x in user_form.errors.as_data():
                        messages.warning(request, user_form.errors[x].first())

                    error_message_company = get_error_messages(user_form)
                    error_messages_person = get_error_messages(person_form)
                    error_messages_communication = get_error_messages(communication_form)
                    error_messages_employee = get_error_messages(employe_form)
                    error_messages = error_messages_communication + error_message_company + error_messages_person + error_messages_employee

                    return render(request, 'personel/personel-ekle.html',
                                  {'user_form': user_form, 'person_form': person_form,
                                   'communication_form': communication_form,
                                   'employee_form': employee_form, 'error_messages': error_messages,
                                   })

            return render(request, 'personel/personel-ekle.html',
                          {'user_form': user_form, 'person_form': person_form, 'communication_form': communication_form,
                           'employee_form': employee_form,
                           })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:add_employee')


@login_required
def edit_employee(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    employefilter = {
        'uuid': pk
    }
    employee = EmployeeService(request, employefilter).first()
    user_form = UserForm(request.POST or None, instance=employee.user)
    person_form = PersonForm(request.POST or None, request.FILES or None, instance=employee.person)
    communication_form = CommunicationForm(request.POST or None, instance=employee.communication)

    employee_form = EmployeeForm(request.POST or None, instance=employee)
    categoryfilter = {
        'forWhichClazz': "EMPLOYEE_WORKDEFINITION"
    }
    employee_form.fields['workDefinition'].queryset = CategoryItemService(request, categoryfilter)

    try:
        with transaction.atomic():
            if request.method == 'POST':

                if user_form.is_valid() and communication_form.is_valid() and person_form.is_valid() and employee_form.is_valid():

                    user = user_form.save(commit=False)
                    user.username = user_form.cleaned_data['email']
                    user.first_name = user_form.cleaned_data['first_name']
                    user.last_name = user_form.cleaned_data['last_name']
                    user.email = user_form.cleaned_data['email']
                    user.save()
                    person_form.save()
                    communication_form.save()
                    employee_form.save()

                    log = str(user.get_full_name()) + " personel güncellendi"
                    log = general_methods.logwrite(request, request.user, log)

                    messages.success(request, 'Personel Başarıyla Güncellenmiştir.')

                    return redirect('ekabis:view_employee')

                else:

                    for x in user_form.errors.as_data():
                        messages.warning(request, user_form.errors[x].first())

                    error_message_company = get_error_messages(user_form)
                    error_messages_communication = get_error_messages(communication_form)
                    error_messages_person = get_error_messages(person_form)
                    error_messages_employee = get_error_messages(employee_form)

                    error_messages = error_messages_communication + error_message_company + error_messages_person + error_messages_employee
                    return render(request, 'personel/personel-duzenle.html',
                                  {'user_form': user_form, 'communication_form': communication_form,
                                   'person_form': person_form, 'employee_form': employee_form,
                                   'error_messages': error_messages,
                                   })

            return render(request, 'personel/personel-duzenle.html',
                          {'user_form': user_form, 'communication_form': communication_form,
                           'person_form': person_form, 'employee_form': employee_form, 'error_messages': '',
                           })

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:change_employee', pk)


@login_required
def delete_employee(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']

                empoyefilter = {
                    'uuid': uuid
                }
                obj = EmployeeService(request, empoyefilter).first()
                obj.isDeleted = True
                obj.save()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})


            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def return_employees(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    user_form = UserSearchForm()
    employees = None
    get = request.GET.get('get')
    if get:
        if get == 'hepsi':
            employees = EmployeeService(request, None)
    try:
        with transaction.atomic():
            if request.method == 'POST':

                user_form = UserSearchForm(request.POST)

                if user_form.is_valid():
                    firstName = user_form.cleaned_data.get('first_name')
                    lastName = user_form.cleaned_data.get('last_name')
                    email = user_form.cleaned_data.get('email')
                    workDefinition = user_form.cleaned_data.get('workDefinition')
                    group = request.POST.get('group')
                    if not (firstName or lastName or email or workDefinition or group):
                        personfilter = {
                            'isDeleted': False
                        }
                        employees = EmployeeService(request, personfilter)

                    else:
                        query = Q()
                        if lastName:
                            query &= Q(user__last_name__icontains=lastName)
                        if firstName:
                            query &= Q(user__first_name__icontains=firstName)
                        if email:
                            query &= Q(user__email__icontains=email)
                        if workDefinition:
                            query &= Q(workDefinition=workDefinition)
                        if group:
                            query &= Q(user__groups__name=group)

                        employees = EmployeeService(request, query)

        return render(request, 'personel/personeller.html',
                      {'employees': employees, 'user_form': user_form, })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_employee')


@login_required
def return_workdefinitionslist(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    category_item_form = CategoryItemForm()
    try:
        with transaction.atomic():
            if request.method == 'POST':

                category_item_form = CategoryItemForm(request.POST)
                name = request.POST.get('name')
                if name is not None:
                    categoryItem = CategoryItem(name=name)
                    categoryItem.forWhichClazz = "EMPLOYEE_WORKDEFINITION"
                    categoryItem.isFirst = False
                    categoryItem.save()

                    log = str(name) + " unvanini ekledi"
                    log = general_methods.logwrite(request, request.user, log)

                    return redirect('ekabis:view_categoryitem')

                else:

                    messages.warning(request, 'Alanları Kontrol Ediniz')

        categoryfilter = {
            'forWhichClazz': "EMPLOYEE_WORKDEFINITION",
            'isDeleted': False
        }
        categoryitem = CategoryItemService(request, categoryfilter)
        return render(request, 'personel/unvanListesi.html',
                      {'category_item_form': category_item_form, 'categoryitem': categoryitem})
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_categoryitem')


@login_required
def delete_workdefinition(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():

                categoryfilter = {
                    'pk': pk
                }
                obj = CategoryItemService(request, categoryfilter).first()

                log = str(obj.name) + " unvani sildi"
                log = general_methods.logwrite(request, log)

                obj.delete()

                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except CategoryItem.DoesNotExist:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def edit_workdefinition(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    categoryfilter = {
        'pk': pk
    }
    categoryItem = CategoryItemService(request, categoryfilter).first()
    category_item_form = CategoryItemForm(request.POST or None, instance=categoryItem)
    try:
        with transaction.atomic():
            if request.method == 'POST':

                if request.POST.get('name') is not None:
                    categoryItem.name = request.POST.get('name')
                    categoryItem.save()
                    messages.success(request, 'Başarıyla Güncellendi')

                    log = str(request.POST.get('name')) + " is tanimi güncelledi"
                    log = general_methods.logwrite(request, log)
                    return redirect('ekabis:istanimiListesi')
                else:
                    messages.warning(request, 'Alanları Kontrol Ediniz')

            return render(request, 'personel/istanimi-duzenle.html',
                          {'category_item_form': category_item_form})
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')


@login_required
def edit_workdefinitionUnvan(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    categoryfilter = {
        'uuid': uuid
    }
    categoryItem = CategoryItemService(request, categoryfilter).first()
    category_item_form = CategoryItemForm(request.POST or None, instance=categoryItem)
    try:
        with transaction.atomic():
            if request.method == 'POST':

                if request.POST.get('name') is not None:
                    categoryItem.name = request.POST.get('name')
                    categoryItem.save()
                    messages.success(request, 'Başarıyla Güncellendi')

                    log = str(request.POST.get('name')) + " Unvan güncelledi"
                    log = general_methods.logwrite(request, request.user, log)
                    return redirect('ekabis:view_categoryitem')
                else:
                    messages.warning(request, 'Alanları Kontrol Ediniz')

        return render(request, 'personel/unvan-duzenle.html',
                      {'category_item_form': category_item_form})
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_categoryitem')


@login_required
def delete_employeetitle(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            with transaction.atomic():
                uuid = request.POST['uuid']
                categoryfilter = {
                    'uuid': uuid
                }
                obj = CategoryItemService(request, categoryfilter).first()
                obj.isDeleted = True
                obj.save()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except CategoryItem.DoesNotExist:
            traceback.print_exc()
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def updateRefereeProfile(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    employeefilter = {
        'user': request.user
    }
    employee = EmployeeService(request, employeefilter).first()
    user_form = DisabledUserForm(request.POST or None, instance=employee.user)
    person_form = DisabledPersonForm(request.POST or None, request.FILES or None, instance=employee.person)
    communication_form = DisabledCommunicationForm(request.POST or None, instance=employee.communication)
    password_form = SetPasswordForm(request.user, request.POST)

    if request.method == 'POST':
        person_form = DisabledPersonForm(request.POST, request.FILES)
        try:
            with transaction.atomic():
                if request.FILES['profileImage']:
                    employee.person.profileImage = request.FILES['profileImage']
                    employee.person.save()
                    messages.success(request, 'Resim güncellendi.')
        except Exception as e:
            print(e)
        if password_form.is_valid():
            employee.user.set_password(password_form.cleaned_data['new_password2'])
            employee.user.save()
            update_session_auth_hash(request, employee.user)
            messages.success(request, 'Şifre Başarıyla Güncellenmiştir.')
            return redirect('ekabis:personel-profil-guncelle')

        else:
            error_message_company = get_error_messages(password_form)
            # error_messages_communication = get_error_messages(communication_form)
            # error_messages_person = get_error_messages(person_form)
            # error_messages_employee = get_error_messages(communication_form)

            error_messages = password_form
            return render(request, 'personel/Personel-Profil-güncelle.html',
                          {'user_form': user_form, 'communication_form': communication_form,
                           'person_form': person_form, 'password_form': password_form,
                           'error_messages': error_messages})
    return render(request, 'personel/Personel-Profil-güncelle.html',
                  {'user_form': user_form, 'communication_form': communication_form,
                   'person_form': person_form, 'password_form': password_form, 'error_messages': ''})
