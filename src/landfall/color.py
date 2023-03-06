"""
Functions for using colors.
"""

import random
from typing import Sequence, List, Mapping, Union

from staticmaps import Color, parse_color

from .distinctipy import get_distict_colors
from .colorsys import get_wheel_colors


def random_color():
    r = random.randrange(0, 256)
    g = random.randrange(0, 256)
    b = random.randrange(0, 256)
    return Color(r, g, b)


def process_colors(
    colors: Sequence,
    count: int
) -> List[Color]:
    if type(colors) is str:
        if colors == 'random':
            colors = [random_color() for _ in range(count)]
        elif colors == 'distinct':
            colors = convert_colors(get_distict_colors(count))
        elif colors == 'wheel':
            colors = convert_colors(get_wheel_colors(count))
        else:
            raise ValueError('str must be "random", "distinct", or "wheel"')
    else:
        colors = convert_colors(colors)
    return colors


def convert_colors(colors) -> List[Color]:
    return [convert_color(color) for color in colors]


def convert_color(color) -> Color:
    if isinstance(color, str):
        return parse_color(color)
    if isinstance(color, Color):
        return color
    if len(color) in (3, 4):
        return Color(*color)
    else:
        raise ValueError('process_color only takes str, Color or (r, g, b)')
    

def process_id_colors(ids: Sequence, id_colors: Union[Mapping, str]) -> List[Color]:
    """Return a list of unique colors for each id."""
    if type(id_colors) is str:
        id_colors = map_id_colors(ids, id_colors)
    return [convert_color(id_colors[id]) for id in ids]


def map_id_colors(ids: Sequence, color_code: str) -> dict:
    """Map colors to each id."""
    count = len(ids)
    unique_ids = list(set(ids))
    return {id: color for id, color in zip(unique_ids, process_colors(color_code, count))}
    


