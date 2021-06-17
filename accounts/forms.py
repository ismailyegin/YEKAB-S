from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.models import Permission


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'text', 'id': 'username'}))
    password = forms.CharField(label="Password", max_length=30, widget=forms.TextInput(
        attrs={'class': 'mdl-textfield__input', 'type': 'password', 'id': 'password'}))


class PermForm(forms.Form):
    permission = forms.ModelMultipleChoiceField(queryset=Permission.objects.all(),
                                                widget=FilteredSelectMultiple("Permission", False, attrs={'rows': '2'}))

    class Media:
        css = {'all': ('/static/admin/css/widgets.css',), }
        js = ('/admin/jsi18n/',)
