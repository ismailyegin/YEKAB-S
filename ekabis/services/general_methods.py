import csv
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import Permission, User, Group

from ekabis.models.ActiveGroup import ActiveGroup
from ekabis.models.Logs import Logs


from ekabis.models.Employee import Employee
from ekabis.models.MenuAdmin import MenuAdmin
from ekabis.models.MenuDirectory import MenuDirectory
from ekabis.models.MenuPersonel import MenuPersonel
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
    menus = Menu.objects.all()
    return {'menus': menus}


def getAdminMenu(request):
    adminmenus = MenuAdmin.objects.all().order_by("sorting")
    return {'adminmenus': adminmenus}





def getDirectoryMenu(request):
    refereemenus = MenuDirectory.objects.all().order_by("sorting")
    return {'refereemenus': refereemenus}


def getPersonelMenu(request):
    coachmenus = MenuPersonel.objects.all().order_by("sorting")
    return {'coachmenus': coachmenus}



def show_urls(urllist, depth=0):
    urls = []

    # show_urls(urls.urlpatterns)
    for entry in urllist:

        urls.append(entry)
        perm = Permission(name=entry.name, codename=entry.pattern.regex.pattern, content_type_id=7)

        if Permission.objects.filter(name=entry.name).count() == 0:
            perm.save()
        if hasattr(entry, 'url_patterns'):
            show_urls(entry.url_patterns, depth + 1)

    return urls


def show_urls_deneme(urllist, depth=0):
    urls = []
    # show_urls(urls.urlpatterns)
    for entry in urllist:

        urls.append(entry)

        if hasattr(entry, 'url_patterns'):
            show_urls(entry.url_patterns, depth + 1)

    return urls
def control_access(request):
    groups = request.user.groups.all()
    is_exist = False

    for group in groups:
        permissions = group.permissions.all()

        for perm in permissions:

            if request.resolver_match.url_name == perm.name:
                is_exist = True

        if group.name == "Admin":
            is_exist = True

    return is_exist

def control_access_directory(request):
    groups = request.user.groups.all()
    is_exist = False

    for group in groups:
        permissions = group.permissions.all()

        for perm in permissions:

            if request.resolver_match.url_name == perm.name:
                is_exist = True

        if group.name == "Admin" or group.name == "Yonetim" or  group.name == 'Personel':
            is_exist = True

    return is_exist







def control_access_personel(request):
    groups = request.user.groups.all()
    is_exist = False

    for group in groups:
        permissions = group.permissions.all()

        for perm in permissions:

            if request.resolver_match.url_name == perm.name:
                is_exist = True

        if group.name == "Admin" or group.name == "Yonetim" or  group.name == 'Personel':
            is_exist = True

    return is_exist


def aktif(request):
    if User.objects.filter(pk=request.user.pk):
        if not (ActiveGroup.objects.filter(user=request.user)):
            aktive = ActiveGroup(user=request.user, group=request.user.groups.all()[0])
            aktive.save()
            aktif = request.user.groups.exclude(name='Sporcu')[0]
        else:
            aktif = ActiveGroup.objects.get(user=request.user).group.name
        group = request.user.groups.all()
        return {'aktif': aktif,
                'group': group,
                }

    else:
        return {}


def controlGroup(request):
    if User.objects.filter(pk=request.user.pk):
        if not (ActiveGroup.objects.filter(user=request.user)):
            aktive = ActiveGroup(user=request.user, group=request.user.groups.exclude(name='Sporcu')[0])
            aktive.save()
            active = request.user.groups.exclude(name='Sporcu')[0]

        else:
            active = ActiveGroup.objects.get(user=request.user).group.name
        return active

    else:
        return {}




def getProfileImage(request):
    if (request.user.id):
        current_user = request.user

        if current_user.groups.filter(name='Admin').exists():
            person = dict()
            person['profileImage'] = "profile/logo.png"

        if current_user.groups.filter(name='Arsiv').exists():
            person = dict()
            person['profileImage'] = "profile/logo.png"

        elif current_user.groups.filter(name='KlupUye').exists():
            athlete = SportClubUser.objects.get(user=current_user)
            person = Person.objects.get(id=athlete.person.id)
        elif current_user.groups.filter(name='Personel').exists():
            athlete = Employe.objects.get(user=current_user)
            person = Person.objects.get(id=athlete.person.id)


        elif current_user.groups.filter(name='Sporcu').exists():
            athlete = Athlete.objects.get(user=current_user)
            person = Person.objects.get(id=athlete.person.id)

        elif current_user.groups.filter(name='Antrenor').exists():
            athlete = Coach.objects.get(user=current_user)
            person = Person.objects.get(id=athlete.person.id)

        elif current_user.groups.filter(name='Hakem').exists():
            athlete = Judge.objects.get(user=current_user)
            person = Person.objects.get(id=athlete.person.id)

        elif current_user.groups.filter(name='Yonetim').exists():
            athlete = DirectoryMember.objects.get(user=current_user)
            person = Person.objects.get(id=athlete.person.id)

        else:
            person = None

        return {'person': person}

    return {}


def get_notification(request):
    if (request.user.id):
        current_user = request.user
        if current_user.groups.filter(name='Admin').exists():
            print('Admin bildirimleri')


            return {}


    return {}



