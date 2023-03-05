"""
Functions for using colors.
"""

from itertools import repeat
import random
from typing import Sequence, List, Mapping

from staticmaps import Color, parse_color

from .distinctipy import get_colors


def random_color():
    r = random.randrange(0, 256)
    g = random.randrange(0, 256)
    b = random.randrange(0, 256)
    return Color(r, g, b)


def process_colors(
    colors: Sequence,
    count: int
) -> List[Color]:
    if colors == 'random':
        colors = [random_color() for _ in range(count)]
    elif colors == 'test_colors':
        colors = convert_colors(get_colors(count))
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
    

def process_id_colors(ids: Sequence, id_colors: Mapping) -> List[Color]:
    ...
    


