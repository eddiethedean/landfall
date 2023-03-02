"""
Functions for plotting points.
"""

from typing import Mapping, Optional, Sequence, Union
from itertools import repeat

import staticmaps
import pygeodesy
from PIL.Image import Image

from landfall.color import process_colors, random_color


tp = staticmaps.tile_provider_OSM


def plot_points(
    lats,
    lons,
    colors: Optional[Union[Sequence, str]] = None,
    tile_provider=tp,
    point_size=10,
    window_size=(500, 400),
    zoom=0,
    color=staticmaps.color.BLUE,
    set_zoom=None,
    center=None
) -> Image:
    context = staticmaps.Context()
    context.set_tile_provider(tile_provider)
    count = len(lats)
    if colors == 'random':
        colors = [random_color() for _ in range(count)]
    elif colors is not None:
        colors = process_colors(colors)
    else:
        colors = [color for _ in range(count)]

    for lat, lon, color in zip(lats, lons, colors):
        point = staticmaps.create_latlng(lat, lon)
        marker = staticmaps.Marker(point, color=color, size=point_size)
        context.add_object(marker)

    _center, _zoom = context.determine_center_zoom(*window_size)
    context.set_zoom(_zoom + zoom)

    if center is not None:
        if type(center) is tuple:
            point = staticmaps.create_latlng(*center)
        if type(center) is str:
            lat, lon = pygeodesy.geohash.decode(*center)
            point = staticmaps.create_latlng(float(lat), float(lon))
        context.set_center(point)
    if set_zoom is not None:
        context.set_zoom(set_zoom)
    return context.render_pillow(*window_size)
    

def plot_points_data(
    data: Mapping[str, Sequence],
    lat_name: str,
    lon_name: str,
    tile_provider=tp,
    point_size=10,
    window_size=(500, 400),
    zoom=0,
    color=staticmaps.color.BLUE,
    set_zoom=None,
    center=None
) -> Image:
    lats = data[lat_name]
    lons = data[lon_name]
    return plot_points(
        lats, lons, tile_provider,
        point_size, window_size, zoom,
        color, set_zoom, center)