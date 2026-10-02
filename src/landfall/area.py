"""Polygon rendering that preserves interior rings."""

from typing import Any, List, Sequence

import staticmaps
from PIL import Image, ImageDraw


class PolygonArea(staticmaps.Area):
    """A staticmaps area with transparent holes in each supported renderer."""

    def __init__(
        self,
        rings: Sequence[List[Any]],
        fill_color: staticmaps.Color,
        color: staticmaps.Color,
        width: int,
    ) -> None:
        super().__init__(rings[0], fill_color=fill_color, color=color, width=width)
        self._rings = [
            staticmaps.Line(ring, color=color, width=width) for ring in rings
        ]

    def render_pillow(self, renderer: Any) -> None:
        rings = [
            [
                (x + renderer.offset_x(), y)
                for x, y in (
                    renderer.transformer().ll2pixel(point)
                    for point in ring.interpolate()
                )
            ]
            for ring in self._rings
        ]
        overlay = Image.new("RGBA", renderer.image().size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        draw.polygon(rings[0], fill=self.fill_color().int_rgba())
        for hole in rings[1:]:
            draw.polygon(hole, fill=(0, 0, 0, 0))
        if self.width() > 0:
            for ring in rings:
                draw.line(ring, fill=self.color().int_rgba(), width=self.width())
        renderer.alpha_compose(overlay)

    def render_svg(self, renderer: Any) -> None:
        path = renderer.drawing().path(
            fill=self.fill_color().hex_rgb(),
            fill_opacity=self.fill_color().float_a(),
            fill_rule="evenodd",
            stroke=self.color().hex_rgb() if self.width() > 0 else "none",
            stroke_opacity=self.color().float_a(),
            stroke_width=self.width(),
        )
        for ring in self._rings:
            points = [
                renderer.transformer().ll2pixel(point) for point in ring.interpolate()
            ]
            path.push("M", points[0])
            for point in points[1:]:
                path.push("L", point)
            path.push("Z")
        renderer.group().add(path)

    def render_cairo(self, renderer: Any) -> None:
        context = renderer.context()
        context.save()
        try:
            context.new_path()
            context.set_fill_rule(1)  # Cairo FILL_RULE_EVEN_ODD
            for ring in self._rings:
                points = [
                    renderer.transformer().ll2pixel(point)
                    for point in ring.interpolate()
                ]
                context.move_to(*points[0])
                for point in points[1:]:
                    context.line_to(*point)
                context.close_path()
            context.set_source_rgba(*self.fill_color().float_rgba())
            context.fill_preserve()
            if self.width() > 0:
                context.set_source_rgba(*self.color().float_rgba())
                context.set_line_width(self.width())
                context.stroke()
            else:
                context.new_path()
        finally:
            context.restore()
