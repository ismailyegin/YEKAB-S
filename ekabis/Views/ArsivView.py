import os
import zipfile
from builtins import print
from io import StringIO

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from unicode_tr import unicode_tr

from sbs.Forms.AbirimForm import AbirimForm
from sbs.Forms.AbirimSearchForm import AbirimSearchForm
from sbs.Forms.AbirimparametreFrom import AbirimparametreForm
from sbs.Forms.AcategoriForm import AcategoriForm
from sbs.Forms.AdosyaForm import AdosyaForm
from sbs.Forms.AdosyaFormSearch import AdosyaFormSearch
from sbs.Forms.AevrakForm import AevrakForm
from sbs.Forms.AklasorForm import AklasorForm
from sbs.Forms.AklasorSearchForm import AklasorSearchForm
from sbs.models.Abirim import Abirim
from sbs.models.AbirimParametre import AbirimParametre
from sbs.models.Adosya import Adosya
from sbs.models.AdosyaParametre import AdosyaParametre
from sbs.models.Aevrak import Aevrak
from sbs.models.Aklasor import Aklasor
from sbs.models.CategoryItem import CategoryItem
from sbs.services import general_methods
from sbs.models.Employe import Employe

@login_required
def return_arsiv(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    return render(request, 'arsiv/arsiv.html')
@login_required
def arsiv_location_add(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST':
        category_item_form = AcategoriForm(request.POST)
        if category_item_form.is_valid():
            categori = category_item_form.save(commit=False)
            categori.forWhichClazz = "location"
            categori.save()
    category_item_form = AcategoriForm()
    categoryitem = CategoryItem.objects.filter(forWhichClazz='location')
    return render(request, 'arsiv/location.html',
                  {'category_item_form': category_item_form, 'categoryitem': categoryitem})
@login_required
def arsiv_location_update(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    categori = CategoryItem.objects.get(pk=pk)
    category_item_form = AcategoriForm(request.POST or None, instance=categori)
    if request.method == 'POST':
        if category_item_form.is_valid():
            category_item_form.save()
            return redirect('sbs:arsiv-konumEkle')
    categoryitem = CategoryItem.objects.filter(forWhichClazz='location')

    return render(request, 'arsiv/locationUpdate.html',
                  {'category_item_form': category_item_form, 'categoryitem': categoryitem})


@login_required
def arsiv_birim_add(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST':
        category_item_form = AbirimForm(request.POST)
        if category_item_form.is_valid():
            birim = category_item_form.save(commit=False)
            birim.save()
            return redirect('sbs:arsiv-birimUpdate', pk=birim.pk)

    category_item_form = AbirimForm()
    return render(request, 'arsiv/birimAdd.html',
                  {'category_item_form': category_item_form, })


@login_required
def categoryItemDelete(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = Abirim.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except CategoryItem.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def arsiv_birim_update(request, pk):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    birim = Abirim.objects.get(pk=pk)
    category_item_form = AbirimForm(request.POST or None, instance=birim)

    if request.method == 'POST':
        if category_item_form.is_valid():
            category_item_form.save()
    categoryitem = AbirimParametre.objects.filter(birim=birim)
    klasor = Aklasor.objects.filter(birim=birim)
    return render(request, 'arsiv/birimGuncelle.html', {'category_item_form': category_item_form,
                                                        'categoryitem': categoryitem,
                                                        'birim': birim,
                                                        'klasor': klasor})


@login_required
def arsiv_birimParametre(request, pk):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    abirim = Abirim.objects.get(pk=pk)
    category_item_form = AbirimparametreForm(request.POST or None)
    if request.method == 'POST':
        if category_item_form.is_valid():
            test = AbirimParametre(title=category_item_form.cleaned_data['title'],
                                   birim=abirim,
                                   type=category_item_form.cleaned_data['type']
                                   )
            test.save()

            return redirect('sbs:arsiv-birimUpdate', pk=abirim.pk)

    return render(request, 'arsiv/parametreEkle.html', {'parametre_form': category_item_form, })


@login_required
def arsiv_birimParametreUpdate(request, pk):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    if AbirimParametre.objects.filter(pk=pk):
        parametre = AbirimParametre.objects.get(pk=pk)
        category_item_form = AbirimparametreForm(request.POST or None, instance=parametre)
    else:
        parametre = AbirimParametre.objects.none()
        category_item_form = AbirimparametreForm(request.POST or None)

    if request.method == 'POST':
        if category_item_form.is_valid():
            test = category_item_form.save()
            test.save()
            return redirect('sbs:arsiv-birimUpdate', parametre.birim.pk)
    return render(request, 'arsiv/parametreEkle.html', {'parametre_form': category_item_form, })


@login_required
def arsiv_birimListesi(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    birim_form = AbirimSearchForm()
    birimler = Abirim.objects.none()
    if request.method == 'POST':
        name = request.POST.get('name')
        active = general_methods.controlGroup(request)
        if not (name):

            if active != 'Personel':
                birimler = Abirim.objects.all()
            else:
                birimler = Abirim.objects.filter(employe=Employe.objects.get(user=request.user))


        else:
            query = Q()
            if name:
                query &= Q(name__icontains=name)

            if active != 'Personel':
                birimler = Abirim.objects.filter(query)
            else:
                birimler = Abirim.objects.filter(employe=Employe.objects.get(user=request.user)).filter(query)

    return render(request, 'arsiv/BirimList.html', {'birimler': birimler,
                                                    'birim_form': birim_form})
@login_required
def parametredelete(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:

            if AbirimParametre.objects.filter(pk=pk):
                obj = AbirimParametre.objects.get(pk=pk)

                obj.delete()
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'id degeri yok'})

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except CategoryItem.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


def arsiv_klasorEkle(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    if request.GET.get('birim'):
        if Abirim.objects.filter(pk=request.GET.get('birim')):
            form = AklasorForm(initial={'birim': Abirim.objects.get(pk=request.GET.get('birim'))})
    else:
        form = AklasorForm()

    if request.method == 'POST':
        form = AklasorForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()

            return redirect('sbs:klasor-guncelle', form.pk)

    return render(request, 'arsiv/KlasorEkle.html', {'form': form})


def arsiv_klasorler(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    klasor = Aklasor.objects.none()
    klasor_form = AklasorSearchForm()
    if request.method == 'POST':
        name = request.POST.get('name')
        sirano = request.POST.get('sirano')
        location = request.POST.get('location')
        birim = request.POST.get('birim')
        start = request.POST.get('startyear')
        finish = request.POST.get('finishyear')
        active = general_methods.controlGroup(request)
        if not (name or sirano or location or birim or finish or start):
            if active != 'Personel':
                klasor = Aklasor.objects.all()
            else:
                klasor =Aklasor.objects.filter(birim__employe=Employe.objects.get(user=request.user))
        else:
            query = Q()
            if name:
                query &= Q(name__icontains=name)
            if sirano:
                query &= Q(sirano=sirano)
            if location:
                query &= Q(location__pk=int(location))
            if birim:
                query &= Q(birim__pk=int(birim))
            if start:
                query &= Q(startyear__gte=start)
            if finish:
                query &= Q(finishyear__lte=finish)

            if active != 'Personel':
                klasor = Aklasor.objects.filter(query)
            else:
                klasor = Aklasor.objects.filter(birim__employe=Employe.objects.get(user=request.user)).filter(query)


    #
    # for item in klasor:
    #     parametre = Adosya.objects.filter(klasor=item)
    #     # print(parametre.values_list("title","title"))
    #     beka = {
    #         'pk': item.pk,
    #         'name': item.name,
    #         'parametre': parametre
    #     }
    #     birimler.append(beka)

    # arama alani yazılacak
    # if request.method == 'POST':
    #     if category_item_form.is_valid():
    #         category_item_form.save()
    #         return redirect('sbs:arsiv-birimEkle')

    return render(request, 'arsiv/KlasorListesi.html', {'klasor': klasor,
                                                        'klasor_form': klasor_form})


@login_required
def arsiv_klasorUpdate(request, pk):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    klasor = Aklasor.objects.get(pk=pk)
    klasor_form = AklasorForm(request.POST or None, instance=klasor)
    dosya = Adosya.objects.filter(klasor=klasor)
    if request.method == 'POST':
        if klasor_form.is_valid():
            test = klasor_form.save()
            test.save()
    ileri = 0
    geri = 0
    x = 0
    for item in Aklasor.objects.filter(birim=klasor.birim):
        if item.pk == klasor.pk:
            x = 1
        else:
            if x == 0:
                geri = item.pk
            if x == 1:
                ileri = item.pk
                break
    return render(request, 'arsiv/KlasorGuncelle.html', {'form': klasor_form,
                                                         'dosya': dosya,
                                                         'klasor': klasor,
                                                         'back': geri,
                                                         'forward': ileri,
                                                         })

def arsiv_dosyaEkle(request, pk):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    klasor = Aklasor.objects.get(pk=pk)
    form = AdosyaForm(pk)
    if request.method == 'POST':

        form = AdosyaForm(pk, request.POST)
        if form.is_valid():
            pk = form.save(pk)
            return redirect('sbs:dosya-guncelle', pk)
    return render(request, 'arsiv/DosyaEkle.html', {'form': form})


@login_required
def arsiv_dosyaUpdate(request, pk):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    dosya = Adosya.objects.get(pk=pk)
    form = AdosyaForm(dosya.klasor.pk, request.POST or None, instance=dosya)
    dosyaparametre = AdosyaParametre.objects.filter(dosya=dosya)
    for item in dosyaparametre:
        form.fields[item.parametre.title].initial = item.value

    files = Aevrak.objects.filter(adosya=dosya)
    evraklist = []
    for item in files:
        # print(item.file.name)
        if item.file.name.split(".")[len(item.file.name.split(".")) - 1] == "pdf":
            evraklist.append(item)
    if request.method == 'POST':
        if request.FILES.get('file'):
            evrak = Aevrak(file=request.FILES.get('file'))
            evrak.save()
            dosya = Adosya.objects.get(pk=pk)
            dosya.evrak.add(evrak)
            dosya.save()

        dosya.sirano = request.POST.get('sirano')

        birimparametre = AbirimParametre.objects.filter(birim=dosya.klasor.birim)
        for item in birimparametre:
            if dosyaparametre.filter(parametre=item):
                deger = dosyaparametre.filter(parametre=item)[0]
                if request.POST.get(deger.parametre.title):
                    deger.value = request.POST.get(deger.parametre.title)
                    deger.save()
            else:
                dosyaParametre = AdosyaParametre(
                    value=str(request.POST.get(item.title)),
                    dosya=dosya,
                )
                dosyaParametre.parametre = item
                dosyaParametre.save()
    dosya.save()
    ileri = 0
    geri = 0
    x = 0
    for item in Adosya.objects.filter(klasor=dosya.klasor):
        if item.pk == dosya.pk:
            x = 1
        else:
            if x == 0:
                geri = item.pk
            if x == 1:
                ileri = item.pk
                break
    return render(request, 'arsiv/DosyaGuncelle.html',
                  {'form': form,
                   'dosya': dosya,
                   'files': files,
                   'evraklist': evraklist,
                   'back': geri,
                   'forward': ileri,
                   })
@login_required
def arsiv_evrakEkle(request, pk):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    form = AevrakForm()
    if request.method == 'POST':
        form = AevrakForm(request.POST, request.FILES)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            for file in files:
                evrak = Aevrak(file=file)
                evrak.save()
                dosya = Adosya.objects.get(pk=pk)
                dosya.evrak.add(evrak)
                dosya.save()
            return redirect('sbs:dosya-guncelle', dosya.pk)

    return render(request, 'arsiv/EvrakEkle.html',
                  {'form': form, }
                  )
@login_required
def arsiv_evrakDelete(request, pk):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    evrak = Aevrak.objects.get(pk=pk)
    dosya = Adosya.objects.filter(evrak=evrak)[0]
    evrak.delete()
    return redirect('sbs:dosya-guncelle', dosya.pk)
@login_required
def arsiv_anasayfa(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    data = []
    oran = []
    units_count = Abirim.objects.count()
    klasor_count = Aklasor.objects.count()
    dosyalar_count = Adosya.objects.count()
    evrak_count = Aevrak.objects.count()
    # öz yinelemeli hale gelecek
    beka = []
    birimler = Abirim.objects.distinct()
    for birim in birimler:
        sayi = 0
        klasorler = Aklasor.objects.filter(birim=birim)
        for klasor in klasorler:
            dosyalar = Adosya.objects.filter(klasor=klasor)
            for dosya in dosyalar:
                sayi += int(dosya.evrak.count())
        beka.append((birim.name, sayi))

    def takeSecond(elem):
        return elem[1]

    beka.sort(key=takeSecond, reverse=True)
    for item in beka[:6]:
        data.append({'sayi': item[1], 'birim': item[0]})
        oran.append({'oran': round((item[1] / beka[0][1]) * 100)})

    return render(request, "arsiv/arsivAnasayfa.html",
                  {'units_count': units_count,
                   'klasor_count': klasor_count,
                   'dosyalar_count': dosyalar_count,
                   'evrak_count': evrak_count,
                   'data': data,
                   'oran': oran,

                   }
                  )


@login_required
def parametre(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    if request.method == 'POST':
        if request.POST.get('cmd'):
            birim = Abirim.objects.get(pk=int(request.POST.get('cmd')))
            parametre = AbirimParametre.objects.filter(birim=birim)

            beka = []
            for item in parametre:
                data = {
                    'pk': item.pk,
                    'title': item.title,
                    'type': item.type,
                }
                beka.append(data)
            return JsonResponse(
                {
                    'data': beka,
                    'msg': 'Valid is  request'
                })
        else:
            return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


def birimGeneralSearch(request):
    dosya = Adosya.objects.none()
    units = Abirim.objects.none()
    klasor = Aklasor.objects.none()

    if request.method == 'POST':
        if request.POST.get('search'):
            search = unicode_tr(request.POST.get('search')).upper()
            units |= Abirim.objects.filter(name__icontains=search)

            klasor |= Aklasor.objects.filter(name__icontains=search)
            try:
                dosya |= Adosya.objects.filter(sirano=search)
            except:
                print('Sayisal degil')
            if klasor:
                for item in klasor:
                    units |= Abirim.objects.filter(pk=item.birim.pk)
            if dosya:
                for item in dosya:
                    klasor |= Aklasor.objects.filter(pk=item.klasor.pk)
                    units |= Abirim.objects.filter(pk=item.klasor.birim.pk)
            dosyaparametre = AdosyaParametre.objects.filter(value__contains=search)
            if dosyaparametre:
                for item in dosyaparametre:
                    dosya |= Adosya.objects.filter(pk=int(item.dosya.pk))
                    klasor |= Aklasor.objects.filter(pk=item.dosya.klasor.pk)
                    units |= Abirim.objects.filter(pk=item.dosya.klasor.birim.pk)
    return render(request, "arsiv/GenelArama.html",
                  {
                      'units': units.distinct(),
                      'klasor': klasor.distinct(),
                      'files': dosya.distinct()
                  })


def birimsearch(request):
    birimler = []
    categori = Abirim.objects.all()

    for item in categori:
        parametre = AbirimParametre.objects.filter(birim=item)
        # print(parametre.values_list("title","title"))
        beka = {
            'pk': item.pk,
            'name': item.name,
            'parametre': parametre
        }
        birimler.append(beka)
    test = []
    dosya = Adosya.objects.none()
    birimdizi = []

    units = Abirim.objects.none()
    klasor = Aklasor.objects.none()

    if request.method == 'POST':
        if request.POST.get('birim_id'):
            birimparametre = AbirimParametre.objects.filter(birim__id=int(request.POST.get('birim_id')))
            for item in birimparametre:
                if request.POST.get(item.title):
                    # print(request.POST.get(item.title))
                    dosyaParametre = AdosyaParametre.objects.filter(value__icontains=request.POST.get(item.title))
                    for item in dosyaParametre:
                        dosya |= Adosya.objects.filter(pk=int(item.dosya.pk))
                        klasor |= Aklasor.objects.filter(pk=item.dosya.klasor.pk)
                        units |= Abirim.objects.filter(pk=item.dosya.klasor.birim.pk)
    return render(request, "arsiv/BirimSearch.html",
                  {
                      'birimler': birimler,
                      'units': units.distinct(),
                      'klasor': klasor.distinct(),
                      'files': dosya.distinct()
                  })


def arsiv_dosyalar(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    dosya = Adosya.objects.none()
    dosya_form = AdosyaFormSearch()
    klasor_form = AklasorSearchForm()

    if request.method == 'POST':
        sirano = request.POST.get('sirano')
        location = request.POST.get('location')
        birim = request.POST.get('birim')
        klasor = request.POST.get('klasor')
        active = general_methods.controlGroup(request)
        if not (klasor or sirano or location or birim):


            if active != 'Personel':
                dosya = Adosya.objects.all()
            else:
                dosya=Adosya.objects.filter(klasor__birim__employe=Employe.objects.get(user=request.user))
        else:
            query = Q()
            if klasor:
                query &= Q(klasor__pk=klasor)
            if sirano:
                query &= Q(sirano=sirano)
            if location:
                query &= Q(klasor__location__pk=location)
            if birim:
                query &= Q(klasor__birim__pk=birim)
            if active != 'Personel':
                dosya = Adosya.objects.filter(query)
            else:
                dosya=Adosya.objects.filter(klasor__birim__employe=Employe.objects.get(user=request.user)).filter(query)

    return render(request, 'arsiv/DosyaListesi.html', {'dosya': dosya,
                                                       'klasor_form': klasor_form,
                                                       'dosya_form': dosya_form
                                                       })


@login_required
def birimSearch(request):
    active = general_methods.controlGroup(request)
    dosya = Adosya.objects.none()
    units = Abirim.objects.none()
    klasor = Aklasor.objects.none()
    klasor_form = AklasorSearchForm()

    dosyadizi = []
    dosyaX=[]
    backdata = None
    backsearch = None
    employe=Employe.objects.none()
    if active == 'Personel':
        employe = Employe.objects.get(user=request.user)

    if request.method == 'POST':
        name = request.POST.get('klasorname')
        sirano = request.POST.get('klasorsirano')
        location = request.POST.get('klasorlocation')
        birim = request.POST.get('klasorbirim')
        start = request.POST.get('klasorstartyear')
        finish = request.POST.get('klasorfinishyear')

        dosyaparametre=AdosyaParametre.objects.none()

        # genel arama alani
        if request.POST.get('search'):
            search = unicode_tr(request.POST.get('search')).upper()
            backdata = search
            backsearch = "genelArama"
            # print('genel arama ')
            if active != 'Personel':
                units |= Abirim.objects.filter(name__icontains=search)
                klasor |= Aklasor.objects.filter(name__icontains=search)
                try:
                    dosya |= Adosya.objects.filter(sirano=search)
                except:
                    print('Sayisal degil')
                if klasor:
                    for item in klasor:
                        units |= Abirim.objects.filter(pk=item.birim.pk)
                if dosya:
                    for item in dosya:
                        klasor |= Aklasor.objects.filter(pk=item.klasor.pk)
                        units |= Abirim.objects.filter(pk=item.klasor.birim.pk)
                dosyaparametre = AdosyaParametre.objects.filter(value__contains=search)
            else:
                employe=Employe.objects.get(user=request.user)
                units |= Abirim.objects.filter(employe=employe).filter(name__icontains=search)
                klasor |= Aklasor.objects.filter(birim__employe=employe).filter(name__icontains=search)
                try:
                    dosya |= Adosya.objects.filter(klasor__birim__employe=employe).filter(sirano=search)
                except:
                    print('Sayisal degil')
                if klasor:
                    for item in klasor:
                        units |= Abirim.objects.filter(employe=employe).filter(pk=item.birim.pk)
                if dosya:
                    for item in dosya:
                        klasor |= Aklasor.objects.filter(birim__employe=employe).filter(pk=item.klasor.pk)
                        units |= Abirim.objects.filter(employe=employe).filter(pk=item.klasor.birim.pk)
                dosyaparametre = AdosyaParametre.objects.filter(value__contains=search)

            if dosyaparametre:
                for item in dosyaparametre:
                    dosya |= Adosya.objects.filter(pk=int(item.dosya.pk))
                    klasor |= Aklasor.objects.filter(pk=item.dosya.klasor.pk)
                    units |= Abirim.objects.filter(pk=item.dosya.klasor.birim.pk)
                    beka = {
                        'pk': item.dosya.pk,
                        'sirano': item.dosya.sirano,
                        'parametre': search + '/' + item.parametre.title,
                        'klasor_id': item.dosya.klasor.pk,
                        'parametre':item.parametre.title,
                        'birim':item.parametre.birim.pk
                          }
                    dosyadizi.append(beka)

            if dosya:
                test=[]
                for item in dosya:
                    test.append(item.pk)

                for item in AdosyaParametre.objects.filter(dosya__in=test):
                    beka = {
                        'pk': item.dosya.pk,
                        'sirano': item.dosya.sirano,
                        'birim':item.parametre.birim.pk,
                        'value':item.value,
                        'title':item.parametre.title,
                          }
                    dosyaX.append(beka)
        # dosya arama alani
        # if request.POST.get('searchdosya'):
        #     dosya |=Adosya.objects.filter(sirano=request.POST.get('searchdosya'))
        #     for item in dosya:
        #         klasor |= Aklasor.objects.filter(pk=item.klasor.pk)
        #         units |= Abirim.objects.filter(pk=item.klasor.birim.pk)
        # birim arama alani
        elif request.POST.get('searchbirim'):
            # print('birim arama ')
            units=Abirim.objects.none()

            if active != 'Personel':
                units = Abirim.objects.filter(pk=request.POST.get('searchbirim'))
            else:
                units = Abirim.objects.filter(employe=Employe.objects.filter(user__last_name__icontains=request.user)).filter(pk=request.POST.get('searchbirim'))

            backdata = Abirim.objects.get(pk=request.POST.get('searchbirim')).pk
            backsearch = "birimArama"
            birimparametre = AbirimParametre.objects.filter(birim__id=int(request.POST.get('searchbirim')))
            if birimparametre:
                for item in birimparametre:
                    if request.POST.get(item.title):
                        # print(request.POST.get(item.title))

                        dosyaParametre = AdosyaParametre.objects.filter(
                            value__icontains=unicode_tr(request.POST.get(item.title)).upper())
                        for dosyapara in dosyaParametre:
                            dosya |= Adosya.objects.filter(pk=int(dosyapara.dosya.pk))
                            klasor |= Aklasor.objects.filter(pk=dosyapara.dosya.klasor.pk)

                            beka = {
                                'pk': dosyapara.dosya.pk,
                                'sirano': dosyapara.dosya.sirano,
                                'parametre': unicode_tr(
                                    request.POST.get(item.title)).upper() + '/' + dosyapara.parametre.title,
                                'klasor_id': dosyapara.dosya.klasor.pk
                            }
                            dosyadizi.append(beka)

            if not (klasor):
                if active != 'Personel':
                    klasor = Aklasor.objects.filter(birim=Abirim.objects.get(pk=request.POST.get('searchbirim')))
                    dosya = Adosya.objects.filter(klasor__birim__pk=request.POST.get('searchbirim'))
                else:
                    klasor = Aklasor.objects.filter(birim__employe=Employe.objects.filter(user=request.user)).filter(birim=Abirim.objects.get(pk=request.POST.get('searchbirim')))
                    dosya = Adosya.objects.filter(klasor__birim__employe=Employe.objects.get(user=request.user)).filter(klasor__birim__pk=request.POST.get('searchbirim'))


        # klasör arama alani

        elif (name or sirano or location or birim or start or finish):

            backdata = name + "/" + sirano + "/" + location + "/" + birim
            backsearch = "searchKlasor"
            # print('klasor  arama ')
            query = Q()
            if name:
                query &= Q(name__icontains=name)
            if sirano:
                query &= Q(sirano=sirano)
            if location:
                query &= Q(location__pk=int(location))
            if birim:
                query &= Q(birim__pk=int(birim))
            if start:
                query &= Q(startyear=int(start))
            if finish:
                query &= Q(finishyear=int(finish))

            if active != 'Personel':
                klasor |= Aklasor.objects.filter(query)
            else:
                klasor |= Aklasor.objects.filter(birim__employe=Employe.objects.get(user=request.user)).filter(query)


            for item in klasor:
                units |= Abirim.objects.filter(pk=item.birim.pk)
                #seçim olmazsa hepsini getir
        else:
            if active != 'Personel':
                units = Abirim.objects.all()
                klasor = Aklasor.objects.all()
                dosya = Adosya.objects.all()
            else:

                employe=Employe.objects.get(user=request.user)
                units |= Abirim.objects.filter(employe=employe)
                klasor |= Aklasor.objects.filter(birim__employe=employe)
                dosya = Adosya.objects.filter(klasor__birim__employe=employe)


    # if len(dosyadizi) == 0:
    #     for item in dosya.distinct():
    #         if AdosyaParametre.objects.filter(dosya=item):
    #             test = AdosyaParametre.objects.filter(dosya=item)[0]
    #             # print(test.parametre)
    #             beka = {
    #                 'pk': item.pk,
    #                 'sirano': item.sirano,
    #                 'klasor_id': item.klasor.pk
    #             }
    #             dosyadizi.append(beka)
    #             print(dosyadizi)
    return render(request, "arsiv/Arama.html",
                  {
                      'units': units.distinct(),
                      'klasor': klasor.distinct(),
                      # 'files': dosyadizi,
                      'dosya': dosya,
                      'klasor_form': klasor_form,
                      'backdata': backdata,
                      'backsearch': backsearch,
                      'employe':employe,
                      'dosyadizi':dosyadizi,
                      'dosyaX':dosyaX


                  })
@login_required
def zipfile(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    dosya = Adosya.objects.get(pk=pk)
    files = Aevrak.objects.filter(adosya=dosya)
    evraklist = []

    for item in files:
        # print(item.file.name)
        if item.file.name.split(".")[len(item.file.name.split(".")) - 1] == "pdf":
            evraklist.append(item)

        # Files (local path) to put in the .zip
        # FIXME: Change this (get paths from DB etc)
    filenames = evraklist

    # Folder name in ZIP archive which contains the above files
    # E.g [thearchive.zip]/somefiles/file2.txt
    # FIXME: Set this to something better
    zip_subdir = "somefiles"
    zip_filename = "%s.zip" % zip_subdir

    # Open StringIO to grab in-memory ZIP contents
    s = StringIO()

    # The zip compressor
    zf = zipfile.ZipFile(s, "w")

    for fpath in filenames:
        # Calculate path for file in zip
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)

        # Add file, at correct path
        zf.write(fpath, zip_path)

    # Must close zip for all contents to be written
    zf.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = HttpResponse(s.getvalue(), mimetype="application/x-zip-compressed")
    # ..and correct content-disposition
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

    return resp

    # if request.method == 'POST' and request.is_ajax():
    #
    #
    #     try:
    #         obj = Abirim.objects.get(pk=pk)
    #         obj.delete()
    #         return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
    #     except CategoryItem.DoesNotExist:
    #         return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})
    #
    # else:
    #     return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def arsiv_evrakDelete_ajax(request, pk):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    if request.method == 'POST' and request.is_ajax():

        try:
            evrak = Aevrak.objects.get(pk=pk)
            dosya = Adosya.objects.filter(evrak=evrak)[0]
            evrak.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except CategoryItem.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def arsiv_klasor_delete(request, pk):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    if request.method == 'POST' and request.is_ajax():
        klasor = Aklasor.objects.get(pk=pk)
        klasor.delete()

        try:

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except CategoryItem.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def arsiv_dosya_delete(request, pk):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    if request.method == 'POST' and request.is_ajax():
        dosya = Adosya.objects.get(pk=pk)
        dosya.delete()

        try:

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except CategoryItem.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


def arsiv_dosyaEkle_full(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    active = general_methods.controlGroup(request)
    employe=Employe.objects.none()


    if active != 'Personel':
        units = Abirim.objects.all()

    else:
        units=Abirim.objects.filter(employe=Employe.objects.get(user=request.user).pk)
        employe = Employe.objects.get(user=request.user)

    unit_form = AbirimForm()
    klasor_form = AklasorForm()

    if request.method == 'POST':
        if request.POST.get("modaldosyaaddklasor"):
            form = AdosyaForm(int(request.POST.get("modaldosyaaddklasor")), request.POST)
            if form.is_valid():
                pk = form.save(int(request.POST.get("modaldosyaaddklasor")))
                return redirect('sbs:dosya-guncelle', pk)

        elif request.POST.get("dosyaupdatepk"):
            dosya = Adosya.objects.get(pk=int(request.POST.get("dosyaupdatepk")))
            dosyaparametre = AdosyaParametre.objects.filter(dosya=dosya)
            dosya.sirano = request.POST.get('sirano')
            birimparametre = AbirimParametre.objects.filter(birim=dosya.klasor.birim)
            for item in birimparametre:
                if dosyaparametre.filter(parametre=item):
                    deger = dosyaparametre.filter(parametre=item)[0]
                    if request.POST.get(deger.parametre.title):
                        deger.value = request.POST.get(deger.parametre.title)
                        deger.save()
                else:
                    dosyaParametre = AdosyaParametre(
                        value=str(request.POST.get(item.title)),
                        dosya=dosya,
                    )
                    dosyaParametre.parametre = item
                    dosyaParametre.save()
            dosya.save()
            return redirect('sbs:dosya-guncelle', dosya.pk)
        elif request.POST.get("dosya_id"):
            if Adosya.objects.filter(pk=int(request.POST.get("dosya_id"))):
                dosya = Adosya.objects.get(pk=int(request.POST.get("dosya_id")))
                if request.FILES.getlist('file'):
                    for item in request.FILES.getlist('file'):
                        evrak = Aevrak(file=item)
                        evrak.save()
                        dosya.evrak.add(evrak)
                        dosya.save()
                return redirect('sbs:dosya-guncelle', pk=dosya.pk)

    return render(request, 'arsiv/EvrakEkleSec.html', {
        'units': units,
        'unit_form': unit_form,
        'klasor_form': klasor_form,
        'employe':employe
    })


@login_required
def ajax_klasor(request):
    try:
        if request.method == 'POST':
            klasor = Aklasor.objects.filter(birim__pk=request.POST.get('cmd'))
            beka = []
            for item in klasor:
                data = {
                    'pk': item.pk,
                    'name': item.name,
                }
                beka.append(data)
            return JsonResponse(
                {
                    'data': beka,
                    'msg': 'Valid is  request'
                })
    except:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def ajax_klasor_update(request):
    try:
        if request.method == 'POST':
            if request.POST.get('pk'):
                if Aklasor.objects.filter(pk=request.POST.get('pk')):
                    klasor = Aklasor.objects.get(pk=request.POST.get('pk'))
                    return JsonResponse(
                        {
                            'pk': klasor.pk,
                            'location': klasor.location.pk,
                            'birim': klasor.birim.pk,
                            'name': klasor.name,
                            'sirano': klasor.sirano,
                            'finish': klasor.finishyear,
                            'start': klasor.startyear,
                            'status': 'Success',
                            'msg': 'Valid is  request'
                        })
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
        else:
            return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

    except:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def ajax_klasor_update_add(request):
    try:
        if request.method == 'POST':
            if request.POST.get('pk'):
                if Aklasor.objects.filter(pk=request.POST.get('pk')):
                    klasor = Aklasor.objects.get(pk=request.POST.get('pk'))
                    if request.POST.get('name'):
                        klasor.name = request.POST.get('name')
                    if request.POST.get('sirano'):
                        klasor.sirano = request.POST.get('sirano')
                    if request.POST.get('location'):
                        klasor.location_id = request.POST.get('location')
                    if request.POST.get('birim'):
                        klasor.birim_id = request.POST.get('birim')
                    if request.POST.get('finish'):
                        klasor.finishyear = request.POST.get('finish')
                    if request.POST.get('start'):
                        klasor.startyear = request.POST.get('start')

                    klasor.save()

                    return JsonResponse(
                        {
                            'pk': klasor.pk,
                            'name': klasor.name,
                            'birimpk': klasor.birim.pk,
                            'birimname': klasor.birim.name,
                            'finish': klasor.finishyear,
                            'start': klasor.startyear,
                            'status': 'Success',
                            'msg': 'İşlem Başari ile gerçekleşti'

                        })
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
        else:
            return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

    except:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def ajax_dosya(request):
    try:
        if request.method == 'POST':
            project = Adosya.objects.filter(klasor__pk=request.POST.get('cmd'))
            beka = []
            for item in project:
                data = {
                    'pk': item.pk,
                    'name': item.sirano,
                }
                beka.append(data)
            return JsonResponse(
                {
                    'data': beka,
                    'msg': 'Valid is  request'
                })

    except:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def ajax_dosyaform(request):
    if request.POST.get('cmd'):
        klasor = Aklasor.objects.get(pk=int(request.POST.get('cmd')))
        form = str(AdosyaForm(klasor.pk))
        return JsonResponse(
            {
                'data': form,
                'msg': 'Valid is  request'
            })
    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def ajax_dosyaform_update(request):
    if request.POST.get('dosya'):
        if Adosya.objects.filter(pk=int(request.POST.get('dosya'))):
            dosya = Adosya.objects.get(pk=int(request.POST.get('dosya')))
            form = AdosyaForm(dosya.klasor.pk, instance=dosya)
            dosyaparametre = AdosyaParametre.objects.filter(dosya=dosya)
            for item in dosyaparametre:
                form.fields[item.parametre.title].initial = item.value
            data = str(form)
            return JsonResponse(
                {
                    'data': data,
                    'msg': 'Valid is  request',
                    'status': 'Success'
                })
        else:
            return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def ajax_birimAdd(request):
    if request.POST.get('cmd'):
        birim = Abirim(name=request.POST.get('cmd'))
        birim.save()
        return JsonResponse(
            {
                'pk': birim.pk,
                'status': 'Success',
                'msg': 'Valid is  request'
            })
    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def ajax_birimUpdateParametre(request):
    if request.method == 'POST':
        if Abirim.objects.get(pk=request.POST.get('pk')):
            birim = Abirim.objects.get(pk=request.POST.get('pk'))
            say = 1
            beka = []
            for item in AbirimParametre.objects.filter(birim=birim):
                data = {
                    'pk': item.pk,
                    'count': say,
                    'tanımı': item.title,
                }
                beka.append(data)
                say += 1
            total = AbirimParametre.objects.filter(birim=birim).count()
            response = {
                'data': beka,
                'recordsTotal': total,
                'recordsFiltered': total,
            }
            return JsonResponse(response)
    return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def ajax_birimUpdateParametreAdd(request):
    if request.POST.get('type') and request.POST.get('title') and request.POST.get('birim'):

        parametre = AbirimParametre(
            title=request.POST.get('title'),
            type=request.POST.get('type'),
            birim=Abirim.objects.get(pk=int(request.POST.get('birim')))
        )
        parametre.save()

        return JsonResponse(
            {
                'pk': parametre.pk,
                'title': parametre.title,
                'status': 'Success',
                'msg': 'Valid is  request'
            })
    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def ajax_birimUpdate(request):
    if request.POST.get('pk') and request.POST.get('name'):
        if Abirim.objects.filter(pk=int(request.POST.get('pk'))):
            birim = Abirim.objects.get(pk=int(request.POST.get('pk')))
            birim.name = request.POST.get('name')
            birim.save()
            return JsonResponse(
                {
                    'pk': birim.pk,
                    'name': birim.name,
                    'status': 'Success',
                    'msg': 'Valid is  request'
                })
        else:

            return JsonResponse({'status': 'Fail', 'msg': 'Birim Yok '})



    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def ajax_klasorAdd(request):
    if request.POST.get('name') and request.POST.get('sirano') and request.POST.get('location') and request.POST.get(
            'birim'):
        klasor = Aklasor(name=request.POST.get('name'),
                         sirano=int(request.POST.get('sirano')),
                         location_id=int(request.POST.get('location')),
                         birim_id=int(request.POST.get('birim')),
                         startyear=int(request.POST.get('finish')),
                         finishyear=int(request.POST.get('start')),
                         )
        klasor.save()
        return JsonResponse(
            {
                'pk': klasor.pk,
                'status': 'Success',
                'msg': 'Valid is  request'
            })
    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})





