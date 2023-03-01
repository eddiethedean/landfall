"""
Functions for plotting points.
"""

import staticmaps
import pygeodesy


tp = staticmaps.tile_provider_OSM


def plot_points(
    lats,
    lons,
    tile_provider=tp,
    point_size=10,
    window_size=(500, 400),
    zoom=0,
    color=staticmaps.color.BLUE,
    set_zoom=None,
    center=None
):
    context = staticmaps.Context()
    context.set_tile_provider(tile_provider)

    for lat, lon in zip(lats, lons):
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
    