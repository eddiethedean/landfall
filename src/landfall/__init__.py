__version__ = "0.3.6"

# Apply compatibility patches first
import landfall.compatibility  # noqa: F401

from landfall.color import random_color
from landfall.points import plot_points, plot_points_data
from landfall.polygons import plot_polygons, plot_polygon
from landfall.context import Context

__all__ = [
    "plot_points",
    "plot_points_data",
    "plot_polygons",
    "plot_polygon",
    "random_color",
    "Context",
]
