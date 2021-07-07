import traceback

from django.contrib.auth.models import User, Group
from django.db import transaction
from django.db.models import Q

from ekabis.models import ConnectionRegion, ConnectionCapacity
from ekabis.models.ActiveGroup import ActiveGroup
from ekabis.models.CategoryItem import CategoryItem
from ekabis.models.Claim import Claim
from ekabis.models.Communication import Communication
from ekabis.models.Company import Company
from ekabis.models.ConnectionUnit import ConnectionUnit
from ekabis.models.DirectoryCommission import DirectoryCommission
from ekabis.models.DirectoryMember import DirectoryMember
from ekabis.models.DirectoryMemberRole import DirectoryMemberRole
from ekabis.models.Employee import Employee
from ekabis.models.Logs import Logs
from ekabis.models.Menu import Menu
from ekabis.models.MenuAdmin import MenuAdmin
from ekabis.models.MenuDirectory import MenuDirectory
from ekabis.models.MenuPersonel import MenuPersonel
from ekabis.models.Notification import Notification
from ekabis.models.Permission import Permission
from ekabis.models.PermissionGroup import PermissionGroup
from ekabis.models.Person import Person
from ekabis.models.Settings import Settings


def UserService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                return User.objects.filter(**filter)
            else:
                return User.objects.filter(filter)
        else:
            return User.objects.all()
    except User.DoesNotExist:
        return None
    except Exception as e:
        traceback.print_exc()
        print(e)
        pass


def GroupService(request, filter):
    try:
        if filter:
            return Group.objects.filter(**filter)
        else:
            return Group.objects.all()
    except Group.DoesNotExist:
        return None
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass


def PersonService(request, filter):
    try:
        if filter:
            return Person.objects.filter(**filter)
        else:
            return Person.objects.all()
    # except Person.DoesNotExist:
    #     return None
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass


def CommunicationService(request, filter):
    try:
        if filter:
            return Communication.objects.filter(**filter)
        else:
            return Communication.objects.all()
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass


def CategoryItemService(request, filter):
    try:
        if filter:
            return CategoryItem.objects.filter(**filter)
        else:
            return CategoryItem.objects.all()
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass


def CompanyService(request, filter):
    try:
        if filter:
            return Company.objects.filter(**filter)
        else:
            return Company.objects.all()
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass


def DirectoryMemberService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                return DirectoryMember.objects.filter(**filter)
            else:
                return DirectoryMember.objects.filter(filter)
        else:
            return DirectoryMember.objects.all()
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass


def DirectoryCommissionService(request, filter):
    try:
        if filter:
            return DirectoryCommission.objects.filter(**filter)
        else:
            return DirectoryCommission.objects.all()
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass


def DirectoryMemberRoleService(request, filter):
    try:
        with transaction.atomic():

            if filter:
                return DirectoryMemberRole.objects.filter(**filter)
            else:
                return DirectoryMemberRole.objects.all()
    except Exception as e:
        traceback.print_exc()
        print(e)
        pass


def EmployeeService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                return Employee.objects.filter(**filter)
            else:
                Employee.objects.filter(filter)
        else:
            return Employee.objects.all()
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass


def LogsService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                return Logs.objects.filter(**filter)
            else:
                return Logs.objects.filter(filter)
        else:
            return Logs.objects.all()
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass


def MenuService(request, filter):
    try:
        if filter:
            return Menu.objects.filter(**filter)
        else:
            return Menu.objects.all()
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass


def MenuAdminService(request, filter):
    try:
        if filter:
            return MenuAdmin.objects.filter(**filter).order_by("sorting")
        else:
            return MenuAdmin.objects.all().order_by("sorting")
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass


def MenuDirectoryService(request, filter):
    try:
        if filter:
            return MenuDirectory.objects.filter(**filter).order_by("sorting")
        else:
            return MenuDirectory.objects.all().order_by("sorting")
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass


def MenuPersonelService(request, filter):
    try:
        if filter:
            return MenuPersonel.objects.filter(**filter).order_by("sorting")
        else:
            return MenuPersonel.objects.all().order_by("sorting")
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass


def NotificationService(request, filter):
    try:
        if filter:
            return Notification.objects.filter(**filter)
        else:
            return Notification.objects.all()
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass


def ActiveGroupService(request, filter):
    try:
        if filter:
            return ActiveGroup.objects.filter(**filter)
        else:
            return ActiveGroup.objects.all()
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass


def PermissionService(request, filter):
    try:
        if filter:
            return Permission.objects.filter(**filter)
        else:
            return Permission.objects.all()
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass


def ClaimService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                return Claim.objects.filter(**filter)
            else:
                return Claim.objects.filter(filter)
        else:
            return Claim.objects.all()
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass


def PermissionGroupService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                return PermissionGroup.objects.filter(**filter)
            else:
                return PermissionGroup.objects.filter(filter)
        else:
            return PermissionGroup.objects.all()
    except Exception as e:
        traceback.print_exc()


def SettingsService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                return Settings.objects.filter(**filter)
            else:
                return Settings.objects.filter(filter)
        else:
            return Settings.objects.all()
    except Exception as e:
        traceback.print_exc()


def UnitService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return ConnectionUnit.objects.filter(**filter)
            else:
                return ConnectionUnit.objects.all()
    except Exception as e:
        traceback.print_exc()
        print(e)
        pass


def RegionService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return ConnectionRegion.objects.filter(**filter)
            else:
                return ConnectionRegion.objects.all()
    except Exception as e:
        traceback.print_exc()
        print(e)
        pass


def CapacityService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return ConnectionCapacity.objects.filter(**filter)
            else:
                return ConnectionCapacity.objects.all()
    except Exception as e:
        traceback.print_exc()
        print(e)
        pass
