from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import MultiPolygon, Polygon
from django.core.management.base import BaseCommand
from map_administrative.models.country import Country
from map_administrative.models.province import Province


class Command(BaseCommand):
    help = 'Import countries'
    included_country = ["South Africa"]

    def handle(self, *args, **options):
        Country.objects.all().delete()
        Province.objects.all().delete()
        data_source = DataSource('map_administrative/data/ne_10m_admin_0_countries.shp')
        layer = data_source[0]
        for feature in layer:
            country_name = feature['NAME'].value
            if country_name in self.included_country:
                geometry = feature.geom
                try:
                    country = Country.objects.get(name=country_name)
                except Country.DoesNotExist:
                    country = Country(name=country_name, )

                try:
                    if 'MultiPolygon' not in geometry.geojson:
                        geometry = MultiPolygon(
                            [Polygon(coords) for coords in
                             country.geometry.coords[0]] +
                            [Polygon(geometry.coords[0])]).geojson
                    else:
                        geometry = MultiPolygon(
                            [Polygon(coords) for coords in
                             country.geometry.coords[0]] +
                            [Polygon(coords) for coords in geometry.coords[0]]).geojson
                    country.polygon_geometry = geometry
                except:
                    if 'MultiPolygon' not in geometry.geojson:
                        geometry = MultiPolygon(Polygon(geometry.coords[0])).geojson
                    else:
                        geometry = geometry.geojson
                    country.polygon_geometry = geometry
                country.save()
                break

        print("Processing provinces")

        data_source = DataSource(
            'map_administrative/data/ne_10m_admin_1_states_provinces.shp')
        layer = data_source[0]
        for feature in layer:
            province_name = feature['NAME'].value
            country_name = feature['ADMIN'].value
            geometry = feature.geom
            if country_name in self.included_country:
                try:
                    province = Province.objects.get(name=province_name)
                    if 'MultiPolygon' not in geometry.geojson:
                        geometry = MultiPolygon(
                            [Polygon(coords) for coords in
                             province.geometry.coords[0]] +
                            [Polygon(geometry.coords[0])]).geojson
                    else:
                        geometry = MultiPolygon(
                            [Polygon(coords) for coords in
                             province.geometry.coords[0]] +
                            [Polygon(coords) for coords in geometry.coords[0]]).geojson
                    province.polygon_geometry = geometry
                except:
                    if 'MultiPolygon' not in geometry.geojson:
                        geometry = MultiPolygon(Polygon(geometry.coords[0])).geojson
                    else:
                        geometry = geometry.geojson
                    province = Province(name=province_name, )
                    province.polygon_geometry = geometry
                try:
                    country = Country.objects.get(name=country_name)
                    province.country = country
                    province.save()
                except:
                    print("missing country %s " % country_name)
                    print("skipped province %s " % province_name)
                    pass
        print("Done")
