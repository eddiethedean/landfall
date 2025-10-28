"""
Functions for using colors.
"""

import random
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple, Union

from staticmaps import Color, parse_color

from .distinctipy import get_distinct_colors
from .colorsys import get_wheel_colors


def random_color(rng: Optional[int] = None) -> Color:
    random.seed(rng)
    r = random.randrange(0, 256)
    g = random.randrange(0, 256)
    b = random.randrange(0, 256)
    return Color(r, g, b)


def process_colors(
    colors: Sequence[Any], count: int, rng: Optional[int] = None
) -> List[Color]:
    if isinstance(colors, str):
        if colors == "random":
            colors = [random_color(rng) for _ in range(count)]
        elif colors == "distinct":
            colors = convert_colors(get_distinct_colors(count, rng=rng))
        elif colors == "wheel":
            colors = convert_colors(list(get_wheel_colors(count)))
        else:
            raise ValueError('str must be "random", "distinct", or "wheel"')
    else:
        colors = convert_colors(colors)
    return colors


def convert_colors(colors: Sequence[Any]) -> List[Color]:
    return [convert_color(color) for color in colors]


def convert_color(
    color: Union[str, Color, Tuple[int, int, int], Tuple[int, int, int, int]],
) -> Color:
    if isinstance(color, str):
        return parse_color(color)
    if isinstance(color, Color):
        return color
    if len(color) in (3, 4):
        return Color(*color)
    else:
        raise ValueError(
            f"convert_color requires str, Color, or RGB tuple, "
            f"got {type(color).__name__}"
        )


def process_id_colors(
    ids: Sequence[Any], id_colors: Union[Mapping[Any, Any], str]
) -> List[Color]:
    """Return a list of unique colors for each id."""
    if isinstance(id_colors, str):
        id_colors = map_id_colors(ids, id_colors)
    return [convert_color(id_colors[id]) for id in ids]


def map_id_colors(ids: Sequence[Any], color_code: str) -> Dict[Any, Color]:
    """Map colors to each id."""
    count = len(ids)
    unique_ids = list(set(ids))
    return {
        id: color for id, color in zip(unique_ids, process_colors(color_code, count))
    }
