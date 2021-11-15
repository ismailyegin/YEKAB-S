from datetime import datetime, timedelta
from django.contrib.auth import logout
from django.shortcuts import redirect

from ekabis.models.Settings import Settings


class AutoLogout(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated is True:

            try:
                time = float(Settings.objects.get(key='logout_time').value)
                if datetime.now() - request.session['last_touch'] > timedelta(0, time * 60, 0):
                    del request.session['last_touch']
                    logout(request)
                    return redirect('accounts:login')

            except KeyError:
                pass

            request.session['last_touch'] = datetime.now()

        response = self.get_response(request)
        return response
