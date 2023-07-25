import staticmaps

from landfall.points import add_points, add_point
from landfall.polygons import add_polygons, add_polygon


class Context(staticmaps.Context):
    def add_points(self, *args, **kwargs):
        add_points(self, *args, **kwargs)

    def add_point(self, *args, **kwargs):
        add_point(self, *args, **kwargs)

    def add_polygons(self, *args, **kwargs):
        add_polygons(self, *args, **kwargs)

    def add_polygon(self, *args, **kwargs):
        add_polygon(self, *args, **kwargs)