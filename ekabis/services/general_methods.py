from datetime import datetime

from ekabis.models.ActiveGroup import ActiveGroup
from ekabis.models.Logs import Logs
from ekabis.models.Menu import Menu
from ekabis.models.PermissionGroup import PermissionGroup
from ekabis.services.services import ActiveGroupService, MenuAdminService, MenuDirectoryService, MenuPersonelService, \
    MenuService, EmployeeService, DirectoryMemberService, UserService, PermissionGroupService


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
    menus = MenuService(request, None)
    active = controlGroup(request)
    activefilter = {
        'group__name': active,
        'is_active': True

    }
    permGrup = PermissionGroupService(request, activefilter)
    menu = []
    activ_urls = None
    for item in menus:
        if item.is_parent == False:
            if item.url:
                for tk in permGrup:
                    if tk.permissions.codename == item.url.split(":")[1]:
                        if request.resolver_match.url_name == item.url.split(":")[1]:
                            activ_urls = item
                        menu.append(item.pk)
                        menu.append(item.parent.pk)

    menus = Menu.objects.filter(id__in=menu).distinct()
    return {'menus': menus, 'activ_url': activ_urls}


def getAdminMenu(request):
    adminmenus = MenuAdminService(request, None)
    return {'adminmenus1': adminmenus}


def getDirectoryMenu(request):
    refereemenus = MenuDirectoryService(request, None)
    return {'refereemenus': refereemenus}


def getPersonelMenu(request):
    coachmenus = MenuPersonelService(request, None)
    return {'coachmenus': coachmenus}


def control_access(request):
    is_exist = False
    groupfilter = {
        'user': request.user
    }
    aktifgroup = ActiveGroupService(request, groupfilter)[0].group
    for perm in PermissionGroup.objects.filter(group=aktifgroup, is_active=True):
        if request.resolver_match.url_name == perm.permissions.codename:
            print('Okey')
            is_exist = True

    if request.user.groups.filter(name="Admin"):
        is_exist = True
    return is_exist


def aktif(request):
    userfilter = {
        'pk': request.user.pk
    }
    if UserService(request, userfilter):
        activfilter = {
            'user': request.user
        }

        aktifgroup = None

        if not (ActiveGroupService(request, activfilter)):
            aktifgroup = ActiveGroup(user=request.user, group=request.user.groups.all()[0])
            aktifgroup.save()
            aktif = aktifgroup.name
        else:
            activfilter = {
                'user': request.user
            }
            aktifgroup = ActiveGroupService(request, activfilter)[0]
            # aktifgroup = ActiveGroupService(request, activfilter)[0]
            aktif = aktifgroup.group.name
        perm = []

        groupfilter = {
            'group_id': aktifgroup.pk,
            'is_active': True
        }
        permission = PermissionGroupService(request, groupfilter)
        for item in permission:
            perm.append(item.permissions.codename)

        group = request.user.groups.all()
        return {'aktif': aktif,
                'group': group,
                'perm': perm,

                }
    else:
        return {}


def controlGroup(request):
    userfilter = {
        'pk': request.user.pk
    }
    if UserService(request, userfilter):
        activfilter = {
            'user': request.user
        }
        if not (ActiveGroupService(request, activfilter)):
            aktive = ActiveGroup(user=request.user, group=request.user.groups.all()[0])
            aktive.save()
            active = request.user.groups.all()[0].name

        else:
            activfilter = {
                'user': request.user
            }
            active = ActiveGroupService(request, activfilter)[0]
            active = active.group.name
        return active

    else:
        return {}


def getProfileImage(request):
    if (request.user.id):
        userfilter = {
            'user': request.user
        }

        if request.user.groups.filter(name='Admin').exists():
            person = dict()
            person['profileImage'] = "profile/logo.png"
        elif request.user.groups.filter(name='Personel').exists():
            athlete = EmployeeService(request, userfilter)[0]
            person = athlete.person
        elif request.user.groups.filter(name='Yonetim').exists():
            athlete = DirectoryMemberService(request, userfilter)[0]
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


def get_error_messages(form):
    if form:
        print(form.errors)
        error_messages = []
        for key in form.errors:
            for field in form.fields:
                if key == field:
                    entry = {'key': field, 'value': form.errors[key][0]}
                    error_messages.append(entry)
        return error_messages
    return {}
