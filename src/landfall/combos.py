from typing import Any, Optional, Sequence, Tuple

from PIL.Image import Image
from staticmaps import RED, Color, Context, tile_provider_OSM

from landfall.plot import set_tile_provider
from landfall.points import add_point
from landfall.polygons import add_polygons, flip_polygon_coords

tp = tile_provider_OSM
TRED = Color(255, 0, 0, 100)


def plot_points_and_polygons(
    points: Sequence[Tuple[float, float]],
    polygons: Sequence[Sequence[Tuple[float, float]]],
    tile_provider: Any = tile_provider_OSM,
    point_size: int = 10,
    fill_color: Color = Color(255, 0, 0, 100),
    color: Color = RED,
    width: int = 2,
    size: Tuple[int, int] = (800, 600),
    flip_coords: bool = False,
    api_key: Optional[str] = None,
) -> Image:
    context = Context()
    set_tile_provider(context, tile_provider, api_key)
    if flip_coords:
        polygons = [flip_polygon_coords(polygon) for polygon in polygons]
    add_polygons(context, polygons, fill_color=fill_color, width=width, color=color)
    for lat, lon in points:
        if flip_coords:
            lat, lon = lon, lat
        add_point(context, lat, lon, color, point_size)
    return context.render_pillow(*size)  # type: ignore
