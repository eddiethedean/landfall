"""
Functions for plotting points.
"""
from typing import Mapping, Optional, Sequence, Tuple, Union
from itertools import repeat

import staticmaps
from PIL.Image import Image

from landfall.color import process_colors, process_id_colors


tp = staticmaps.tile_provider_OSM


def plot_points(
    latitudes: Sequence,
    longitudes: Optional[Sequence] = None,
    colors: Optional[Union[Sequence, str]] = None,
    ids: Optional[Sequence] = None,
    id_colors: Optional[Union[Mapping, str]] = None,
    tile_provider=tp,
    point_size=10,
    window_size=(500, 400),
    zoom=0,
    color=staticmaps.color.BLUE,
    set_zoom=None
) -> Image:
    context = staticmaps.Context()
    context.set_tile_provider(tile_provider)
    count = len(latitudes)

    if longitudes is None:
        latitudes, longitudes = points_to_lats_lons(latitudes)

    if colors is not None:
        colors = process_colors(colors, count)
    else:
        colors = list(repeat(color, count))

    if ids is not None and id_colors is not None:
        colors = process_id_colors(ids, id_colors)

    for lat, lon, clr in zip(latitudes, longitudes, colors):
        add_point(context, lat, lon, clr, point_size)

    _, _zoom = context.determine_center_zoom(*window_size)
    if _zoom is not None:
        context.set_zoom(_zoom + zoom)

    if set_zoom is not None:
        context.set_zoom(set_zoom)
    
    return context.render_pillow(*window_size) # type: ignore
    

def plot_points_data(
    data: Mapping[str, Sequence],
    latitude_name: str,
    longitude_name: str,
    color_name: Optional[str] = None,
    colors: Optional[str] = None,
    ids_name: Optional[str] = None,
    id_colors: Optional[Union[Mapping, str]] = None,
    tile_provider=tp,
    point_size=10,
    window_size=(500, 400),
    zoom=0,
    color=staticmaps.color.BLUE,
    set_zoom=None
) -> Image:
    lats = data[latitude_name]
    lons = data[longitude_name]
    colors_values = None if color_name is None else data[color_name]
    if colors_values is None and colors is not None:
        colors_values = colors
    ids_values = None if ids_name is None else data[ids_name]

    return plot_points(
        lats,
        lons,
        colors=colors_values,
        ids=ids_values,
        id_colors=id_colors,
        tile_provider=tile_provider,
        point_size=point_size,
        window_size=window_size,
        zoom=zoom,
        color=color,
        set_zoom=set_zoom)


def points_to_lats_lons(
    points: Sequence[Sequence[float]]
) -> Tuple[Sequence[float], Sequence[float]]:
    latitudes, longitudes = zip(*points)
    return latitudes, longitudes


def plot_points_tuples(points: Sequence[tuple], **kwargs) -> Image:
    latitudes, longitudes = points_to_lats_lons(points)
    return plot_points(latitudes, longitudes, **kwargs)


def add_point(
    context: staticmaps.Context,
    lat: float,
    lon: float,
    color: staticmaps.Color,
    point_size: int
) -> None:
    point = staticmaps.create_latlng(lat, lon)
    marker = staticmaps.Marker(point, color=color, size=point_size)
    context.add_object(marker)


def add_points(
        context: staticmaps.Context,
        latitudes: Sequence[float],
        longitudes: Sequence[float],
        colors: Sequence[staticmaps.Color],
        point_size: int
) -> None:
    for lat, lon, clr in zip(latitudes, longitudes, colors):
        add_point(context, lat, lon, clr, point_size)