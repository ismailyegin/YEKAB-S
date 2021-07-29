from django.http import JsonResponse
from rest_framework.decorators import api_view

from ekabis.models.District import District
from ekabis.serializers.DistrictSerializer import DistrictSerializer


@api_view(http_method_names=['POST'])
def get_districts(request):
    if request.POST:
        try:

            il_id = request.POST.get('il_id')
            districts = District.objects.filter(city_id=il_id)

            data = DistrictSerializer(districts, many=True)

            responseData = dict()
            responseData['ilceler'] = data.data

            return JsonResponse(responseData, safe=True)

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})
