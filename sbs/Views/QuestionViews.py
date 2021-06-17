from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from sbs.models.Question import Question
from sbs.Forms.QuestionsForm import QuestionsForm
from sbs.services import general_methods


@login_required
def soru_goster(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    questions = Question.objects.filter(isActiv=True).order_by('count')

    return render(request, 'Soru/Sorular.html',
                  {'questions': questions})


@login_required
def soru_update(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    questions = Question.objects.get(pk=pk)
    form = QuestionsForm(request.POST or None, instance=questions)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Soru-Cevap Başari ile Güncellenmiştir.')
            return redirect('sbs:soru-ekle')
        else:
            messages.warning(request, 'Alanlari kontrol ediniz')

    return render(request, 'Soru/soru-guncelle.html',
                  {'form': form})


@login_required
def soru_ekle(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    form = QuestionsForm()

    questions = Question.objects.all()

    if request.method == 'POST':
        form = QuestionsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Soru-Cevap Başari ile eklenmiştir.')
            return redirect('sbs:sorular')
        else:
            messages.warning(request, 'Alanlari kontrol ediniz')

    return render(request, 'Soru/Soru-ekle.html',
                  {'form': form, 'questions': questions})


@login_required
def categoryItemDelete(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = Question.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except CategoryItem.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
