"""
Functions for plotting polygons.
"""
from typing import Iterable, List, Optional, Tuple
import staticmaps
from PIL.Image import Image

tp = staticmaps.tile_provider_OSM
TRED = staticmaps.Color(255, 0, 0, 100)
RED = staticmaps.RED


def create_polygon_points(polygon: Iterable[Tuple[float, float]]) -> List:
    return [staticmaps.create_latlng(lat, lon) for lat, lon in polygon]


def flip_polygon_coords(
    polygon: Iterable[Tuple[float, float]]
) -> List[Tuple[float, float]]:
    return [(lon, lat) for lat, lon in polygon]


def plot_polygons(
        polygons,
        tileprovider=tp,
        fill_color=TRED,
        color=RED,
        width=2,
        size=(500, 400),
        flip_coords=False,
        context: Optional[staticmaps.Context] = None
) -> Image:
    if context is None:
        context = staticmaps.Context()
    context.set_tile_provider(tileprovider)
    if flip_coords:
        polygons = [flip_polygon_coords(polygon) for polygon in polygons]
    add_polygons(context, polygons, fill_color=fill_color, width=width, color=color)
    return context.render_pillow(*size) # type: ignore


def plot_polygon(
    polygon: Iterable[Tuple[float, float]],
    tileprovider=tp,
    fill_color=TRED,
    color=RED,
    width=2,
    size=(500, 400),
    flip_coords=False,
    context: Optional[staticmaps.Context] = None
) -> Image:
    if context is None:
        context = staticmaps.Context()
    context.set_tile_provider(tileprovider)
    if flip_coords:
        polygon = flip_polygon_coords(polygon)
    add_polygon(context, polygon, fill_color=fill_color, width=width, color=color)
    return context.render_pillow(*size) # type: ignore


def add_polygon(
    context: staticmaps.Context,
    polygon: Iterable[Tuple[float, float]],
    fill_color,
    width,
    color,
    flip_coords=False,
) -> None:
    if flip_coords:
        polygon = flip_polygon_coords(polygon)
    context.add_object(staticmaps.Area(
        create_polygon_points(polygon),
        fill_color=fill_color,
        width=width,
        color=color))
    

def add_polygons(
    context: staticmaps.Context,
    polygons: Iterable[Iterable[Tuple[float, float]]],
    fill_color,
    width,
    color,
    flip_coords=False
) -> None:
    for polygon in polygons:
        add_polygon(context, polygon, fill_color, width, color, flip_coords=flip_coords)