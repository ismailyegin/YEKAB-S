import csv
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import Permission, User, Group

from sbs.models import Menu, MenuAdmin, MenuAthlete, MenuReferee, MenuCoach, MenuDirectory, MenuClubUser, \
    SportClubUser, Person, Athlete, Coach, Judge, DirectoryMember, SportsClub, Communication, City, Country, ClubRole
from sbs.models.ActiveGroup import ActiveGroup
from sbs.models.Logs import Logs
from sbs.models.MenuArsiv import MenuArsiv
from sbs.models.PreRegistration import PreRegistration
from sbs.models.ReferenceCoach import ReferenceCoach
from sbs.models.ReferenceReferee import ReferenceReferee
from sbs.models.Employe import Employe


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


def getAthleteMenu(request):
    athletemenus = MenuAthlete.objects.all()
    return {'athletemenus': athletemenus}


def getRefereeMenu(request):
    refereemenus = MenuReferee.objects.all().order_by("sorting")
    return {'refereemenus': refereemenus}


def getCoachMenu(request):
    coachmenus = MenuCoach.objects.all().order_by("sorting")
    return {'coachmenus': coachmenus}


def getDirectoryMenu(request):
    directorymenus = MenuDirectory.objects.all().order_by("sorting")
    return {'directorymenus': directorymenus}


def getClubUserMenu(request):
    clubusermenus = MenuClubUser.objects.all().order_by("sorting")
    return {'clubusermenus': clubusermenus}

def getArsivMenu(request):
    arsivmenus = MenuArsiv.objects.all().order_by("sorting")
    return {'arsivmenus': arsivmenus}


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
def control_access_judge(request):
    groups = request.user.groups.all()
    is_exist = False

    for group in groups:
        permissions = group.permissions.all()

        for perm in permissions:

            if request.resolver_match.url_name == perm.name:
                is_exist = True

        if group.name == "Admin" or group.name == "Hakem" or group.name == "Yonetim" or group.name =='Personel':
            is_exist = True

    return is_exist

def control_access(request):
    groups = request.user.groups.all()
    is_exist = False

    for group in groups:
        permissions = group.permissions.all()

        for perm in permissions:

            if request.resolver_match.url_name == perm.name:
                is_exist = True

        if group.name == "Admin" or group.name == "Yonetim" or group.name == "Arsiv" or group.name == 'Personel':
            is_exist = True

    return is_exist


def control_access_klup(request):
    groups = request.user.groups.all()
    is_exist = False

    for group in groups:
        permissions = group.permissions.all()

        for perm in permissions:

            if request.resolver_match.url_name == perm.name:
                is_exist = True

        if group.name == "Admin" or group.name == "Hakem" or group.name == "Antrenor" or group.name == "Yonetim" or group.name == 'Personel':
            is_exist = True

    return is_exist

def aktif(request):
    if User.objects.filter(pk=request.user.pk):
        if not (ActiveGroup.objects.filter(user=request.user)):
            aktive = ActiveGroup(user=request.user, group=request.user.groups.exclude(name='Sporcu')[0])
            aktive.save()
            aktif = request.user.groups.exclude(name='Sporcu')[0]
        else:
            aktif = ActiveGroup.objects.get(user=request.user).group.name
        group = request.user.groups.exclude(name='Sporcu')
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
            total_notifications_refere = ReferenceReferee.objects.filter(status=ReferenceReferee.WAITED).count()
            total_notifications_coach = ReferenceReferee.objects.filter(status=ReferenceCoach.WAITED).count()
            total_notifications_clup = PreRegistration.objects.filter(status=PreRegistration.WAITED).count()
            notifications_tatal = total_notifications_refere + total_notifications_coach + total_notifications_clup

            return {
                'total_notifications_refere': total_notifications_refere,
                'total_notifications_coach': total_notifications_coach,
                'total_notifications_clup': total_notifications_clup,
                'notifications_tatal': notifications_tatal}

    return {}


def import_csv():
    doc_root = settings.BASE_DIR + '/media/wushu_csv.csv'
    with open(doc_root) as csv_file:
        file_reader = csv.reader(csv_file, delimiter=';')
        next(file_reader, None)  # skip the headers
        for row in file_reader:
            club = SportsClub()
            club.name = row[14]
            club.shortName = row[15]
            club.foundingDate = row[16]

            club.save()

            comClub = Communication()
            comClub.city = City.objects.get(name__icontains=row[18].strip())
            comClub.phoneNumber = row[17]
            comClub.address = row[19]
            comClub.country = Country.objects.get(name__icontains="TÜRKİYE")
            comClub.save()

            club.comminication = comClub

            club.save()


            user = User()
            user.first_name = row[1]
            user.last_name = row[2]
            user.username = row[10]

            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()

            user.groups.add(Group.objects.get(name='KlupUye'))
            user.save()

            person = Person()
            person.tc = row[0]
            person.motherName = row[3]
            person.fatherName = row[4]
            person.gender = row[5]
            person.birthDate = row[7]
            person.birthplace = row[6]
            person.bloodType = row[8]
            person.save()

            comClubUser = Communication()
            comClubUser.city = City.objects.get(name__icontains=row[12].strip())
            comClubUser.phoneNumber = row[11]
            comClubUser.address = row[13]
            comClubUser.country = Country.objects.get(name="TÜRKİYE")
            comClubUser.save()

            sportClubUser = SportClubUser()
            sportClubUser.person = person
            sportClubUser.user = user
            sportClubUser.communication = comClubUser
            sportClubUser.sportClub = club
            sportClubUser.role = ClubRole.objects.get(name__icontains=row[9].strip())

            sportClubUser.save()

            print(row)
