from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import MultiPolygon, Polygon
from django.core.management.base import BaseCommand
from map_administrative.models.municipality import Municipality
from map_administrative.models.district import District


class Command(BaseCommand):
    help = 'Import municipalities'

    def handle(self, *args, **options):
        Municipality.objects.all().delete()
        data_source = DataSource('map_administrative/data/municipalities.shp')
        layer = data_source[0]
        for feature in layer:
            district_name = feature['district_n'].value
            municipality_name = feature['municname'].value

            geometry = feature.geom

            try:
                district = District.objects.get(name=district_name)
            except District.DoesNotExist:
                continue

            try:
                municipality = Municipality.objects.get(name=municipality_name)
            except Municipality.DoesNotExist:
                municipality = Municipality(name=municipality_name, )

            try:
                if 'MultiPolygon' not in geometry.geojson:
                    geometry = MultiPolygon(
                        [Polygon(coords) for coords in
                         municipality.polygon_geometry.coords[0]] +
                        [Polygon(geometry.coords[0])]).geojson
                else:
                    geometry = MultiPolygon(
                        [Polygon(coords) for coords in
                         municipality.polygon_geometry.coords[0]] +
                        [Polygon(coords) for coords in geometry.coords[0]]).geojson
                municipality.polygon_geometry = geometry
            except:
                if 'MultiPolygon' not in geometry.geojson:
                    geometry = MultiPolygon(Polygon(geometry.coords[0])).geojson
                else:
                    geometry = geometry.geojson
                municipality.polygon_geometry = geometry

            municipality.district = district
            municipality.save()

        print("Done")
