import staticmaps

from landfall.points import add_points, add_point
from landfall.polygons import add_polygons, add_polygon


class Context(staticmaps.Context):
    def add_points(self, *args, **kwargs):
        add_points(*args, **kwargs)

    def add_point(self, *args, **kwargs):
        add_point(*args, **kwargs)

    def add_polygons(self, *args, **kwargs):
        add_polygons(*args, **kwargs)

    def add_polygon(self, *args, **kwargs):
        add_polygon(*args, **kwargs)