import os
from os import PathLike
from typing import Any, Optional, Union

import staticmaps

from landfall.circles import add_circle, add_circles
from landfall.lines import add_line, add_lines
from landfall.points import add_point, add_points
from landfall.polygons import add_polygon, add_polygons


class Context(staticmaps.Context):
    def save(
        self,
        path: Union[str, PathLike[str]],
        width: int,
        height: int,
        *,
        renderer: Optional[str] = None,
    ) -> None:
        """Render this context and save it as PNG or SVG.

        The file suffix selects Pillow PNG or SVG output by default. Pass
        ``renderer="cairo"`` to write a Cairo PNG explicitly.
        """
        output_path = os.fspath(path)
        suffix = os.path.splitext(output_path)[1].lower()

        if renderer is None:
            if suffix == ".png":
                renderer = "pillow"
            elif suffix == ".svg":
                renderer = "svg"
            else:
                raise ValueError("Output path must end in .png or .svg")

        if renderer == "pillow":
            if suffix != ".png":
                raise ValueError("The Pillow renderer requires a .png output path")
            self.render_pillow(width, height).save(output_path)
        elif renderer == "svg":
            if suffix != ".svg":
                raise ValueError("The SVG renderer requires a .svg output path")
            self.render_svg(width, height).saveas(output_path)
        elif renderer == "cairo":
            if suffix != ".png":
                raise ValueError("The Cairo renderer requires a .png output path")
            self.render_cairo(width, height).write_to_png(output_path)
        else:
            raise ValueError("renderer must be 'pillow', 'svg', or 'cairo'")

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
