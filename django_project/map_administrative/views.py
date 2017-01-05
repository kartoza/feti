from rest_framework.response import Response

from .models import Province, Country, District, Municipality
from .serializers.country_serializer import CountrySerializer
from .serializers.province_serializer import ProvinceSerializer
from .serializers.district_serializer import DistrictSerializer
from .serializers.municipality_serializer import MunicipalitySerializer
from rest_framework.views import APIView

ALLOWED_COUNTRIES = ["South Africa"]


def get_boundary(administrative):
    boundary = None
    if (administrative):
        administratives = administrative.split(",")
        index = 0
        try:
            for administrative in administratives:
                if index == 0:
                    if administrative in ALLOWED_COUNTRIES:
                        boundary = Country.objects.get(name=administrative)
                elif index == 1:
                    boundary = Province.objects.get(name=administrative, country=boundary)
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
                        if country.name in ALLOWED_COUNTRIES:
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
                elif layer == 'district':
                    try:
                        district = District.objects.get(polygon_geometry__contains=point)
                        serializer = DistrictSerializer(district)
                        return Response(serializer.data)
                    except District.DoesNotExist:
                        pass
                elif layer == 'municipality':
                    try:
                        municipality = Municipality.objects.get(polygon_geometry__contains=point)
                        serializer = MunicipalitySerializer(municipality)
                        return Response(serializer.data)
                    except Municipality.DoesNotExist:
                        pass
            else:
                boundary = get_boundary(request.GET.get('administrative'))
                if boundary:
                    if type(boundary) == Country:
                        serializer = CountrySerializer(boundary)
                        return Response(serializer.data)
                    elif type(boundary) == Province:
                        serializer = ProvinceSerializer(boundary)
                        return Response(serializer.data)

        return Response({})
