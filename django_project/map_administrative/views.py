from rest_framework.response import Response

from .models import Province, Country
from .serializers.country_serializer import CountrySerializer
from .serializers.province_serializer import ProvinceSerializer
from rest_framework.views import APIView


def get_boundary(administrative):
    boundary = None
    if (administrative):
        administratives = administrative.split(",")
        index = 0
        try:
            for administrative in administratives:
                if index == 0:
                    boundary = Country.objects.get(name=administrative)
                    print(administrative)
                elif index == 1:
                    boundary = Province.objects.get(name=administrative, country=boundary)
                    print(administrative)
                index += 1
        except Country.DoesNotExist:
            pass
        except Province.DoesNotExist:
            pass

    return boundary


class GetAdministrative(APIView):
    def get(self, request, format=None):
        if request.method == "GET":
            lat = request.GET.get('lat')
            lng = request.GET.get('lng')
            layer = request.GET.get('layer')

            if lat and lng:
                point = 'POINT(' + lng + ' ' + lat + ')'
                if layer == 'country':
                    try:
                        country = Country.objects.get(polygon_geometry__contains=point)
                        serializer = CountrySerializer(country)
                        return Response(serializer.data)
                    except Country.DoesNotExist:
                        pass
                elif layer == 'province':
                    try:
                        province = Province.objects.get(polygon_geometry__contains=point)
                        serializer = ProvinceSerializer(province)
                        return Response(serializer.data)
                    except Country.DoesNotExist:
                        pass
            else:
                boundary = get_boundary(request.GET.get('administrative'))
                if boundary:
                    print(type(boundary))
                    if type(boundary) == Country:
                        print(type(boundary))
                        serializer = CountrySerializer(boundary)
                        return Response(serializer.data)
                    elif type(boundary) == Province:
                        print(type(boundary))
                        serializer = ProvinceSerializer(boundary)
                        return Response(serializer.data)

        return Response({})
