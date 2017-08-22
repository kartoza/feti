from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import MultiPolygon, Polygon
from django.core.management.base import BaseCommand
from map_administrative.models.province import Province
from map_administrative.models.district import District
from django.conf import settings


class Command(BaseCommand):
    help = 'Import districts'
    provinces = {
        'EC': 'Eastern Cape',
        'WC': 'Western Cape'
    }

    def handle(self, *args, **options):
        District.objects.all().delete()
        data_source = DataSource('map_administrative/data/district.shp')
        layer = data_source[0]
        for feature in layer:
            province_name = feature['PROVINCE'].value
            district_name = feature['DISTRICT_N'].value

            if province_name in self.provinces:

                if settings.ADMINISTRATIVE:
                    if self.provinces[province_name] != \
                            settings.ADMINISTRATIVE:
                        continue

                geometry = feature.geom

                try:
                    district = District.objects.get(name=district_name)
                except District.DoesNotExist:
                    district = District(name=district_name, )

                try:
                    if 'MultiPolygon' not in geometry.geojson:
                        geometry = MultiPolygon(
                            [Polygon(coords) for coords in
                             district.polygon_geometry.coords[0]] +
                            [Polygon(geometry.coords[0])]).geojson
                    else:
                        geometry = MultiPolygon(
                            [Polygon(coords) for coords in
                             district.polygon_geometry.coords[0]] +
                            [Polygon(coords) for coords in geometry.coords[0]]).geojson
                    district.polygon_geometry = geometry
                except:
                    if 'MultiPolygon' not in geometry.geojson:
                        geometry = MultiPolygon(Polygon(geometry.coords[0])).geojson
                    else:
                        geometry = geometry.geojson
                    district.polygon_geometry = geometry

                try:
                    province = Province.objects.get(name=self.provinces[province_name])
                    district.province = province
                    district.save()
                except:
                    pass

        print("Done")
