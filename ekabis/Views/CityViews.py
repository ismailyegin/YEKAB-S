from django.http import JsonResponse
from rest_framework.decorators import api_view

from ekabis.models import Neighborhood
from ekabis.models.District import District
from ekabis.serializers.DistrictSerializer import DistrictSerializer
from ekabis.serializers.NeighborhoodSerializer import NeighborhoodSerializer


@api_view(http_method_names=['POST'])
def get_districts(request):
    if request.POST:
        try:

            il_id = request.POST.get('il_id')
            districts = District.objects.filter(city_id=il_id)

            data = DistrictSerializer(districts, many=True)

            responseData = dict()
            responseData['ilceler'] = data.data

            neighborhoods = Neighborhood.objects.filter(district=districts[0].id)

            data_neighborhood = NeighborhoodSerializer(neighborhoods, many=True)

            responseData['neighborhoods'] = data_neighborhood.data

            return JsonResponse(responseData, safe=True)

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})

@api_view(http_method_names=['POST'])
def get_neighborhood(request):
    if request.POST:
        try:

            ilce_id= request.POST.get('ilce_id')
            neighborhoods = Neighborhood.objects.filter(district=ilce_id)

            data = NeighborhoodSerializer(neighborhoods, many=True)

            responseData = dict()
            responseData['neighborhoods'] = data.data

            return JsonResponse(responseData, safe=True)

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})
