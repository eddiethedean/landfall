import random

import staticmaps


def random_color():
    r = random.randrange(0, 256)
    g = random.randrange(0, 256)
    b = random.randrange(0, 256)
    return staticmaps.Color(r, g, b)