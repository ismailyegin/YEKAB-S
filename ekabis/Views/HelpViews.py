import traceback
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect
from django.core.mail import BadHeaderError, send_mail


def help(request):
    try:
        with transaction.atomic():
            if request.method == 'POST':

                user = request.user
                konu = request.POST['konu']
                icerik = request.POST['icerik']
                if konu and icerik:
                    try:
                        konu = "[" + user.email + "] - " + konu
                        send_mail(konu, icerik, 'ekabis@kobiltek.com', ['fatih@kobiltek.com'])
                        messages.success(request, 'Yardım ve Destek talebi basari ile gönderilmistir.')
                    except BadHeaderError:
                        # print('Invalid header found.')
                        messages.warning(request, 'Alanları Kontrol Ediniz Bir Şeyler Ters Gitti')

            return render(request, 'Yardim/Help.html')
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
