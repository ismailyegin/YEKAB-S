import traceback

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import resolve

from ekabis.Forms.HelpMenuForm import HelpMenuForm
from ekabis.models import Permission, HelpMenu
from ekabis.services import general_methods
from ekabis.services.general_methods import get_error_messages, log_model
from ekabis.services.services import last_urls, HelpMenuGetService


@login_required
def help_text_add(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    help_form = HelpMenuForm()
    perms = Permission.objects.all()
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        with transaction.atomic():
            if request.method == 'POST':

                help_form = HelpMenuForm(request.POST)
                if help_form.is_valid():
                    help = help_form.save(request, commit=False)
                    help.save()
                    messages.success(request, 'Yardım Metni Eklendi.')
                    return redirect('ekabis:view_help_text')
                else:
                    error_messages = get_error_messages(help_form)

                    return render(request, 'helpMenu/add_help_text.html',
                                  {'help_form': help_form, 'error_messages': error_messages, 'perms': perms})
            return render(request, 'helpMenu/add_help_text.html',
                          {'help_form': help_form, 'perms': perms, 'error_messages': '', 'urls': urls,
                           'current_url': current_url,
                           'url_name': url_name})

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')


@login_required
def return_help_text(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    urls = last_urls(request)
    current_url = resolve(request.path_info)
    url_name = Permission.objects.get(codename=current_url.url_name)

    help_texts = HelpMenu.objects.filter(isDeleted=False)
    return render(request, 'helpMenu/view_help_text.html',
                  {'texts': help_texts, 'urls': urls, 'current_url': current_url, 'url_name': url_name})


@login_required
def update_help_menu(request, uuid):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    filter = {
        'uuid': uuid
    }
    help_text = HelpMenuGetService(request, filter)
    help_form = HelpMenuForm(request.POST or None, instance=help_text)
    try:
        urls = last_urls(request)
        current_url = resolve(request.path_info)
        url_name = Permission.objects.get(codename=current_url.url_name)
        with transaction.atomic():
            if request.method == 'POST':
                if help_form.is_valid():
                    help = help_form.save(request, commit=False)
                    help.save()
                    messages.success(request, 'Yardım Metni Güncellenmiştir')
                    return redirect('ekabis:view_help_text')
                else:
                    error_messages = get_error_messages(help_form)
                    return render(request, 'helpMenu/add_help_text.html',
                                  {'help_form': help_form,
                                   'error_messages': error_messages, 'urls': urls, 'current_url': current_url,
                                   'url_name': url_name
                                   })

            return render(request, 'helpMenu/add_help_text.html',
                          {'help_form': help_form, 'urls': urls, 'current_url': current_url,
                           'url_name': url_name, 'error_messages': ''})
    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:view_help_text')
