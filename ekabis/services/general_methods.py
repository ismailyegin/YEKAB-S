from datetime import datetime
from ekabis.services.services import ActiveGroupService,MenuAdminService,MenuDirectoryService,MenuPersonelService,MenuService,EmployeeService,DirectoryMemberService,UserService
from ekabis.models.Logs import Logs
from  ekabis.models.ActiveGroup import ActiveGroup

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
    menus = MenuService(request,None)
    return {'menus': menus}


def getAdminMenu(request):
    adminmenus = MenuAdminService(request,None)
    return {'adminmenus': adminmenus}





def getDirectoryMenu(request):
    refereemenus = MenuDirectoryService(request,None)
    return {'refereemenus': refereemenus}


def getPersonelMenu(request):
    coachmenus = MenuPersonelService(request,None)
    return {'coachmenus': coachmenus}

def control_access(request):
    print(request.resolver_match.url_name)
    is_exist = False
    for group in request.user.groups.all():
        permissions = group.permissions.all()
        for perm in permissions:
            if request.resolver_match.url_name == perm.codename:
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
            active = request.user.groups.all()[0]

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



