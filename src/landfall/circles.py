"""
Functions for plotting circles and buffers.
"""

from typing import Any, Mapping, Optional, Sequence, Tuple, Union
import staticmaps
from PIL.Image import Image

from landfall.plot import plot_colors, plot_fill_colors, plot_zoom

tp = staticmaps.tile_provider_OSM
TRED = staticmaps.Color(255, 0, 0, 100)
RED = staticmaps.RED


def plot_circles(
    latitudes: Sequence[float],
    longitudes: Sequence[float],
    radii: Sequence[float],
    *,
    color: staticmaps.Color = RED,
    colors: Optional[Union[Sequence[Any], str]] = None,
    fill_color: staticmaps.Color = TRED,
    fill_colors: Optional[Union[Sequence[Any], str]] = None,
    fill_same: Optional[bool] = None,
    fill_transparency: Optional[int] = None,
    ids: Optional[Sequence[Any]] = None,
    id_colors: Optional[Union[Mapping[Any, Any], str]] = None,
    id_fill_colors: Optional[Union[Mapping[Any, Any], str]] = None,
    radius_unit: str = "meters",
    tile_provider: Any = tp,
    width: int = 2,
    window_size: Tuple[int, int] = (500, 400),
    zoom: int = 0,
    set_zoom: Optional[int] = None,
    flip_coords: bool = False,
    context: Optional[staticmaps.Context] = None,
) -> Image:
    """Plot multiple circles on a map.

    Args:
        latitudes: Circle center latitudes
        longitudes: Circle center longitudes
        radii: Circle radii
        color: Default border color for all circles
        colors: Border colors for circles
        fill_color: Default fill color for all circles
        fill_colors: Fill colors for circles
        fill_same: Use border color for fill
        fill_transparency: Transparency for fills
        ids: IDs for grouping circles
        id_colors: Border color mapping for IDs
        id_fill_colors: Fill color mapping for IDs
        radius_unit: Unit for radii ('meters' or 'kilometers')
        tile_provider: Map tile provider
        width: Border width in pixels
        window_size: Output image size (width, height)
        zoom: Zoom level adjustment
        set_zoom: Override automatic zoom level
        flip_coords: Whether coordinates are in (lon, lat) order
        context: Optional existing staticmaps context

    Returns:
        PIL Image with plotted circles
    """
    if context is None:
        context = staticmaps.Context()

    context.set_tile_provider(tile_provider)

    add_circles(
        context,
        latitudes,
        longitudes,
        radii,
        color=color,
        colors=colors,
        fill_color=fill_color,
        fill_colors=fill_colors,
        fill_same=fill_same,
        fill_transparency=fill_transparency,
        ids=ids,
        id_colors=id_colors,
        id_fill_colors=id_fill_colors,
        radius_unit=radius_unit,
        width=width,
        flip_coords=flip_coords,
    )

    zoom = plot_zoom(context, window_size, zoom, set_zoom)
    context.set_zoom(zoom)

    return context.render_pillow(*window_size)  # type: ignore


def add_circles(
    context: staticmaps.Context,
    latitudes: Sequence[float],
    longitudes: Sequence[float],
    radii: Sequence[float],
    color: staticmaps.Color = RED,
    colors: Optional[Union[Sequence[Any], str]] = None,
    fill_color: staticmaps.Color = TRED,
    fill_colors: Optional[Union[Sequence[Any], str]] = None,
    fill_same: Optional[bool] = None,
    fill_transparency: Optional[int] = None,
    ids: Optional[Sequence[Any]] = None,
    id_colors: Optional[Union[Mapping[Any, Any], str]] = None,
    id_fill_colors: Optional[Union[Mapping[Any, Any], str]] = None,
    radius_unit: str = "meters",
    width: int = 2,
    flip_coords: bool = False,
) -> None:
    """Add multiple circles to a staticmaps context.

    Args:
        context: staticmaps Context to add circles to
        latitudes: Circle center latitudes
        longitudes: Circle center longitudes
        radii: Circle radii
        color: Default border color
        colors: Border colors
        fill_color: Default fill color
        fill_colors: Fill colors
        fill_same: Use border color for fill
        fill_transparency: Transparency for fills
        ids: IDs for grouping circles
        id_colors: Border color mapping for IDs
        id_fill_colors: Fill color mapping for IDs
        radius_unit: Unit for radii ('meters' or 'kilometers')
        width: Border width in pixels
        flip_coords: Whether coordinates are in (lon, lat) order
    """
    if flip_coords:
        latitudes, longitudes = longitudes, latitudes

    count = len(latitudes)

    colors = plot_colors(
        count=count, colors=colors, ids=ids, id_colors=id_colors, color=color
    )

    fill_colors = plot_fill_colors(
        count,
        colors=colors,
        ids=ids,
        fill_same=fill_same,
        fill_transparency=fill_transparency,
        fill_colors=fill_colors,
        fill_color=fill_color,
        id_fill_colors=id_fill_colors,
    )

    for lat, lon, radius, color, fill_color in zip(
        latitudes, longitudes, radii, colors, fill_colors
    ):
        add_circle(context, lat, lon, radius, color, fill_color, width, radius_unit)


def plot_circle(
    latitude: float,
    longitude: float,
    radius: float,
    tile_provider: Any = tp,
    fill_color: staticmaps.Color = TRED,
    color: staticmaps.Color = RED,
    width: int = 2,
    radius_unit: str = "meters",
    window_size: Tuple[int, int] = (500, 400),
    zoom: int = 0,
    set_zoom: Optional[int] = None,
    flip_coords: bool = False,
    context: Optional[staticmaps.Context] = None,
) -> Image:
    """Plot a single circle on a map.

    Args:
        latitude: Circle center latitude
        longitude: Circle center longitude
        radius: Circle radius
        tile_provider: Map tile provider
        fill_color: Fill color
        color: Border color
        width: Border width in pixels
        radius_unit: Unit for radius ('meters' or 'kilometers')
        window_size: Output image size (width, height)
        zoom: Zoom level adjustment
        set_zoom: Override automatic zoom level
        flip_coords: Whether coordinates are in (lon, lat) order
        context: Optional existing staticmaps context

    Returns:
        PIL Image with plotted circle
    """
    if context is None:
        context = staticmaps.Context()

    context.set_tile_provider(tile_provider)

    if flip_coords:
        latitude, longitude = longitude, latitude

    add_circle(
        context, latitude, longitude, radius, color, fill_color, width, radius_unit
    )

    zoom = plot_zoom(context, window_size, zoom, set_zoom)
    context.set_zoom(zoom)

    return context.render_pillow(*window_size)  # type: ignore


def add_circle(
    context: staticmaps.Context,
    latitude: float,
    longitude: float,
    radius: float,
    color: staticmaps.Color,
    fill_color: staticmaps.Color,
    width: int,
    radius_unit: str = "meters",
) -> None:
    """Add a single circle to a staticmaps context.

    Args:
        context: staticmaps Context to add circle to
        latitude: Circle center latitude
        longitude: Circle center longitude
        radius: Circle radius
        color: Border color
        fill_color: Fill color
        width: Border width in pixels
        radius_unit: Unit for radius ('meters' or 'kilometers')
    """
    # Convert radius to meters if needed
    if radius_unit == "kilometers":
        radius_meters = radius * 1000
    elif radius_unit == "meters":
        radius_meters = radius
    else:
        raise ValueError("radius_unit must be 'meters' or 'kilometers'")

    center = staticmaps.create_latlng(latitude, longitude)
    circle = staticmaps.Circle(
        center,
        radius_meters,
        color=color,
        fill_color=fill_color,
        width=width,
    )
    context.add_object(circle)
