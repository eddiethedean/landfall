from typing import List, Optional, Tuple
import warnings

import distinctipy


def get_distinct_colors(
    qty: int, pastel_factor: int = 0, rng: Optional[int] = None
) -> List[Tuple[int, int, int]]:
    colors = distinctipy.get_colors(qty, pastel_factor=pastel_factor, rng=rng)
    return [(int(r * 255), int(g * 255), int(b * 255)) for r, g, b in colors]


def get_distict_colors(
    qty: int, pastel_factor: int = 0, rng: Optional[int] = None
) -> List[Tuple[int, int, int]]:
    """Deprecated: Use get_distinct_colors instead."""
    warnings.warn(
        "get_distict_colors is deprecated, use get_distinct_colors instead",
        DeprecationWarning,
        stacklevel=2,
    )
    return get_distinct_colors(qty, pastel_factor, rng)
