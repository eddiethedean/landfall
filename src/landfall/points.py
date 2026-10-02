"""
Functions for plotting points.
"""

from typing import Any, List, Mapping, Optional, Sequence, Tuple, Union

import staticmaps
from PIL.Image import Image

from landfall.color import ColorInput, convert_color
from landfall.plot import plot_colors, plot_zoom
from landfall.validation import create_latlng

tp = staticmaps.tile_provider_OSM


def plot_points(
    latitudes: Union[Sequence[float], Sequence[Tuple[float, float]]],
    longitudes: Optional[Sequence[float]] = None,
    *,
    colors: Optional[Union[Sequence[Any], str]] = None,
    ids: Optional[Sequence[Any]] = None,
    id_colors: Optional[Union[Mapping[Any, Any], str]] = None,
    tile_provider: Any = tp,
    point_size: int = 10,
    window_size: Tuple[int, int] = (500, 400),
    zoom: int = 0,
    color: ColorInput = staticmaps.color.BLUE,
    set_zoom: Optional[int] = None,
    flip_coords: bool = False,
    context: Optional[staticmaps.Context] = None,
) -> Image:
    if context is None:
        context = staticmaps.Context()

    context.set_tile_provider(tile_provider)

    add_points(
        context=context,
        latitudes=latitudes,
        longitudes=longitudes,
        colors=colors,
        ids=ids,
        id_colors=id_colors,
        point_size=point_size,
        color=color,
        flip_coords=flip_coords,
    )

    zoom = plot_zoom(context, window_size, zoom, set_zoom)
    context.set_zoom(zoom)

    return context.render_pillow(*window_size)  # type: ignore


def add_points(
    context: staticmaps.Context,
    latitudes: Union[Sequence[float], Sequence[Tuple[float, float]]],
    longitudes: Optional[Sequence[float]] = None,
    *,
    colors: Optional[Union[Sequence[Any], str]] = None,
    ids: Optional[Sequence[Any]] = None,
    id_colors: Optional[Union[Mapping[Any, Any], str]] = None,
    point_size: int = 10,
    color: ColorInput = staticmaps.color.BLUE,
    flip_coords: bool = False,
) -> None:
    if longitudes is None:
        latitudes, longitudes = points_to_lats_lons(latitudes)  # type: ignore[arg-type]
    if len(latitudes) != len(longitudes):
        raise ValueError("latitudes and longitudes must have the same length")
    count = len(latitudes)

    colors = plot_colors(
        count=count, colors=colors, ids=ids, id_colors=id_colors, color=color
    )

    if flip_coords:
        latitudes, longitudes = longitudes, latitudes

    for lat, lon, clr in zip(latitudes, longitudes, colors):
        add_point(context, lat, lon, clr, point_size)  # type: ignore[arg-type]


def plot_points_data(
    data: Mapping[str, Sequence[Any]],
    latitude_name: str,
    longitude_name: str,
    *,
    color_name: Optional[str] = None,
    ids_name: Optional[str] = None,
    id_colors: Optional[Union[Mapping[Any, Any], str]] = None,
    colors: Optional[str] = None,
    tile_provider: Any = tp,
    point_size: int = 10,
    window_size: Tuple[int, int] = (500, 400),
    zoom: int = 0,
    color: ColorInput = staticmaps.color.BLUE,
    set_zoom: Optional[int] = None,
    flip_coords: bool = False,
    context: Optional[staticmaps.Context] = None,
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
        set_zoom=set_zoom,
        flip_coords=flip_coords,
        context=context,
    )


def points_to_lats_lons(
    points: Sequence[Sequence[float]],
) -> Tuple[List[float], List[float]]:
    if len(points) == 0:
        return [], []
    try:
        invalid_pair = any(len(point) != 2 for point in points)
    except TypeError as error:
        raise ValueError("points must contain (latitude, longitude) pairs") from error
    if invalid_pair:
        raise ValueError("points must contain (latitude, longitude) pairs")
    latitudes, longitudes = zip(*points)
    return list(latitudes), list(longitudes)


def plot_points_tuples(points: Sequence[Tuple[float, float]], **kwargs: Any) -> Image:
    latitudes, longitudes = points_to_lats_lons(points)
    return plot_points(latitudes, longitudes, **kwargs)


def add_point(
    context: staticmaps.Context,
    lat: float,
    lon: float,
    color: ColorInput = staticmaps.color.BLUE,
    point_size: int = 10,
) -> None:
    point = create_latlng(lat, lon)
    marker = staticmaps.Marker(point, color=convert_color(color), size=point_size)
    context.add_object(marker)
