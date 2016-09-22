# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'Christian Christelis <christian@kartoza.com>'
__project_name = 'watchkeeper'
__date__ = '8/05/15'
__copyright__ = 'kartoza.com'
__doc__ = ''

from django.db import models, migrations

from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import MultiPolygon, Polygon


def import_countries(apps, schema_editor):
    data_source = DataSource('map_administrative/data/ne_10m_admin_0_countries.shp')
    Country = apps.get_model("map_administrative", "Country")
    layer = data_source[0]
    for feature in layer:
        country_name = feature['NAME'].value
        geometry = feature.geom
        try:
            country = Country.objects.get(name=country_name)
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
            country = Country(name=country_name, )
            country.polygon_geometry = geometry
        country.save()

    data_source = DataSource(
        'map_administrative/data/ne_10m_admin_1_states_provinces.shp')
    Province = apps.get_model("map_administrative", "Province")
    Country = apps.get_model("map_administrative", "Country")
    layer = data_source[0]
    for feature in layer:
        province_name = feature['NAME'].value
        country_name = feature['ADMIN'].value
        geometry = feature.geom
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


class Migration(migrations.Migration):
    dependencies = [
        ('map_administrative', '0002_province'),
    ]

    operations = [
        migrations.RunPython(import_countries),
    ]
