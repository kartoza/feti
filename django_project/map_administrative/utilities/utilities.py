# -*- coding: UTF-8 -*-
from django.contrib.gis import geos

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '12/01/17'


def simplify_polygon_geometry_of_boundary(Boundary):
    """Simplify polygon geometry of boundary.

    This method will simplify polygon_geometry from boundary.
    Taking current polygon, simplify it and save simplified geometry.

    :param Boundary: Boundary Model that will be simplify
    :type Boundary: Boundary
    """
    TOLERANCE = 0.001  # tolerance for the Douglas-Peucker algorithm
    if hasattr(Boundary, 'polygon_geometry'):
        for boundary in Boundary.objects.all():
            new_geometry = boundary.polygon_geometry.simplify(tolerance=TOLERANCE)
            if new_geometry and isinstance(new_geometry, geos.Polygon):
                new_geometry = geos.MultiPolygon(new_geometry)
            boundary.polygon_geometry = new_geometry
            boundary.save()
