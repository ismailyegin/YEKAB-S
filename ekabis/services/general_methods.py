from datetime import datetime

from ekabis.models.ActiveGroup import ActiveGroup
from ekabis.models.Logs import Logs
from ekabis.models.PermissionGroup import PermissionGroup
from ekabis.models.Permission import Permission
from ekabis.services.services import ActiveGroupService, MenuAdminService, MenuDirectoryService, MenuPersonelService, \
    MenuService, EmployeeService, DirectoryMemberService, UserService, PermissionGroupService

from ekabis.models.Menu import Menu

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def logwrite(request, user, log):
    try:
        logs = Logs(user=user, subject=log, ip=get_client_ip(request))
        logs.save()

        # f = open("log.txt", "a")
        # log = get_client_ip(request) + "    [" + datetime.today().strftime('%d-%m-%Y %H:%M') + "] " + str(
        #     user) + " " + log + " \n "
        # f.write(log)
        # f.close()

    except Exception as e:
        f = open("log.txt", "a")
        log = "[" + datetime.today().strftime('%d-%m-%Y %H:%M') + "]  lag kaydetme hata   \n "
        f.write(log)
        f.close()

    return log


def getMenu(request):
    print('getMenu')
    menus = MenuService(request,None)
    active = controlGroup(request)
    activefilter={
        'group__name' : active,

    }
    permGrup=PermissionGroupService(request,activefilter)
    menu=[]
    for item in menus:
        print(item)
        if item.is_parent == False:
            if item.url:
                for tk in permGrup:
                    if tk.permissions.codename == item.url.split(":")[1]:
                        print(item.url.split(":")[1])
                        menu.append(item.pk)
                        menu.append(item.parent.pk)

    menus = Menu.objects.filter(id__in=menu).distinct()
    print(menus)
    return {'menus': menus}


def getAdminMenu(request):
    adminmenus = MenuAdminService(request,None)
    return {'adminmenus1': adminmenus}





def getDirectoryMenu(request):
    refereemenus = MenuDirectoryService(request,None)
    return {'refereemenus': refereemenus}


def getPersonelMenu(request):
    coachmenus = MenuPersonelService(request,None)
    return {'coachmenus': coachmenus}

def control_access(request):
    is_exist = False
    for group in request.user.groups.all():
        permissions = PermissionGroup.objects.filter(group=group)
        for perm in permissions:
            if request.resolver_match.url_name == perm.permissions.codename:
                print('Okey')
                is_exist = True

        if group.name == "Admin":
            is_exist = True

    return is_exist



def aktif(request):
    userfilter={
        'pk' :request.user.pk
    }
    if UserService(request,userfilter):
        activfilter={
            'user' : request.user
        }
        if not (ActiveGroupService(request,activfilter)):
            aktive = ActiveGroup(user=request.user, group=request.user.groups.all()[0])
            aktive.save()
            aktif =aktive
        else:
            activfilter={
                'user' : request.user
            }
            aktif = ActiveGroupService(request,activfilter)[0]
            aktif=aktif.group.name
        group = request.user.groups.all()
        return {'aktif': aktif,
                'group': group,
                }

    else:
        return {}


def controlGroup(request):
    userfilter = {
        'pk': request.user.pk
    }
    if UserService(request,userfilter):
        activfilter={
            'user' :request.user
        }
        if not (ActiveGroupService(request,activfilter)):
            aktive = ActiveGroup(user=request.user, group=request.user.groups.all()[0])
            aktive.save()
            active = request.user.groups.all()[0].name

        else:
            activfilter = {
                'user': request.user
            }
            active = ActiveGroupService(request, activfilter)[0]
            active=active.group.name
        return active

    else:
        return {}

def getProfileImage(request):
    if (request.user.id):
        userfilter={
            'user' : request.user
        }

        if request.user.groups.filter(name='Admin').exists():
            person = dict()
            person['profileImage'] = "profile/logo.png"
        elif request.user.groups.filter(name='Personel').exists():
            athlete = EmployeeService(request,userfilter)[0]
            person = athlete.person
        elif request.user.groups.filter(name='Yonetim').exists():
            athlete = DirectoryMemberService(request,userfilter)[0]
            person = athlete.person
        else:
            person = None
        return {'person': person}
    return {}
def get_notification(request):
    # if (request.user.id):
    #     current_user = request.user
    #     if current_user.groups.filter(name='Admin').exists():
    #         print('Admin bildirimleri')
    #         return {}
    return {}



