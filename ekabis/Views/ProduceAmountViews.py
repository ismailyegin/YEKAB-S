import traceback

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import resolve

from ekabis.Forms.ProduceAmountForm import ProduceAmountForm
from ekabis.models import Permission, BusinessBlog, YekaProduceAmount, YekaBusinessBlog, YekaBusiness, YekaCompetition, \
    ProduceAmount, Logs, YekaPurchaseGuarantee
from ekabis.models.Competition import Competition
from ekabis.services import general_methods
from ekabis.services.NotificationServices import notification
from ekabis.services.general_methods import get_error_messages, get_client_ip
from ekabis.services.services import last_urls, YekaBusinessBlogGetService, BusinessBlogGetService, \
    YekaBusinessGetService


# Add Production Quantity where Purchase Guarantee is "Quantity"
@login_required
def add_produce_amount(request, yeka_business_uuid, yeka_business_block_uuid):
    form = ProduceAmountForm()
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        filter = {
            'uuid': yeka_business_uuid
        }
        yeka_business = YekaBusinessGetService(request, filter)
        filter = {
            'uuid': yeka_business_block_uuid
        }
        name = general_methods.yekaname(yeka_business)

        yeka_business_block = YekaBusinessBlogGetService(request, filter)
        yeka_produce_amount = YekaProduceAmount.objects.get(yekabusinessblog=yeka_business_block)
        total = 0
        for amount in yeka_produce_amount.amount.all():
            total = total + amount
        if YekaPurchaseGuarantee.objects.filter(business=yeka_business):
            purchase_guarantee = YekaPurchaseGuarantee.objects.get(business=yeka_business)
        else:
            purchase_guarantee = 0
        competition = YekaCompetition.objects.get(business=yeka_business)
        if YekaPurchaseGuarantee.objects.get(business=yeka_business).type=='Süre' or YekaPurchaseGuarantee.objects.get(business=yeka_business).type ==None:
            messages.warning(request, 'Alım garantisi süre seçilmiştir.')
            return redirect('ekabis:view_yeka_competition_detail', competition.uuid)
        if request.method == 'POST':
            with transaction.atomic():
                form = ProduceAmountForm(request.POST)
                if not purchase_guarantee ==0:
                    if purchase_guarantee.total_quantity:
                        if total<purchase_guarantee.total_quantity:
                            if form.is_valid():
                                produce_amount = form.save(request, commit=False)
                                produce_amount.save()
                                yeka_produce_amount.save()
                                yeka_produce_amount.amount.add(produce_amount)
                                yeka_produce_amount.save()

                                url = redirect('ekabis:view_yeka_competition_detail', competition.uuid).url
                                html = '<a style="" href="' + url + '"> ID : ' + str(competition.pk) + ' - ' + str(
                                    competition.name) + '</a> adlı YEKA yarışmasına ait  ' + str(yeka_produce_amount.pk) + ' id li üretim miktarı bilgileri eklendi.'
                                notification(request, html, competition.uuid, 'yeka_competition')

                                messages.success(request, 'Üretim Miktarı Başarıyla  Eklenmiştir.')
                                return redirect('ekabis:view_yeka_competition_detail', competition.uuid)
                            else:
                                error_messages = get_error_messages(form)
                                return render(request, 'ProduceAmount/add_produce_amount.html', {'form': form,
                                                                                                 'error_messages': error_messages,
                                                                                                 'urls': urls,
                                                                                                 'current_url': current_url,
                                                                                                 'url_name': url_name
                                                                                                 })
                        else:
                            messages.success(request, 'Toplam üretim miktarına ulaşıldığı için yeni bir miktar eklenememektedir.')
                            return redirect('ekabis:view_yeka_competition_detail', competition.uuid)
                    else:
                        messages.warning(request, 'Üretim miktarı girilmemiştir.')
                        return redirect('ekabis:view_yeka_competition_detail', competition.uuid)
        return render(request, 'ProduceAmount/add_produce_amount.html', {'form': form,
                                                                         'error_messages': '', 'urls': urls,
                                                                         'current_url': current_url,
                                                                         'url_name': url_name,'competition':name,
                                                                         })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')

# added production quantities for the work block
@login_required
def view_business_block_produce_amount(request, yeka_business_uuid, yeka_business_block_uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        filter = {
            'uuid': yeka_business_uuid
        }
        yeka_business = YekaBusinessGetService(request, filter)
        filter = {
            'uuid': yeka_business_block_uuid
        }


        yeka_business_block = YekaBusinessBlogGetService(request, filter)
        competition=YekaCompetition.objects.get(business=yeka_business)
        name = general_methods.yekaname(yeka_business)

        if YekaProduceAmount.objects.filter(yekabusinessblog=yeka_business_block):
            produce_amount = YekaProduceAmount.objects.get(business=yeka_business).amount.filter(
                isDeleted=False)
        else:
            produce_amount = YekaProduceAmount()
            produce_amount.business = yeka_business
            produce_amount.yekabusinessblog = yeka_business_block
            produce_amount.save()

        return render(request, 'ProduceAmount/view_produce_amount.html',
                      {'produce_amounts': produce_amount, 'yeka_business_uuid': yeka_business.uuid,
                       'yeka_business_block_uuid': yeka_business_block.uuid,
                       'urls': urls,'competition':name,
                       'current_url': current_url,
                       'url_name': url_name})
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')

# update the production quantities added for the work block
@login_required
def change_produce_amount(request, uuid, yeka_business_uuid):
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        produce_amount = ProduceAmount.objects.get(uuid=uuid)
        yeka_produce_amount=YekaProduceAmount.objects.get(amount=produce_amount)
        form = ProduceAmountForm(request.POST or None, instance=produce_amount)

        if request.method == 'POST':
            with transaction.atomic():

                if form.is_valid():

                    produce_amount = form.save(request, commit=False)
                    produce_amount.save()

                    filter = {
                        'uuid': yeka_business_uuid
                    }
                    yeka_business = YekaBusinessGetService(request, filter)

                    competition = YekaCompetition.objects.get(business=yeka_business)
                    messages.success(request, 'Üretim Miktarı Başarıyla  Güncellenmiştir.')
                    url = redirect('ekabis:view_yeka_competition_detail', competition.uuid).url
                    html = '<a style="" href="' + url + '"> ID : ' + str(competition.pk) + ' - ' + str(
                        competition.name) + '</a> adlı YEKA yarışmasına ait  ' + str(
                        yeka_produce_amount.pk) + ' id li üretim miktarı bilgileri güncellendi.'
                    notification(request, html, competition.uuid, 'yeka_competition')
                    return redirect('ekabis:view_yeka_competition_detail', competition.uuid)
                else:
                    error_messages = get_error_messages(form)
                    return render(request, 'ProduceAmount/add_produce_amount.html', {'form': form,
                                                                                     'error_messages': error_messages,
                                                                                     'urls': urls,
                                                                                     'current_url': current_url,
                                                                                     'url_name': url_name
                                                                                     })

        return render(request, 'ProduceAmount/add_produce_amount.html', {'form': form,
                                                                         'error_messages': '', 'urls': urls,
                                                                         'current_url': current_url,
                                                                         'url_name': url_name
                                                                         })
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_yeka')

# deletion of production quantity
@login_required
def delete_produce_amount(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']

                obj = ProduceAmount.objects.get(uuid=uuid)
                yeka_produce_amount = YekaProduceAmount.objects.get(amount=obj)
                data_as_json_pre = serializers.serialize('json', ProduceAmount.objects.filter(uuid=uuid))

                obj.isDeleted = True
                obj.save()
                yeka_produce_amount.isDeleted = True
                yeka_produce_amount.save()
                log = str(obj.id) + " - üretim miktarı silindi."
                logs = Logs(user=request.user, subject=log, ip=get_client_ip(request), previousData=data_as_json_pre)
                logs.save()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

    except obj.DoesNotExist:
        traceback.print_exc()
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})
