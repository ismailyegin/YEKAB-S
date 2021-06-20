from datetime import timedelta, datetime

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from sbs.services import general_methods

from django.core.mail import BadHeaderError, send_mail


def help(request):
    if request.method == 'POST':
        user = request.user
        konu = request.POST['konu']
        icerik = request.POST['icerik']
        if konu and icerik:
            try:
                konu = "[" + user.email + "] - " + konu
                send_mail(konu, icerik, 'taekwondo@kobiltek.com', ['fatih@kobiltek.com'])
                messages.success(request, 'Yardım ve Destek talebi basari ile gönderilmistir.')
            except BadHeaderError:
                # print('Invalid header found.')
                messages.warning(request, 'Alanları Kontrol Ediniz Bir Şeyler Ters Gitti')
    return render(request, 'help/Help.html')
