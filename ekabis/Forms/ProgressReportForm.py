from django import forms

from ekabis.Forms.BaseForm import BaseForm
from ekabis.models.ProgressReport import ProgressReport


class ProgressReportForm(BaseForm):
    class Meta:
        model = ProgressReport
        fields = ('definition','reportFile',)
        labels = {'definition': 'Açıklama',
                  'reportFile': 'İlerleme Raporu',
                  }
        widgets = {
            'definition': forms.TextInput(
                attrs={'class': 'form-control '}),

        }