from typing import Any

import staticmaps

from landfall.points import add_points, add_point
from landfall.polygons import add_polygons, add_polygon
from landfall.lines import add_lines, add_line
from landfall.circles import add_circles, add_circle


class Context(staticmaps.Context):
    def add_points(self, *args: Any, **kwargs: Any) -> None:
        add_points(self, *args, **kwargs)

    def add_point(self, *args: Any, **kwargs: Any) -> None:
        add_point(self, *args, **kwargs)

    def add_polygons(self, *args: Any, **kwargs: Any) -> None:
        add_polygons(self, *args, **kwargs)

    def add_polygon(self, *args: Any, **kwargs: Any) -> None:
        add_polygon(self, *args, **kwargs)

    def add_lines(self, *args: Any, **kwargs: Any) -> None:
        add_lines(self, *args, **kwargs)

    def add_line(self, *args: Any, **kwargs: Any) -> None:
        add_line(self, *args, **kwargs)

    def add_circles(self, *args: Any, **kwargs: Any) -> None:
        add_circles(self, *args, **kwargs)

    def add_circle(self, *args: Any, **kwargs: Any) -> None:
        add_circle(self, *args, **kwargs)
