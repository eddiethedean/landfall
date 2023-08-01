"""
Functions for plotting polygons.
"""
from typing import Iterable, List, Mapping, Optional, Sequence, Tuple, Union
import staticmaps
from PIL.Image import Image

from landfall.plot import plot_colors, plot_fill_colors

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
    *,
    color=RED,
    colors: Optional[Union[Sequence, str]] = None,
    fill_same: Optional[bool] = None,
    fill_transparency: Optional[int] = None,
    fill_colors: Optional[Union[Sequence, str]] = None,
    fill_color: staticmaps.Color = TRED,
    ids: Optional[Sequence] = None,
    id_colors: Optional[Union[Mapping, str]] = None,
    id_fill_colors: Optional[Union[Mapping, str]] = None,
    tileprovider=tp,
    width=2,
    window_size=(500, 400),
    flip_coords: bool =False,
    context: Optional[staticmaps.Context] = None
) -> Image:
    if context is None:
        context = staticmaps.Context()

    context.set_tile_provider(tileprovider)

    add_polygons(
        context,
        polygons,
        color=color,
        colors=colors,
        fill_same=fill_same,
        fill_transparency=fill_transparency,
        fill_colors=fill_colors,
        fill_color=fill_color,
        ids=ids,
        id_colors=id_colors,
        id_fill_colors=id_fill_colors,
        width=width,
        flip_coords=flip_coords
    )
    
    return context.render_pillow(*window_size) # type: ignore

def add_polygons(
    context: staticmaps.Context,
    polygons,
    color=RED,
    colors: Optional[Union[Sequence, str]] = None,
    fill_same: Optional[bool] = None,
    fill_transparency: Optional[int] = None,
    fill_colors: Optional[Union[Sequence, str]] = None,
    fill_color: staticmaps.Color = TRED,
    ids: Optional[Sequence] = None,
    id_colors: Optional[Union[Mapping, str]] = None,
    id_fill_colors: Optional[Union[Mapping, str]] = None,
    width=2,
    flip_coords: bool =False
) -> None:

    if flip_coords:
        polygons = [flip_polygon_coords(polygon) for polygon in polygons]

    count = len(polygons)

    colors = plot_colors(
        count=count,
        colors=colors,
        ids=ids,
        id_colors=id_colors,
        color=color
    )
    
    fill_colors = plot_fill_colors(
        count,
        colors=colors,
        ids=ids,
        fill_same=fill_same,
        fill_transparency=fill_transparency,
        fill_colors=fill_colors,
        fill_color=fill_color,
        id_fill_colors=id_fill_colors
    )
    
    for polygon, color, fill_color in zip(polygons, colors, fill_colors):
        add_polygon(
            context,
            polygon,
            fill_color,
            width,
            color,
            flip_coords=flip_coords
        )
    

def plot_polygon(
    polygon: Iterable[Tuple[float, float]],
    tileprovider=tp,
    fill_color=TRED,
    color=RED,
    width=2,
    window_size=(500, 400),
    flip_coords=False,
    context: Optional[staticmaps.Context] = None
) -> Image:
    if context is None:
        context = staticmaps.Context()

    context.set_tile_provider(tileprovider)

    if flip_coords:
        polygon = flip_polygon_coords(polygon)

    add_polygon(
        context,
        polygon,
        fill_color=fill_color,
        width=width,
        color=color
    )
    
    return context.render_pillow(*window_size) # type: ignore


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
    context.add_object(
        staticmaps.Area(
            create_polygon_points(polygon),
            fill_color=fill_color,
            width=width,
            color=color
        )
    )