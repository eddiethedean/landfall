from typing import List

import distinctipy


def get_distict_colors(
    qty: int,
    pastel_factor = 0
) -> List[tuple]:
    colors = distinctipy.get_colors(qty, pastel_factor=pastel_factor)
    return [(int(r) * 255, int(g) * 255, int(b) * 255) for r, g, b in colors]