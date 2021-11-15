import json

from django import forms
from django.core import serializers

from ekabis.services.general_methods import log


class BaseForm(forms.ModelForm):

    def save(self, request, *args, **kwargs):
        model = self._meta.model
        x = log(request)
        data_as_json_pre = serializers.serialize('json', model.objects.filter(pk=self.instance.pk))
        x.previousData = data_as_json_pre
        super().save()
        data_as_json_next = serializers.serialize('json', model.objects.filter(pk=self.instance.pk))
        x.nextData = data_as_json_next
        x.save()
        return super().save()
