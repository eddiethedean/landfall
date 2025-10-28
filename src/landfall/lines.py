"""
Functions for plotting lines and polylines.
"""

from typing import Any, Iterable, List, Mapping, Optional, Sequence, Tuple, Union
import staticmaps
from PIL.Image import Image

from landfall.plot import plot_colors, plot_zoom

tp = staticmaps.tile_provider_OSM
RED = staticmaps.RED


def create_line_points(line: Iterable[Tuple[float, float]]) -> List[Any]:
    """Convert line coordinates to staticmaps LatLng objects."""
    return [staticmaps.create_latlng(lat, lon) for lat, lon in line]


def flip_line_coords(
    line: Iterable[Tuple[float, float]],
) -> List[Tuple[float, float]]:
    """Flip coordinates from (lat, lon) to (lon, lat)."""
    return [(lon, lat) for lat, lon in line]


def plot_lines(
    lines: Sequence[Sequence[Tuple[float, float]]],
    *,
    color: staticmaps.Color = RED,
    colors: Optional[Union[Sequence[Any], str]] = None,
    ids: Optional[Sequence[Any]] = None,
    id_colors: Optional[Union[Mapping[Any, Any], str]] = None,
    tile_provider: Any = tp,
    width: int = 2,
    window_size: Tuple[int, int] = (500, 400),
    zoom: int = 0,
    set_zoom: Optional[int] = None,
    flip_coords: bool = False,
    context: Optional[staticmaps.Context] = None,
) -> Image:
    """Plot multiple lines on a map.

    Args:
        lines: Sequence of lines, where each line is a sequence of (lat, lon) tuples
        color: Default color for all lines
        colors: Colors for lines (can be sequence, string, or None)
        ids: IDs for grouping lines
        id_colors: Color mapping for IDs
        tile_provider: Map tile provider
        width: Line width in pixels
        window_size: Output image size (width, height)
        zoom: Zoom level adjustment
        set_zoom: Override automatic zoom level
        flip_coords: Whether coordinates are in (lon, lat) order
        context: Optional existing staticmaps context

    Returns:
        PIL Image with plotted lines
    """
    if context is None:
        context = staticmaps.Context()

    context.set_tile_provider(tile_provider)

    add_lines(
        context,
        lines,
        color=color,
        colors=colors,
        ids=ids,
        id_colors=id_colors,
        width=width,
        flip_coords=flip_coords,
    )

    zoom = plot_zoom(context, window_size, zoom, set_zoom)
    context.set_zoom(zoom)

    return context.render_pillow(*window_size)  # type: ignore


def add_lines(
    context: staticmaps.Context,
    lines: Sequence[Sequence[Tuple[float, float]]],
    color: staticmaps.Color = RED,
    colors: Optional[Union[Sequence[Any], str]] = None,
    ids: Optional[Sequence[Any]] = None,
    id_colors: Optional[Union[Mapping[Any, Any], str]] = None,
    width: int = 2,
    flip_coords: bool = False,
) -> None:
    """Add multiple lines to a staticmaps context.

    Args:
        context: staticmaps Context to add lines to
        lines: Sequence of lines to add
        color: Default color for lines
        colors: Colors for lines
        ids: IDs for grouping lines
        id_colors: Color mapping for IDs
        width: Line width in pixels
        flip_coords: Whether coordinates are in (lon, lat) order
    """
    if flip_coords:
        lines = [flip_line_coords(line) for line in lines]

    count = len(lines)

    colors = plot_colors(
        count=count, colors=colors, ids=ids, id_colors=id_colors, color=color
    )

    for line, color in zip(lines, colors):
        add_line(context, line, color, width, flip_coords=flip_coords)


def plot_line(
    line: Sequence[Tuple[float, float]],
    tile_provider: Any = tp,
    color: staticmaps.Color = RED,
    width: int = 2,
    window_size: Tuple[int, int] = (500, 400),
    zoom: int = 0,
    set_zoom: Optional[int] = None,
    flip_coords: bool = False,
    context: Optional[staticmaps.Context] = None,
) -> Image:
    """Plot a single line on a map.

    Args:
        line: Line as sequence of (lat, lon) tuples
        tile_provider: Map tile provider
        color: Line color
        width: Line width in pixels
        window_size: Output image size (width, height)
        zoom: Zoom level adjustment
        set_zoom: Override automatic zoom level
        flip_coords: Whether coordinates are in (lon, lat) order
        context: Optional existing staticmaps context

    Returns:
        PIL Image with plotted line
    """
    if context is None:
        context = staticmaps.Context()

    context.set_tile_provider(tile_provider)

    if flip_coords:
        line = flip_line_coords(line)

    add_line(context, line, color=color, width=width)

    zoom = plot_zoom(context, window_size, zoom, set_zoom)
    context.set_zoom(zoom)

    return context.render_pillow(*window_size)  # type: ignore


def add_line(
    context: staticmaps.Context,
    line: Sequence[Tuple[float, float]],
    color: staticmaps.Color,
    width: int,
    flip_coords: bool = False,
) -> None:
    """Add a single line to a staticmaps context.

    Args:
        context: staticmaps Context to add line to
        line: Line as sequence of (lat, lon) tuples
        color: Line color
        width: Line width in pixels
        flip_coords: Whether coordinates are in (lon, lat) order
    """
    if flip_coords:
        line = flip_line_coords(line)

    context.add_object(
        staticmaps.Line(
            create_line_points(line),
            color=color,
            width=width,
        )
    )
