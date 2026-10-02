"""
Functions for using colors.
"""

import random
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple, Union

from staticmaps import Color, parse_color

from .colorsys import get_wheel_colors
from .distinctipy import get_distinct_colors

ColorInput = Union[str, Color, Tuple[int, int, int], Tuple[int, int, int, int]]


def random_color(rng: Optional[int] = None) -> Color:
    generator = random.Random(rng)
    r = generator.randrange(0, 256)
    g = generator.randrange(0, 256)
    b = generator.randrange(0, 256)
    return Color(r, g, b)


def process_colors(
    colors: Sequence[Any], count: int, rng: Optional[int] = None
) -> List[Color]:
    if count < 0:
        raise ValueError("count must be non-negative")
    if isinstance(colors, str):
        if colors == "random":
            generator = random.Random(rng)
            colors = [
                Color(*(generator.randrange(256) for _ in range(3)))
                for _ in range(count)
            ]
        elif colors == "distinct":
            colors = convert_colors(get_distinct_colors(count, rng=rng))
        elif colors == "wheel":
            colors = convert_colors(sorted(get_wheel_colors(count)))
        else:
            raise ValueError('str must be "random", "distinct", or "wheel"')
    else:
        colors = convert_colors(colors)
        if len(colors) == 1:
            colors = list(colors) * count
        elif len(colors) != count:
            raise ValueError(
                "colors must contain one color or match the number of objects"
            )
    return colors


def convert_colors(colors: Sequence[Any]) -> List[Color]:
    return [convert_color(color) for color in colors]


def convert_color(
    color: ColorInput,
) -> Color:
    if isinstance(color, str):
        return parse_color(color)
    if isinstance(color, Color):
        return color
    if isinstance(color, (tuple, list)) and len(color) in (3, 4):
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
    unique_ids = list(dict.fromkeys(ids))
    count = len(unique_ids)
    return {
        id: color for id, color in zip(unique_ids, process_colors(color_code, count))
    }
