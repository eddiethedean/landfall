from staticmaps import Color, Context, RED, tile_provider_OSM
from PIL.Image import Image

from landfall.polygons import add_polygons, flip_polygon_coords
from landfall.points import add_point

tp = tile_provider_OSM
TRED = Color(255, 0, 0, 100)


def plot_points_and_polygons(
    points,
    polygons,
    tileprovider=tile_provider_OSM,
    point_size=10,
    fill_color=Color(255, 0, 0, 100),
    color=RED,
    width=2,
    size=(800, 600),
    flip_coords=False
) -> Image:
    context = Context()
    context.set_tile_provider(tileprovider)
    if flip_coords:
        polygons = [flip_polygon_coords(polygon) for polygon in polygons]
    add_polygons(context, polygons, fill_color=fill_color, width=width, color=color)
    for lat, lon in points:
        add_point(context, lat, lon, color, point_size)
    return context.render_pillow(*size) # type: ignore