import traceback

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db import transaction
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import resolve

from ekabis.Forms.ConnectionRegionForm import ConnectionRegionForm
from ekabis.Forms.ConnectionUnitForm import ConnectionUnitForm
from ekabis.models import YekaCompetition, Permission, Logs
from ekabis.models.ConnectionRegion import ConnectionRegion
from ekabis.models.ConnectionUnit import ConnectionUnit
from ekabis.services import general_methods
from ekabis.services.general_methods import get_error_messages, get_client_ip
from ekabis.services.services import UnitService, ConnectionUnitGetService, \
    ConnectionRegionGetService, YekaGetService, CityService, CityGetService, last_urls


@login_required
def return_connectionRegionUnit(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    unit_form = ConnectionUnitForm()

    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        with transaction.atomic():
            if request.method == 'POST':

                unit_form = ConnectionUnitForm(request.POST)

                if unit_form.is_valid():

                    unit = unit_form.save(request,commit=False)
                    unit.save()


                    messages.success(request, 'Birim Başarıyla Kayıt Edilmiştir.')
                    return redirect('ekabis:view_units')

                else:
                    error_message_unit = get_error_messages(unit_form)
                    unitfilter = {
                        'isDeleted': False
                    }
                    units = UnitService(request, unitfilter)
                    return render(request, 'ConnectionRegion/add_unit.html',
                                  {'unit_form': unit_form, 'units': units, 'error_messages': error_message_unit,'urls': urls, 'current_url': current_url, 'url_name': url_name})
            unitfilter = {
                'isDeleted': False
            }
            units = UnitService(request, unitfilter)
            return render(request, 'ConnectionRegion/add_unit.html',
                          {'unit_form': unit_form, 'units': units, 'error_messages': '','urls': urls, 'current_url': current_url, 'url_name': url_name})

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
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        with transaction.atomic():
            if request.method == 'POST':

                if unit_form.is_valid():
                    unit=unit_form.save(request,commit=False)
                    unit.name = unit_form.cleaned_data['name']
                    unit.save()
                    messages.success(request, 'Başarıyla Güncellendi')
                    return redirect('ekabis:view_units')
                else:
                    error_message_unit = get_error_messages(unit_form)
                    return render(request, 'ConnectionRegion/update_unit.html',
                                  {'unit_form': unit_form, 'error_messages': error_message_unit, 'units': '','urls': urls, 'current_url': current_url, 'url_name': url_name})

            return render(request, 'ConnectionRegion/update_unit.html',
                          {'unit_form': unit_form, 'error_messages': '', 'units': '','urls': urls, 'current_url': current_url, 'url_name': url_name})
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
@login_required
def return_connectionRegion(request,uuid):
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)

    yeka_filter = {
        'uuid': uuid,
        'isDeleted': False,
    }
    yeka = YekaGetService(request, yeka_filter)
    regions = yeka.connection_region.filter(isDeleted=False)
    return render(request, 'ConnectionRegion/view_connection_region.html',
                  { 'regions': regions, 'error_messages': '', 'yeka': yeka, 'urls': urls,
                   'current_url': current_url, 'url_name': url_name})

@login_required
def add_connectionRegion(request,uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    region_form = ConnectionRegionForm()


    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)

        yeka_filter={
            'uuid' :uuid,
            'isDeleted' : False,
        }
        yeka=YekaGetService(request,yeka_filter)
        with transaction.atomic():

            if request.method == 'POST':

                region_form = ConnectionRegionForm(request.POST)

                if region_form.is_valid():
                    region = region_form.save(request,commit=False)
                    total = int(
                        ConnectionRegion.objects.filter(yeka=yeka).distinct().aggregate(Sum('capacity'))[
                            'capacity__sum'] or 0)
                    total +=region.capacity

                    if yeka.capacity<total:
                        messages.warning(request, 'Bölgelerin Kapasite  toplamı Yekanın Kapasitesinden büyük olamaz')

                        return render(request, 'ConnectionRegion/add_connectionRegion.html',
                                      {'region_form': region_form, 'yeka': yeka,'urls': urls, 'current_url': current_url, 'url_name': url_name,
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


                    messages.success(request, 'Bölge Başarıyla Kayıt Edilmiştir.')
                    return redirect('ekabis:view_yeka_detail' ,yeka.uuid)

                else:
                    error_message_region = get_error_messages(region_form)

                    return render(request, 'ConnectionRegion/add_connectionRegion.html',
                                  {'region_form': region_form, 'yeka':yeka, 'error_messages': error_message_region,'urls': urls, 'current_url': current_url, 'url_name': url_name})
            regionfilter = {
                'isDeleted': False

            }
            name=general_methods.yekaname(yeka.business)
            return render(request, 'ConnectionRegion/add_connectionRegion.html',
                          {'region_form': region_form, 'error_messages': '', 'yeka':yeka,'urls': urls,
                           'current_url': current_url, 'url_name': url_name,'name':name})

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, e)
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
                    'uuid': uuid,
                }
                obj = ConnectionRegionGetService(request, regionfilter)
                data_as_json_pre = serializers.serialize('json', ConnectionRegion.objects.filter(uuid=uuid))

                if obj:
                    if obj.yekacompetition.count() > 0:
                        return JsonResponse(
                            {'status': 'Fail', 'msg': 'Bölge için tanımlanmış yarışmalar  var. Bölge silinemez'})
                    else:
                        log = "Bölge Sil"
                        logs = Logs(user=request.user, subject=log, ip=get_client_ip(request),
                                    previousData=data_as_json_pre)
                        obj.isDeleted = True
                        obj.save()
                        logs.save()
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
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
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
        with transaction.atomic():
            if request.method == 'POST':

                if region_form.is_valid():
                    region = region_form.save(request,commit=False)
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
                    return redirect('ekabis:view_yeka_detail' ,yeka.uuid)
                else:
                    error_message_unit = get_error_messages(region_form)
                    return render(request, 'ConnectionRegion/update_region.html',
                                  {'region_form': region_form, 'error_messages': error_message_unit, 'units': '','urls': urls, 'current_url': current_url, 'url_name': url_name})

            return render(request, 'ConnectionRegion/update_region.html',
                          {'region_form': region_form, 'error_messages': '', 'units': '','urls': urls, 'current_url': current_url, 'url_name': url_name})
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, e)
        return redirect('ekabis:view_yeka')

