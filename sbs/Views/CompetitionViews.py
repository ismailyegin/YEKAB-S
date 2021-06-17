from builtins import print, property
from warnings import catch_warnings

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from sbs.Forms.CompetitionForm import CompetitionForm
from sbs.Forms.CompetitionSearchForm import CompetitionSearchForm
from sbs.Forms.SimplecategoryForm import SimplecategoryForm
from sbs.models import SportClubUser, SportsClub, Competition, Athlete, CompCategory, Coach
from sbs.models.Category import Category
from sbs.models.CompetitionAges import CompetitionAges
from sbs.models.CompetitionsAthlete import CompetitionsAthlete
from sbs.models.SandaAthlete import SandaAthlete
from sbs.models.SimpleCategory import SimpleCategory
from sbs.services import general_methods


@login_required
def categori_ekle(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    simplecategoryForm = SimplecategoryForm()
    categoryitem = SimpleCategory.objects.all()
    if request.method == 'POST':
        simplecategoryForm = SimplecategoryForm(request.POST)
        if simplecategoryForm.is_valid():
            simplecategoryForm.save()
            messages.success(request, 'Kategori Başarıyla Güncellenmiştir.')
        else:
            messages.warning(request, 'Birşeyler ters gitti yeniden deneyiniz.')

    return render(request, 'musabaka/musabaka-Simplecategori.html',
                  {'category_item_form': simplecategoryForm, 'categoryitem': categoryitem})


@login_required
def aplication(request, pk):
    perm = general_methods.control_access_klup(request)
    active = general_methods.controlGroup(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')


    musabaka = Competition.objects.get(pk=pk)

    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    weights = Category.objects.all()
    if active == 'KlupUye':
        sc_user = SportClubUser.objects.get(user=user)
        if sc_user.dataAccessControl == True:
            if active == 'KlupUye':
                clubsPk = []
                clubs = SportsClub.objects.filter(clubUser=sc_user)
                for club in clubs:
                    clubsPk.append(club.pk)

                comAthlete = CompetitionsAthlete.objects.filter(competition=pk,
                                                        athlete__licenses__sportsClub__in=clubsPk).distinct()
        else:
            messages.warning(request, 'Lütfen Eksik olan Sporcu Bilgilerini tamamlayiniz.')
            return redirect('sbs:musabakalar')
    elif active == 'Yonetim' or active == 'Admin':
        comAthlete = CompetitionsAthlete.objects.filter(competition=pk).distinct()

    elif active == 'Antrenor':
        coach = Coach.objects.get(user=user)
        comAthlete = CompetitionsAthlete.objects.filter(competition=pk, athlete__licenses__coach=coach).distinct()
    return render(request, 'musabaka/basvuru.html',
                  {'athletes': comAthlete, 'competition': musabaka, 'weights': weights})


@login_required
def return_competition(request):

    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    competitions = Competition.objects.filter(startDate__year=timezone.now().year)
    year = timezone.now().year
    year = Competition.objects.values('year').distinct().order_by('year')
    return render(request, 'musabaka/sonuclar.html', {'competitions': competitions, 'year': year})


@login_required
def return_competitions(request):
    perm = general_methods.control_access_klup(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    comquery = CompetitionSearchForm()
    competition = Competition.objects.filter(registerStartDate__lte=timezone.now(),
                                             registerFinishDate__gte=timezone.now())
    competitions = Competition.objects.none()


    if request.method == 'POST':
        name = request.POST.get('name')
        startDate = request.POST.get('startDate')

        if name or startDate:
            query = Q()
            if name:
                query &= Q(name__icontains=name)
            if startDate:
                query &= Q(finishDate__year=int(startDate))

            competitions = Competition.objects.filter(query).order_by('-startDate').distinct()
        else:
            competitions = Competition.objects.all().order_by('-startDate')
    return render(request, 'musabaka/musabakalar.html',
                  {'competitions': competitions, 'query': comquery, 'application': competition})


@login_required
def musabaka_ekle(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    competition_form = CompetitionForm()
    if request.method == 'POST':
        competition_form = CompetitionForm(request.POST)
        if competition_form.is_valid():
            musabaka = competition_form.save(commit=False)
            musabaka.juryCount = 0;
            musabaka.save()

            log = str(request.POST.get('name')) + "  Musabaka eklendi "
            log = general_methods.logwrite(request, request.user, log)

            messages.success(request, 'Müsabaka Başarıyla Kaydedilmiştir.')

            return redirect('sbs:musabaka-duzenle', pk=musabaka.pk)
        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'musabaka/musabaka-ekle.html',
                  {'competition_form': competition_form})


@login_required
def musabaka_duzenle(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    musabaka = Competition.objects.get(pk=pk)
    athletes = CompetitionsAthlete.objects.filter(competition=musabaka).order_by('category')

    competition_form = CompetitionForm(request.POST or None, instance=musabaka)
    category = Category.objects.all()
    ages=CompetitionAges.objects.all()

    if request.method == 'POST':
        if competition_form.is_valid():

            for item in musabaka.categoryies.all():
                musabaka.categoryies.remove(item)
                musabaka.save()
            if request.POST.getlist('jobDesription'):
                for item in request.POST.getlist('jobDesription'):
                    musabaka.categoryies.add(Category.objects.get(pk=item))
                    musabaka.save()
            for item in musabaka.ages.all():
                musabaka.ages.remove(item)
                musabaka.save()
            if request.POST.getlist('ages'):
                for item in request.POST.getlist('ages'):
                    musabaka.ages.add(CompetitionAges.objects.get(pk=item))
                    musabaka.save()

            competition_form.save()
            messages.success(request, 'Müsabaka Başarıyla Güncellenmiştir.')

            log = str(request.POST.get('name')) + "  Musabaka guncellendi "
            log = general_methods.logwrite(request, request.user, log)

            return redirect('sbs:musabaka-duzenle', pk=pk)
        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'musabaka/musabaka-duzenle.html',
                  {'competition_form': competition_form, 'competition': musabaka, 'athletes': athletes,
                    'category': category,'ages':ages})


@login_required
def musabaka_sil(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = Competition.objects.get(pk=pk)

            log = str(obj.name) + "  Musabaka silindi "
            log = general_methods.logwrite(request, request.user, log)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Competition.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


def musabaka_sporcu_ekle(request, athlete_pk, competition_pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    if request.method == 'POST':
        compAthlete = CompetitionsAthlete()
        compAthlete.athlete = Athlete.objects.get(pk=athlete_pk)
        compAthlete.competition = Competition.objects.get(pk=competition_pk)
        compAthlete.save()
        messages.success(request, 'Sporcu Eklenmiştir')

    return redirect('sbs:lisans-listesi')


@login_required
def musabaka_sporcu_sec(request, pk):
    perm = general_methods.control_access_klup(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    category = Category.objects.all()

    competition = Competition.objects.filter(registerStartDate__lte=timezone.now(),
                                             registerFinishDate__gte=timezone.now())


    return render(request, 'musabaka/musabaka-sporcu-sec.html',
                  {'pk': pk, 'weights': category, 'application': competition})


@login_required
def return_sporcu_ajax(request):
    # print('ben geldim')
    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    # /datatablesten gelen veri kümesi datatables degiskenine alindi
    if request.method == 'GET':
        datatables = request.GET
        secilenler = request.GET.getlist('secilenler[]')
        pk = request.GET.get('athlete')
        athlete = Athlete.objects.get(pk=pk)

        # print('pk beklenen deger =',pk)
        # kategori = CompetitionCategori.objects.get(pk=request.GET.get('cmd'))

    elif request.method == 'POST':
        datatables = request.POST


    # /Sayfanın baska bir yerden istenmesi durumunda degerlerin None dönmemesi icin degerler try boklari icerisine alindi

    try:
        draw = int(datatables.get('draw'))
        # print("draw degeri =", draw)
        # Ambil start
        start = int(datatables.get('start'))
        # print("start degeri =", start)
        # Ambil length (limit)
        length = int(datatables.get('length'))
        # print("lenght  degeri =", length)
        # Ambil data search
        search = datatables.get('search[value]')
        # print("search degeri =", search)
    except:
        draw = 1
        start = 0
        length = 10
    modeldata = Athlete.objects.none()
    if length == -1:

        # athletes = []
        # for comp in compAthlete:
        #     if comp.athlete:
        #         athletes.append(comp.athlete.pk)
        modeldata = Athlete.objects.exclude(pk=athlete.pk)
        total = Athlete.objects.exclude(pk=athlete.pk).count()







    else:
        if search:
            modeldata = Athlete.objects.none()

            athletes = []
            modeldata = Athlete.objects.filter(
                Q(user__last_name__icontains=search) | Q(user__first_name__icontains=search) | Q(
                    user__email__icontains=search)).exclude(pk=athlete.pk)

            total = modeldata.count()


        else:
            modeldata = Athlete.objects.exclude(pk=athlete.pk)[start:start + length]
            total = Athlete.objects.exclude(pk=athlete.pk).distinct().count()

    say = start + 1
    start = start + length
    page = start / length

    beka = []

    for item in modeldata:
        klup = ''
        try:
            if item.licenses:
                for lisans in item.licenses.all():
                    if lisans.sportsClub:
                        klup = str(lisans.sportsClub) + "<br>" + klup
        except:
            klup = ''
        if item.person.birthDate is not None:
            date = item.person.birthDate.strftime('%d/%m/%Y')
        else:
            date = ''
        data = {
            'id': 'row-' + str(item.pk),
            'say': say,
            'pk': item.pk,
            'tc': item.person.tc,
            'mail': item.user.email,
            'anne': item.person.motherName,
            'baba': item.person.fatherName,


            'name': item.user.first_name + ' ' + item.user.last_name,

            'birthDate': date,

            'klup': klup,

        }
        beka.append(data)
        say += 1

    response = {

        'data': beka,
        'draw': draw,
        'recordsTotal': total,
        'recordsFiltered': total,

    }
    return JsonResponse(response)


@login_required
def return_sporcu(request):
    active = general_methods.controlGroup(request)
    # print('ben geldim')
    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    # /datatablesten gelen veri kümesi datatables degiskenine alindi
    if request.method == 'GET':
        datatables = request.GET
        pk = request.GET.get('cmd')
        # print('pk beklenen deger =',pk)
        competition = Competition.objects.get(pk=pk)
        # kategori = CompetitionCategori.objects.get(pk=request.GET.get('cmd'))

    elif request.method == 'POST':
        datatables = request.POST
        # print(datatables)
        # print("post islemi gerceklesti")

    # /Sayfanın baska bir yerden istenmesi durumunda degerlerin None dönmemesi icin degerler try boklari icerisine alindi
    try:
        draw = int(datatables.get('draw'))
        # print("draw degeri =", draw)
        # Ambil start
        start = int(datatables.get('start'))
        # print("start degeri =", start)
        # Ambil length (limit)
        length = int(datatables.get('length'))
        # print("lenght  degeri =", length)
        # Ambil data search
        search = datatables.get('search[value]')
        # print("search degeri =", search)
    except:
        draw = 1
        start = 0
        length = 10

    if length == -1:

        athletes = []
        # for comp in compAthlete:
        #     if comp.athlete:
        #         athletes.append(comp.athlete.pk)

        if active == 'KlupUye':
            sc_user = SportClubUser.objects.get(user=user)
            clubsPk = []
            clubs = SportsClub.objects.filter(clubUser=sc_user)
            for club in clubs:
                clubsPk.append(club.pk)


            modeldata = Athlete.objects.exclude(pk__in=athletes).filter(licenses__sportsClub__in=clubsPk).distinct()
            total = modeldata.count()

        elif active == 'Yonetim' or active == 'Admin':
            modeldata = Athlete.objects.exclude(pk__in=athletes)
            total = Athlete.objects.exclude(pk__in=athletes).count()

        elif active == 'Antrenor':

            coach = Coach.objects.get(user=request.user)
            clup = SportsClub.objects.filter(coachs=coach)
            clupsPk = []
            for item in clup:
                clupsPk.append(item.pk)
            athletes = Athlete.objects.filter(licenses__sportsClub_id__in=clupsPk).distinct()
            athletes |= Athlete.objects.filter(licenses__coach=coach).distinct()
            modeldata = athletes.distinct()[start:start + length]
            total = athletes.distinct().count()

    else:
        if search:
            modeldate = Athlete.objects.none()

            compAthlete = CompetitionsAthlete.objects.filter(competition=competition)
            athletes = []
            modeldata = Athlete.objects.filter(
                Q(user__last_name__icontains=search) | Q(user__first_name__icontains=search) | Q(
                    user__email__icontains=search))


            for comp in compAthlete:
                if comp.athlete:
                    athletes.append(comp.athlete.pk)
            if active == 'KlupUye':
                sc_user = SportClubUser.objects.get(user=user)
                clubsPk = []
                clubs = SportsClub.objects.filter(clubUser=sc_user)
                for club in clubs:
                    clubsPk.append(club.pk)
                modeldata = modeldata.exclude(pk__in=athletes).filter(
                    licenses__sportsClub__in=clubsPk).distinct()
                total = modeldata.exclude(pk__in=athletes).filter(
                    licenses__sportsClub__in=clubsPk).distinct().count()
            # elif active == 'Yonetim' or active == 'Admin':
            #     modeldata = modeldata.exclude(pk__in=athletes)


            elif active == 'Antrenor':
                coach = Coach.objects.get(user=request.user)
                clup = SportsClub.objects.filter(coachs=coach)
                clupsPk = []
                for item in clup:
                    clupsPk.append(item.pk)
                athletes = modeldata.filter(licenses__sportsClub_id__in=clupsPk).distinct()
                athletes |= modeldata.filter(licenses__coach=coach).distinct()
                modeldata = athletes.distinct()

            total = modeldata.count()


        else:
            compAthlete = CompetitionsAthlete.objects.filter(competition=competition)
            athletes = []
            for comp in compAthlete:
                if comp.athlete:
                    athletes.append(comp.athlete.pk)
                    # print(comp.athlete)
            if active == 'KlupUye':
                sc_user = SportClubUser.objects.get(user=user)
                clubsPk = []
                clubs = SportsClub.objects.filter(clubUser=sc_user)
                for club in clubs:
                    clubsPk.append(club.pk)
                modeldata = Athlete.objects.exclude(pk__in=athletes).filter(
                    licenses__sportsClub__in=clubsPk).distinct()[start:start + length]
                total = Athlete.objects.exclude(pk__in=athletes).filter(
                    licenses__sportsClub__in=clubsPk).distinct().count()
            elif active == 'Yonetim' or active == 'Admin':
                modeldata = Athlete.objects.exclude(pk__in=athletes)[start:start + length]
                total = Athlete.objects.exclude(pk__in=athletes).distinct().count()


            elif active == 'Antrenor':

                coach = Coach.objects.get(user=request.user)
                clup = SportsClub.objects.filter(coachs=coach)
                clupsPk = []
                for item in clup:
                    clupsPk.append(item.pk)
                athletes = Athlete.objects.filter(licenses__sportsClub_id__in=clupsPk).distinct()
                athletes |= Athlete.objects.filter(licenses__coach=coach).distinct()
                modeldata = athletes.distinct()[start:start + length]
                total = athletes.distinct().count()


    say = start + 1
    start = start + length
    page = start / length

    beka = []
    for item in modeldata:
        klup = ''
        try:
            if item.licenses:
                for lisans in item.licenses.all():
                    if lisans.sportsClub:
                        klup = str(lisans.sportsClub) + "<br>" + klup
        except:
            klup = ''
        if item.person.birthDate is not None:
            date = item.person.birthDate.strftime('%d/%m/%Y')
        else:
            date = ''
        data = {
            'say': say,
            'pk': item.pk,

            'name': item.user.first_name + ' ' + item.user.last_name,

            'birthDate': date,

            'klup': klup,

        }
        beka.append(data)
        say += 1


    response = {

        'data': beka,
        'draw': draw,
        'recordsTotal': total,
        'recordsFiltered': total,

    }
    return JsonResponse(response)


@login_required
def update_athlete(request, pk, competition):
    perm = general_methods.control_access_klup(request)
    login_user = request.user

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():

        try:
            user = User.objects.get(pk=login_user.pk)
            compAthlete = CompetitionsAthlete.objects.get(pk=competition)
            category = request.POST.get('category')
            if request.POST.get('sporcu'):
                compAthlete.athleteTwo = Athlete.objects.get(pk=request.POST.get('sporcu'))
            if category is not None:
                compAthlete.category = Category.objects.get(pk=category)
            compAthlete.save()

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except SandaAthlete.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})



    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def choose_athlete_update(request, pk, competition):
    perm = general_methods.control_access_klup(request)
    login_user = request.user

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():


        try:

            # bu alanda sporcu güncelleme alani olacak kategorisini güncelleme yapabilecegiz
            return JsonResponse({'status': 'Success', 'msg': 'save successfully'})
        except SandaAthlete.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def choose_athlete(request, pk, competition):
    perm = general_methods.control_access_klup(request)
    login_user = request.user

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():

        try:
            if request.POST.get('weight'):

                user = User.objects.get(pk=login_user.pk)
                competition = Competition.objects.get(pk=competition)
                athlete = Athlete.objects.get(pk=pk)
                compAthlete = CompetitionsAthlete()
                if CompetitionsAthlete.objects.filter(competition=competition).filter(athlete=athlete).count() <= 1:
                    if CompetitionsAthlete.objects.filter(competition=competition).filter(athlete=athlete):
                        competitionAthlete=CompetitionsAthlete.objects.get(athlete=athlete , competition=competition)
                        katagori=competitionAthlete.category.pk
                        if str(katagori) != request.POST.get('weight'):
                            if request.POST.get('sporcu'):
                                compAthlete.athleteTwo = Athlete.objects.get(pk=request.POST.get('sporcu'))
                            compAthlete.athlete = athlete
                            compAthlete.competition = competition
                            compAthlete.category = Category.objects.get(pk=request.POST.get('weight'))
                            compAthlete.save()
                            log = str(athlete.user.get_full_name()) + "  Musabakaya sporcu eklendi "
                            log = general_methods.logwrite(request, request.user, log)
                            return JsonResponse({'status': 'Success', 'msg': 'Sporcu Başarı ile kaydedilmiştir.'})
                        else:
                            return JsonResponse({'status': 'Fail', 'msg': 'Aynı kategoride kayıt vardır.'})
                    else:
                        if request.POST.get('sporcu'):
                            compAthlete.athleteTwo = Athlete.objects.get(pk=request.POST.get('sporcu'))
                        compAthlete.athlete = athlete
                        compAthlete.competition = competition
                        compAthlete.category = Category.objects.get(pk=request.POST.get('weight'))
                        compAthlete.save()
                        log = str(athlete.user.get_full_name()) + "  Musabakaya sporcu eklendi "
                        log = general_methods.logwrite(request, request.user, log)
                        return JsonResponse({'status': 'Success', 'msg': 'Sporcu Başarı ile kaydedilmiştir.'})


                else:
                    return JsonResponse({'status': 'Fail', 'msg': 'Bir sporcu 3. defa eklenemez.'})

            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Eksik'})


        except SandaAthlete.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

@login_required
def choose_athlete_competition(request):
    perm = general_methods.control_access(request)
    login_user = request.user

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():

        if request.POST.get('categori') and request.POST.get('competition'):
            print(request.POST.get('categori'))
            print(request.POST.get('competition'))
            if Category.objects.filter(pk=request.POST.get('categori')) and Competition.objects.filter(
                    pk=request.POST.get('competition')):
                categori = Category.objects.get(pk=request.POST.get('categori'))
                competition = Competition.objects.get(pk=request.POST.get('competition'))
                comAthlete = CompetitionsAthlete.objects.filter(category=categori , competition=competition).distinct()
                dizi=[]
                for item in comAthlete:
                    beka={
                        'name': item.athlete.user.get_full_name()+ ' - ' + item.athleteTwo.user.get_full_name() if item.athleteTwo else item.athlete.user.get_full_name(),
                        'pk':item.pk
                    }
                    dizi.append(beka)
                return JsonResponse(
                    {'status': 'Success', 'msg': 'Basarili bir şekilde sporcular alındı', 'athlete': dizi,'categori':categori.kategoriadi})

        else:
            return JsonResponse({'status': 'Fail', 'msg': 'Eksik'})

        # try:
        #
        #
        #
        # except :
        #     return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
@login_required
def musabaka_sporcu_tamamla(request, athletes):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST':
        athletes1 = request.POST.getlist('selected_options')
        if athletes1:
            return redirect('sbs:musabaka-sporcu-tamamla', athletes=athletes1)
            # for x in athletes1:
            #
            #         athlete = Athlete.objects.get(pk=x)
            #         compAthlete = CompAthlete()
            #         compAthlete.athlete = athlete
            #         compAthlete.competition = competition
            #         compAthlete.save()
        else:
            messages.warning(request, 'Sporcu Seçiniz')

    return render(request, 'musabaka/musabaka-sonuclar.html', {'athletes': athletes})


@login_required
def musabaka_sporcu_sil(request, pk):
    perm = general_methods.control_access_klup(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            athlete = CompetitionsAthlete.objects.get(pk=pk)

            log = str(athlete.athlete.user.get_full_name()) + "  müsabakadan silindi "
            log = general_methods.logwrite(request, request.user, log)

            athlete.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except SandaAthlete.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def result_list(request, pk):
    perm = general_methods.control_access_klup(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    competition = Competition.objects.get(pk=pk)
    compAthlete = CompetitionsAthlete.objects.exclude(degree=0).filter(competition=pk).order_by('degree')
    return render(request, 'musabaka/musabaka-sonuclar.html',
                  { 'compAthlete': compAthlete,'competition':competition})


@login_required
def return_competition_ajax(request):
    active = general_methods.controlGroup(request)
    # print('ben geldim')
    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    # /datatablesten gelen veri kümesi datatables degiskenine alindi
    if request.method == 'GET':
        datatables = request.GET
        pk = request.GET.get('cmd').strip()

    elif request.method == 'POST':
        datatables = request.POST
        # print(datatables)
        # print("post islemi gerceklesti")

    # /Sayfanın baska bir yerden istenmesi durumunda degerlerin None dönmemesi icin degerler try boklari icerisine alindi
    try:
        draw = int(datatables.get('draw'))
        # print("draw degeri =", draw)
        # Ambil start
        start = int(datatables.get('start'))
        # print("start degeri =", start)
        # Ambil length (limit)
        length = int(datatables.get('length'))
        # print("lenght  degeri =", length)
        # Ambil data search
        search = datatables.get('search[value]')
        # print("search degeri =", search)
    except:
        draw = 1
        start = 0
        length = 10
    modeldata = Competition.objects.none()
    if length == -1:
        print()

        # if user.groups.filter(name='KulupUye'):
        #     sc_user = SportClubUser.objects.get(user=user)
        #     clubsPk = []
        #     clubs = SportsClub.objects.filter(clubUser=sc_user)
        #     for club in clubs:
        #         clubsPk.append(club.pk)
        #
        #     modeldata = Athlete.objects.filter(licenses__sportsClub__in=clubsPk).distinct()
        #     total = modeldata.count()
        #
        # elif user.groups.filter(name__in=['Yonetim', 'Admin']):
        #     modeldata = Athlete.objects.all()
        #     total = Athlete.objects.all().count()


    else:
        if search:
            modeldata = Competition.objects.filter(
                Q(name=search))
            total = modeldata.count();

        else:
            # compAthlete=CompAthlete.objects.filter(competition=competition)
            # athletes = []
            # for comp in compAthlete:
            #     if comp.athlete:
            #             athletes.append(comp.athlete.pk)
            if active == 'KlupUye':
                # bu alan kontrol edilecek
                modeldata = Competition.objects.filter(year=pk)
                total = modeldata.count()
                # print('klüp üye ')
                # sc_user = SportClubUser.objects.get(user=user)
                # clubsPk = []
                # clubs = SportsClub.objects.filter(clubUser=sc_user)
                # for club in clubs:
                #     clubsPk.append(club.pk)
                # modeldata = Athlete.objects.exclude(pk__in=athletes).filter(licenses__sportsClub__in=clubsPk).distinct()[start:start + length]
                # total = mAthlete.objects.exclude(pk__in=athletes).filter(licenses__sportsClub__in=clubsPk).distinct().count()


            elif active == 'Yonetim' or active == 'Admin':

                modeldata = Competition.objects.filter(year=pk)
                total = modeldata.count()


    say = start + 1
    start = start + length
    page = start / length

    beka = []
    for item in modeldata:
        data = {
            'say': say,
            'pk': item.pk,
            'name': item.name,

        }
        beka.append(data)
        say += 1

    response = {

        'data': beka,
        'draw': draw,
        'recordsTotal': total,
        'recordsFiltered': total,

    }
    return JsonResponse(response)


@login_required
def upload(request, pk):
    if Competition.objects.filter(pk=pk):
        competition = Competition.objects.filter(pk=pk)[0]
    else:
        return redirect('sbs:musabakalar')
    # if request.method == "POST":

    # excel_file = request.FILES["file"]
    # data = None
    # if (str(excel_file).split('.')[-1] == "xls"):
    #     data = xls_get(excel_file)
    #
    # elif (str(excel_file).split('.')[-1] == "xlsx"):
    #     data = xlsx_get(excel_file)
    # else:
    #     messages.warning(request, 'Lütfen bir excel dosyasi seçiniz (.xls -.xlsx)')
    #
    # if data:
    #     for item in data.items():
    #         count = 0
    #         for count in range(len(item[1])):
    #             # bir row alınmıs oldu
    #             print(item[1][count][0])
    #         print(len(item[1]))

    return render(request, 'musabaka/SonucAktar.html', {'competition': competition})



@login_required
def antrenor_ajax(request):
    perm = general_methods.control_access_klup(request)
    login_user = request.user

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():

        beka = []
        for item in Coach.objects.all():
            data = {
                'pk': item.pk,
                'name': item.user.get_full_name(),
            }
            beka.append(data)
        return JsonResponse({'data': beka})
        # return HttpResponse(serializers.serialize("json", Coach.objects.all()))
    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})




@login_required
def antrenor_sporcu_ajax(request):
    perm = general_methods.control_access_klup(request)
    login_user = request.user

    if not perm:
        logout(request)
        return redirect('accounts:login')


    if request.method == 'POST' and request.is_ajax():
        if request.POST.get('coach'):
            athletes=Athlete.objects.none()
            if Coach.objects.filter(pk= request.POST.get('coach')):
                coach = Coach.objects.filter(pk=request.POST.get('coach'))[0]
                clup = SportsClub.objects.filter(coachs=coach)
                clupsPk = []
                for item in clup:
                    clupsPk.append(item.pk)
                athletes = Athlete.objects.filter(licenses__sportsClub_id__in=clupsPk).distinct()
                athletes |= Athlete.objects.filter(licenses__coach=coach).distinct()
            beka = []
            # antrenor verisi alınıp sistemde filtreleme yapılacak
            for item in athletes:
                data = {
                    'pk': item.pk,
                    'name': item.user.get_full_name(),
                }
                beka.append(data)
            return JsonResponse({'data': beka})



        # return HttpResponse(serializers.serialize("json", Coach.objects.all()))
    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def musabakaResultAdd(request):
    competition = Competition.objects.none()
    categori=Category.objects.none()
    if Competition.objects.all():
        competition = Competition.objects.all().order_by('-creationDate')
    if Category.objects.all():
        categori = Category.objects.all()

    if request.POST:
        if request.POST.get('categori') and request.POST.get('competitions') and request.POST.get('athlete') and request.POST.get('degre'):
            pk=int(request.POST.get('athlete'))
            comAthlete=CompetitionsAthlete.objects.get(pk=pk)
            comAthlete.degree=int(request.POST.get('degre'))
            comAthlete.save()
            messages.success(request, 'Basarili bir sekilde kaydedildi.')
        else:
            messages.warning(request, 'Alanlari kontrol ediniz.')



    return render(request, 'musabaka/musabakaSonucEkle.html', {'competition': competition,'categori':categori})
