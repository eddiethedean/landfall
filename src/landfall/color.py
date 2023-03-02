"""
Functions for using colors.
"""

import random
from typing import Sequence, List

from staticmaps import Color, parse_color


def random_color():
    r = random.randrange(0, 256)
    g = random.randrange(0, 256)
    b = random.randrange(0, 256)
    return Color(r, g, b)


def process_colors(
    colors: Sequence
) -> List[Color]:
    return [process_color(color) for color in colors]


def process_color(color) -> Color:
    if isinstance(color, str):
        return parse_color(color)
    if isinstance(color, Color):
        return color
    if len(color) in (3, 4):
        return Color(*color)
    else:
        raise ValueError('process_color only takes str, Color or (r, g, b)')
