import traceback

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import redirect, render

from ekabis.Forms.ConnectionRegionForm import ConnectionRegionForm
from ekabis.Forms.ConnectionUnitForm import ConnectionUnitForm
from ekabis.models import YekaCompetition
from ekabis.models.ConnectionRegion import ConnectionRegion
from ekabis.models.ConnectionUnit import ConnectionUnit
from ekabis.services import general_methods
from ekabis.services.general_methods import get_error_messages
from ekabis.services.services import UnitService, ConnectionUnitGetService, \
    ConnectionRegionGetService, YekaGetService, CityService, CityGetService


@login_required
def return_connectionRegionUnit(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    unit_form = ConnectionUnitForm()

    try:
        with transaction.atomic():
            if request.method == 'POST':

                unit_form = ConnectionUnitForm(request.POST)

                if unit_form.is_valid():

                    unit = ConnectionUnit(name=unit_form.cleaned_data['name'])
                    unit.save()

                    log = " Birim eklendi"
                    log = general_methods.logwrite(request, request.user, log)
                    messages.success(request, 'Birim Başarıyla Kayıt Edilmiştir.')
                    return redirect('ekabis:view_units')

                else:
                    error_message_unit = get_error_messages(unit_form)
                    unitfilter = {
                        'isDeleted': False
                    }
                    units = UnitService(request, unitfilter)
                    return render(request, 'ConnectionRegion/add_unit.html',
                                  {'unit_form': unit_form, 'units': units, 'error_messages': error_message_unit})
            unitfilter = {
                'isDeleted': False
            }
            units = UnitService(request, unitfilter)
            return render(request, 'ConnectionRegion/add_unit.html',
                          {'unit_form': unit_form, 'units': units, 'error_messages': ''})

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_units')


@login_required
def delete_unit(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']
                unitfilter = {
                    'uuid': uuid
                }
                obj = ConnectionUnitGetService(request, unitfilter)
                log = str(obj.name) + " Birim silindi"
                log = general_methods.logwrite(request, request.user, log)
                obj.isDeleted = True
                obj.save()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})


            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

    except obj.DoesNotExist:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

@login_required
def update_unit(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    unitfilter = {
        'uuid': uuid
    }
    unit = ConnectionUnitGetService(request, unitfilter)
    unit_form = ConnectionUnitForm(request.POST or None, instance=unit)
    try:
        with transaction.atomic():
            if request.method == 'POST':

                if unit_form.is_valid():
                    unit.name = unit_form.cleaned_data['name']
                    unit.save()
                    messages.success(request, 'Başarıyla Güncellendi')
                    return redirect('ekabis:view_units')
                else:
                    error_message_unit = get_error_messages(unit_form)
                    return render(request, 'ConnectionRegion/update_unit.html',
                                  {'unit_form': unit_form, 'error_messages': error_message_unit, 'units': ''})

            return render(request, 'ConnectionRegion/update_unit.html',
                          {'unit_form': unit_form, 'error_messages': '', 'units': ''})
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')


@login_required
def add_connectionRegion(request,uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    region_form = ConnectionRegionForm()


    try:

        yeka_filter={
            'uuid' :uuid,
            'isDeleted' : False,
        }
        yeka=YekaGetService(request,yeka_filter)
        with transaction.atomic():

            if request.method == 'POST':

                region_form = ConnectionRegionForm(request.POST)

                if region_form.is_valid():



                    region = region_form.save(commit=False)
                    total = int(
                        ConnectionRegion.objects.filter(yeka=yeka).distinct().aggregate(Sum('capacity'))[
                            'capacity__sum'] or 0)
                    total +=region.capacity

                    if yeka.capacity<total:
                        messages.warning(request, 'Bölgelerin Kapasite  toplamı Yekanın Kapasitesinden büyük olamaz')

                        return render(request, 'ConnectionRegion/add_connectionRegion.html',
                                      {'region_form': region_form, 'yeka': yeka,
                                       })

                    region.save()
                    yeka.connection_region.add(region)
                    yeka.save()

                    region_city = request.POST.getlist('cities')
                    cities=[]
                    for item in region_city:
                        city_filter={
                            'pk':item
                        }
                        region.cities.add(CityGetService(request, city_filter))
                        region.save()

                    log = " Bölge eklendi"
                    log = general_methods.logwrite(request, request.user, log)
                    messages.success(request, 'Bölge Başarıyla Kayıt Edilmiştir.')
                    return redirect('ekabis:add_region' ,region.uuid)

                else:
                    error_message_region = get_error_messages(region_form)

                    return render(request, 'ConnectionRegion/add_connectionRegion.html',
                                  {'region_form': region_form, 'yeka':yeka, 'error_messages': error_message_region})
            regionfilter = {
                'isDeleted': False

            }
            regions = yeka.connection_region.all()
            return render(request, 'ConnectionRegion/add_connectionRegion.html',
                          {'region_form': region_form, 'regions': regions, 'error_messages': '', 'yeka':yeka})

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')




@login_required
def delete_region(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']
                regionfilter = {
                    'uuid': uuid
                }
                obj = ConnectionRegionGetService(request, regionfilter)
                # not: Silme işleminde kontrol yapılacak yarışma var mı şimdi yarışma alanını yazmadıgım için kontrol edemiyorum
                region_capacities = YekaCompetition.objects.filter(isDeleted=False)
                if region_capacities:
                    return JsonResponse(
                        {'status': 'Fail', 'msg': 'Bölge için tanımlanmış yarışmalar  var. Bölge silinemez'})
                else:
                    log = str(obj.name) + "Bölge silindi"
                    log = general_methods.logwrite(request, request.user, log)
                    obj.isDeleted = True
                    obj.save()
                    return JsonResponse({'status': 'Success', 'messages': 'save successfully'})


            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

    except obj.DoesNotExist:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def update_region(request, uuid,yeka):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        regionfilter = {
            'uuid': uuid,
            'isDeleted': False
        }
        yeka_filter={
            'uuid':yeka,
            'isDeleted': False

        }
        yeka=YekaGetService(request,yeka_filter)
        region = ConnectionRegionGetService(request, regionfilter)
        region_form = ConnectionRegionForm(request.POST or None, instance=region ,initial={'cities': region.cities.all()})
        print(region_form.fields['cities'].initial)
        for item in region.cities.all():
            print(item)
        with transaction.atomic():
            if request.method == 'POST':

                if region_form.is_valid():
                    region=region_form.save(commit=False)
                    region = region_form.save(commit=False)
                    total = int(
                        ConnectionRegion.objects.exclude(uuid=region.uuid).filter(yeka=yeka).distinct().aggregate(Sum('capacity'))[
                            'capacity__sum'] or 0)
                    total += region.capacity

                    if yeka.capacity < total:
                        messages.warning(request, 'Bölgelerin Kapasite  toplamı Yekanın Kapasitesinden büyük olamaz')
                        return render(request, 'ConnectionRegion/update_region.html',
                                      {'region_form': region_form, 'units': ''})
                    region.save()

                    region_city = request.POST.getlist('cities')
                    city_list = []
                    region_city_list=[]
                    for item in region.cities.all():
                        city_list.append(item.pk)
                    for item in region_city:
                        city_filter = {
                            'pk': item
                        }
                        region_city_list.append(int(item))
                        if CityService(request, city_filter):
                            if not region.cities.filter(pk=item):
                                # deger yoksa kaydedildi
                                region.cities.add(CityGetService(request, city_filter))
                                region.save()
                    remove=list(set(city_list) - set(region_city_list))

                    for item in remove:
                        city_filter = {
                            'pk': item
                        }
                        region.cities.remove(CityGetService(request, city_filter))
                        region.save()

                    messages.success(request, 'Bölge Başarıyla Güncellendi')
                    return redirect('ekabis:add_region' ,yeka.uuid)
                else:
                    error_message_unit = get_error_messages(region_form)
                    return render(request, 'ConnectionRegion/update_region.html',
                                  {'region_form': region_form, 'error_messages': error_message_unit, 'units': ''})

            return render(request, 'ConnectionRegion/update_region.html',
                          {'region_form': region_form, 'error_messages': '', 'units': ''})
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
