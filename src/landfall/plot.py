from typing import List, Mapping, Optional, Sequence, Tuple, Union
from itertools import repeat

import staticmaps

from landfall.color import convert_color, process_colors, process_id_colors


def plot_colors(
    count: int,
    colors: Optional[Union[Sequence, str]] = None,
    ids: Optional[Sequence] = None,
    id_colors: Optional[Union[Mapping, str]] = None,
    color: Optional[staticmaps.Color] = None,
) -> List[staticmaps.Color]:
    if colors is not None:
        colors = process_colors(colors, count)
    else:
        if color is not None:
            color = convert_color(color)
        colors = list(repeat(color, count))

    if ids is not None and id_colors is not None:
        colors = process_id_colors(ids, id_colors)

    return colors


def plot_fill_colors(
    count: int,
    colors: Sequence[staticmaps.Color],
    ids: Optional[Sequence] = None,
    fill_same: Optional[bool] = None,
    fill_transparency: Optional[int] = None,
    fill_colors: Optional[Union[Sequence, str]] = None,
    fill_color: staticmaps.Color = staticmaps.Color(0, 0, 0, 0),
    id_fill_colors: Optional[Union[Mapping, str]] = None
) -> List[staticmaps.Color]:
    if fill_color is not None:
        fill_color = convert_color(fill_color)
    if fill_same:
        fill_colors = [set_transparency(c, fill_transparency) for c in colors]
    elif fill_colors is not None:
        fill_colors = process_colors(fill_colors, count)
    else:
        fill_colors = list(repeat(fill_color, count))

    if ids is not None and id_fill_colors is not None:
        fill_colors = process_id_colors(ids, id_fill_colors)

    if fill_transparency:
        fill_colors = [set_transparency(c, fill_transparency) for c in fill_colors]
    return fill_colors


def plot_zoom(
    context: staticmaps.Context,
    window_size: Tuple[int, int] = (500, 400),
    zoom: int = 0,
    set_zoom: Optional[int] = None,
) -> int:
    _, _zoom = context.determine_center_zoom(*window_size)
    if _zoom is not None:
        zoom = _zoom + zoom

    if set_zoom is not None:
        zoom = set_zoom

    return zoom


def set_transparency(
    color: staticmaps.Color,
    a: Optional[int] = None
) -> staticmaps.Color:
    if a is None:
        return color
    r, g, b = color.int_rgb()
    return staticmaps.Color(r, g, b, a)