from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from ekabis.services import general_methods
from ekabis.services.services import SettingsService
from ekabis.Forms.SettingsForm import SettingsForm

@login_required
def view_settinsList(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    setting = SettingsService(request,None)[0]
    return render(request, 'Ayar/ayarlistesi.html',
                  {'settings': setting})
@login_required
def change_serttings(request, pk):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    groupfilter={
        'pk':pk
    }
    setting = SettingsService(request,groupfilter)[0] if SettingsService(request,groupfilter) else None
    settings_form = SettingsForm(request.POST or None, instance=setting)
    if request.method == 'POST':
        if settings_form.is_valid():
            settings_form.save()
            messages.success(request, 'Ayarlar Güncellenmiştir.')
            return redirect('ekabis:view_settings')

        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'Ayar/ayarguncelle.html',
                  {'settings_form': settings_form,
                   })


