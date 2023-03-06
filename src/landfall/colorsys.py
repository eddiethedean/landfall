import colorsys
from typing import Set, Tuple 
 
    
def hsvt_to_rgb(h, s, v) -> Tuple[int, int, int]:
    (r, g, b) = colorsys.hsv_to_rgb(h, s, v) 
    return int(r*255), int(g*255), int(b*255)
 
    
def get_wheel_colors(n) -> Set[Tuple[int, int, int]]:
    hue_partition = 1 / (n + 1)
    colors = set()
    for value in range(0, n):
        new_color = hsvt_to_rgb(hue_partition * value, .99, 1)
        if new_color in colors:
            raise ValueError('n is too high')
        if max(new_color) > 255 or min(new_color) < 0:
            raise ValueError('color is not real')
        colors.add(new_color)
    return colors