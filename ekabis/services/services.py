import traceback

from django.contrib.auth.models import User, Group
from django.db import transaction
from django.db.models import Q
from django.urls import resolve

from ekabis.models import ConnectionRegion, Yeka, YekaPersonHistory, YekaCompany, \
    YekaCompanyHistory, HistoryGroup, ExtraTime, Country, City, BusinessBlog, BusinessBlogParametreType, YekaCompetition
from ekabis.models.ActiveGroup import ActiveGroup
from ekabis.models.CategoryItem import CategoryItem
from ekabis.models.Claim import Claim
from ekabis.models.Communication import Communication
from ekabis.models.Company import Company
from ekabis.models.YekaCompetitionPerson import YekaCompetitionPerson
from ekabis.models.DirectoryCommission import DirectoryCommission
from ekabis.models.DirectoryMember import DirectoryMember
from ekabis.models.DirectoryMemberRole import DirectoryMemberRole
from ekabis.models.Employee import Employee
from ekabis.models.Logs import Logs
from ekabis.models.Menu import Menu
from ekabis.models.Notification import Notification
from ekabis.models.Permission import Permission
from ekabis.models.PermissionGroup import PermissionGroup
from ekabis.models.Person import Person
from ekabis.models.Settings import Settings
from ekabis.models import YekaConnectionRegion,YekaPersonHistory,YekaPerson,YekaBusiness,YekaBusinessBlog,YekaBusinessBlogParemetre,ConnectionRegion,ConnectionUnit,CompanyUser,CompanyFiles,CompanyFileNames,CalendarName,Calendar
from ekabis.models.ExtraTimeFile import ExtraTimeFile

def CityService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                return City.objects.filter(**filter)
            else:
                return City.objects.filter(filter,isDeleted=False)
        else:
            return City.objects.filter(isDeleted=False)
    except City.DoesNotExist:
        return None
    except Exception as e:
        traceback.print_exc()
def YekaCompanyService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                return YekaCompany.objects.filter(**filter)
            else:
                return YekaCompany.objects.filter(filter,isDeleted=False)
        else:
            return YekaCompany.objects.filter(isDeleted=False)
    except YekaCompany.DoesNotExist:
        return None
    except Exception as e:
        traceback.print_exc()
def YekaPersonService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                return YekaPerson.objects.filter(**filter)
            else:
                return YekaPerson.objects.filter(filter,isDeleted=False)
        else:
            return YekaPerson.objects.filter(isDeleted=False)
    except YekaPerson.DoesNotExist:
        return None
    except Exception as e:
        traceback.print_exc()

def YekaCompetitionServiceService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                return YekaCompetition.objects.filter(**filter)
            else:
                return YekaCompetition.objects.filter(filter,isDeleted=False)
        else:
            return YekaCompetition.objects.filter(isDeleted=False)
    except YekaCompetition.DoesNotExist:
        return None
    except Exception as e:
        traceback.print_exc()

def YekaConnectionRegionService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                return YekaConnectionRegion.objects.filter(**filter)
            else:
                return YekaConnectionRegion.objects.filter(filter,isDeleted=False)
        else:
            return YekaConnectionRegion.objects.filter(isDeleted=False)
    except YekaConnectionRegion.DoesNotExist:
        return None
    except Exception as e:
        traceback.print_exc()
def ConnectionRegionService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                return ConnectionRegion.objects.filter(**filter)
            else:
                return ConnectionRegion.objects.filter(filter,isDeleted=False)
        else:
            return ConnectionRegion.objects.filter(isDeleted=False)
    except ConnectionRegion.DoesNotExist:
        return None
    except Exception as e:
        traceback.print_exc()


def ExtraTimeService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                return ExtraTime.objects.filter(**filter)
            else:
                return ExtraTime.objects.filter(filter,isDeleted=False)
        else:
            return ExtraTime.objects.filter(isDeleted=False)
    except ExtraTime.DoesNotExist:
        return None
    except Exception as e:
        traceback.print_exc()


def CalendarNameService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                return CalendarName.objects.filter(**filter)
            else:
                return CalendarName.objects.filter(filter,isDeleted=False)
        else:
            return CalendarName.objects.filter(isDeleted=False)
    except CalendarName.DoesNotExist:
        return None
    except Exception as e:
        traceback.print_exc()


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
            return Person.objects.filter(isDeleted=False)
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
            return Communication.objects.filter(isDeleted=False)
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass


def CategoryItemService(request, filter):
    try:
        if filter:
            return CategoryItem.objects.filter(**filter)
        else:
            return CategoryItem.objects.filter(isDeleted=False)
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass


def CompanyService(request, filter):
    try:
        if filter:
            return Company.objects.filter(**filter)
        else:
            return Company.objects.filter(isDeleted=False)
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
                return DirectoryMember.objects.filter(filter,isDeleted=False)
        else:
            return DirectoryMember.objects.filter(isDeleted=False)
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass


def DirectoryCommissionService(request, filter):
    try:
        if filter:
            return DirectoryCommission.objects.filter(**filter)
        else:
            return DirectoryCommission.objects.filter(isDeleted=False)
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
                return DirectoryMemberRole.objects.filter(isDeleted=False)
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
                Employee.objects.filter(filter,isDeleted=False)
        else:
            return Employee.objects.filter(isDeleted=False)
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
                return Logs.objects.filter(filter,isDeleted=False)
        else:
            return Logs.objects.filter(isDeleted=False)
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass


def MenuService(request, filter):
    try:
        if filter:
            return Menu.objects.filter(**filter)
        else:
            return Menu.objects.filter(isDeleted=False)
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass


def NotificationService(request, filter):
    try:
        if filter:
            return Notification.objects.filter(**filter)
        else:
            return Notification.objects.filter(isDeleted=False)
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass


def ActiveGroupService(request, filter):
    try:
        if filter:
            return ActiveGroup.objects.filter(**filter)
        else:
            return ActiveGroup.objects.filter(isDeleted=False)
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass



def YekaCompetitionPersonService(request, filter):
    try:
        if filter:
            return YekaCompetitionPerson.objects.filter(**filter)
        else:
            return YekaCompetitionPerson.objects.filter(isDeleted=False)
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass

def PermissionService(request, filter):
    try:
        if filter:
            return Permission.objects.filter(**filter)
        else:
            return Permission.objects.filter(isDeleted=False)
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass

def CompanyFileNamesService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return CompanyFileNames.objects.filter(**filter)
            else:
                return CompanyFileNames.objects.filter(isDeleted=False)
    except Exception as e:
        traceback.print_exc()
        pass
def ClaimService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                return Claim.objects.filter(**filter)
            else:
                return Claim.objects.filter(filter,isDeleted=False)
        else:
            return Claim.objects.filter(isDeleted=False)
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
                return PermissionGroup.objects.filter(filter,isDeleted=False)
        else:
            return PermissionGroup.objects.filter(isDeleted=False)
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
                return ConnectionUnit.objects.filter(isDeleted=False)
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
                return ConnectionRegion.objects.filter(isDeleted=False)
    except Exception as e:
        traceback.print_exc()
        print(e)
        pass

def ExtraTimeFileService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return ExtraTimeFile.objects.filter(**filter)
            else:
                return ExtraTimeFile.objects.filter(isDeleted=False)
    except Exception as e:
        traceback.print_exc()
        print(e)
        pass

def YekaService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return Yeka.objects.filter(**filter)
            else:
                return Yeka.objects.filter(isDeleted=False)
    except Exception as e:
        traceback.print_exc()
        pass

# get servisler
def YekaGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return Yeka.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def UserGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return User.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def YekaPersonGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return YekaPerson.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass
def YekaConnectionRegionGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return YekaConnectionRegion.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass



def YekaCompanyGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return YekaCompany.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass
def YekaCompanyHistoryGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return YekaCompanyHistory.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass
def YekaBusinessGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return YekaBusiness.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass
def YekaBusinessBlogGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return YekaBusinessBlog.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass
def YekaBusinessBlogParemetreGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return YekaBusinessBlogParemetre.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass




def SettingsGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return Settings.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def PersonGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return Person.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def PermissionGetService(request, filter,isDeleted=False):
    try:
        with transaction.atomic():
            if filter:
                return Permission.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def PermissionGroupGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return PermissionGroup.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def NotificationGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return Notification.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def UserGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return User.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def MenuGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return Menu.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def LogsGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return Logs.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def HistoryGroupGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return HistoryGroup.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass
def ExtraTimeFileGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return ExtraTimeFile.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass



def ExtraTimeGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return ExtraTime.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def EmployeeGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return Employee.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def DirectoryCommissionGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return DirectoryCommission.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def DirectoryMemberRoleGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return DirectoryMemberRole.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def DirectoryMemberGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return DirectoryMember.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def ConnectionUnitGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return ConnectionUnit.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def ConnectionRegionGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return ConnectionRegion.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass



def CompanyUserGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return CompanyUser.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def CompanyFilesGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return CompanyFiles.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def CompanyFileNamesGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return CompanyFileNames.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def CompanyGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return Company.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def CommunicationGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return Communication.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass
def YekaCompetitionPersonGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return YekaCompetitionPerson.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass

def YekaCompetitionGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return YekaCompetition.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass
from ekabis.models import YekaConnectionRegion, YekaPersonHistory, YekaPerson, YekaBusiness, YekaBusinessBlog, \
    YekaBusinessBlogParemetre, SubYekaCapacity, ConnectionRegion, ConnectionCapacity, ConnectionUnit, CompanyUser, \
    CompanyFiles, CompanyFileNames, CalendarName, Calendar
from ekabis.models.VacationDay import VacationDay

def ClaimGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return Claim.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def CountryGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return Country.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def CityGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return City.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def CategoryItemGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return CategoryItem.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def CalendarNameGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return CalendarName.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def CalendarGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return Calendar.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def BusinessBlogGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return BusinessBlog.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def BusinessBlogParametreTypeGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return BusinessBlogParametreType.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def ActiveGroupGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return ActiveGroup.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def GroupGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return Group.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass





def GroupExcludeService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return Group.objects.exclude(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()


def VacationDayGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return VacationDay.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def VacationDayService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return VacationDay.objects.filter(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def last_urls(request):
    try:
        urls = []
        from urllib.parse import urlparse
        from ekabis.urls import urlpatterns

        last_url_name = ""
        current_url_name = resolve(request.path_info).url_name
        with transaction.atomic():
            if request.META.get('HTTP_REFERER'):
                for urlpattern in urlpatterns:
                    if str(urlpattern.pattern) == \
                            urlparse(request.META.get('HTTP_REFERER')).path.split('/yekabis/')[1]:
                        last_url_name = urlpattern.name

                url = {
                    'last': request.META.get('HTTP_REFERER'),
                    'last_url_name': Permission.objects.get(codename=last_url_name).name,
                    # 'current': request.get_full_path(),
                    # 'current_name': Permission.objects.get(codename=current_url_name).name,
                }
                urls.append(url)

            else:
                url = {
                    'last': '',
                    # 'current': request.get_full_path(),
                    # 'current_name': Permission.objects.get(codename=current_url_name).name,
                }
                urls.append(url)

            return urls
    except Exception as e:
        traceback.print_exc()
        pass
