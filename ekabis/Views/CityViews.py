import traceback

import pandas
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from rest_framework.decorators import api_view

from ekabis.models import Neighborhood, City
from ekabis.models.District import District
from ekabis.serializers.DistrictSerializer import DistrictSerializer
from ekabis.serializers.NeighborhoodSerializer import NeighborhoodSerializer


# Fetch county by city id
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


# Fetch neighborhood by county id
@api_view(http_method_names=['POST'])
def get_neighborhood(request):
    if request.POST:
        try:

            ilce_id = request.POST.get('ilce_id')
            neighborhoods = Neighborhood.objects.filter(district=ilce_id)

            data = NeighborhoodSerializer(neighborhoods, many=True)

            responseData = dict()
            responseData['neighborhoods'] = data.data

            return JsonResponse(responseData, safe=True)

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


def add_city(request):
    import pandas
    try:

        df = pandas.read_csv('city.csv')
        for value in df.values:

            city_name = value[0].split(';')[1].split('"')[1]
            plateNo = value[0].split(';')[0]
            if not City.objects.filter(name=city_name):
                city = City(name=city_name, plateNo=plateNo)
                city.save()
        print('İller eklendi')
        return redirect('ekabis:initial_data_success_page')

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:initial_data_error_page')



def add_district(request):
    import pandas
    try:

        df = pandas.read_csv('district.csv')
        for value in df.values:
            district_name = value[0].split(';')[1].split('"')[1]
            city = City.objects.get(plateNo=value[0].split(';')[0])
            if not District.objects.filter(name=district_name, city=city):
                new = District(name=district_name, city=city)
                new.save()
        return redirect('ekabis:initial_data_success_page')

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:initial_data_error_page')



def add_neighborhood(request):
    import pandas
    try:

        df = pandas.read_csv('neighborhoods.csv')
        for value in df.values:
            neighborhood_name = value[0].split(';')[3].split('->')[0]
            district_name = value[0].split(';')[5].split('->')[1].split(' ')[1]
            city_name = value[0].split(';')[5].split('->')[0]
            city = City.objects.get(name=city_name)
            district = District.objects.filter(city=city, name=district_name)
            if district:
                if not Neighborhood.objects.filter(name=neighborhood_name, district=district[0]):
                    neighborhood = Neighborhood(name=neighborhood_name, district=district[0])
                    neighborhood.save()
            else:
                district = District.objects.filter(city=city, name='MERKEZ')
                if district:
                    if not Neighborhood.objects.filter(name=neighborhood_name, district=district[0]):
                        neighborhood = Neighborhood(name=neighborhood_name, district=district[0])
                        neighborhood.save()
                else:
                    new_district = District(city=city, name='MERKEZ')
                    new_district.save()
                    if not Neighborhood.objects.filter(name=neighborhood_name, district=new_district):
                        neighborhood = Neighborhood(name=neighborhood_name, district=new_district)
                        neighborhood.save()

        return redirect('ekabis:initial_data_success_page')

    except Exception as e:
        traceback.print_exc()
        messages.warning(request, 'Lütfen Tekrar Deneyiniz.')
        return redirect('ekabis:initial_data_error_page')


