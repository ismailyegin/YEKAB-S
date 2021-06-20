from datetime import datetime

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
# from rest_framework_simplejwt import views as jwt_views
from django.http import JsonResponse
from django.shortcuts import render, redirect

from sbs.models import SportClubUser, SportsClub, Coach, Level, Athlete, Person, Judge
# from rest_framework.authtoken.models import Token
from sbs.models.ActiveGroup import ActiveGroup
from sbs.models.Competition import Competition
from sbs.models.CompetitionsAthlete import CompetitionsAthlete
from sbs.models.PreRegistration import PreRegistration
from sbs.models.ReferenceCoach import ReferenceCoach
from sbs.models.ReferenceReferee import ReferenceReferee
from sbs.services import general_methods
from sbs.models.CategoryItem import CategoryItem
from sbs.models.Category import Category
from sbs.models.Activity import Activity
from sbs.models.Logs import Logs


@login_required
def return_message(request):
    return render(request, 'Chat/chat.html')



@login_required
def return_athlete_dashboard(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    return render(request, 'anasayfa/sporcu.html')


@login_required
def return_referee_dashboard(request):
    perm = general_methods.control_access_judge(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    max = 0
    maxcom = Competition.objects.none()
    competitions = Competition.objects.filter().order_by('creationDate')
    for item in competitions:
        if max < int(CompetitionsAthlete.objects.filter(competition=item).count()):
            maxcom = item
            max = int(CompetitionsAthlete.objects.filter(competition=item).count())

    max = CompetitionsAthlete.objects.filter(competition=maxcom).count()
    max_male = CompetitionsAthlete.objects.filter(competition=maxcom, athlete__person__gender=Person.MALE).count()
    max_female = CompetitionsAthlete.objects.filter(competition=maxcom, athlete__person__gender=Person.FEMALE).count()

    competitions = Competition.objects.filter().order_by('creationDate')[:6]
    lastcompetition = Competition.objects.filter().order_by('-creationDate')[0]

    datacount = []
    for item in competitions:
        competition = CompetitionsAthlete.objects.filter(competition_id=item.pk)
        beka = {
            'count': competition.count(),
            'competiton': item
        }
        datacount.append(beka)


    return render(request, 'anasayfa/hakem.html',
                  {

                      'max_male': max_male,
                      'max_female': max_female,
                      'competition_male': CompetitionsAthlete.objects.filter(competition=lastcompetition,
                                                                             athlete__person__gender=Person.MALE).count(),
                      'competition_male_x': int((CompetitionsAthlete.objects.filter(competition=lastcompetition,
                                                                                    athlete__person__gender=Person.MALE).count() * 100) / CompetitionsAthlete.objects.filter(
                          competition=maxcom, athlete__person__gender=Person.MALE).count()),
                      'competition_female': CompetitionsAthlete.objects.filter(competition=lastcompetition,
                                                                               athlete__person__gender=Person.FEMALE).count(),
                      'competition_female_x': int((CompetitionsAthlete.objects.filter(competition=lastcompetition,
                                                                                      athlete__person__gender=Person.FEMALE).count() * 100) / CompetitionsAthlete.objects.filter(
                          competition=maxcom, athlete__person__gender=Person.FEMALE).count()),
                      'competition_athlete_count': CompetitionsAthlete.objects.filter(
                          competition=lastcompetition).count(),
                      'max': max,
                      'max_x': int(
                          (CompetitionsAthlete.objects.filter(competition=lastcompetition).count() * 100) / max),

                      'lastcompetition': lastcompetition,
                      'data': datacount,
                  })



@login_required
def return_coach_dashboard(request):
    perm = general_methods.control_access_klup(request)
    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    coach = Coach.objects.get(user_id=request.user.pk)
    clup = SportsClub.objects.filter(coachs=coach)
    clupsPk = []
    for item in clup:
        clupsPk.append(item.pk)
    athletes = Athlete.objects.filter(licenses__sportsClub_id__in=clupsPk).distinct()
    athletes |= Athlete.objects.filter(licenses__coach=coach).distinct()

    athlete_count = athletes.count()
    max = 0
    maxcom = Competition.objects.none()
    competitions = Competition.objects.filter().order_by('creationDate')
    for item in competitions:
        if max < int(CompetitionsAthlete.objects.filter(competition=item).count()):
            maxcom = item
            max = int(CompetitionsAthlete.objects.filter(competition=item).count())

    max = CompetitionsAthlete.objects.filter(competition=maxcom).count()
    max_male = CompetitionsAthlete.objects.filter(competition=maxcom, athlete__person__gender=Person.MALE).count()
    max_female = CompetitionsAthlete.objects.filter(competition=maxcom, athlete__person__gender=Person.FEMALE).count()

    competitions = Competition.objects.filter().order_by('creationDate')[:6]
    lastcompetition = Competition.objects.filter().order_by('-creationDate')[0]

    datacount = []
    for item in competitions:
        competition = CompetitionsAthlete.objects.filter(competition_id=item.pk)
        beka = {
            'count': competition.count(),
            'competiton': item
        }

        datacount.append(beka)
        last_athlete = Athlete.objects.order_by('-creationDate')[:8]
        total_club = SportsClub.objects.all().count()
        total_athlete = Athlete.objects.all().count()
        total_athlete_gender_man = Athlete.objects.filter(person__gender=Person.MALE).count()
        total_athlete_gender_woman = Athlete.objects.filter(person__gender=Person.FEMALE).count()
        total_athlate_last_month = Athlete.objects.exclude(user__date_joined__month=datetime.now().month).count()
        total_club_user = SportClubUser.objects.all().count()
        total_coachs = Coach.objects.all().count()
        total_judge = Judge.objects.all().count()



    return render(request, 'anasayfa/antrenor.html',
                  {
                      'athlete_count': athlete_count,
                      'max_male': max_male,
                      'max_female': max_female,
                      'competition_male': CompetitionsAthlete.objects.filter(competition=lastcompetition,
                                                                             athlete__person__gender=Person.MALE).count(),
                      'competition_male_x': int((CompetitionsAthlete.objects.filter(competition=lastcompetition,
                                                                                    athlete__person__gender=Person.MALE).count() * 100) / CompetitionsAthlete.objects.filter(
                          competition=maxcom, athlete__person__gender=Person.MALE).count()),
                      'competition_female': CompetitionsAthlete.objects.filter(competition=lastcompetition,
                                                                               athlete__person__gender=Person.FEMALE).count(),
                      'competition_female_x': int((CompetitionsAthlete.objects.filter(competition=lastcompetition,
                                                                                      athlete__person__gender=Person.FEMALE).count() * 100) / CompetitionsAthlete.objects.filter(
                          competition=maxcom, athlete__person__gender=Person.FEMALE).count()),
                      'competition_athlete_count': CompetitionsAthlete.objects.filter(
                          competition=lastcompetition).count(),
                      'max': max,
                      'max_x': int(
                          (CompetitionsAthlete.objects.filter(competition=lastcompetition).count() * 100) / max),

                      'lastcompetition': lastcompetition,
                      'data': datacount,
                      'total_club': total_club,
                      'total_athlete': total_athlete, 'total_coachs': total_coachs, 'last_athletes': last_athlete,
                      'total_athlete_gender_man': total_athlete_gender_man,
                      'total_athlete_gender_woman': total_athlete_gender_woman,
                      'total_athlate_last_month': total_athlate_last_month,
                      'total_judge': total_judge,
                      'total_club_user': total_club_user,

                  })


@login_required
def return_directory_dashboard(request):
    perm = general_methods.control_access(request)
    perm = general_methods.control_access(request)
    # x = general_methods.import_csv()

    if not perm:
        logout(request)
        return redirect('accounts:login')

    # son eklenen 8 sporcuyu ekledik
    last_athlete = Athlete.objects.order_by('-creationDate')[:8]
    total_club = SportsClub.objects.all().count()
    total_athlete = Athlete.objects.all().count()
    total_athlete_gender_man = Athlete.objects.filter(person__gender=Person.MALE).count()
    total_athlete_gender_woman = Athlete.objects.filter(person__gender=Person.FEMALE).count()
    total_athlate_last_month = Athlete.objects.exclude(user__date_joined__month=datetime.now().month).count()
    total_club_user = SportClubUser.objects.all().count()
    total_coachs = Coach.objects.all().count()
    total_judge = Judge.objects.all().count()
    total_user = User.objects.all().count()

    max = 0
    maxcom = Competition.objects.none()
    competitions = Competition.objects.filter().order_by('creationDate')
    for item in competitions:
        if max < int(CompetitionsAthlete.objects.filter(competition=item).count()):
            maxcom = item
            max = int(CompetitionsAthlete.objects.filter(competition=item).count())

    max = CompetitionsAthlete.objects.filter(competition=maxcom).count()
    max_male = CompetitionsAthlete.objects.filter(competition=maxcom, athlete__person__gender=Person.MALE).count()
    max_female = CompetitionsAthlete.objects.filter(competition=maxcom, athlete__person__gender=Person.FEMALE).count()

    competitions = Competition.objects.filter().order_by('creationDate')[:6]
    lastcompetition = Competition.objects.filter().order_by('-creationDate')[0]

    datacount = []
    for item in competitions:
        competition = CompetitionsAthlete.objects.filter(competition_id=item.pk)
        beka = {
            'count': competition.count(),
            'competiton': item
        }
        datacount.append(beka)
        # print(data)

    total_notifications_refere = ReferenceReferee.objects.filter(status=ReferenceReferee.WAITED).count()
    total_notifications_coach = ReferenceReferee.objects.filter(status=ReferenceCoach.WAITED).count()
    total_notifications_clup = PreRegistration.objects.filter(status=PreRegistration.WAITED).count()
    notifications_tatal = total_notifications_refere + total_notifications_coach + total_notifications_clup

    # hakem kademe sayilari
    judge_grades = []
    categori = CategoryItem.objects.filter(forWhichClazz='REFEREE_GRADE')

    for item in categori:
        beka = {
            'name': item.name,
            'count': Judge.objects.filter(grades__definition=item).count()
        }
        judge_grades.append(beka)

    coach_grades = []
    categori = CategoryItem.objects.filter(forWhichClazz='COACH_GRADE')

    for item in categori:
        beka = {
            'name': item.name,
            'count': Coach.objects.filter(grades__definition=item).count()
        }
        coach_grades.append(beka)

    return render(request, 'anasayfa/federasyon.html',
                  {
                      'coach_grades': coach_grades,
                      'judge_grades': judge_grades,
                      'max_male': max_male,
                      'max_female': max_female,
                      'competition_male': CompetitionsAthlete.objects.filter(competition=lastcompetition,
                                                                             athlete__person__gender=Person.MALE).count(),
                      'competition_male_x': int((CompetitionsAthlete.objects.filter(competition=lastcompetition,
                                                                                    athlete__person__gender=Person.MALE).count() * 100) / CompetitionsAthlete.objects.filter(
                          competition=maxcom, athlete__person__gender=Person.MALE).count()),
                      'competition_female': CompetitionsAthlete.objects.filter(competition=lastcompetition,
                                                                               athlete__person__gender=Person.FEMALE).count(),
                      'competition_female_x': int((CompetitionsAthlete.objects.filter(competition=lastcompetition,
                                                                                      athlete__person__gender=Person.FEMALE).count() * 100) / CompetitionsAthlete.objects.filter(
                          competition=maxcom, athlete__person__gender=Person.FEMALE).count()),
                      'competition_athlete_count': CompetitionsAthlete.objects.filter(
                          competition=lastcompetition).count(),
                      'max': max,
                      'max_x': int(
                          (CompetitionsAthlete.objects.filter(competition=lastcompetition).count() * 100) / max),

                      'lastcompetition': lastcompetition,
                      'data': datacount, 'total_club_user': total_club_user,
                      'total_club': total_club,
                      'total_athlete': total_athlete, 'total_coachs': total_coachs, 'last_athletes': last_athlete,
                      'total_athlete_gender_man': total_athlete_gender_man,
                      'total_athlete_gender_woman': total_athlete_gender_woman,
                      'total_athlate_last_month': total_athlate_last_month,
                      'total_judge': total_judge, 'total_user': total_user,
                      'total_notifications_refere': total_notifications_refere,
                      'total_notifications_coach': total_notifications_coach,
                      'total_notifications_clup': total_notifications_clup,
                      'notifications_tatal': notifications_tatal

                  })



@login_required
def return_club_user_dashboard(request):
    active = general_methods.controlGroup(request)
    perm = general_methods.control_access_klup(request)
    # x = general_methods.import_csv()


    if not perm:
        logout(request)
        return redirect('accounts:login')

    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    current_user = request.user
    clubuser = SportClubUser.objects.get(user=current_user)
    club = SportsClub.objects.none()

    if SportsClub.objects.filter(clubUser=clubuser):
        club = SportsClub.objects.filter(clubUser=clubuser)[0]
    total_club_user = 0
    total_coach = 0
    if SportsClub.objects.filter(clubUser=clubuser):
        total_club_user = club.clubUser.count()
        total_coach = Coach.objects.filter(sportsclub=club).count()

    sc_user = SportClubUser.objects.get(user=user)
    clubsPk = []
    clubs = SportsClub.objects.filter(clubUser=sc_user)
    for club in clubs:
        clubsPk.append(club.pk)
    total_athlete = Athlete.objects.filter(licenses__sportsClub__in=clubsPk).distinct().count()

    # Sporcu bilgilerinde eksik var mı diye control
    athletes = Athlete.objects.none()
    if active == 'KlupUye':
        sc_user = SportClubUser.objects.get(user=user)
        if sc_user.dataAccessControl == False or sc_user.dataAccessControl == None:
            clubsPk = []
            clubs = SportsClub.objects.filter(clubUser=sc_user)
            for club in clubs:
                if club.dataAccessControl == False or club.dataAccessControl is None:
                    clubsPk.append(club.pk)
            # print(len(clubsPk))
            if len(clubsPk) != 0:
                athletes = Athlete.objects.filter(licenses__sportsClub__in=clubsPk).distinct()
                athletes = athletes.filter(user__last_name='') | athletes.filter(user__first_name='') | athletes.filter(
                    user__email='') | athletes.filter(person__tc='') | athletes.filter(
                    person__birthDate=None) | athletes.filter(
                    person__gender=None) | athletes.filter(person__birthplace='') | athletes.filter(
                    person__motherName='') | athletes.filter(person__fatherName='') | athletes.filter(
                    communication__city__name='') | athletes.filter(communication__country__name='')
                # false degerinde clubun eksigi yok anlamında kulanilmistir.
                for club in clubs:
                    if athletes:
                        club.dataAccessControl = False
                        club.save()

                    else:

                        club.dataAccessControl = True
                        club.save()

                if athletes:
                    sc_user.dataAccessControl = False

                else:
                    sc_user.dataAccessControl = True

                sc_user.save()


            else:
                sc_user.dataAccessControl = True
                sc_user.save()

    return render(request, 'anasayfa/kulup-uyesi.html',
                  {'total_club_user': total_club_user, 'total_coach': total_coach,
                   'total_athlete': total_athlete, 'athletes': athletes})


@login_required
def return_admin_dashboard(request):
    perm = general_methods.control_access(request)
    # x = general_methods.import_csv()

    if not perm:
        logout(request)
        return redirect('accounts:login')

    # son eklenen 8 sporcuyu ekledik
    last_athlete = Athlete.objects.order_by('-creationDate')[:8]
    total_club = SportsClub.objects.all().count()
    total_athlete = Athlete.objects.all().count()
    total_athlete_gender_man = Athlete.objects.filter(person__gender=Person.MALE).count()
    total_athlete_gender_woman = Athlete.objects.filter(person__gender=Person.FEMALE).count()
    total_athlate_last_month = Athlete.objects.exclude(user__date_joined__month=datetime.now().month).count()
    total_club_user = SportClubUser.objects.all().count()
    total_coachs = Coach.objects.all().count()
    total_judge = Judge.objects.all().count()
    total_user = User.objects.all().count()
    lastcompetition = Competition.objects.none()

    max = 0
    max_male=0
    max_female=0
    maxcom = Competition.objects.none()
    competitions = Competition.objects.filter().order_by('creationDate')
    for item in competitions:
        if max < int(CompetitionsAthlete.objects.filter(competition=item).count()):
            maxcom = item
            max = int(CompetitionsAthlete.objects.filter(competition=item).count())
    if maxcom:
        max = CompetitionsAthlete.objects.filter(competition=maxcom).count()
        max_male = CompetitionsAthlete.objects.filter(competition=maxcom, athlete__person__gender=Person.MALE).count()
        max_female = CompetitionsAthlete.objects.filter(competition=maxcom, athlete__person__gender=Person.FEMALE).count()

    competitions = Competition.objects.filter().order_by('creationDate')[:6]
    if Competition.objects.all():
        lastcompetition = Competition.objects.order_by('-creationDate')[0]


    lastcompetitionArray = []

    for item in Category.objects.all():
        beka = {
            'name': item.kategoriadi,
            'count': CompetitionsAthlete.objects.filter(competition=lastcompetition, category=item).count()

        }
        lastcompetitionArray.append(beka)
    datacount = []
    for item in competitions:
        competition = CompetitionsAthlete.objects.filter(competition_id=item.pk)
        beka = {
            'count': competition.count(),
            'competiton': item
        }
        datacount.append(beka)
        # print(data)

    total_notifications_refere = ReferenceReferee.objects.filter(status=ReferenceReferee.WAITED).count()
    total_notifications_coach = ReferenceReferee.objects.filter(status=ReferenceCoach.WAITED).count()
    total_notifications_clup = PreRegistration.objects.filter(status=PreRegistration.WAITED).count()
    notifications_tatal = total_notifications_refere + total_notifications_coach + total_notifications_clup

    # hakem kademe sayilari
    judge_grades = []
    categori = CategoryItem.objects.filter(forWhichClazz='REFEREE_GRADE')
    for item in categori:
        beka = {
            'name': item.name,
            'count': Judge.objects.filter(grades__definition=item).count()
        }
        judge_grades.append(beka)

    coach_grades = []
    categori = CategoryItem.objects.filter(forWhichClazz='COACH_GRADE')

    for item in categori:
        beka = {
            'name': item.name,
            'count': Coach.objects.filter(grades__definition=item).count()
        }
        coach_grades.append(beka)
    active = Activity.objects.all().order_by('-creationDate')[:5]
    logs = Logs.objects.all().order_by('-creationDate')[:5]
    if lastcompetition:
        competition_athlete_count=CompetitionsAthlete.objects.filter(competition=lastcompetition).count()
        competition_male= CompetitionsAthlete.objects.filter(competition=lastcompetition,athlete__person__gender=Person.MALE).count()
        competition_male_x= int(CompetitionsAthlete.objects.filter(competition=lastcompetition,athlete__person__gender=Person.MALE).count() * 100) / CompetitionsAthlete.objects.filter(competition= maxcom, athlete__person__gender=Person.MALE).count()
        competition_female= CompetitionsAthlete.objects.filter(competition=lastcompetition, athlete__person__gender=Person.FEMALE).count()
        competition_female_x= int((CompetitionsAthlete.objects.filter(competition=lastcompetition, athlete__person__gender=Person.FEMALE).count() * 100) / CompetitionsAthlete.objects.filter( competition=maxcom, athlete__person__gender=Person.FEMALE).count())
        max_x= int((CompetitionsAthlete.objects.filter(competition=lastcompetition).count() * 100) / max)

    else:
        competition_athlete_count = 0
        competition_male = 0
        competition_male_x = 0
        competition_female = 0
        competition_female_x = 0
        max_x = 0

    return render(request, 'anasayfa/admin.html',
                  {
                      'active': active,
                      'logs': logs,
                      'lastcompetitionArray': lastcompetitionArray,
                      'coach_grades': coach_grades,
                      'judge_grades': judge_grades,
                      'max_male': max_male,
                      'max_female': max_female,
                      'competition_male': competition_male,
                      'competition_male_x': competition_male_x,
                      'competition_female': competition_female,
                      'competition_female_x': competition_female_x,
                      'competition_athlete_count': competition_athlete_count,
                      'max': max,
                      'max_x':max_x,
                      'lastcompetition': lastcompetition,
                      'data': datacount, 'total_club_user': total_club_user,
                      'total_club': total_club,
                      'total_athlete': total_athlete, 'total_coachs': total_coachs, 'last_athletes': last_athlete,
                      'total_athlete_gender_man': total_athlete_gender_man,
                      'total_athlete_gender_woman': total_athlete_gender_woman,
                      'total_athlate_last_month': total_athlate_last_month,
                      'total_judge': total_judge, 'total_user': total_user,
                      'total_notifications_refere': total_notifications_refere,
                      'total_notifications_coach': total_notifications_coach,
                      'total_notifications_clup': total_notifications_clup,
                      'notifications_tatal': notifications_tatal

                  })


def City_athlete_cout(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            athletecout = Athlete.objects.filter(communication__city__name__icontains=request.POST.get('city')).count()
            coachcout = Coach.objects.filter(communication__city__name__icontains=request.POST.get('city')).count()
            refereecout = Judge.objects.filter(communication__city__name__icontains=request.POST.get('city')).count()
            sportsClub = SportsClub.objects.filter(
                communication__city__name__icontains=request.POST.get('city')).count()
            data = {
                'athlete': athletecout,
                'coach': coachcout,
                'referee': refereecout,
                'sportsClub': sportsClub

            }
            return JsonResponse(data)
        except Level.DoesNotExist:
            return JsonResponse({'status': 'Fail'})

    else:
        return JsonResponse({'status': 'Fail'})

@login_required
def activeGroup(request, pk):
    userActive = ActiveGroup.objects.get(user=request.user)
    group = Group.objects.get(pk=pk)
    userActive.group = group
    userActive.save()
    if group.name == "Admin":
        return redirect('sbs:admin')
    elif group.name == "Antrenor":
        return redirect('sbs:antrenor')
    elif group.name == 'Hakem':
        return redirect('sbs:hakem', )
    elif group.name == 'KlupUye':
        return redirect('sbs:kulup-uyesi')
    elif group.name == 'Sporcu':
        return redirect('sbs:sporcu')
    elif group.name == 'Yonetim':
        return redirect('sbs:federasyon')
    elif group.name == 'Arsiv':
        return redirect('sbs:evrak-anasayfa')
    else:
        return {}
