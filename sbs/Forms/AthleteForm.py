from django import forms
from django.forms import ModelForm

from sbs.models import Athlete
class AthleteForm(ModelForm):
    class Meta:
        model = Athlete
