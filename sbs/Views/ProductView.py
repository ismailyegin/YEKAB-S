from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render

from sbs.Forms.ProductForm import ProductForm
from sbs.Forms.DepositForm import DepositForm
from sbs.models.Deposit import Deposit
from sbs.models.Products import Products
from sbs.services import general_methods

from sbs.Forms.DepositSearchForm import DepositSearchForm

from datetime import timedelta, datetime

from sbs.Forms.ProductSearchForm import ProductSearchForm

@login_required
def add_product(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    product_form = ProductForm()
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, 'Ürün  Başarıyla Eklenmiştir.')
            return redirect('sbs:urunler')
    return render(request, 'product/urunEkle.html', {'product_form': product_form})


@login_required
def return_products(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    search_form = ProductSearchForm(request.POST or None)
    products = Products.objects.none()
    if request.method == 'POST':
        if search_form.is_valid():
            name = request.POST.get('name')
            print(name)
            suppeliers = request.POST.get('suppeliers')
            category = search_form.cleaned_data['category']
            description = request.POST.get('description')
            if name or suppeliers or category or description:
                query = Q()
                if name:
                    query &= Q(name=name)
                if suppeliers:
                    query &= Q(suppeliers__icontains=suppeliers)
                if description:
                    query &= Q(description__icontains=description)
                if category:
                    query &= Q(category=category)
                products = Products.objects.filter(query).distinct()
            else:
                products = Products.objects.all()
    return render(request, 'product/urunler.html', {'products': products, 'search_form': search_form})


@login_required
def product_delete(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():


        try:
            obj = Products.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def product_update(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    product = Products.objects.get(pk=pk)
    product_form = ProductForm(request.POST or None, instance=product)
    if request.method == 'POST':

        if product_form.is_valid():
            product_form.save()

            log = str(request.POST.get('name')) + " ürün guncelledi"
            log = general_methods.logwrite(request, request.user, log)

            messages.success(request, 'Ürün  Başarıyla Güncellenmiştir.')

            return redirect('sbs:urunler')
        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'product/urunDuzenle.html',
                  {'product_form': product_form})


@login_required
def add_product_deposit(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    product_form = DepositForm()
    if request.method == 'POST':
        product_form = DepositForm(request.POST)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, 'Emanet   Başarıyla Eklenmiştir.')
            return redirect('sbs:urunler-emanet')
    return render(request, 'product/emanetEkle.html', {'product_form': product_form})


@login_required
def return_products_deposit(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    # comquery = CompetitionSearchForm()
    products = Deposit.objects.none()
    search = DepositSearchForm(request.POST or None)

    if request.method == 'POST':
        product = request.POST.get('product')
        club = request.POST.get('club')
        date = request.POST.get('date')

        if date:
            date = datetime.strptime(date, "%d/%m/%Y").date()

        if product or club or date:
            query = Q()
            if product:
                query &= Q(product__in=product)
            if club:
                query &= Q(club__in=club)
            if date:
                query &= Q(date=date)

            products = Deposit.objects.filter(query).distinct()
        else:
            products = Deposit.objects.all()
    return render(request, 'product/emanetler.html', {'search_form': search, 'products': products})


@login_required
def product_delete_deposit(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():

        try:
            obj = Deposit.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def product_update_deposit(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    product = Deposit.objects.get(pk=pk)
    product_form = DepositForm(request.POST or None, instance=product)
    if request.method == 'POST':

        if product_form.is_valid():
            product_form.save()

            log = str(request.POST.get('name')) + " ürün emanet  guncelledi"
            log = general_methods.logwrite(request, request.user, log)

            messages.success(request, 'Ürün  Başarıyla Güncellenmiştir.')

            return redirect('sbs:urunler-emanet')
        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'product/emanetDuzenle.html',
                  {'product_form': product_form})
