import traceback

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render

from ekabis.Forms.ConnectionCapacityForm import ConnectionCapacityForm
from ekabis.Forms.ConnectionRegionForm import ConnectionRegionForm
from ekabis.Forms.ConnectionUnitForm import ConnectionUnitForm
from ekabis.models import ConnectionRegion, ConnectionCapacity
from ekabis.models.ConnectionUnit import ConnectionUnit
from ekabis.services import general_methods
from ekabis.services.general_methods import get_error_messages
from ekabis.services.services import UnitService, RegionService, CapacityService


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
                obj = UnitService(request, unitfilter).first()
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

    unit = UnitService(request, unitfilter).first()
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
def return_connectionRegion(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    region_form = ConnectionRegionForm()

    try:
        with transaction.atomic():
            if request.method == 'POST':

                region_form = ConnectionRegionForm(request.POST)

                if region_form.is_valid():

                    region = ConnectionRegion(name=region_form.cleaned_data['name'],
                                              value=int(region_form.cleaned_data['value']),
                                              unit=region_form.cleaned_data['unit'])
                    region.save()

                    log = " Bölge eklendi"
                    log = general_methods.logwrite(request, request.user, log)
                    messages.success(request, 'Bölge Başarıyla Kayıt Edilmiştir.')
                    return redirect('ekabis:view_region')

                else:
                    error_message_region = get_error_messages(region_form)
                    unitfilter = {
                        'isDeleted': False
                    }
                    units = ConnectionRegion(request, unitfilter)
                    return render(request, 'ConnectionRegion/add_connectionRegion.html',
                                  {'region_form': region_form, 'units': units, 'error_messages': error_message_region})
            regionfilter = {
                'isDeleted': False
            }
            regions = RegionService(request, regionfilter)
            return render(request, 'ConnectionRegion/add_connectionRegion.html',
                          {'region_form': region_form, 'regions': regions, 'error_messages': ''})

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_region')


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
                obj = RegionService(request, regionfilter).first()
                region_capacities = ConnectionCapacity.objects.filter(connection_region=obj, isDeleted=False)
                if region_capacities:
                    return JsonResponse(
                        {'status': 'Fail', 'msg': 'Bölge için tanımlanmış kapasiteler var. Bölge silinemez'})
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
def update_region(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    regionfilter = {
        'uuid': uuid
    }

    region = RegionService(request, regionfilter).first()
    region_form = ConnectionRegionForm(request.POST or None, instance=region)
    try:
        with transaction.atomic():
            if request.method == 'POST':

                if region_form.is_valid():
                    region.name = region_form.cleaned_data['name']
                    region.value = region_form.cleaned_data['value']
                    region.unit = region_form.cleaned_data['unit']

                    region.save()

                    messages.success(request, 'Bölge Başarıyla Güncellendi')
                    return redirect('ekabis:view_region')
                else:
                    error_message_unit = get_error_messages(region_form)
                    return render(request, 'ConnectionRegion/update_region.html',
                                  {'region_form': region_form, 'error_messages': error_message_unit, 'units': ''})

            return render(request, 'ConnectionRegion/update_region.html',
                          {'region_form': region_form, 'error_messages': '', 'units': ''})
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')


@login_required
def return_connectionCapacity(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    capacities = ConnectionCapacity.objects.filter(connection_region__uuid=uuid, isDeleted=False)
    capacity_form = ConnectionCapacityForm()

    try:
        with transaction.atomic():
            if request.method == 'POST':
                capacity_form = ConnectionCapacityForm(request.POST)
                region = ConnectionRegion.objects.get(uuid=uuid)
                region_capacities = ConnectionCapacity.objects.filter(connection_region__uuid=uuid, isDeleted=False)

                if capacity_form.is_valid():

                    capacity_value = int(capacity_form.cleaned_data['value'])

                    total_capacity = 0
                    for capacity in region_capacities:
                        total_capacity = total_capacity + capacity.value
                    total_capacity = total_capacity + capacity_value
                    region_value = region.value

                    if region_value >= total_capacity:
                        capacity = ConnectionCapacity(name=capacity_form.cleaned_data['name'],
                                                      unit=capacity_form.cleaned_data['unit'],
                                                      value=capacity_value)
                        capacity.save()

                        capacity.connection_region = ConnectionRegion.objects.get(uuid=uuid)
                        capacity.save()

                        log = "Kapasite eklendi"
                        log = general_methods.logwrite(request, request.user, log)
                        messages.success(request, 'Kapasite Başarıyla Kayıt Edilmiştir.')
                        return redirect('ekabis:view_region')
                    else:
                        messages.warning(request, 'Kapasite toplam değeri bölge değerinden büyük olamaz.')
                else:
                    error_message_capacity = get_error_messages(capacity_form)
                    capacities = ConnectionCapacity.objects.filter(connection_region__uuid=uuid, isDeleted=False)

                    return render(request, 'ConnectionRegion/add-connectionCapacity.html',
                                  {'capacity_form': capacity_form, 'capacities': capacities,
                                   'error_messages': error_message_capacity})

            return render(request, 'ConnectionRegion/add-connectionCapacity.html',
                          {'capacity_form': capacity_form, 'capacities': capacities, 'error_messages': ''})

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_capacity')


@login_required
def update_capacity(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    capacityfilter = {
        'uuid': uuid
    }

    region_uuid = ConnectionCapacity.objects.get(uuid=uuid)

    capacity = CapacityService(request, capacityfilter).first()
    capacity_form = ConnectionCapacityForm(request.POST or None, instance=capacity)
    try:
        with transaction.atomic():
            if request.method == 'POST':

                capacity_form = ConnectionCapacityForm(request.POST)
                region_capacity = ConnectionCapacity.objects.get(uuid=uuid)
                region = region_capacity.connection_region
                region_capacities = ConnectionCapacity.objects.filter(connection_region=region, isDeleted=False)

                if capacity_form.is_valid():

                    capacity_value = int(capacity_form.cleaned_data['value'])

                    if len(region_capacities) > 1:
                        total = 0
                        for capacity in region_capacities.exclude(uuid=uuid):
                            total = total + capacity.value
                        total_capacity = total + capacity_value
                    else:
                        total_capacity = capacity_value

                    region_value = region.value

                    if region_value >= total_capacity:
                        capacity.value = capacity_form.cleaned_data['value']
                        capacity.name = capacity_form.cleaned_data['name']
                        capacity.unit = capacity_form.cleaned_data['unit']
                        capacity.save()

                        messages.success(request, 'Kapasite Başarıyla Güncellendi')
                        return redirect('ekabis:view_region')
                    else:
                        messages.warning(request,
                                         'Kapasite toplam değeri bölge değerinden büyük olamaz.Eklenen Toplam Kapasite: ' + str(
                                             total) + ' En fazla ' + str(region_value - total) + ' eklenebilir')

                else:
                    error_message_unit = get_error_messages(capacity_form)
                    return render(request, 'ConnectionRegion/update_capacity.html',
                                  {'capacity_form': capacity_form, 'error_messages': error_message_unit, })

            return render(request, 'ConnectionRegion/update_capacity.html',
                          {'capacity_form': capacity_form, 'error_messages': ''})
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')


@login_required
def delete_capacity(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']
                capacityfilter = {
                    'uuid': uuid
                }
                obj = CapacityService(request, capacityfilter).first()
                log = str(obj.name) + " Kapasite silindi"
                log = general_methods.logwrite(request, request.user, log)
                obj.isDeleted = True
                obj.save()

                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})


            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

    except obj.DoesNotExist:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})
