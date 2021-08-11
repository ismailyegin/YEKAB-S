import traceback

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from ekabis.services import general_methods
from ekabis.services.general_methods import get_error_messages
from ekabis.services.services import SettingsService, SettingsGetService
from ekabis.Forms.SettingsForm import SettingsForm

# Sistem ayarlarının listelendigi sayfa
@login_required
def view_settinsList(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    setting = SettingsService(request, None)
    return render(request, 'Ayar/ayarlistesi.html',
                  {'settings': setting})


@login_required
def change_serttings(request, pk):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        setting_filter = {
            'pk': pk
        }
        setting = SettingsGetService(request, setting_filter) if SettingsService(request, setting_filter) else None
        settings_form = SettingsForm(request.POST or None, instance=setting)
        if request.method == 'POST':
            if settings_form.is_valid():
                settings_form.save()
                messages.success(request, 'Ayarlar Güncellenmiştir.')
                return redirect('ekabis:view_settings')

            else:
                error_messages = get_error_messages(settings_form)
                return render(request, 'Ayar/ayarguncelle.html',
                              {'settings_form': settings_form, 'error_messages': error_messages
                               })

        return render(request, 'Ayar/ayarguncelle.html',
                      {'settings_form': settings_form, 'error_messages': ''
                       })

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')

