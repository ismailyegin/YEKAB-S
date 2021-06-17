from django.forms import ModelForm

from sbs.models import Judge


class JudgeForm(ModelForm):
    class Meta:
        model = Judge
