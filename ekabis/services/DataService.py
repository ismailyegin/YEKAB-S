import traceback

from django.shortcuts import redirect

from ekabis.models import City, Neighborhood, BusinessBlog, BusinessBlogParametreType
from ekabis.models.District import District
import pandas

def add_city():
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
        return redirect('ekabis:initial_data_error_page')


def add_district():
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
        return redirect('ekabis:initial_data_error_page')


def add_neighborhood():
    try:

        df = pandas.read_csv('neighborhoods.csv')
        for value in df.values:
            neighborhood_name = value[0].split(';')[3].split('->')[0]
            district_name = value[0].split(';')[5].split('->')[1].split(' ')[1]
            city_name = value[0].split(';')[5].split('->')[0].strip()
            print(city_name)
            print(district_name)
            print(neighborhood_name)
          
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
        return redirect('ekabis:initial_data_error_page')


def data_business_blog():
    try:

        df = pandas.read_csv('business_blocks.csv')
        for value in df.values:
            name = value[0]
            block = BusinessBlog(name=name)
            block.save()
        return redirect('ekabis:initial_data_success_page')

    except Exception as e:
        traceback.print_exc()
        return redirect('ekabis:initial_data_success_page')


def data_parameter():
    try:

        df = pandas.read_csv('parameter.csv')
        for value in df.values:
            data = value[0].split(';')
            block = BusinessBlogParametreType(title=data[0], type=data[1].split('"')[1])
            block.save()
        return redirect('ekabis:initial_data_success_page')

    except Exception as e:
        traceback.print_exc()
        return redirect('ekabis:initial_data_error_page')


def data_parameter_block_id():
    try:

        df = pandas.read_csv('block_parametre_id.csv')
        for value in df.values:
            data = value[0].split(';')
            block = BusinessBlog.objects.get(pk=int(data[0]))
            parametre = BusinessBlogParametreType.objects.get(pk=int(data[1]))
            block.parametre.add(parametre)
            block.save()
        return redirect('ekabis:initial_data_success_page')

    except Exception as e:
        traceback.print_exc()
        return redirect('ekabis:initial_data_error_page')
